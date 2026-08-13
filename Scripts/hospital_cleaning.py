import pandas as pd

# Load dataset
df = pd.read_csv("Data/hospital_raw_data.csv")

print("Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

# Fill Insurance Missing Values

df["policy_number"] = df["policy_number"].fillna("N/A")
df["provider_name"] = df["provider_name"].fillna("No Insurance")
df["provider_type"] = df["provider_type"].fillna("N/A")

# Fill Diagnostic Missing Values

df["result_status"] = df["result_status"].fillna("Not Tested")
df["specialization"] = df["specialization"].fillna("Unknown")
df["employee_name"] = df["employee_name"].fillna("Unknown Doctor")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Add Hospital Name

df["hospital_name"] = "MedTrack General Hospital"

equipment_mapping = {
    "ICU": 50,
    "Surgery": 40,
    "Emergency": 35,
    "Orthopedics": 25,
    "Internal Medicine": 30,
    "Pediatrics": 20,
    "Neurology": 22,
    "Cardiology": 28,
    "Oncology": 18,
    "Radiology": 15
}

df["equipment_count"] = (
    df["department_name"].map(equipment_mapping)
)

print(df[["department_name", "equipment_count"]].head())

df["admission_date"] = pd.to_datetime(
    df["admission_date"],
    dayfirst=True
)

df["discharge_date"] = pd.to_datetime(
    df["discharge_date"],
    dayfirst=True
)

df["date_of_birth"] = pd.to_datetime(
    df["date_of_birth"],
    dayfirst=True
)

df["length_of_stay"] = (
    df["discharge_date"] -
    df["admission_date"]
).dt.days

df["readmission_flag"] = (
    df.groupby("patient_id")["patient_id"]
    .transform("count") > 1
)

import numpy as np

df["bed_status"] = np.random.choice(
    ["Occupied", "Available", "Maintenance"],
    size=len(df),
    p=[0.7, 0.2, 0.1]
)

df.to_csv(
    "Data/hospital_cleaned.csv",
    index=False
)

print("hospital_cleaned.csv created successfully!")

df.to_excel(
    "Data/hospital_final_dataset.xlsx",
      index=False
)

print("hospital_final_dataset.xlsx created successfully!")