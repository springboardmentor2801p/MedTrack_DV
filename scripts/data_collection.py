import os
import pandas as pd
import numpy as np


# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_PATH, exist_ok=True)


# =====================================================
# LOAD CSV FILES
# =====================================================

admissions = pd.read_csv(
    os.path.join(RAW_PATH, "admissions.csv")
)

patient = pd.read_csv(
    os.path.join(RAW_PATH, "patient.csv")
)

department = pd.read_csv(
    os.path.join(RAW_PATH, "department.csv")
)

ward = pd.read_csv(
    os.path.join(RAW_PATH, "ward.csv")
)

bed = pd.read_csv(
    os.path.join(RAW_PATH, "bed.csv")
)

disease = pd.read_csv(
    os.path.join(RAW_PATH, "disease.csv")
)

billing = pd.read_csv(
    os.path.join(RAW_PATH, "billing.csv")
)

patient_insurance = pd.read_csv(
    os.path.join(RAW_PATH, "patient_insurance.csv")
)

insurance_provider = pd.read_csv(
    os.path.join(RAW_PATH, "insurance_provider.csv")
)


print("ALL FILES LOADED")


# =====================================================
# CLEAN INSURANCE DATA
# ONE POLICY PER PATIENT
# =====================================================

patient_insurance = (
    patient_insurance
    .sort_values("patient_insurance_id")
    .drop_duplicates(
        subset=["patient_id"],
        keep="last"
    )
)


# =====================================================
# START WITH ADMISSIONS
# =====================================================

df = admissions.copy()


# =====================================================
# MERGE TABLES
# =====================================================

df = df.merge(
    patient,
    on="patient_id",
    how="left"
)


df = df.merge(
    department,
    on="department_id",
    how="left"
)


df = df.merge(
    ward,
    on=["ward_id", "department_id"],
    how="left"
)


df = df.merge(
    bed,
    on=["bed_id", "ward_id"],
    how="left"
)


df = df.merge(
    disease,
    on="disease_id",
    how="left"
)


df = df.merge(
    billing,
    on="admission_id",
    how="left"
)


df = df.merge(
    patient_insurance,
    on="patient_id",
    how="left"
)


df = df.merge(
    insurance_provider,
    on="insurance_provider_id",
    how="left"
)


# =====================================================
# REMOVE DUPLICATE COLUMNS
# =====================================================

df = df.loc[:, ~df.columns.duplicated()]


# =====================================================
# DATE CONVERSION
# =====================================================

date_columns = [

    "admission_date",
    "discharge_date",
    "date_of_birth",
    "bill_date",
    "policy_start_date",
    "policy_end_date"

]


for col in date_columns:

    if col in df.columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )


# =====================================================
# HANDLE MISSING INSURANCE DATA
# =====================================================

insurance_defaults = {

    "patient_insurance_id": 0,
    "policy_number": "NO_INSURANCE",
    "coverage_percentage": 0,
    "insurance_provider_id": 0,
    "provider_name": "Self Pay",
    "provider_type": "None",
    "contact_details": "N/A",
    "coverage_limit": 0

}


for col, value in insurance_defaults.items():

    if col in df.columns:

        df[col] = df[col].fillna(value)


df["policy_start_date"] = (
    df["policy_start_date"]
    .fillna(pd.Timestamp("1900-01-01"))
)


df["policy_end_date"] = (
    df["policy_end_date"]
    .fillna(pd.Timestamp("1900-01-01"))
)
# =====================================================
# ANALYTICS COLUMNS
# =====================================================


# =====================================================
# 1. LENGTH OF STAY
# =====================================================

df["length_of_stay"] = (

    df["discharge_date"]
    -
    df["admission_date"]

).dt.days


df["length_of_stay"] = (
    df["length_of_stay"]
    .clip(lower=0)
)



# =====================================================
# 2. PATIENT AGE
# =====================================================

df["patient_age"] = (

    df["admission_date"].dt.year
    -
    df["date_of_birth"].dt.year

)



# =====================================================
# 3. AGE GROUP
# =====================================================

def age_group(age):

    if age < 18:
        return "Child"

    elif age <= 30:
        return "Young Adult"

    elif age <= 60:
        return "Adult"

    else:
        return "Senior"


df["age_group"] = (
    df["patient_age"]
    .apply(age_group)
)



# =====================================================
# 4. INSURANCE STATUS
# =====================================================

df["insurance_status"] = np.where(

    df["policy_number"] == "NO_INSURANCE",

    "Self Pay",

    "Insured"

)



# =====================================================
# 5. REVENUE CATEGORY
# =====================================================

def revenue_category(amount):

    if amount < 10000:
        return "Low"

    elif amount <= 50000:
        return "Medium"

    else:
        return "High"



df["revenue_category"] = (

    df["total_amount"]
    .fillna(0)
    .apply(revenue_category)

)



# =====================================================
# 6. ADMISSION YEAR
# =====================================================

df["admission_year"] = (

    df["admission_date"]
    .dt.year

)



# =====================================================
# 7. ADMISSION MONTH
# =====================================================

df["admission_month"] = (

    df["admission_date"]
    .dt.month_name()

)



# =====================================================
# 8. ADMISSION MONTH NUMBER
# (TABLEAU SORTING)
# =====================================================

df["admission_month_number"] = (

    df["admission_date"]
    .dt.month

)



# =====================================================
# 9. YEAR MONTH
# =====================================================

df["admission_year_month"] = (

    df["admission_date"]
    .dt.to_period("M")
    .astype(str)

)



# =====================================================
# 10. ADMISSION QUARTER
# =====================================================

df["admission_quarter"] = (

    "Q"
    +
    df["admission_date"]
    .dt.quarter
    .astype(str)

)



# =====================================================
# 11. EMERGENCY FLAG
# =====================================================

df["emergency_flag"] = np.where(

    df["admission_type"]
    .str.lower()
    .str.contains(
        "emergency",
        na=False
    ),

    1,

    0

)



# =====================================================
# 12. STAY CATEGORY
# =====================================================

def stay_category(days):

    if days <= 3:

        return "Short Stay"

    elif days <= 7:

        return "Medium Stay"

    else:

        return "Long Stay"



df["stay_category"] = (

    df["length_of_stay"]
    .apply(stay_category)

)



# =====================================================
# 13. DEPARTMENT REVENUE
# =====================================================

df["department_revenue"] = (

    df["total_amount"]
    .fillna(0)

)



# =====================================================
# 14. DISEASE LOAD
# =====================================================

disease_count = (

    df["disease_name"]
    .value_counts()

)


df["disease_load"] = (

    df["disease_name"]
    .map(disease_count)

)



df["disease_load_category"] = pd.cut(

    df["disease_load"],

    bins=3,

    labels=[

        "Low Load",
        "Medium Load",
        "High Load"

    ]

)



# =====================================================
# 15. BED OCCUPANCY FLAG
# =====================================================

df["bed_occupancy_flag"] = np.where(

    df["admission_id"].notna(),

    1,

    0

)
# =====================================================
# SORT CHRONOLOGICALLY
# =====================================================
df = (
    df.sort_values(
        by=["admission_date", "bill_date"],
        ascending=[True, True]
    )
    .reset_index(drop=True)
)


# =====================================================
# DUPLICATE CHECK
# =====================================================

print("\nDuplicate Admission IDs:")

duplicate_count = (

    df["admission_id"]
    .duplicated()
    .sum()

)

print(duplicate_count)



# =====================================================
# SAVE FINAL DATASET
# =====================================================

output_file = os.path.join(

    PROCESSED_PATH,

    "hospital_raw_data.csv"

)


df.to_csv(

    output_file,

    index=False

)



# =====================================================
# DATASET REPORT
# =====================================================

total_cells = df.shape[0] * df.shape[1]

missing_cells = df.isnull().sum().sum()


completeness = (

    (total_cells - missing_cells)
    /
    total_cells

) * 100



print("\nSUCCESS")

print("Rows :", len(df))

print("Columns :", len(df.columns))

print("Saved to :", output_file)

print(
    f"Dataset Completeness: {completeness:.2f}%"
)



# =====================================================
# FINAL CHECK
# =====================================================

print("\nFirst 10 Admission IDs:")

print(

    df["admission_id"]
    .head(10)
    .to_list()

)


print("\nLast 10 Admission IDs:")

print(

    df["admission_id"]
    .tail(10)
    .to_list()

)