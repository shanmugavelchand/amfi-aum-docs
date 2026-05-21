# export_to_csv()

Saves a dictionary of DataFrames to individual CSV files.

---

## Signature

```python
amfi_aum.export_to_csv(
    dataframes : dict,
    output_dir : str,
) -> list[str]
```

---

## Parameters

| Name | Type | Description |
|---|---|---|
| `dataframes` | `dict` | A dict mapping a name string to a `pandas.DataFrame`. Typically the return value of `scrape_all()`. |
| `output_dir` | `str` | Directory where files will be written. Created automatically if it does not exist. |

---

## Returns

`list of str` — the absolute paths of the files written.

---

## Example

```python
import amfi_aum

dfs   = amfi_aum.scrape_all()
paths = amfi_aum.export_to_csv(dfs, output_dir="./output")

for p in paths:
    print(p)
# /absolute/path/to/output/amfi_aum_fundwise.csv
# /absolute/path/to/output/amfi_aum_schemewise_category.csv
# /absolute/path/to/output/amfi_aum_schemewise_type.csv
```

---

## Notes

- File names follow the pattern `amfi_aum_{key}.csv` where `key` is the dict key.
- Files are encoded as UTF-8 with BOM (`utf-8-sig`) so they open correctly in Excel on Windows.
- Passing `output_dir` to `scrape_all()` calls this function internally. Use `export_to_csv()` directly only if you want to save at a different time or location.
