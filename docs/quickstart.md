# Quick Start

## Installation

Copy `amfi_aum.py` into your project directory. Then install the three required packages:

```bash
pip install requests pandas openpyxl
```

Python 3.10 or later is required.

---

## Fetch all financial years

```python
import amfi_aum

years = amfi_aum.get_financial_years()
print(years[0])
# {"id": 1, "financial_year": "April 2025 - March 2026"}
```

---

## Fetch periods within a financial year

```python
periods = amfi_aum.get_periods(fy_id=1)
print(periods[0])
# {"id": 1, "period": "January - March 2026"}
```

---

## Fetch fund-level data for one period

```python
df = amfi_aum.get_fundwise_data(fy_id=1, period_id=1)
print(df[["mutual_fund_name", "avg_aum_excl_domestic_fof_incl_overseas"]])
```

---

## Fetch scheme-level data for one period

```python
df = amfi_aum.get_schemewise_data(
    fy_id=1,
    period_id=1,
    str_type="Categorywise"
)
print(df["scheme_category"].unique())
```

---

## Download everything and save to files

```python
dfs = amfi_aum.scrape_all(output_dir="./output")

print(dfs["fundwise"].shape)
print(dfs["schemewise_category"].shape)
print(dfs["schemewise_type"].shape)
```

This writes four files to `./output/`:

- `amfi_aum_fundwise.csv`
- `amfi_aum_schemewise_category.csv`
- `amfi_aum_schemewise_type.csv`
- `amfi_aum_all.xlsx` (all three sheets combined)

!!! note
    `scrape_all()` makes approximately 240 HTTP requests. With the default 0.5-second delay it takes around 4 to 5 minutes.

---

## Run from the command line

You can also run the module directly as a script. Pass an optional output directory as the first argument:

```bash
python amfi_aum.py ./output
```

If no argument is given, files are saved in the same directory as the script.
