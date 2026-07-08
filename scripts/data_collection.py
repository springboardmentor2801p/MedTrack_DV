import os
import pandas as pd
import numpy as np


# Project location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_PATH, exist_ok=True)


# Reading files

admissions = pd.read_csv(os.path.join(RAW_PATH, "admissions.csv"))
patients = pd.read_csv(os.path.join(RAW_PATH, "patient.csv"))
departments = pd.read_csv(os.path.join(RAW_PATH, "department.csv"))
wards = pd.read_csv(os.path.join(RAW_PATH, "ward.csv"))
beds = pd.read_csv(os.path.join(RAW_PATH, "bed.csv"))
diseases = pd.read_csv(os.path.join(RAW_PATH, "disease.csv"))
billing = pd.read_csv(os.path.join(RAW_PATH, "billing.csv"))
patient_insurance = pd.read_csv(
    os.path.join(RAW_PATH, "patient_insurance.csv")
)
insurance_provider = pd.read_csv(
    os.path.join(RAW_PATH, "insurance_provider.csv")
)

print("Dataset loading completed")


# Removing duplicate insurance entries

patient_insurance = (
    patient_insurance
    .sort_values("patient_insurance_id")
    .drop_duplicates("patient_id", keep="last")
)


# Combining tables

df = admissions.merge(
    patients,
    on="patient_id",
    how="left"
)

df = df.merge(
    departments,
    on="department_id",
    how="left"
)

df = df.merge(
    wards,
    on=["ward_id", "department_id"],
    how="left"
)

df = df.merge(
    beds,
    on=["bed_id", "ward_id"],
    how="left"
)

df = df.merge(
    diseases,
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


# Removing duplicate column names

df = df.loc[:, ~df.columns.duplicated()]


# Date conversion

date_cols = [
    "admission_date",
    "discharge_date",
    "date_of_birth",
    "bill_date",
    "policy_start_date",
    "policy_end_date"
]

for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")


# Filling insurance missing values

df["policy_number"] = df["policy_number"].fillna("NO_INSURANCE")
df["provider_name"] = df["provider_name"].fillna("Self Pay")
df["provider_type"] = df["provider_type"].fillna("None")
df["coverage_percentage"] = df["coverage_percentage"].fillna(0)


# Creating useful columns

df["length_of_stay"] = (
    df["discharge_date"] -
    df["admission_date"]
).dt.days

df["length_of_stay"] = df["length_of_stay"].clip(lower=0)


df["patient_age"] = (
    df["admission_date"].dt.year -
    df["date_of_birth"].dt.year
)


def get_age_group(age):
    if age < 18:
        return "Child"
    elif age <= 30:
        return "Young Adult"
    elif age <= 60:
        return "Adult"
    return "Senior"


df["age_group"] = df["patient_age"].apply(get_age_group)


df["insurance_status"] = np.where(
    df["policy_number"] == "NO_INSURANCE",
    "Self Pay",
    "Insured"
)


def get_revenue_category(amount):
    if amount < 10000:
        return "Low"
    elif amount <= 50000:
        return "Medium"
    return "High"


df["revenue_category"] = (
    df["total_amount"]
    .fillna(0)
    .apply(get_revenue_category)
)


df["admission_year"] = df["admission_date"].dt.year
df["admission_month"] = df["admission_date"].dt.month_name()
df["admission_month_number"] = df["admission_date"].dt.month


df["emergency_flag"] = np.where(
    df["admission_type"]
    .str.lower()
    .str.contains("emergency", na=False),
    1,
    0
)


def get_stay_category(days):
    if days <= 3:
        return "Short Stay"
    elif days <= 7:
        return "Medium Stay"
    return "Long Stay"


df["stay_category"] = (
    df["length_of_stay"]
    .apply(get_stay_category)
)


df["department_revenue"] = df["total_amount"].fillna(0)


disease_count = df["disease_name"].value_counts()

df["disease_load"] = (
    df["disease_name"]
    .map(disease_count)
)


df["bed_occupancy_flag"] = 1


# Final checks

print("Duplicate admissions:",
      df["admission_id"].duplicated().sum())

print("Final shape:", df.shape)


# Saving file

output = os.path.join(
    PROCESSED_PATH,
    "hospital_raw_data.csv"
)

df.to_csv(output, index=False)

print("File saved successfully")