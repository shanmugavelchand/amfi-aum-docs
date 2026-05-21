# scrape_all()

Downloads all available AUM data across every financial year, period, and grouping mode.

---

## Signature

```python
amfi_aum.scrape_all(
    output_dir : str   = None,
    delay      : float = 0.5,
) -> dict[str, pandas.DataFrame]
```

---

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `output_dir` | `str` | `None` | Directory where CSV and Excel files will be saved. Pass `None` to skip saving and only receive the DataFrames. The directory is created automatically if it does not exist. |
| `delay` | `float` | `0.5` | Seconds to wait between HTTP requests. Increase this if the server returns errors. |

---

## Returns

`dict` with three keys:

| Key | Value |
|---|---|
| `"fundwise"` | DataFrame with fund-house-level data for all financial years and periods. |
| `"schemewise_category"` | DataFrame with scheme-level Categorywise data for all financial years and periods. |
| `"schemewise_type"` | DataFrame with scheme-level Typewise data for all financial years and periods. |

---

## Files written (when output_dir is provided)

| File | Contents |
|---|---|
| `amfi_aum_fundwise.csv` | Fundwise DataFrame as CSV |
| `amfi_aum_schemewise_category.csv` | Schemewise Categorywise DataFrame as CSV |
| `amfi_aum_schemewise_type.csv` | Schemewise Typewise DataFrame as CSV |
| `amfi_aum_all.xlsx` | All three DataFrames as separate sheets in one workbook |

---

## Examples

```python
import amfi_aum

# Download everything and save to ./output/
dfs = amfi_aum.scrape_all(output_dir="./output")

# Download without saving to disk
dfs = amfi_aum.scrape_all()
fw  = dfs["fundwise"]
cat = dfs["schemewise_category"]
typ = dfs["schemewise_type"]

# Slower delay if you see server errors
dfs = amfi_aum.scrape_all(output_dir="./output", delay=1.0)
```

---

## Notes

!!! warning
    This function makes approximately 240 HTTP requests. With the default 0.5-second delay it takes around 4 to 5 minutes to complete.

- Progress is printed to stdout as each financial year and period is processed.
- A `RuntimeError` is raised only if the initial financial-years call fails completely. All other failures produce empty DataFrames for the affected periods and are logged to stdout.
