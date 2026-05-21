# get_fundwise_data()

Fetches fund-house-level average AUM for one financial year and period.

---

## Signature

```python
amfi_aum.get_fundwise_data(
    fy_id     : int,
    period_id : int,
) -> pandas.DataFrame
```

---

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `fy_id` | `int` | required | Financial year ID from `get_financial_years()`. |
| `period_id` | `int` | required | Period ID from `get_periods()`. |

---

## Returns

`pandas.DataFrame` — one row per mutual fund house, plus a final `"Grand Total"` row.

See [Data Dictionary](../data_dictionary.md#fundwise-columns) for the full column schema.

---

## Example

```python
import amfi_aum

df = amfi_aum.get_fundwise_data(fy_id=1, period_id=1)

print(df.shape)           # (53, 6)  — 52 funds + 1 total row
print(df.columns.tolist())
print(df.head(3))
```

---

## Notes

- Each row represents one mutual fund house (AMC).
- The last row has `mutual_fund_name = "Grand Total"` and `sr_no = "TOTAL"`. Filter it out with `df[df["sr_no"] != "TOTAL"]` if you do not need industry totals.
- AUM values are in INR lakhs (1 lakh = 100,000 rupees).
