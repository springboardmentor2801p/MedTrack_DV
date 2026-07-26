import pandas as pd

print("Loading datasets...")

# Load datasets
patients = pd.read_csv("data/patient_admissions.csv")
hospitals = pd.read_csv("data/hospital_data.csv")
departments = pd.read_csv("data/department_data.csv")
resources = pd.read_csv("data/resource_data.csv")

print("Datasets Loaded Successfully!")

# Merge Patient + Hospital
hospital_raw = pd.merge(
    patients,
    hospitals,
    on="Hospital_ID",
    how="left"
)

# Merge Resource
hospital_raw = pd.merge(
    hospital_raw,
    resources,
    on="Hospital_ID",
    how="left"
)

# Merge Department
hospital_raw = pd.merge(
    hospital_raw,
    departments,
    on="Department_ID",
    how="left"
)

# Save Integrated Dataset
hospital_raw.to_csv(
    "data/hospital_raw_data.csv",
    index=False
)

print("Integrated Dataset Created Successfully!")
print("Rows :", hospital_raw.shape[0])
print("Columns :", hospital_raw.shape[1])

print(hospital_raw.head())