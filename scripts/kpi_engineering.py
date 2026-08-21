import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/hospital_cleaned.csv")

print("=" * 50)
print("        MEDTRACK_DV KPI REPORT")
print("=" * 50)

# KPIs
total_patients = df["Patient_ID"].nunique()
total_hospitals = df["Hospital_Name"].nunique()
total_departments = df["Department_Name"].nunique()
total_doctors = df["Doctor_ID"].nunique()
total_beds = df["Total_Beds"].sum()
available_beds = df["Available_Beds"].sum()
occupied_beds = df["Occupied_Beds"].sum()
icu_beds = df["ICU_Beds"].sum()
emergency_beds = df["Emergency_Beds"].sum()
total_nurses = df["Total_Nurses"].sum()
ambulances = df["Ambulances"].sum()
ventilators = df["Ventilators"].sum()
average_bill = df["Bill_Amount"].mean()
average_stay = df["Length_of_Stay"].mean()

# Bed Occupancy %
bed_occupancy = (occupied_beds / total_beds) * 100

print(f"Total Patients        : {total_patients}")
print(f"Total Hospitals       : {total_hospitals}")
print(f"Total Departments     : {total_departments}")
print(f"Total Doctors         : {total_doctors}")
print(f"Total Nurses          : {total_nurses}")
print(f"Total Beds            : {total_beds}")
print(f"Available Beds        : {available_beds}")
print(f"Occupied Beds         : {occupied_beds}")
print(f"ICU Beds              : {icu_beds}")
print(f"Emergency Beds        : {emergency_beds}")
print(f"Ventilators           : {ventilators}")
print(f"Ambulances            : {ambulances}")
print(f"Average Bill Amount   : ₹{average_bill:.2f}")
print(f"Average Stay (Days)   : {average_stay:.2f}")
print(f"Bed Occupancy Rate    : {bed_occupancy:.2f}%")

print("=" * 50)