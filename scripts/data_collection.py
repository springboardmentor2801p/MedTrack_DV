import os
import pandas as pd
import numpy as np


# Project paths

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(OUTPUT_PATH, exist_ok=True)


# Load datasets

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


print("All datasets loaded successfully")


# Remove duplicate insurance records

patient_insurance = (
    patient_insurance
    .sort_values("patient_insurance_id")
    .drop_duplicates(
        subset="patient_id",
        keep="last"
    )
)


# Merge datasets

df = admissions.copy()


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


if "insurance_provider_id" in df.columns:

    df = df.merge(
        insurance_provider,
        on="insurance_provider_id",
        how="left"
    )


# Remove duplicate column names

df = df.loc[:, ~df.columns.duplicated()]


# Convert dates

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


# Insurance handling

insurance_defaults = {

    "policy_number": "NO_INSURANCE",
    "provider_name": "Self Pay",
    "provider_type": "None",
    "contact_details": "N/A",
    "coverage_percentage": 0,
    "coverage_limit": 0

}


for col, value in insurance_defaults.items():

    if col in df.columns:

        df[col] = df[col].fillna(value)



# Length of stay

if (
    "admission_date" in df.columns
    and "discharge_date" in df.columns
):

    df["length_of_stay"] = (

        df["discharge_date"]
        -
        df["admission_date"]

    ).dt.days


    df["length_of_stay"] = (
        df["length_of_stay"]
        .clip(lower=0)
    )



# Patient age

if (
    "date_of_birth" in df.columns
    and "admission_date" in df.columns
):

    df["patient_age"] = (

        df["admission_date"].dt.year
        -
        df["date_of_birth"].dt.year

    )



def age_group(age):

    if age < 18:
        return "Child"

    elif age <= 30:
        return "Young Adult"

    elif age <= 60:
        return "Adult"

    else:
        return "Senior"



if "patient_age" in df.columns:

    df["age_group"] = (
        df["patient_age"]
        .apply(age_group)
    )



# Insurance status

if "policy_number" in df.columns:

    df["insurance_status"] = np.where(

        df["policy_number"] == "NO_INSURANCE",

        "Self Pay",

        "Insured"

    )



# Revenue category

def revenue_category(amount):

    if amount < 10000:
        return "Low"

    elif amount <= 50000:
        return "Medium"

    else:
        return "High"



if "total_amount" in df.columns:

    df["revenue_category"] = (

        df["total_amount"]
        .fillna(0)
        .apply(revenue_category)

    )



# Time features

if "admission_date" in df.columns:

    df["admission_year"] = (
        df["admission_date"].dt.year
    )

    df["admission_month"] = (
        df["admission_date"].dt.month_name()
    )

    df["admission_month_number"] = (
        df["admission_date"].dt.month
    )

    df["admission_year_month"] = (
        df["admission_date"]
        .dt.to_period("M")
        .astype(str)
    )

    df["admission_quarter"] = (

        "Q"
        +
        df["admission_date"]
        .dt.quarter
        .astype(str)

    )



# Emergency flag

if "admission_type" in df.columns:

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



# Stay category

def stay_category(days):

    if days <= 3:
        return "Short Stay"

    elif days <= 7:
        return "Medium Stay"

    else:
        return "Long Stay"



if "length_of_stay" in df.columns:

    df["stay_category"] = (

        df["length_of_stay"]
        .apply(stay_category)

    )



# Department revenue

if "total_amount" in df.columns:

    df["department_revenue"] = (
        df["total_amount"]
        .fillna(0)
    )



# Disease load

if "disease_name" in df.columns:

    disease_count = (
        df["disease_name"]
        .value_counts()
    )

    df["disease_load"] = (
        df["disease_name"]
        .map(disease_count)
    )



# Bed occupancy

df["bed_occupancy_flag"] = np.where(

    df["admission_id"].notna(),

    1,

    0

)



# Sort data

if "admission_date" in df.columns:

    df = (
        df.sort_values(
            "admission_date"
        )
        .reset_index(drop=True)
    )



# Validation

print("\nDuplicate Admission IDs:")

print(
    df["admission_id"]
    .duplicated()
    .sum()
)


print("\nRows:", df.shape[0])

print("Columns:", df.shape[1])



# Save output

output_file = os.path.join(

    OUTPUT_PATH,

    "hospital_raw_data.csv"

)


df.to_csv(

    output_file,

    index=False

)


print("\nSUCCESS")

print("Saved:", output_file)