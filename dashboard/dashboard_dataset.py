import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/hospital_cleaned.csv")

# Dashboard Dataset
dashboard_df = pd.DataFrame()

# IDs
dashboard_df["Patient_ID"] = df["Patient_ID"]
dashboard_df["Doctor_ID"] = df["Doctor_ID"]
dashboard_df["Hospital_ID"] = df["Hospital_ID"]
dashboard_df["Department_ID"] = df["Department_ID"]

# Hospital Information
dashboard_df["Hospital"] = df["Hospital_Name"]
dashboard_df["Department"] = df["Department_Name"]
dashboard_df["City"] = df["City"]
dashboard_df["State"] = df["State"]

# Patient Information
dashboard_df["Gender"] = df["Gender"]
dashboard_df["Age"] = df["Age"]
dashboard_df["Diagnosis"] = df["Diagnosis"]
dashboard_df["Treatment"] = df["Treatment"]

# Dates
dashboard_df["Admission_Date"] = df["Admission_Date"]
dashboard_df["Discharge_Date"] = df["Discharge_Date"]

# Billing
dashboard_df["Bill_Amount"] = df["Bill_Amount"]
dashboard_df["Insurance_Status"] = df["Insurance_Status"]
dashboard_df["Length_of_Stay"] = df["Length_of_Stay"]

# Resources
dashboard_df["Total_Beds"] = df["Total_Beds"]
dashboard_df["Available_Beds"] = df["Available_Beds"]
dashboard_df["Occupied_Beds"] = df["Occupied_Beds"]
dashboard_df["ICU_Beds"] = df["ICU_Beds"]
dashboard_df["Emergency_Beds"] = df["Emergency_Beds"]
dashboard_df["Doctors"] = df["Total_Doctors"]
dashboard_df["Nurses"] = df["Total_Nurses"]
dashboard_df["Ventilators"] = df["Ventilators"]
dashboard_df["Ambulances"] = df["Ambulances"]
import numpy as np

dashboard_df["Readmission"] = np.random.choice(
    ["Yes", "No"],
    size=len(df),
    p=[0.08, 0.92]
)
# Save
dashboard_df.to_csv(
    "dashboard/dashboard_data.csv",
    index=False
)

print("=" * 60)
print("Dashboard Dataset Created Successfully")
print("=" * 60)
print(dashboard_df.head())
print("\nColumns:")
print(dashboard_df.columns)