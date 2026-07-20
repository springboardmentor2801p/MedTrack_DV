#!/usr/bin/env python3
"""Build Tableau-ready hospital datasets and KPI summary workbooks."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


INPUT_FILE = Path("hospital_dataset.xlsx")
FINAL_DATASET_FILE = Path("hospital_final_dataset.xlsx")
SUMMARY_FILE = Path("hospital_kpi_summary.xlsx")

DATE_COLUMNS = ("Admission_Date", "Discharge_Date", "Follow_Up_Date", "Created_At")
NUMERIC_COLUMNS = ("Age", "Bill_Amount", "Hospital_Rating", "Total_Beds")
REQUIRED_COLUMNS = (
    "Patient_ID",
    "Admission_ID",
    "Admission_Date",
    "Discharge_Date",
    "Department",
)

LOGGER = logging.getLogger("hospital_kpis")


def standardize_column_name(column: object) -> str:
    """Return a Tableau-friendly Pascal_Snake_Case column name."""
    text = str(column).strip().replace("&", "And")
    text = "_".join(text.replace("-", " ").replace("/", " ").split())
    return "_".join(part[:1].upper() + part[1:] for part in text.split("_") if part)


def read_dataset(path: Path) -> pd.DataFrame:
    """Read and validate the source Excel workbook."""
    if not path.exists():
        raise FileNotFoundError(f"Input workbook not found: {path.resolve()}")
    LOGGER.info("Reading source workbook: %s", path)
    frame = pd.read_excel(path, engine="openpyxl")
    if frame.empty:
        raise ValueError("The source workbook contains no patient records.")
    frame.columns = [standardize_column_name(column) for column in frame.columns]
    missing = sorted(set(REQUIRED_COLUMNS).difference(frame.columns))
    if missing:
        raise ValueError(f"Required columns are missing: {', '.join(missing)}")
    return frame


def _fill_missing_values(frame: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values without deleting otherwise valid admissions."""
    numeric_columns = frame.select_dtypes(include="number").columns
    for column in numeric_columns:
        median = frame[column].median()
        frame[column] = frame[column].fillna(0 if pd.isna(median) else median)

    text_columns = frame.select_dtypes(include=("object", "string")).columns
    for column in text_columns:
        if column.endswith("_ID") or column in {"Patient_ID", "Admission_ID"}:
            frame[column] = frame[column].fillna("Unknown")
        else:
            mode = frame[column].mode(dropna=True)
            frame[column] = frame[column].fillna(mode.iloc[0] if not mode.empty else "Unknown")
    return frame


def clean_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, coerce types, and impute missing values."""
    original_rows = len(frame)
    duplicate_key = ["Admission_ID"] if "Admission_ID" in frame else None
    frame = frame.drop_duplicates(subset=duplicate_key, keep="first").copy()
    LOGGER.info("Removed %d duplicate admission rows", original_rows - len(frame))

    for column in DATE_COLUMNS:
        if column in frame:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")

    # Records without valid core dates cannot support stay or utilization KPIs.
    invalid_dates = frame[["Admission_Date", "Discharge_Date"]].isna().any(axis=1)
    if invalid_dates.any():
        LOGGER.warning("Dropping %d rows with invalid core dates", int(invalid_dates.sum()))
        frame = frame.loc[~invalid_dates].copy()

    reversed_dates = frame["Discharge_Date"] < frame["Admission_Date"]
    if reversed_dates.any():
        LOGGER.warning("Correcting %d discharge dates earlier than admission", int(reversed_dates.sum()))
        frame.loc[reversed_dates, "Discharge_Date"] = frame.loc[reversed_dates, "Admission_Date"]

    for column in NUMERIC_COLUMNS:
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = _fill_missing_values(frame)
    frame["Age"] = frame["Age"].clip(lower=0).round().astype("int64")
    frame["Admission_Month"] = frame["Admission_Date"].dt.to_period("M").dt.to_timestamp()
    return frame.reset_index(drop=True)


def add_readmission_fields(frame: pd.DataFrame) -> pd.DataFrame:
    """Flag admissions occurring within 30 days of a prior discharge."""
    ordered = frame.sort_values(["Patient_ID", "Admission_Date", "Admission_ID"]).copy()
    ordered["Previous_Discharge_Date"] = ordered.groupby("Patient_ID")["Discharge_Date"].shift()
    ordered["Days_Since_Previous_Discharge"] = (
        ordered["Admission_Date"] - ordered["Previous_Discharge_Date"]
    ).dt.days
    ordered["Readmitted_Within_30_Days"] = ordered["Days_Since_Previous_Discharge"].between(
        0, 30, inclusive="both"
    )
    return ordered.sort_index().drop(columns="Previous_Discharge_Date")


def add_capacity_fields(frame: pd.DataFrame) -> pd.DataFrame:
    """Add total beds and occupied-bed metrics with a schema-safe fallback."""
    scope = [column for column in ("Hospital_ID", "Department") if column in frame]
    if not scope:
        scope = ["Department"]

    supplied_capacity = next(
        (column for column in ("Total_Beds", "Bed_Capacity", "Available_Beds") if column in frame),
        None,
    )
    if supplied_capacity:
        capacity = pd.to_numeric(frame[supplied_capacity], errors="coerce")
        fallback = frame.groupby(scope)["Bed_Number"].transform("nunique") if "Bed_Number" in frame else 1
        frame["Total_Beds"] = capacity.fillna(fallback).clip(lower=1)
    elif "Bed_Number" in frame:
        frame["Total_Beds"] = frame.groupby(scope)["Bed_Number"].transform("nunique").clip(lower=1)
        LOGGER.info("Total beds inferred from distinct bed identifiers by hospital and department")
    else:
        frame["Total_Beds"] = 1
        LOGGER.warning("No bed capacity fields found; defaulting Total_Beds to 1")

    hospital_key = frame["Hospital_ID"].astype(str) if "Hospital_ID" in frame else "Hospital"
    department_key = frame["Department"].astype(str)
    bed_key = frame["Bed_Number"].astype(str) if "Bed_Number" in frame else frame.index.astype(str)
    frame["Capacity_Scope_Key"] = hospital_key + "|" + department_key
    frame["Bed_Scope_Key"] = frame["Capacity_Scope_Key"] + "|" + bed_key
    frame["Occupied_Beds"] = 1
    frame["Length_Of_Stay_Days"] = (
        frame["Discharge_Date"] - frame["Admission_Date"]
    ).dt.days.clip(lower=0)
    # A same-day admission consumes one operational bed day.
    frame["Occupied_Bed_Days"] = frame["Length_Of_Stay_Days"].clip(lower=1)
    return frame


def _safe_percentage(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return np.where(denominator.gt(0), numerator.div(denominator).mul(100), 0.0)


def _efficiency_score(summary: pd.DataFrame) -> pd.Series:
    """Create a balanced 0-100 score from four normalized KPI components."""
    alos_score = (100 - summary["Average_Length_Of_Stay_Days"].div(30).mul(100)).clip(0, 100)
    readmission_score = (100 - summary["Readmission_Rate_Pct"]).clip(0, 100)
    occupancy_score = summary["Occupancy_Rate_Pct"].clip(0, 100)
    utilization_score = summary["Bed_Utilization_Rate_Pct"].clip(0, 100)
    return pd.concat(
        [alos_score, readmission_score, occupancy_score, utilization_score], axis=1
    ).mean(axis=1).clip(0, 100)


def calculate_summary(frame: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Aggregate all KPIs for an overall, department, or monthly grain."""
    working = frame.copy()
    if not group_columns:
        working["Hospital_Scope"] = "Overall Hospital"
        group_columns = ["Hospital_Scope"]

    grouped = working.groupby(group_columns, dropna=False, observed=True)
    capacity = (
        working.drop_duplicates(group_columns + ["Capacity_Scope_Key"])
        .groupby(group_columns, dropna=False, observed=True)["Total_Beds"]
        .sum()
        .rename("Total_Beds")
        .reset_index()
    )
    summary = grouped.agg(
        Total_Admissions=("Admission_ID", "nunique"),
        Total_Patients=("Patient_ID", "nunique"),
        Patients_Readmitted_Within_30_Days=("Readmitted_Within_30_Days", "sum"),
        Occupied_Beds=("Bed_Scope_Key", "nunique"),
        Average_Length_Of_Stay_Days=("Length_Of_Stay_Days", "mean"),
        Occupied_Bed_Days=("Occupied_Bed_Days", "sum"),
        Period_Start=("Admission_Date", "min"),
        Period_End=("Discharge_Date", "max"),
    ).reset_index().merge(capacity, on=group_columns, how="left", validate="one_to_one")

    summary["Available_Bed_Days"] = (
        (summary["Period_End"] - summary["Period_Start"]).dt.days.add(1).clip(lower=1)
        * summary["Total_Beds"]
    )
    summary["Occupancy_Rate_Pct"] = _safe_percentage(
        summary["Occupied_Beds"], summary["Total_Beds"]
    )
    summary["Readmission_Rate_Pct"] = _safe_percentage(
        summary["Patients_Readmitted_Within_30_Days"], summary["Total_Patients"]
    )
    summary["Bed_Utilization_Rate_Pct"] = _safe_percentage(
        summary["Occupied_Bed_Days"], summary["Available_Bed_Days"]
    )
    summary["Department_Efficiency_Score"] = _efficiency_score(summary)

    percentage_columns = [column for column in summary if column.endswith("_Pct")]
    summary[percentage_columns] = summary[percentage_columns].round(2)
    summary["Average_Length_Of_Stay_Days"] = summary["Average_Length_Of_Stay_Days"].round(2)
    summary["Department_Efficiency_Score"] = summary["Department_Efficiency_Score"].round(2)
    return summary


def add_record_kpis(
    frame: pd.DataFrame,
    overall: pd.DataFrame,
    department: pd.DataFrame,
    monthly: pd.DataFrame,
) -> pd.DataFrame:
    """Attach overall and contextual KPI columns to each patient admission."""
    overall_values = overall.iloc[0]
    for column in (
        "Total_Admissions",
        "Occupancy_Rate_Pct",
        "Average_Length_Of_Stay_Days",
        "Readmission_Rate_Pct",
        "Bed_Utilization_Rate_Pct",
        "Department_Efficiency_Score",
    ):
        target = "Hospital_Efficiency_Score" if column == "Department_Efficiency_Score" else f"Hospital_{column}"
        frame[target] = overall_values[column]

    department_columns = [
        "Department",
        "Total_Admissions",
        "Occupancy_Rate_Pct",
        "Average_Length_Of_Stay_Days",
        "Readmission_Rate_Pct",
        "Bed_Utilization_Rate_Pct",
        "Department_Efficiency_Score",
    ]
    department_names = {
        column: (
            "Department_Efficiency_Score"
            if column == "Department_Efficiency_Score"
            else f"Department_{column}"
        )
        for column in department_columns
        if column != "Department"
    }
    department_map = department[department_columns].rename(columns=department_names)
    frame = frame.merge(department_map, on="Department", how="left", validate="many_to_one")

    monthly_columns = [
        "Admission_Month",
        "Total_Admissions",
        "Occupancy_Rate_Pct",
        "Average_Length_Of_Stay_Days",
        "Readmission_Rate_Pct",
        "Bed_Utilization_Rate_Pct",
    ]
    monthly_map = monthly[monthly_columns].rename(
        columns={column: f"Monthly_{column}" for column in monthly_columns if column != "Admission_Month"}
    )
    return frame.merge(monthly_map, on="Admission_Month", how="left", validate="many_to_one")


def style_workbook(path: Path, table_sheets: Iterable[str]) -> None:
    """Apply filters, frozen headers, formats, and Excel tables without merges."""
    workbook = load_workbook(path)
    for sheet_name in table_sheets:
        sheet = workbook[sheet_name]
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
        header_fill = PatternFill("solid", fgColor="1F4E78")
        for cell in sheet[1]:
            cell.font = Font(color="FFFFFF", bold=True)
            cell.fill = header_fill

        for index, column_cells in enumerate(sheet.iter_cols(), start=1):
            values = [str(cell.value) for cell in list(column_cells)[:200] if cell.value is not None]
            width = min(max([len(value) for value in values] + [10]) + 2, 35)
            sheet.column_dimensions[get_column_letter(index)].width = width

        if sheet.max_row >= 2 and sheet.max_column >= 1:
            table_name = "Tbl" + "".join(character for character in sheet_name if character.isalnum())
            table = Table(displayName=table_name[:250], ref=sheet.dimensions)
            table.tableStyleInfo = TableStyleInfo(
                name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False,
                showRowStripes=True, showColumnStripes=False,
            )
            sheet.add_table(table)
    workbook.save(path)


def export_outputs(
    frame: pd.DataFrame,
    overall: pd.DataFrame,
    department: pd.DataFrame,
    monthly: pd.DataFrame,
) -> None:
    """Write the Tableau dataset and three KPI summary sheets."""
    LOGGER.info("Exporting Tableau-ready dataset: %s", FINAL_DATASET_FILE)
    with pd.ExcelWriter(FINAL_DATASET_FILE, engine="openpyxl", datetime_format="yyyy-mm-dd") as writer:
        frame.to_excel(writer, sheet_name="Patient_KPI_Data", index=False)
    style_workbook(FINAL_DATASET_FILE, ["Patient_KPI_Data"])

    LOGGER.info("Exporting KPI summary workbook: %s", SUMMARY_FILE)
    with pd.ExcelWriter(SUMMARY_FILE, engine="openpyxl", datetime_format="yyyy-mm-dd") as writer:
        overall.to_excel(writer, sheet_name="Overall_Hospital_KPIs", index=False)
        department.to_excel(writer, sheet_name="Department_KPIs", index=False)
        monthly.to_excel(writer, sheet_name="Monthly_KPIs", index=False)
    style_workbook(SUMMARY_FILE, ["Overall_Hospital_KPIs", "Department_KPIs", "Monthly_KPIs"])


def print_completion_message() -> None:
    print("\n==================================")
    print("Hospital KPI Engineering Complete")
    print("==================================")
    print("✓ Total Admissions Calculated")
    print("✓ Occupancy Rate Calculated")
    print("✓ Average Length of Stay Calculated")
    print("✓ Readmission Rate Calculated")
    print("✓ Bed Utilization Rate Calculated")
    print("✓ Department Efficiency Score Calculated")
    print("✓ Tableau Dataset Exported")
    print("✓ Summary Report Generated")


def main() -> int:
    """Run the complete KPI engineering pipeline."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    try:
        frame = read_dataset(INPUT_FILE)
        LOGGER.info("Cleaning and validating patient records")
        frame = clean_dataset(frame)
        frame = add_readmission_fields(frame)
        frame = add_capacity_fields(frame)

        LOGGER.info("Calculating overall, department, and monthly KPIs")
        overall = calculate_summary(frame, [])
        department = calculate_summary(frame, ["Department"])
        monthly = calculate_summary(frame, ["Admission_Month"])
        frame = add_record_kpis(frame, overall, department, monthly)
        export_outputs(frame, overall, department, monthly)
        print_completion_message()
        return 0
    except (FileNotFoundError, ValueError, KeyError, OSError) as exc:
        LOGGER.error("Hospital KPI engineering failed: %s", exc)
        return 1
    except Exception:
        LOGGER.exception("Unexpected failure during KPI engineering")
        return 1


if __name__ == "__main__":
    sys.exit(main())
