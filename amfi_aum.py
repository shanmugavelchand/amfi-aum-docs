"""
amfi_aum.py
-----------
A Python module for fetching Average Assets Under Management (AAUM) data
published by the Association of Mutual Funds in India (AMFI).

Data source : https://www.amfiindia.com/aum-data/average-aum
Coverage    : April 2006 to present (quarterly from Dec 2010, monthly before)

Public API
----------
    get_financial_years()
    get_periods(fy_id, mode, str_type)
    get_fundwise_data(fy_id, period_id)
    get_schemewise_data(fy_id, period_id, str_type, mf_id)
    scrape_all(output_dir, delay)
    export_to_csv(dataframes, output_dir)
    export_to_excel(dataframes, output_dir)

Quick start
-----------
    import amfi_aum

    # List all available financial years
    years = amfi_aum.get_financial_years()

    # Get fundwise data for a single period
    df = amfi_aum.get_fundwise_data(fy_id=1, period_id=1)

    # Download everything and save to files
    dfs = amfi_aum.scrape_all(output_dir="./output")
"""

import os
import time
import requests
import pandas as pd

# ---------------------------------------------------------------------------
# Module-level configuration
# ---------------------------------------------------------------------------

_BASE_URL = "https://www.amfiindia.com/api"
_HEADERS  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"}

SCHEMEWISE_TYPES = ("Categorywise", "Typewise")


# ---------------------------------------------------------------------------
# Internal HTTP helper
# ---------------------------------------------------------------------------

def _get(url: str, params: dict = None, retries: int = 3) -> dict:
    """
    Send a GET request and return the parsed JSON response.
    Retries up to `retries` times on failure. Returns an empty dict on error.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, headers=_HEADERS, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            print(f"  [warn] attempt {attempt}/{retries} failed: {exc}")
            time.sleep(2 * attempt)
    print(f"  [error] giving up on {url} params={params}")
    return {}


# ---------------------------------------------------------------------------
# Internal flatteners  (raw JSON -> list of plain dicts)
# ---------------------------------------------------------------------------

def _flatten_fundwise(raw: dict, fy_label: str, period_label: str) -> list:
    rows = []
    for rec in raw.get("data", []):
        aum = rec.get("averageAUM", {})
        rows.append({
            "financial_year"                          : fy_label,
            "period"                                  : period_label,
            "sr_no"                                   : rec.get("Sr_No"),
            "mutual_fund_name"                        : rec.get("MutualFundName"),
            "avg_aum_excl_domestic_fof_incl_overseas" : aum.get("average_aum_excluding_domestic_including_overseas"),
            "avg_aum_fof_domestic"                    : aum.get("average_aum_fund_of_funds_domestic"),
        })

    grand = raw.get("grandTotals")
    if grand:
        rows.append({
            "financial_year"                          : fy_label,
            "period"                                  : period_label,
            "sr_no"                                   : "TOTAL",
            "mutual_fund_name"                        : "Grand Total",
            "avg_aum_excl_domestic_fof_incl_overseas" : (
                grand.get("average_aum_excluding_domestic_including_overseas")
                or grand.get("average_aum_excl_domestic_incl_overseas")
            ),
            "avg_aum_fof_domestic"                    : grand.get("average_aum_fund_of_funds_domestic"),
        })
    return rows


def _flatten_schemewise(raw: dict, fy_label: str, period_label: str, str_type: str) -> list:
    rows = []
    for fund in raw.get("data", []):
        mf_name  = fund.get("Mfname", "")
        mf_id    = fund.get("strMFId", "")
        category = fund.get("SchemeCat_Desc", "")

        for scheme in fund.get("schemes", []):
            aum = scheme.get("AverageAumForTheMonth", {})
            rows.append({
                "financial_year"                          : fy_label,
                "period"                                  : period_label,
                "type"                                    : str_type,
                "mf_id"                                   : mf_id,
                "mutual_fund_name"                        : mf_name,
                "scheme_category"                         : category,
                "scheme_name"                             : scheme.get("SchemeNAVName"),
                "amfi_code"                               : scheme.get("AMFI_Code"),
                "avg_aum_excl_domestic_fof_incl_overseas" : aum.get("ExcludingFundOfFundsDomesticButIncludingFundOfFundsOverseas"),
                "avg_aum_fof_domestic"                    : aum.get("FundOfFundsDomestic"),
            })

        total = fund.get("totalAUM", {})
        if total:
            rows.append({
                "financial_year"                          : fy_label,
                "period"                                  : period_label,
                "type"                                    : str_type,
                "mf_id"                                   : mf_id,
                "mutual_fund_name"                        : mf_name,
                "scheme_category"                         : category,
                "scheme_name"                             : "[FUND TOTAL]",
                "amfi_code"                               : None,
                "avg_aum_excl_domestic_fof_incl_overseas" : total.get("ExcludingFundOfFundsDomesticButIncludingFundOfFundsOverseas"),
                "avg_aum_fof_domestic"                    : total.get("FundOfFundsDomestic"),
            })
    return rows


# ---------------------------------------------------------------------------
# Public API  -- discovery
# ---------------------------------------------------------------------------

def get_financial_years() -> list:
    """
    Return a list of all financial years available on AMFI.

    Returns
    -------
    list of dict
        Each dict has two keys:
            "id"             : int   -- numeric ID used in other calls
            "financial_year" : str   -- human-readable label, e.g. "April 2025 - March 2026"

    Example
    -------
        years = get_financial_years()
        # [{"id": 1, "financial_year": "April 2025 - March 2026"}, ...]
    """
    data = _get(f"{_BASE_URL}/average-aum-fundwise")
    return data.get("data", [])


def get_periods(fy_id: int, mode: str = "fundwise", str_type: str = "Categorywise") -> list:
    """
    Return all reporting periods available for a given financial year.

    Parameters
    ----------
    fy_id    : int
        The financial year ID obtained from get_financial_years().
    mode     : str, optional
        "fundwise" (default) or "schemewise".
        Use "schemewise" when you need periods that match a schemewise query.
    str_type : str, optional
        Only used when mode="schemewise". Either "Categorywise" (default)
        or "Typewise".

    Returns
    -------
    list of dict
        Each dict has two keys:
            "id"     : int -- numeric ID used in data-fetch calls
            "period" : str -- human-readable label, e.g. "January - March 2026"

    Example
    -------
        periods = get_periods(fy_id=1)
        # [{"id": 1, "period": "January - March 2026"}, ...]
    """
    if mode == "fundwise":
        url    = f"{_BASE_URL}/average-aum-fundwise"
        params = {"fyId": fy_id}
    else:
        url    = f"{_BASE_URL}/average-aum-schemewise"
        params = {"fyId": fy_id, "strType": str_type, "MF_ID": 0}

    data = _get(url, params)
    if data.get("type") == "periods":
        d = data.get("data", {})
        if isinstance(d, dict):
            return d.get("periods", [])
        if isinstance(d, list) and d:
            return d[0].get("periods", [])
    return []


# ---------------------------------------------------------------------------
# Public API  -- data fetchers
# ---------------------------------------------------------------------------

def get_fundwise_data(fy_id: int, period_id: int) -> pd.DataFrame:
    """
    Fetch fund-level average AUM for one financial year and period.

    Each row in the returned DataFrame represents one mutual fund house.
    A final row with mutual_fund_name = "Grand Total" contains the industry total.

    Parameters
    ----------
    fy_id     : int
        Financial year ID from get_financial_years().
    period_id : int
        Period ID from get_periods().

    Returns
    -------
    pandas.DataFrame
        Columns:
            financial_year                          : str
            period                                  : str
            sr_no                                   : str
            mutual_fund_name                        : str
            avg_aum_excl_domestic_fof_incl_overseas : float  (INR lakhs)
            avg_aum_fof_domestic                    : float  (INR lakhs)

    Example
    -------
        df = get_fundwise_data(fy_id=1, period_id=1)
        print(df.head())
    """
    raw = _get(f"{_BASE_URL}/average-aum-fundwise",
               {"fyId": fy_id, "periodId": period_id})

    fy_label = raw.get("selectedPeriod", {}).get("financial_year", "")
    p_label  = raw.get("selectedPeriod", {}).get("period", "")

    # Fall back to empty strings if selectedPeriod is absent
    rows = _flatten_fundwise(raw, fy_label, p_label)
    return pd.DataFrame(rows)


def get_schemewise_data(
    fy_id     : int,
    period_id : int,
    str_type  : str = "Categorywise",
    mf_id     : int = 0,
) -> pd.DataFrame:
    """
    Fetch scheme-level average AUM for one financial year, period, and grouping type.

    Each row represents one individual mutual fund scheme.
    Rows with scheme_name = "[FUND TOTAL]" are fund-house-level subtotals.

    Parameters
    ----------
    fy_id     : int
        Financial year ID from get_financial_years().
    period_id : int
        Period ID from get_periods().
    str_type  : str, optional
        Grouping type. Either "Categorywise" (default) or "Typewise".
    mf_id     : int, optional
        Mutual fund house ID. Use 0 (default) to fetch all fund houses at once.

    Returns
    -------
    pandas.DataFrame
        Columns:
            financial_year                          : str
            period                                  : str
            type                                    : str   ("Categorywise" or "Typewise")
            mf_id                                   : str
            mutual_fund_name                        : str
            scheme_category                         : str
            scheme_name                             : str
            amfi_code                               : int
            avg_aum_excl_domestic_fof_incl_overseas : float  (INR lakhs)
            avg_aum_fof_domestic                    : float  (INR lakhs)

    Example
    -------
        df = get_schemewise_data(fy_id=1, period_id=1, str_type="Typewise")
        print(df["scheme_category"].unique())
    """
    raw = _get(f"{_BASE_URL}/average-aum-schemewise",
               {"fyId": fy_id, "periodId": period_id,
                "strType": str_type, "MF_ID": mf_id})

    period_info = raw.get("selectedPeriod", {})
    fy_label    = period_info.get("financial_year", "")
    p_label     = period_info.get("period", "")

    rows = _flatten_schemewise(raw, fy_label, p_label, str_type)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Public API  -- bulk scrape and export
# ---------------------------------------------------------------------------

def scrape_all(output_dir: str = None, delay: float = 0.5) -> dict:
    """
    Download all available AUM data across every financial year, period, and
    grouping mode, then return the results as a dictionary of DataFrames.

    Modes covered:
        - Fundwise           (one row per fund house)
        - Schemewise Categorywise  (one row per scheme, grouped by category)
        - Schemewise Typewise      (one row per scheme, grouped by type)

    Parameters
    ----------
    output_dir : str, optional
        If provided, results are also saved to CSV and Excel files in this
        directory. Pass None (default) to skip saving.
    delay      : float, optional
        Seconds to wait between HTTP requests. Default is 0.5.
        Increase this if you see rate-limit errors.

    Returns
    -------
    dict
        Keys:
            "fundwise"              : pandas.DataFrame
            "schemewise_category"   : pandas.DataFrame
            "schemewise_type"       : pandas.DataFrame

    Example
    -------
        dfs = scrape_all(output_dir="./output")
        print(dfs["fundwise"].shape)
    """
    print("AMFI India - Average AUM Full Scraper")
    print("-" * 40)

    print("Fetching financial years...")
    fy_list = get_financial_years()
    if not fy_list:
        raise RuntimeError("Could not fetch financial years. Check your internet connection.")
    print(f"  Found {len(fy_list)} financial years")

    fundwise_rows = []
    schemewise_cat_rows  = []
    schemewise_type_rows = []
    total = len(fy_list)

    # -- Fundwise -----------------------------------------------------------
    print("\nScraping Fundwise data...")
    for idx, fy in enumerate(fy_list, 1):
        fy_id, fy_label = fy["id"], fy["financial_year"]
        print(f"  [{idx}/{total}] {fy_label}")
        periods = get_periods(fy_id, mode="fundwise")
        time.sleep(delay)
        for p in periods:
            print(f"    period: {p['period']}")
            raw = _get(f"{_BASE_URL}/average-aum-fundwise",
                       {"fyId": fy_id, "periodId": p["id"]})
            fundwise_rows.extend(_flatten_fundwise(raw, fy_label, p["period"]))
            time.sleep(delay)

    # -- Schemewise ---------------------------------------------------------
    for str_type, store, label in [
        ("Categorywise", schemewise_cat_rows,  "Schemewise - Categorywise"),
        ("Typewise",     schemewise_type_rows, "Schemewise - Typewise"),
    ]:
        print(f"\nScraping {label}...")
        for idx, fy in enumerate(fy_list, 1):
            fy_id, fy_label = fy["id"], fy["financial_year"]
            print(f"  [{idx}/{total}] {fy_label}")
            periods = get_periods(fy_id, mode="schemewise", str_type=str_type)
            time.sleep(delay)
            for p in periods:
                print(f"    period: {p['period']}")
                raw = _get(f"{_BASE_URL}/average-aum-schemewise",
                           {"fyId": fy_id, "periodId": p["id"],
                            "strType": str_type, "MF_ID": 0})
                store.extend(_flatten_schemewise(raw, fy_label, p["period"], str_type))
                time.sleep(delay)

    dataframes = {
        "fundwise"            : pd.DataFrame(fundwise_rows),
        "schemewise_category" : pd.DataFrame(schemewise_cat_rows),
        "schemewise_type"     : pd.DataFrame(schemewise_type_rows),
    }

    print(f"\n  fundwise rows            : {len(dataframes['fundwise']):,}")
    print(f"  schemewise category rows : {len(dataframes['schemewise_category']):,}")
    print(f"  schemewise type rows     : {len(dataframes['schemewise_type']):,}")

    if output_dir:
        export_to_csv(dataframes, output_dir)
        export_to_excel(dataframes, output_dir)

    return dataframes


def export_to_csv(dataframes: dict, output_dir: str) -> list:
    """
    Save a dictionary of DataFrames to individual CSV files.

    Parameters
    ----------
    dataframes : dict
        A dict mapping a name string to a pandas.DataFrame.
        Typically the return value of scrape_all().
    output_dir : str
        Directory where CSV files will be written.
        The directory is created if it does not already exist.

    Returns
    -------
    list of str
        Absolute paths of the files that were written.

    Example
    -------
        dfs = scrape_all()
        paths = export_to_csv(dfs, output_dir="./output")
        print(paths)
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for name, df in dataframes.items():
        path = os.path.join(output_dir, f"amfi_aum_{name}.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  Saved: {path}")
        paths.append(os.path.abspath(path))
    return paths


def export_to_excel(dataframes: dict, output_dir: str) -> str:
    """
    Save a dictionary of DataFrames to a single Excel workbook.
    Each DataFrame becomes one sheet.

    Parameters
    ----------
    dataframes : dict
        A dict mapping a name string to a pandas.DataFrame.
        Typically the return value of scrape_all().
    output_dir : str
        Directory where the Excel file will be written.
        The directory is created if it does not already exist.

    Returns
    -------
    str
        Absolute path of the Excel file that was written.

    Example
    -------
        dfs = scrape_all()
        path = export_to_excel(dfs, output_dir="./output")
        print(path)
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "amfi_aum_all.xlsx")
    sheet_names = {
        "fundwise"            : "Fundwise",
        "schemewise_category" : "Schemewise_Categorywise",
        "schemewise_type"     : "Schemewise_Typewise",
    }
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for key, df in dataframes.items():
            sheet = sheet_names.get(key, key)
            df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"  Saved: {path}")
    return os.path.abspath(path)


# ---------------------------------------------------------------------------
# Command-line entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    scrape_all(output_dir=out)
