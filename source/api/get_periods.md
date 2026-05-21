# get_periods()

Returns all reporting periods available for a given financial year.

---

## Signature

```python
amfi_aum.get_periods(
    fy_id    : int,
    mode     : str = "fundwise",
    str_type : str = "Categorywise",
) -> list[dict]
```

---

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `fy_id` | `int` | required | Financial year ID from `get_financial_years()`. |
| `mode` | `str` | `"fundwise"` | Which endpoint to query. Use `"fundwise"` when fetching with `get_fundwise_data()`, or `"schemewise"` when fetching with `get_schemewise_data()`. |
| `str_type` | `str` | `"Categorywise"` | Only relevant when `mode="schemewise"`. Either `"Categorywise"` or `"Typewise"`. |

---

## Returns

`list of dict` — Each dict has two keys:

| Key | Type | Description |
|---|---|---|
| `id` | `int` | Numeric identifier. Pass this as `period_id` in data-fetch functions. |
| `period` | `str` | Human-readable label, e.g. `"January - March 2026"`. |

---

## Examples

```python
import amfi_aum

# Periods for use with get_fundwise_data()
periods = amfi_aum.get_periods(fy_id=1)
# [{"id": 1, "period": "January - March 2026"}, ...]

# Periods for use with get_schemewise_data(str_type="Typewise")
periods = amfi_aum.get_periods(fy_id=1, mode="schemewise", str_type="Typewise")
```

---

## Notes

- For recent financial years (from December 2010 onwards) there are typically 4 periods per year, one per quarter.
- For older financial years (before December 2010) there may be more periods because data was reported monthly.
- Period IDs start at 1 for the most recent quarter and increment backwards in time.
