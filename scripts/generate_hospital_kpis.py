import pandas as pd

file_path = r"D:\MedTrack_DV\data\cleaned\hospital_cleaned.csv"
df = pd.read_csv(file_path)

total_admissions = len(df)
df["Total_Admissions"] = total_admissions

df["Average_Length_of_Stay"] = round(df["length_of_stay"].mean(), 2)

readmission_rate = 56.92
df["Readmission_Rate"] = readmission_rate

occupancy_rate = round(df["bed_occupancy_flag"].mean() * 100, 2)
df["Occupancy_Rate"] = occupancy_rate

df["Bed_Utilization_Rate"] = occupancy_rate

dept = (
    df.groupby("department_name")
      .agg(
          Admissions=("admission_id", "count"),
          Avg_LOS=("length_of_stay", "mean")
      )
      .reset_index()
)

dept["Department_Efficiency_Score"] = (
    dept["Admissions"] / dept["Avg_LOS"]
).round(2)

df = df.merge(
    dept[["department_name", "Department_Efficiency_Score"]],
    on="department_name",
    how="left"
)

output_file = r"D:\MedTrack_DV\data\cleaned\hospital_final_dataset.xlsx"
df.to_excel(output_file, index=False)

summary = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Occupancy Rate",
        "Average Length of Stay",
        "Readmission Rate",
        "Bed Utilization Rate",
        "Department Efficiency Score"
    ],
    "Value": [
        total_admissions,
        occupancy_rate,
        round(df["length_of_stay"].mean(), 2),
        readmission_rate,
        occupancy_rate,
        round(dept["Department_Efficiency_Score"].mean(), 2)
    ]
})

summary.to_excel(
    r"D:\MedTrack_DV\data\cleaned\hospital_kpi_summary.xlsx",
    index=False
)

print("hospital_final_dataset.xlsx created successfully!")
print(summary)