# Data Dictionary

Column-level schema for every DataFrame returned by the module.

All monetary values are in Indian Rupees (INR) expressed in **lakhs** (1 lakh = 100,000).

---

## Fundwise columns

Returned by `get_fundwise_data()` and found in `scrape_all()["fundwise"]`.

| Column | Type | Description |
|---|---|---|
| `financial_year` | `str` | Financial year label, e.g. `"April 2025 - March 2026"`. |
| `period` | `str` | Reporting period label, e.g. `"January - March 2026"`. |
| `sr_no` | `str` | Serial number. The value `"TOTAL"` appears on the grand total row. |
| `mutual_fund_name` | `str` | Name of the mutual fund house (AMC). `"Grand Total"` on the total row. |
| `avg_aum_excl_domestic_fof_incl_overseas` | `float` | Average AUM excluding domestic fund-of-funds but including overseas fund-of-funds. INR lakhs. |
| `avg_aum_fof_domestic` | `float` | Average AUM from domestic fund-of-funds only. INR lakhs. |

**Row count:** approximately 52 fund houses plus 1 grand total row per period.

---

## Schemewise columns

Returned by `get_schemewise_data()` and found in `scrape_all()["schemewise_category"]` and `scrape_all()["schemewise_type"]`.

| Column | Type | Description |
|---|---|---|
| `financial_year` | `str` | Financial year label. |
| `period` | `str` | Reporting period label. |
| `type` | `str` | Grouping type: `"Categorywise"` or `"Typewise"`. |
| `mf_id` | `str` | Fund house identifier as returned by AMFI. `"0"` when `mf_id=0` was passed (all funds). |
| `mutual_fund_name` | `str` | Name of the mutual fund house. |
| `scheme_category` | `str` | Scheme category description, e.g. `"Other Scheme - Other ETFs"`. |
| `scheme_name` | `str` | Full scheme name as registered with AMFI. The value `"[FUND TOTAL]"` appears on fund-house subtotal rows. |
| `amfi_code` | `int` | Unique AMFI scheme code. `null` on subtotal rows. |
| `avg_aum_excl_domestic_fof_incl_overseas` | `float` | Average AUM excluding domestic fund-of-funds but including overseas fund-of-funds. INR lakhs. |
| `avg_aum_fof_domestic` | `float` | Average AUM from domestic fund-of-funds only. INR lakhs. |

**Row count:** approximately 1,000 or more scheme rows plus fund-house subtotal rows per period.

---

## Filtering tips

Remove the grand total row from fundwise data:

```python
df = df[df["sr_no"] != "TOTAL"]
```

Remove fund-house subtotal rows from schemewise data:

```python
df = df[df["scheme_name"] != "[FUND TOTAL]"]
```

Filter to a specific fund house by name:

```python
df = df[df["mutual_fund_name"] == "HDFC Mutual Fund"]
```

Filter to a specific scheme category:

```python
df = df[df["scheme_category"] == "Equity Scheme - Large Cap Fund"]
```
