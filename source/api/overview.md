# API Reference

The module exposes seven public functions. All functions make live HTTP requests to the AMFI India API.

---

## Discovery functions

These functions return metadata about what data is available. Call them first to get the IDs you need for the data-fetch functions.

| Function | Returns | Use for |
|---|---|---|
| [`get_financial_years()`](get_financial_years.md) | `list of dict` | Getting all `fy_id` values |
| [`get_periods()`](get_periods.md) | `list of dict` | Getting all `period_id` values for a given `fy_id` |

---

## Data-fetch functions

These functions return a `pandas.DataFrame` for a single financial year and period combination.

| Function | Rows | Use for |
|---|---|---|
| [`get_fundwise_data()`](get_fundwise_data.md) | ~52 (one per fund house) | Fund-level AUM |
| [`get_schemewise_data()`](get_schemewise_data.md) | ~1,000+ (one per scheme) | Scheme-level AUM |

---

## Bulk and export functions

| Function | Returns | Use for |
|---|---|---|
| [`scrape_all()`](scrape_all.md) | `dict of DataFrames` | Downloading all data in one call |
| [`export_to_csv()`](export_to_csv.md) | `list of str` | Saving DataFrames as CSV files |
| [`export_to_excel()`](export_to_excel.md) | `str` | Saving DataFrames as a single Excel workbook |

---

## Module constant

```python
amfi_aum.SCHEMEWISE_TYPES  # ("Categorywise", "Typewise")
```

Use this to iterate both grouping types without hard-coding strings.

---

## Error behaviour

All HTTP calls retry up to 3 times with exponential back-off. On permanent failure they log a warning and return an empty `dict`, which produces an empty `DataFrame` in the calling function. `scrape_all()` raises `RuntimeError` only if the initial financial-years call fails completely.
