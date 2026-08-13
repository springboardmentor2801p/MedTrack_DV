import pandas as pd

df = pd.read_csv("Data/hospital_cleaned.csv")

print("\nBed Status Counts:")
print(df["bed_status"].value_counts())

print("Total Admissions:")
print(df["admission_id"].nunique())

print("\nAverage Length of Stay:")
print(df["length_of_stay"].mean())

occupancy_rate = (
    (df["bed_status"] == "Occupied").mean() * 100
)

print("\nOccupancy Rate:")
print(round(occupancy_rate, 2), "%")

print("\nBed Utilization Rate:")
print(round(occupancy_rate, 2), "%")

admission_counts = (
    df[["patient_id", "admission_id"]]
    .drop_duplicates()
    .groupby("patient_id")
    .size()
)

readmission_rate = (
    (admission_counts > 1).mean() * 100
)

print(
    "\nReadmission Rate:",
    round(readmission_rate, 2),
    "%"
)

dept_kpi = (
    df.groupby("department_name")
    .agg(
        total_admissions=("admission_id", "nunique"),
        avg_length_of_stay=("length_of_stay", "mean"),
        occupied_beds=(
            "bed_status",
            lambda x: (x == "Occupied").mean() * 100
        )
    )
    .reset_index()
)

dept_kpi["department_efficiency_score"] = (
    (dept_kpi["total_admissions"] * 0.4) +
    ((100 - dept_kpi["avg_length_of_stay"]) * 0.3) +
    (dept_kpi["occupied_beds"] * 0.3)
)

print("\nDepartment Efficiency Scores:")
print(
    dept_kpi[
        [
            "department_name",
            "department_efficiency_score"
        ]
    ]
)

dept_kpi.to_csv(
    "Data/department_kpis.csv",
    index=False
)

print("department_kpis.csv created successfully!")