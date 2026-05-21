# export_to_excel()

Saves a dictionary of DataFrames to a single Excel workbook. Each DataFrame becomes one sheet.

---

## Signature

```python
amfi_aum.export_to_excel(
    dataframes : dict,
    output_dir : str,
) -> str
```

---

## Parameters

| Name | Type | Description |
|---|---|---|
| `dataframes` | `dict` | A dict mapping a name string to a `pandas.DataFrame`. Typically the return value of `scrape_all()`. |
| `output_dir` | `str` | Directory where the file will be written. Created automatically if it does not exist. |

---

## Returns

`str` — the absolute path of the Excel file written.

---

## Example

```python
import amfi_aum

dfs  = amfi_aum.scrape_all()
path = amfi_aum.export_to_excel(dfs, output_dir="./output")
print(path)
# /absolute/path/to/output/amfi_aum_all.xlsx
```

---

## Notes

- The output file is always named `amfi_aum_all.xlsx`.
- Sheet names are mapped as follows:

| Dict key | Sheet name |
|---|---|
| `fundwise` | `Fundwise` |
| `schemewise_category` | `Schemewise_Categorywise` |
| `schemewise_type` | `Schemewise_Typewise` |

- For any key not in the mapping above, the sheet name equals the dict key.
- Passing `output_dir` to `scrape_all()` calls this function internally.
