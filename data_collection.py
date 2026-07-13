"""
Module 1: Hospital Data Collection
Loads the source hospital dataset and exports the integrated raw dataset.
"""

import pandas as pd

SOURCE_FILE = "hospital_raw_data_.xlsx"
OUTPUT_FILE = "hospital_raw_data.csv"

def load_data(path: str) -> pd.DataFrame:
    """Load the hospital dataset (patient, department, and resource data combined)."""
    df = pd.read_excel(path)
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} columns.")
    return df


def check_completeness(df: pd.DataFrame) -> float:
    """Return overall dataset completeness as a percentage."""
    completeness = df.notna().mean().mean() * 100
    print(f"Dataset completeness: {completeness:.2f}%")
    return completeness


def main():
    df = load_data(SOURCE_FILE)

    # This dataset already integrates patient admissions, department, and
    # resource/bed data into a single table, so no separate merge step is
    # required. If additional sources are added later (e.g. a standalone
    # resource file), merge them here on a shared key such as Department
    # or Hospital before exporting.

    completeness = check_completeness(df)
    assert completeness > 95, "Dataset completeness below 95% threshold."

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved integrated dataset to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
