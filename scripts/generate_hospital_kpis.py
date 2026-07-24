import pandas as pd

# Load Cleaned Dataset

df = pd.read_csv("data/hospital_cleaned.csv")

print("="*50)
print("HOSPITAL KPI REPORT")
print("="*50)

# KPI 1 - Total Admissions

total_admissions = len(df)

# KPI 2 - Occupancy Rate

occupancy_rate = (
    df["Beds_Occupied"].sum()
    /
    df["Total_Beds_Available"].sum()
) * 100

# KPI 3 - Average Length of Stay

average_los = df["Length_of_Stay"].mean()

# KPI 4 - Readmission Rate

readmission_rate = (
    (df["Readmission_Within_30_Days"]=="Yes").sum()
    /
    len(df)
)*100

# KPI 5 - Bed Utilization

bed_utilization = occupancy_rate

# KPI 6 - Department Efficiency

department_summary = df.groupby("Department").agg(

    Admissions=("Patient_ID","count"),

    Average_Stay=("Length_of_Stay","mean"),

    Occupancy=("Beds_Occupied","sum")

).reset_index()

# Print KPIs

print(f"Total Admissions : {total_admissions}")

print(f"Occupancy Rate : {occupancy_rate:.2f}%")

print(f"Average Length of Stay : {average_los:.2f}")

print(f"Readmission Rate : {readmission_rate:.2f}%")

print(f"Bed Utilization Rate : {bed_utilization:.2f}%")

print("\nDepartment Summary")

print(department_summary)

# Save Excel

with pd.ExcelWriter(
    "output/hospital_final_dataset.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Hospital Data",
        index=False
    )

    department_summary.to_excel(
        writer,
        sheet_name="Department Summary",
        index=False
    )

print("\nhospital_final_dataset.xlsx created successfully.")