# ============================================================
# MedTrack DV - Hospital KPI Generator
# ============================================================
# Project : MedTrack DV
# Purpose : Generate the 19 Hospital Operations KPIs
# Output  : hospital_kpi_report.csv
# ============================================================


import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATH
# ============================================================

# This file is located at:
#
# MedTrack_DV/
#     scripts/
#         generate hospital kpis/
#             generate_hospital_kpis.py
#
# Therefore parents[1] points to the scripts folder.

SCRIPTS_DIR = Path(__file__).resolve().parents[1]

OUTPUT_DIR = SCRIPTS_DIR / "outputs"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = OUTPUT_DIR / "hospital_kpi_report.csv"


# ============================================================
# 2. FIND DATASET
# ============================================================

# Search for the cleaned dataset first.

cleaned_files = list(
    SCRIPTS_DIR.rglob("hospital_cleaned.csv")
)


# Search for raw dataset if cleaned dataset is not available.

raw_files = list(
    SCRIPTS_DIR.rglob("hospital_raw_data.csv")
)


if cleaned_files:

    INPUT_FILE = cleaned_files[0]

    print("Cleaned dataset found.")

elif raw_files:

    INPUT_FILE = raw_files[0]

    print("Cleaned dataset not found.")
    print("Using raw dataset instead.")

else:

    print("=" * 70)
    print("ERROR: Dataset not found.")
    print("=" * 70)

    print("\nThe program searched inside:")
    print(SCRIPTS_DIR)

    print("\nExpected one of these files:")
    print("- hospital_cleaned.csv")
    print("- hospital_raw_data.csv")

    raise FileNotFoundError(
        "No hospital dataset was found inside the scripts folder."
    )


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\n" + "=" * 70)
print("MedTrack DV - Hospital KPI Generator")
print("=" * 70)

print("\nDataset:")
print(INPUT_FILE)

df = pd.read_csv(
    INPUT_FILE
)

print("\nDataset loaded successfully.")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ============================================================
# 4. STANDARDIZE COLUMN NAMES
# ============================================================

# Example:
#
# Billing Amount -> billing_amount
# Date of Admission -> date_of_admission
# Length of stay -> length_of_stay

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)


# ============================================================
# 5. DISPLAY COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("AVAILABLE COLUMNS")
print("=" * 70)

for number, column in enumerate(
    df.columns,
    start=1
):

    print(
        f"{number:02d}. {column}"
    )


# ============================================================
# 6. REQUIRED COLUMNS
# ============================================================

# These are the columns required from your actual dataset.
#
# admission_month and admission_year are NOT required here
# because they can be generated automatically from
# date_of_admission.

required_columns = [

    "name",

    "age",

    "gender",

    "blood_type",

    "medical_condition",

    "date_of_admission",

    "doctor",

    "hospital",

    "insurance_provider",

    "billing_amount",

    "room_number",

    "admission_type",

    "discharge_date",

    "medication",

    "test_results",

    "patient_id",

    "department",

    "length_of_stay",

    "readmission_flag",

    "severity",

    "ward",

    "bed_id",

    "room_type",

    "nurse_id",

    "staff_shift",

    "equipment_used",

    "equipment_status",

    "payment_status",

    "payment_method",

    "emergency_case",

    "icu_admission",

    "discharge_status",

    "hospital_region",

    "occupancy_status",

    "bed_capacity"

]


# ============================================================
# 7. CHECK REQUIRED COLUMNS
# ============================================================

missing_columns = [

    column

    for column in required_columns

    if column not in df.columns

]


if missing_columns:

    print("\n" + "=" * 70)
    print("ERROR: REQUIRED COLUMNS ARE MISSING")
    print("=" * 70)

    for column in missing_columns:

        print(
            f"- {column}"
        )

    print(
        "\nPlease check your dataset columns."
    )

    raise ValueError(
        "Required columns are missing from the dataset."
    )


print("\nRequired columns verified successfully.")


# ============================================================
# 8. DATE PROCESSING
# ============================================================

# Convert Date of Admission into datetime.

df["date_of_admission"] = pd.to_datetime(

    df["date_of_admission"],

    errors="coerce"

)


# Create Admission Month if it does not exist.

if "admission_month" not in df.columns:

    df["admission_month"] = (
        df["date_of_admission"]
        .dt.month_name()
    )


# Create Admission Year if it does not exist.

if "admission_year" not in df.columns:

    df["admission_year"] = (
        df["date_of_admission"]
        .dt.year
    )


print("\nDate fields processed successfully.")

print(
    "Admission Month and Admission Year are available."
)


# ============================================================
# 9. NUMERIC DATA CLEANING
# ============================================================

df["billing_amount"] = pd.to_numeric(

    df["billing_amount"],

    errors="coerce"

)


df["length_of_stay"] = pd.to_numeric(

    df["length_of_stay"],

    errors="coerce"

)


df["bed_capacity"] = pd.to_numeric(

    df["bed_capacity"],

    errors="coerce"

)


# ============================================================
# 10. TEXT DATA CLEANING
# ============================================================

text_columns = [

    "readmission_flag",

    "severity",

    "emergency_case",

    "icu_admission",

    "discharge_status",

    "occupancy_status"

]


for column in text_columns:

    df[column] = (

        df[column]
        .astype(str)
        .str.strip()
        .str.lower()

    )


# ============================================================
# 11. BASIC COUNTS
# ============================================================

# Total patients / admissions

total_patients = len(df)


# Total billing

total_billing = (
    df["billing_amount"]
    .sum()
)


# Occupied beds

occupied_beds = (

    df["occupancy_status"]
    .eq("occupied")
    .sum()

)


# Vacant / available beds

available_beds = (

    df["occupancy_status"]
    .eq("vacant")
    .sum()

)


# Total beds

total_beds = (

    occupied_beds
    +
    available_beds

)


# Average length of stay

average_length_of_stay = (

    df["length_of_stay"]
    .mean()

)


# Readmitted patients

readmitted_patients = (

    df["readmission_flag"]
    .isin(
        [
            "yes",
            "1",
            "true"
        ]
    )
    .sum()

)


# Severe cases

severe_cases = (

    df["severity"]
    .eq("severe")
    .sum()

)


# ICU admissions

icu_admissions = (

    df["icu_admission"]
    .isin(
        [
            "yes",
            "1",
            "true"
        ]
    )
    .sum()

)


# Emergency cases

emergency_cases = (

    df["emergency_case"]
    .isin(
        [
            "yes",
            "1",
            "true"
        ]
    )
    .sum()

)


# Recovered patients

recovered_patients = (

    df["discharge_status"]
    .eq("recovered")
    .sum()

)


# Total departments

total_departments = (

    df["department"]
    .nunique()

)


# Total nurses

total_nurses = (

    df["nurse_id"]
    .nunique()

)


# Total doctors

total_doctors = (

    df["doctor"]
    .nunique()

)


# Total wards

total_wards = (

    df["ward"]
    .nunique()

)


# ============================================================
# 12. CALCULATE THE 19 KPIs
# ============================================================


# ------------------------------------------------------------
# KPI 01 - Total Patients
# ------------------------------------------------------------

kpi_01 = total_patients


# ------------------------------------------------------------
# KPI 02 - Total Billing
# ------------------------------------------------------------

kpi_02 = total_billing


# ------------------------------------------------------------
# KPI 03 - Bed Occupancy Rate
# ------------------------------------------------------------

if total_beds > 0:

    kpi_03 = (

        occupied_beds
        /
        total_beds
        *
        100

    )

else:

    kpi_03 = 0


# ------------------------------------------------------------
# KPI 04 - Average Length of Stay
# ------------------------------------------------------------

kpi_04 = average_length_of_stay


# ------------------------------------------------------------
# KPI 05 - Readmission Rate
# ------------------------------------------------------------

if total_patients > 0:

    kpi_05 = (

        readmitted_patients
        /
        total_patients
        *
        100

    )

else:

    kpi_05 = 0


# ------------------------------------------------------------
# KPI 06 - Discharge Rate
# ------------------------------------------------------------

if total_patients > 0:

    kpi_06 = (

        recovered_patients
        /
        total_patients
        *
        100

    )

else:

    kpi_06 = 0


# ------------------------------------------------------------
# KPI 07 - Total Admissions
# ------------------------------------------------------------

kpi_07 = total_patients


# ------------------------------------------------------------
# KPI 08 - Occupied Beds
# ------------------------------------------------------------

kpi_08 = occupied_beds


# ------------------------------------------------------------
# KPI 09 - Severe Cases %
# ------------------------------------------------------------

if total_patients > 0:

    kpi_09 = (

        severe_cases
        /
        total_patients
        *
        100

    )

else:

    kpi_09 = 0


# ------------------------------------------------------------
# KPI 10 - ICU Admissions
# ------------------------------------------------------------

kpi_10 = icu_admissions


# ------------------------------------------------------------
# KPI 11 - Emergency Cases
# ------------------------------------------------------------

kpi_11 = emergency_cases


# ------------------------------------------------------------
# KPI 12 - Average Billing per Patient
# ------------------------------------------------------------

if total_patients > 0:

    kpi_12 = (

        total_billing
        /
        total_patients

    )

else:

    kpi_12 = 0


# ------------------------------------------------------------
# KPI 13 - Total Departments
# ------------------------------------------------------------

kpi_13 = total_departments


# ------------------------------------------------------------
# KPI 14 - Average Patients per Department
# ------------------------------------------------------------

if total_departments > 0:

    kpi_14 = (

        total_patients
        /
        total_departments

    )

else:

    kpi_14 = 0


# ------------------------------------------------------------
# KPI 15 - Average Billing per Department
# ------------------------------------------------------------

if total_departments > 0:

    kpi_15 = (

        total_billing
        /
        total_departments

    )

else:

    kpi_15 = 0


# ------------------------------------------------------------
# KPI 16 - Total Nurses
# ------------------------------------------------------------

kpi_16 = total_nurses


# ------------------------------------------------------------
# KPI 17 - Available Beds
# ------------------------------------------------------------

kpi_17 = available_beds


# ------------------------------------------------------------
# KPI 18 - Average Patients per Doctor
# ------------------------------------------------------------

if total_doctors > 0:

    kpi_18 = (

        total_patients
        /
        total_doctors

    )

else:

    kpi_18 = 0


# ------------------------------------------------------------
# KPI 19 - Total Wards
# ------------------------------------------------------------

kpi_19 = total_wards


# ============================================================
# 13. CREATE KPI REPORT
# ============================================================

kpi_report = pd.DataFrame(

    {

        "KPI_ID": [

            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19

        ],


        "KPI_Name": [

            "Total Patients",

            "Total Billing",

            "Bed Occupancy Rate",

            "Average Length of Stay",

            "Readmission Rate",

            "Discharge Rate",

            "Total Admissions",

            "Occupied Beds",

            "Severe Cases %",

            "ICU Admissions",

            "Emergency Cases",

            "Average Billing per Patient",

            "Total Departments",

            "Average Patients per Department",

            "Average Billing per Department",

            "Total Nurses",

            "Available Beds",

            "Average Patients per Doctor",

            "Total Wards"

        ],


        "Value": [

            kpi_01,

            kpi_02,

            kpi_03,

            kpi_04,

            kpi_05,

            kpi_06,

            kpi_07,

            kpi_08,

            kpi_09,

            kpi_10,

            kpi_11,

            kpi_12,

            kpi_13,

            kpi_14,

            kpi_15,

            kpi_16,

            kpi_17,

            kpi_18,

            kpi_19

        ],


        "Unit": [

            "Patients",

            "Currency",

            "%",

            "Days",

            "%",

            "%",

            "Admissions",

            "Beds",

            "%",

            "Admissions",

            "Cases",

            "Currency",

            "Departments",

            "Patients",

            "Currency",

            "Nurses",

            "Beds",

            "Patients per Doctor",

            "Wards"

        ]

    }

)


# ============================================================
# 14. ROUND KPI VALUES
# ============================================================

kpi_report["Value"] = (

    kpi_report["Value"]
    .round(2)

)


# ============================================================
# 15. SAVE KPI REPORT
# ============================================================

kpi_report.to_csv(

    OUTPUT_FILE,

    index=False

)


# ============================================================
# 16. DISPLAY FINAL RESULTS
# ============================================================

print("\n")

print("=" * 70)

print("19 KPIs GENERATED SUCCESSFULLY")

print("=" * 70)


print("\n")

print(

    kpi_report.to_string(
        index=False
    )

)


# ============================================================
# 17. DISPLAY OUTPUT LOCATION
# ============================================================

print("\n")

print("=" * 70)

print("OUTPUT FILE")

print("=" * 70)

print(

    OUTPUT_FILE

)


print("\n")

print("=" * 70)

print("PROCESS COMPLETED SUCCESSFULLY")

print("=" * 70)