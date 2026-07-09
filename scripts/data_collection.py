import pandas as pd
import os

# Data folder path
data_path = "data"

# Load datasets
operations = pd.read_csv(os.path.join(data_path, "hospital_operations_dataset.csv"))
admissions = pd.read_csv(os.path.join(data_path, "HDHI Admission data.csv"))
patients = pd.read_csv(os.path.join(data_path, "patients.csv"))
staff = pd.read_csv(os.path.join(data_path, "staff.csv"))
staff_schedule = pd.read_csv(os.path.join(data_path, "staff_schedule.csv"))

# Display basic information
datasets = {
    "Hospital Operations": operations,
    "Admissions": admissions,
    "Patients": patients,
    "Staff": staff,
    "Staff Schedule": staff_schedule
}

for name, df in datasets.items():
    print(f"\n{name}")
    print("-" * 40)
    print("Shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())

# Save primary dataset as hospital_raw_data.csv
operations.to_csv(os.path.join(data_path, "hospital_raw_data.csv"), index=False)

print("\n✅ hospital_raw_data.csv created successfully!")