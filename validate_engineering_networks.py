import re
import sys
from datetime import datetime
import pandas as pd

CADASTRAL_NUMBER_PATTERN = re.compile(r"^\d{2}-\d{3}-\d{3}-\d{3}$")
MANDATORY_FIELDS = ["network_type", "diameter_mm", "install_year", "owner_organization"]
MIN_YEAR = 1950
CURRENT_YEAR = datetime.now().year

def load_dataset(path):
    return pd.read_csv(path, dtype={"cadastral_number": str})

def check_cadastral_number_format(df):
    return ~df["cadastral_number"].astype(str).str.match(CADASTRAL_NUMBER_PATTERN)

def check_duplicates(df):
    return df["cadastral_number"].duplicated(keep=False)

def check_missing_mandatory_fields(df):
    missing = pd.Series(False, index=df.index)
    for field in MANDATORY_FIELDS:
        missing = missing | df[field].isna() | (df[field].astype(str).str.strip() == "")
    return missing

def check_diameter_valid(df):
    numeric_diameter = pd.to_numeric(df["diameter_mm"], errors="coerce")
    return numeric_diameter.isna() | (numeric_diameter <= 0)

def check_install_year_valid(df):
    numeric_year = pd.to_numeric(df["install_year"], errors="coerce")
    return numeric_year.isna() | (numeric_year < MIN_YEAR) | (numeric_year > CURRENT_YEAR)

def run_validation(df):
    report = df.copy()
    report["err_format"] = check_cadastral_number_format(df)
    report["err_duplicate"] = check_duplicates(df)
    report["err_missing_field"] = check_missing_mandatory_fields(df)
    report["err_diameter"] = check_diameter_valid(df)
    report["err_year"] = check_install_year_valid(df)
    error_columns = ["err_format", "err_duplicate", "err_missing_field", "err_diameter", "err_year"]
    report["has_error"] = report[error_columns].any(axis=1)
    return report

def print_summary(report):
    total = len(report)
    flagged = int(report["has_error"].sum())
    print(f"Engineering networks QA report — {total} records checked")
    print("-" * 52)
    print(f"  Invalid cadastral number format : {int(report['err_format'].sum())}")
    print(f"  Duplicate cadastral numbers      : {int(report['err_duplicate'].sum())}")
    print(f"  Missing mandatory fields         : {int(report['err_missing_field'].sum())}")
    print(f"  Invalid diameter (<=0 / non-num.): {int(report['err_diameter'].sum())}")
    print(f"  Invalid installation year        : {int(report['err_year'].sum())}")
    print("-" * 52)
    print(f"  TOTAL records flagged for review : {flagged} / {total}")

def main(input_path, output_path):
    df = load_dataset(input_path)
    report = run_validation(df)
    print_summary(report)
    flagged_rows = report[report["has_error"]]
    flagged_rows.to_excel(output_path, index=False)
    print(f"\nFlagged records written to: {output_path}")

if __name__ == "__main__":
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "sample_engineering_networks.csv"
    output_xlsx = sys.argv[2] if len(sys.argv) > 2 else "qa_report_flagged_records.xlsx"
    main(input_csv, output_xlsx)
