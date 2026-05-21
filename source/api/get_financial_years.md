# get_financial_years()

Returns a list of all financial years for which AMFI has published average AUM data.

---

## Signature

```python
amfi_aum.get_financial_years() -> list[dict]
```

---

## Parameters

This function takes no parameters.

---

## Returns

`list of dict` — Each dict has two keys:

| Key | Type | Description |
|---|---|---|
| `id` | `int` | Numeric identifier. Pass this as `fy_id` in other functions. |
| `financial_year` | `str` | Human-readable label, e.g. `"April 2025 - March 2026"`. |

---

## Example

```python
import amfi_aum

years = amfi_aum.get_financial_years()

for y in years:
    print(y["id"], y["financial_year"])

# 1  April 2025 - March 2026
# 2  April 2024 - March 2025
# ...
# 20 April 2006 - March 2007
```

---

## Notes

- As of May 2026 there are 20 financial years, from ID 1 (most recent) to ID 20 (oldest).
- IDs are assigned by AMFI. Do not hard-code them — always call this function at runtime to get current IDs.
