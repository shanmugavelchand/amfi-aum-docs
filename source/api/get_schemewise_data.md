# get_schemewise_data()

Fetches scheme-level average AUM for one financial year, period, and grouping type.

---

## Signature

```python
amfi_aum.get_schemewise_data(
    fy_id     : int,
    period_id : int,
    str_type  : str = "Categorywise",
    mf_id     : int = 0,
) -> pandas.DataFrame
```

---

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `fy_id` | `int` | required | Financial year ID from `get_financial_years()`. |
| `period_id` | `int` | required | Period ID from `get_periods(mode="schemewise")`. |
| `str_type` | `str` | `"Categorywise"` | Grouping type. Either `"Categorywise"` or `"Typewise"`. Use `amfi_aum.SCHEMEWISE_TYPES` to iterate both. |
| `mf_id` | `int` | `0` | Fund house filter. `0` returns all fund houses in a single response. Pass a specific `mf_id` value (from the `mf_id` column of a prior response) to filter to one fund house. |

---

## Returns

`pandas.DataFrame` — one row per mutual fund scheme, plus fund-house subtotal rows.

See [Data Dictionary](../data_dictionary.md#schemewise-columns) for the full column schema.

---

## Examples

```python
import amfi_aum

# Categorywise grouping — default
df = amfi_aum.get_schemewise_data(fy_id=1, period_id=1)
print(df["scheme_category"].unique())

# Typewise grouping
df = amfi_aum.get_schemewise_data(fy_id=1, period_id=1, str_type="Typewise")

# Iterate both types using the module constant
for t in amfi_aum.SCHEMEWISE_TYPES:
    df = amfi_aum.get_schemewise_data(fy_id=1, period_id=1, str_type=t)
    print(t, df.shape)

# Filter out fund subtotal rows
schemes_only = df[df["scheme_name"] != "[FUND TOTAL]"]
```

---

## Notes

- Rows where `scheme_name = "[FUND TOTAL]"` are fund-house-level subtotals inserted for convenience. Filter them out if you only need individual scheme rows.
- AUM values are in INR lakhs (1 lakh = 100,000 rupees).
- `amfi_code` is null on subtotal rows.
- Use `get_periods(mode="schemewise")` (not the default `"fundwise"` mode) to get the correct period IDs for this function.
