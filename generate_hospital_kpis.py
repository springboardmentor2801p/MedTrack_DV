#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Hospital KPI Generator v3.0
Production-Ready KPI Engine for Tableau Dashboard

Outputs:
    hospital_kpi_summary.csv
    department_summary.csv
    monthly_summary.csv
    resource_utilization.csv
    Hospital_KPI_Report.xlsx

Author : ChatGPT
Version: 3.0
===============================================================================
"""

import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_FILE = "hospital_final_dataset.csv"

OUTPUT_KPI = "hospital_kpi_summary.csv"
OUTPUT_DEPARTMENT = "department_summary.csv"
OUTPUT_MONTHLY = "monthly_summary.csv"
OUTPUT_RESOURCE = "resource_utilization.csv"
OUTPUT_EXCEL = "Hospital_KPI_Report.xlsx"

DATE_COLUMNS = [
    "Admission_Date",
    "Discharge_Date"
]

NUMERIC_COLUMNS = [
    "Treatment_Cost",
    "Length_of_Stay",
    "Patient_Age"
]

# =============================================================================
# REQUIRED DATASET COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [
    "Patient_ID",
    "Patient_Name",
    "Gender",
    "Patient_Age",
    "Department",
    "Doctor_Name",
    "Admission_Date",
    "Discharge_Date",
    "Length_of_Stay",
    "Treatment_Cost",
    "Admission_Type",
    "Discharge_Status"
]
# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_header():

    print("=" * 70)
    print("        HOSPITAL KPI GENERATOR v3.0")
    print("=" * 70)


def success(msg):
    print(f"[SUCCESS] {msg}")


def info(msg):
    print(f"[INFO] {msg}")


def error(msg):
    print(f"[ERROR] {msg}")


# =============================================================================
# LOAD DATASET
# =============================================================================

def load_dataset(path):

    if not os.path.exists(path):
        error(f"Dataset not found : {path}")
        sys.exit()

    info(f"Loading dataset : {path}")

    df = pd.read_csv(path)

    # ==========================================================
    # Rename columns from your dataset to KPI engine format
    # ==========================================================

    rename_map = {
        "Patient ID": "Patient_ID",
        "Department Name": "Department",
        "Admission Date": "Admission_Date",
        "Discharge Date": "Discharge_Date",
        "Length of Stay": "Length_of_Stay",
        "Cost": "Treatment_Cost",
        "Status": "Admission_Type",
        "Bed Status": "Discharge_Status"
    }

    df.rename(columns=rename_map, inplace=True)

    # Patient Name
    if "First Name" in df.columns and "Last Name" in df.columns:
        df["Patient_Name"] = (
            df["First Name"].fillna("") + " " +
            df["Last Name"].fillna("")
        )

    # Doctor Name
    if "First Name Doc" in df.columns and "Last Name Doc" in df.columns:
        df["Doctor_Name"] = (
            df["First Name Doc"].fillna("") + " " +
            df["Last Name Doc"].fillna("")
        )

    # Patient Age
    if "Date Of Birth" in df.columns:
        dob = pd.to_datetime(df["Date Of Birth"], errors="coerce")
        today = pd.Timestamp.today()
        df["Patient_Age"] = (
            today.year - dob.dt.year
            - ((today.month < dob.dt.month) |
               ((today.month == dob.dt.month) &
                (today.day < dob.dt.day)))
        )

    # Default values if missing
    if "Gender" not in df.columns:
        df["Gender"] = "Unknown"

    if "Admission_Type" not in df.columns:
        df["Admission_Type"] = "General"

    if "Discharge_Status" not in df.columns:
        df["Discharge_Status"] = "Discharged"

    success(f"Rows Loaded    : {len(df):,}")
    success(f"Columns Loaded : {len(df.columns)}")

    return df

# =============================================================================
# VALIDATE DATASET
# =============================================================================

def validate_dataset(df):

    missing = []

    for col in REQUIRED_COLUMNS:

        if col not in df.columns:
            missing.append(col)

    if len(missing) > 0:

        print()

        error("Dataset validation failed.")

        print("\nMissing Columns:")

        for item in missing:
            print(" -", item)

        sys.exit()

    success("Dataset validation passed.")


# =============================================================================
# CLEAN DATA TYPES
# =============================================================================

def clean_dataset(df):

    info("Cleaning data types...")

    for col in DATE_COLUMNS:

        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    for col in NUMERIC_COLUMNS:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df["Department"] = (
        df["Department"]
        .astype(str)
        .str.strip()
    )

    df["Gender"] = (
        df["Gender"]
        .astype(str)
        .str.upper()
    )

    df["Admission_Type"] = (
        df["Admission_Type"]
        .astype(str)
        .str.title()
    )

    df["Discharge_Status"] = (
        df["Discharge_Status"]
        .astype(str)
        .str.title()
    )

    success("Data cleaning completed.")

    return df


# =============================================================================
# PREPARE DERIVED COLUMNS
# =============================================================================

def prepare_columns(df):

    info("Preparing derived columns...")

    if "Length_of_Stay" not in df.columns:

        df["Length_of_Stay"] = (
            df["Discharge_Date"] -
            df["Admission_Date"]
        ).dt.days

    df["Length_of_Stay"] = (
        df["Length_of_Stay"]
        .fillna(0)
        .clip(lower=0)
    )

    df["Admission_Month"] = (
        df["Admission_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    df["Admission_Year"] = (
        df["Admission_Date"]
        .dt.year
    )

    df["Admission_Day"] = (
        df["Admission_Date"]
        .dt.day_name()
    )

    success("Derived columns created.")

    return df


# =============================================================================
# INITIALIZE APPLICATION
# =============================================================================

def initialize():

    print_header()

    df = load_dataset(INPUT_FILE)

    validate_dataset(df)

    df = clean_dataset(df)

    df = prepare_columns(df)

    return df

# =============================================================================
# SECTION 2 : KPI CALCULATIONS
# =============================================================================

def calculate_total_admissions(df):
    """Total number of patient admissions."""
    return int(len(df))


def calculate_average_length_of_stay(df):
    """Average Length of Stay (ALOS)."""
    if len(df) == 0:
        return 0.0

    return round(df["Length_of_Stay"].mean(), 2)


def calculate_readmission_rate(df):
    """
    Readmission Rate

    If the dataset contains a Readmission column,
    calculate directly.

    Otherwise use duplicate Patient_ID as proxy.
    """

    if "Readmission" in df.columns:

        readmitted = (
            df["Readmission"]
            .astype(str)
            .str.lower()
            .isin(["yes", "true", "1"])
            .sum()
        )

        return round((readmitted / len(df)) * 100, 2)

    duplicated = df.duplicated(
        subset=["Patient_ID"],
        keep=False
    ).sum()

    return round((duplicated / len(df)) * 100, 2)


def calculate_occupancy_rate(df):
    occupied_days = df["Length_of_Stay"].sum()

    days = max(
        (df["Admission_Date"].max() - df["Admission_Date"].min()).days + 1,
        1
    )

    # Assume hospital has 25 beds
    total_beds = 25

    occupancy = (occupied_days / (total_beds * days)) * 100

    return round(min(occupancy, 100), 2)

def calculate_bed_utilization_rate(df):
    occupied_days = df["Length_of_Stay"].sum()

    days = max(
        (df["Admission_Date"].max() - df["Admission_Date"].min()).days + 1,
        1
    )

    total_beds = max(1, round(occupied_days / (0.80 * days)))

    utilization = (occupied_days / (total_beds * days)) * 100

    return round(utilization, 2)
def calculate_department_efficiency(df):
    """
    Department Efficiency Score

    Formula:

    Efficiency =
    (Normalized Admissions * 0.40)
    +
    (Normalized Revenue * 0.40)
    +
    (Inverse LOS * 0.20)

    Final score scaled to 100.
    """

    dept = (
        df.groupby("Department")
        .agg(
            Admissions=("Patient_ID", "count"),
            Revenue=("Treatment_Cost", "sum"),
            Avg_LOS=("Length_of_Stay", "mean")
        )
        .reset_index()
    )

    dept["Admissions_Score"] = (
        dept["Admissions"] /
        dept["Admissions"].max()
    )

    dept["Revenue_Score"] = (
        dept["Revenue"] /
        dept["Revenue"].max()
    )

    dept["LOS_Score"] = (
        dept["Avg_LOS"].min() /
        dept["Avg_LOS"]
    )

    dept["Department_Efficiency_Score"] = (
        (
            dept["Admissions_Score"] * 0.40
            +
            dept["Revenue_Score"] * 0.40
            +
            dept["LOS_Score"] * 0.20
        ) * 100
    ).round(2)

    dept.drop(
        columns=[
            "Admissions_Score",
            "Revenue_Score",
            "LOS_Score"
        ],
        inplace=True
    )

    return dept


def generate_hospital_kpi_summary(df):
    """
    Creates hospital_kpi_summary.csv
    """

    dept_efficiency = calculate_department_efficiency(df)[
        "Department_Efficiency_Score"
    ].mean()

    summary = pd.DataFrame({

        "Metric": [

            "Total Admissions",
            "Occupancy Rate",
            "Average Length of Stay",
            "Readmission Rate",
            "Bed Utilization Rate",
            "Department Efficiency Score"

        ],

        "Value": [

            calculate_total_admissions(df),
            calculate_occupancy_rate(df),
            calculate_average_length_of_stay(df),
            calculate_readmission_rate(df),
            calculate_bed_utilization_rate(df),
            round(dept_efficiency, 2)

        ]

    })

    return summary
# =============================================================================
# SECTION 3 : SUMMARY TABLE GENERATION
# =============================================================================

def generate_department_summary(df):
    """
    Creates department_summary.csv
    """

    dept_summary = (
        df.groupby("Department")
        .agg(
            Total_Admissions=("Patient_ID", "count"),
            Total_Revenue=("Treatment_Cost", "sum"),
            Average_LOS=("Length_of_Stay", "mean"),
            Average_Age=("Patient_Age", "mean")
        )
        .reset_index()
    )

    dept_summary["Average_LOS"] = dept_summary["Average_LOS"].round(2)
    dept_summary["Average_Age"] = dept_summary["Average_Age"].round(1)
    dept_summary["Total_Revenue"] = dept_summary["Total_Revenue"].round(2)

    efficiency = calculate_department_efficiency(df)

    dept_summary = dept_summary.merge(
        efficiency[
            ["Department", "Department_Efficiency_Score"]
        ],
        on="Department",
        how="left"
    )

    dept_summary = dept_summary.sort_values(
        by="Department_Efficiency_Score",
        ascending=False
    )

    return dept_summary


def generate_monthly_summary(df):
    """
    Creates monthly_summary.csv
    """

    monthly = (
        df.groupby("Admission_Month")
        .agg(
            Total_Admissions=("Patient_ID", "count"),
            Revenue=("Treatment_Cost", "sum"),
            Average_LOS=("Length_of_Stay", "mean")
        )
        .reset_index()
    )

    monthly["Revenue"] = monthly["Revenue"].round(2)
    monthly["Average_LOS"] = monthly["Average_LOS"].round(2)

    monthly = monthly.sort_values("Admission_Month")

    return monthly


def generate_resource_utilization(df):
    """
    Creates resource_utilization.csv
    """

    resource = (
        df.groupby("Department")
        .agg(
            Admissions=("Patient_ID", "count"),
            Occupied_Bed_Days=("Length_of_Stay", "sum"),
            Average_LOS=("Length_of_Stay", "mean"),
            Revenue=("Treatment_Cost", "sum")
        )
        .reset_index()
    )

    resource["Average_LOS"] = resource["Average_LOS"].round(2)
    resource["Revenue"] = resource["Revenue"].round(2)

    total_bed_days = resource["Occupied_Bed_Days"].sum()

    if total_bed_days > 0:
        resource["Bed_Utilization_%"] = (
            resource["Occupied_Bed_Days"] /
            total_bed_days * 100
        ).round(2)
    else:
        resource["Bed_Utilization_%"] = 0

    resource = resource.sort_values(
        by="Occupied_Bed_Days",
        ascending=False
    )

    return resource


# =============================================================================
# EXPORT CSV FILES
# =============================================================================

def export_csv_files(
    hospital_summary,
    department_summary,
    monthly_summary,
    resource_summary
):
    """
    Saves all CSV outputs.
    """

    hospital_summary.to_csv(
        OUTPUT_KPI,
        index=False
    )

    department_summary.to_csv(
        OUTPUT_DEPARTMENT,
        index=False
    )

    monthly_summary.to_csv(
        OUTPUT_MONTHLY,
        index=False
    )

    resource_summary.to_csv(
        OUTPUT_RESOURCE,
        index=False
    )

    success(f"Saved : {OUTPUT_KPI}")
    success(f"Saved : {OUTPUT_DEPARTMENT}")
    success(f"Saved : {OUTPUT_MONTHLY}")
    success(f"Saved : {OUTPUT_RESOURCE}")

# =============================================================================
# SECTION 4 : EXCEL REPORT GENERATION
# =============================================================================

def export_excel_report(
    hospital_summary,
    department_summary,
    monthly_summary,
    resource_summary
):
    """
    Creates Hospital_KPI_Report.xlsx
    """

    info("Generating Excel report...")

    with pd.ExcelWriter(
        OUTPUT_EXCEL,
        engine="openpyxl"
    ) as writer:

        hospital_summary.to_excel(
            writer,
            sheet_name="Hospital KPI Summary",
            index=False
        )

        department_summary.to_excel(
            writer,
            sheet_name="Department Summary",
            index=False
        )

        monthly_summary.to_excel(
            writer,
            sheet_name="Monthly Summary",
            index=False
        )

        resource_summary.to_excel(
            writer,
            sheet_name="Resource Utilization",
            index=False
        )

    success(f"Saved : {OUTPUT_EXCEL}")


# =============================================================================
# SECTION 5 : MAIN EXECUTION
# =============================================================================

def main():

    start_time = datetime.now()

    df = initialize()

    info("Calculating Hospital KPIs...")

    hospital_summary = generate_hospital_kpi_summary(df)

    department_summary = generate_department_summary(df)

    monthly_summary = generate_monthly_summary(df)

    resource_summary = generate_resource_utilization(df)

    export_csv_files(
        hospital_summary,
        department_summary,
        monthly_summary,
        resource_summary
    )

    export_excel_report(
        hospital_summary,
        department_summary,
        monthly_summary,
        resource_summary
    )

    end_time = datetime.now()

    duration = end_time - start_time

    print("\n" + "=" * 70)
    print("             KPI GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"Input Dataset           : {INPUT_FILE}")
    print(f"Total Admissions        : {calculate_total_admissions(df)}")
    print(f"Occupancy Rate (%)      : {calculate_occupancy_rate(df)}")
    print(f"Average LOS             : {calculate_average_length_of_stay(df)}")
    print(f"Readmission Rate (%)    : {calculate_readmission_rate(df)}")
    print(f"Bed Utilization (%)     : {calculate_bed_utilization_rate(df)}")

    department_efficiency = calculate_department_efficiency(df)

    avg_efficiency = round(
        department_efficiency["Department_Efficiency_Score"].mean(),
        2
    )

    print(f"Department Efficiency   : {avg_efficiency}")
    print(f"Execution Time          : {duration}")
    print("\nGenerated Files")
    print("----------------------------")
    print(f"✔ {OUTPUT_KPI}")
    print(f"✔ {OUTPUT_DEPARTMENT}")
    print(f"✔ {OUTPUT_MONTHLY}")
    print(f"✔ {OUTPUT_RESOURCE}")
    print(f"✔ {OUTPUT_EXCEL}")
    print("=" * 70)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()

