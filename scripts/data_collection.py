import os
import pandas as pd

# Paths
BASE_DIR = r"D:\MedTrack_DV"
input_file = os.path.join(BASE_DIR, "data", "processed", "hospital_raw_data.csv")
output_dir = os.path.join(BASE_DIR, "data", "cleaned")
output_file = os.path.join(output_dir, "hospital_cleaned.csv")
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(input_file)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Drop columns with excessive missing values
drop_cols = [
    "provider_type",
    "patient_insurance_id",
    "contact_details",
    "policy_start_date",
    "policy_end_date",
    "insurance_provider_id"
]
df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

# Fill remaining missing values
for col in df.select_dtypes(include="object").columns:
    df[col].fillna("Unknown", inplace=True)

for col in df.select_dtypes(include=["int64", "float64"]).columns:
    df[col].fillna(df[col].median(), inplace=True)

# Standardize text columns
for col in ["department_name", "admission_type", "admission_status", "department_type"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Convert dates
for col in ["admission_date", "discharge_date", "date_of_birth"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("Cleaning Completed")
print("Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicates:", df.duplicated().sum())
print("Saved to:", output_file)