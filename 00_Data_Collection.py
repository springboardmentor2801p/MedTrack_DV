
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path.cwd().parent
# Project Root
# Data Folders
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
CLEAN_FOLDER = PROJECT_ROOT / "data" / "cleaned"
FINAL_FOLDER = PROJECT_ROOT / "data" / "final"

print("Project:", PROJECT_ROOT)
print("Raw:", RAW_FOLDER)

datasets = {
    "Patients": "Patients.csv",
    "Department": "Department.csv",
    "Doctor": "Doctor.csv",
    "Nurse": "Nurse.csv",
    "Helpers": "Helpers.csv",
    "Ward": "Ward.csv",
    "Room": "Room.csv",
    "Bed": "Bed.csv",
    "Appointment": "Appointment.csv",
    "MedicalRecord": "MedicalRecord.csv",
    "SurgeryRecord": "SurgeryRecord.csv",
    "RoomRecords": "RoomRecords.csv",
    "BedRecords": "BedRecords.csv",
    "StaffShift": "StaffShift.csv",
    "Equipment": "Equipment.csv",
    "Equipment_Usage": "Equipment_Usage.csv"
}

loaded_data = {}

for name, file in datasets.items():

    df = pd.read_csv(RAW_FOLDER / file)

    loaded_data[name] = df

    print(f" {name:<20} Rows: {df.shape[0]:<6} Columns: {df.shape[1]}")

summary = pd.DataFrame({
    "Dataset": loaded_data.keys(),
    "Rows": [df.shape[0] for df in loaded_data.values()],
    "Columns": [df.shape[1] for df in loaded_data.values()]
})

summary

print("="*60)
print("DATA COLLECTION COMPLETED")
print("="*60)

print(f"Datasets Loaded : {len(loaded_data)}")