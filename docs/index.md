# amfi_aum

Python module for fetching Average Assets Under Management (AAUM) data published by the Association of Mutual Funds in India (AMFI).

Clean access to fund-level and scheme-level AUM data across all available financial years and reporting periods. Returns `pandas.DataFrame` objects ready for analysis or export.

---

## Sections

| Section | Description |
|---|---|
| [Quick Start](quickstart.md) | Install the module and fetch your first dataset in under two minutes |
| [API Reference](api/overview.md) | Full parameter reference for every public function |
| [Data Dictionary](data_dictionary.md) | Column-level schema for every DataFrame returned by the module |

---

## Data Coverage

| Data | Function | CSV | Excel |
|---|---|---|---|
| AUM — Fund-wise (all periods) | `scrape_all()` | Yes | Yes |
| AUM — Scheme-wise Categorywise (all periods) | `scrape_all()` | Yes | Yes |
| AUM — Scheme-wise Typewise (all periods) | `scrape_all()` | Yes | Yes |
| AUM — Fund-wise (single period) | `get_fundwise_data()` | — | — |
| AUM — Scheme-wise (single period) | `get_schemewise_data()` | — | — |
| Financial year list | `get_financial_years()` | — | — |
| Period list | `get_periods()` | — | — |

!!! note
    Data is available from April 2006 to the present. From December 2010 onwards the data is published quarterly. Before that it was monthly.

---

## Data Source

All data is fetched from the JSON endpoints used by [amfiindia.com/aum-data/average-aum](https://www.amfiindia.com/aum-data/average-aum).

No API key is required. No authentication is needed.

---

## Requirements

- Python 3.10 or later
- `requests`
- `pandas`
- `openpyxl`
