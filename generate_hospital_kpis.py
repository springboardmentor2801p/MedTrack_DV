import pandas as pd

df = pd.read_excel("hospital_final_dataset.xlsx")

print("\n===== HOSPITAL KPI REPORT =====\n")

# KPI 1 - Total Admissions
total_admissions = len(df)

# KPI 2 - Average Length of Stay
avg_los = round(df["Length_of_stay"].mean(), 2)

# KPI 3 - Readmission Rate
readmitted = (df["Readmission_Flag"] == "Yes").sum()
readmission_rate = round((readmitted / len(df)) * 100, 2)

# KPI 4 - Occupancy Rate
occupied = (df["Occupancy_Status"] == "Occupied").sum()
occupancy_rate = round((occupied / len(df)) * 100, 2)

# KPI 5 - Bed Utilization Rate
beds_used = df["Bed_ID"].nunique()
total_beds = df["Bed_Capacity"].sum()

bed_utilization_rate = round((beds_used / total_beds) * 100, 2)

# KPI 6 - Department Efficiency
dept_efficiency = (
    df.groupby("Department")["Length_of_stay"]
    .mean()
    .sort_values()
)

print("Total Admissions:", total_admissions)
print("Average Length of Stay:", avg_los, "Days")
print("Readmission Rate:", readmission_rate, "%")
print("Occupancy Rate:", occupancy_rate, "%")
print("Bed Utilization Rate:", bed_utilization_rate, "%")

print("\n===== Department Efficiency =====\n")
print(dept_efficiency)

print("\nKPI Engineering Completed Successfully")
kpi_report = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Average Length of Stay",
        "Readmission Rate",
        "Occupancy Rate",
        "Bed Utilization Rate"
    ],
    "Value": [
        total_admissions,
        avg_los,
        readmission_rate,
        occupancy_rate,
        bed_utilization_rate
    ]
})

kpi_report.to_csv("hospital_kpi_report.csv", index=False)

print("KPI Report Saved Successfully")