# Engineering Network Data Validation Script
### Industrial Practice — RGP «Gosgradkadastr», Astana, June–July 2026

**Student:** Auber Arina  
**Program:** Computer Science, IT-2406  
**University:** Astana IT University (AITU)  
**Practice base:** Republican Center for State Urban Planning and Cadastre (Gosgradkadastr)


About

This script was developed during the industrial practice at RGP «Gosgradkadastr» as a data-quality support tool for the engineering-communications inventory workflow.

It validates attribute tables exported from GIS layers describing utility-network segments (water supply, sewerage, electricity, gas, heat networks) before they are submitted to the AIS GGK state urban-planning cadastre database.


## Files

| File | Description |
|------|-------------|
| `validate_engineering_networks.py` | Main validation script |
| `sample_engineering_networks.csv` | Sample dataset (25 records, illustrative) |


## Checks Performed

- Cadastral number format (regex validation)
- Duplicate cadastral numbers
- Missing mandatory fields (network type, diameter, install year, owner)
- Invalid diameter values
- Implausible installation year


## Usage

```bash
python validate_engineering_networks.py sample_engineering_networks.csv qa_report.xlsx
```

Output: flagged records exported to Excel for specialist review.


## Tech Stack

Python 3 · pandas · openpyxl
