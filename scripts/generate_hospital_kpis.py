# ============================================
# Module 3 : Hospital KPI Engineering
# Project : MedTrack_DV
# Author : Mandadi Niharika Reddy
# ============================================
import pandas as pd
import numpy as np
hospital_df = pd.read_csv(r"C:\Users\manda\Healthcare_analytics_project\data\hospital_cleaned.csv")

department_df = pd.read_csv(r"C:\Users\manda\Healthcare_analytics_project\data\department_data.csv")

resource_df = pd.read_csv(r"C:\Users\manda\Healthcare_analytics_project\data\resource_data.csv")
print("="*60)
print("MODULE 3 : HOSPITAL KPI ENGINEERING")
print("="*60)

print("\nHospital Dataset")
print(hospital_df.shape)

print("\nDepartment Dataset")
print(department_df.shape)

print("\nResource Dataset")
print(resource_df.shape)
print("\nAPR Severity Values")
print(hospital_df["APR Severity of Illness Description"].value_counts())

print("\nAPR Mortality Risk Values")
print(hospital_df["APR Risk of Mortality"].value_counts())

print("\nEmergency Department Indicator")
print(hospital_df["Emergency Department Indicator"].value_counts())
# ============================================
# Feature 1 : Stay Category
# ============================================

def stay_category(days):
    if days <= 3:
        return "Short Stay"
    elif days <= 7:
        return "Medium Stay"
    else:
        return "Long Stay"

hospital_df["Stay_Category"] = hospital_df["Length of Stay"].apply(stay_category)

print("\nStay Category Distribution")
print(hospital_df["Stay_Category"].value_counts())
# ============================================
# Feature 2 : Cost Per Day
# ============================================

hospital_df["Cost_Per_Day"] = (
    hospital_df["Total Costs"] /
    hospital_df["Length of Stay"].replace(0, 1)
).round(2)

print("\nCost Per Day")
print(hospital_df["Cost_Per_Day"].head())
# ============================================
# Feature 3 : Charge Per Day
# ============================================

hospital_df["Charge_Per_Day"] = (
    hospital_df["Total Charges"] /
    hospital_df["Length of Stay"].replace(0, 1)
).round(2)

print("\nCharge Per Day")
print(hospital_df["Charge_Per_Day"].head())
# ============================================
# Feature 4 : Emergency Flag
# ============================================

hospital_df["Emergency_Flag"] = (
    hospital_df["Emergency Department Indicator"]
    .map({"Y": 1, "N": 0})
)

print("\nEmergency Flag Distribution")
print(hospital_df["Emergency_Flag"].value_counts())
# ============================================
# Feature 5 : Severity Score
# ============================================

severity_map = {
    "Minor": 1,
    "Moderate": 2,
    "Major": 3,
    "Extreme": 4,
    "Unknown": 0
}

hospital_df["Severity_Score"] = (
    hospital_df["APR Severity of Illness Description"]
    .map(severity_map)
)

print("\nSeverity Score Distribution")
print(hospital_df["Severity_Score"].value_counts())
# ============================================
# Feature 6 : Mortality Risk Score
# ============================================

mortality_map = {
    "Minor": 1,
    "Moderate": 2,
    "Major": 3,
    "Extreme": 4,
    "Unknown": 0
}

hospital_df["Mortality_Risk_Score"] = (
    hospital_df["APR Risk of Mortality"]
    .map(mortality_map)
)

print("\nMortality Risk Score Distribution")
print(hospital_df["Mortality_Risk_Score"].value_counts())
# ============================================
# Feature 7 : Readmission Risk Flag
# ============================================

high_risk = [
    "Left Against Medical Advice",
    "Skilled Nursing Home",
    "Short-term Hospital",
    "Inpatient Rehabilitation Facility",
    "Psychiatric Hospital or Unit of Hosp"
]

hospital_df["Readmission_Risk_Flag"] = (
    hospital_df["Patient Disposition"]
    .isin(high_risk)
    .astype(int)
)

print("\nReadmission Risk Flag Distribution")
print(hospital_df["Readmission_Risk_Flag"].value_counts())
print("\n" + "=" * 60)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 60)

print("\nCurrent Dataset Shape :", hospital_df.shape)

print("\nNew Feature Columns Added:")
print([
    "Stay_Category",
    "Cost_Per_Day",
    "Charge_Per_Day",
    "Emergency_Flag",
    "Severity_Score",
    "Mortality_Risk_Score",
    "Readmission_Risk_Flag"
])
# ============================================
# KPI 1 : Total Admissions
# ============================================

total_admissions = len(hospital_df)

print("\n" + "=" * 60)
print("KPI 1 : TOTAL ADMISSIONS")
print("=" * 60)
print(f"Total Admissions : {total_admissions}")
# ============================================
# KPI 2 : Average Length of Stay
# ============================================

avg_length_of_stay = hospital_df["Length of Stay"].mean()

print("\n" + "=" * 60)
print("KPI 2 : AVERAGE LENGTH OF STAY")
print("=" * 60)
print(f"Average Length of Stay : {avg_length_of_stay:.2f} Days")
# ============================================
# KPI 3 : Occupancy Rate
# ============================================

total_beds = department_df["Total_Beds"].sum()

total_patient_days = hospital_df["Length of Stay"].sum()

available_bed_days = total_beds * 365

occupancy_rate = (
    total_patient_days /
    available_bed_days
) * 100

print("\n" + "=" * 60)
print("KPI 3 : OCCUPANCY RATE")
print("=" * 60)

print(f"Total Beds          : {total_beds}")
print(f"Patient Days        : {total_patient_days}")
print(f"Available Bed Days  : {available_bed_days}")
print(f"Occupancy Rate      : {occupancy_rate:.2f}%")
# ============================================
# KPI 4 : Bed Utilization Rate
# ============================================

bed_utilization_rate = resource_df["Utilization_Rate"].mean()

print("\n" + "=" * 60)
print("KPI 4 : BED UTILIZATION RATE")
print("=" * 60)
print(f"Bed Utilization Rate : {bed_utilization_rate:.2f}%")
# ============================================
# KPI 5 : Department Efficiency Score
# ============================================

avg_resource_utilization = resource_df["Utilization_Rate"].mean() / 100

department_df["Department_Efficiency_Score"] = (
    department_df["Total_Patients"] /
    (
        department_df["Total_Doctors"] +
        department_df["Total_Nurses"]
    )
) * avg_resource_utilization

department_efficiency_score = department_df[
    "Department_Efficiency_Score"
].mean()

print("\n" + "=" * 60)
print("KPI 5 : DEPARTMENT EFFICIENCY SCORE")
print("=" * 60)

print(f"Average Resource Utilization : {avg_resource_utilization*100:.2f}%")
print(f"Department Efficiency Score  : {department_efficiency_score:.2f}")

print("\nDepartment-wise Efficiency")
print(
    department_df[
        ["Department_Name", "Department_Efficiency_Score"]
    ].round(2)
)
# ============================================
# KPI 6 : Estimated Readmission Rate
# ============================================

estimated_readmission_rate = (
    hospital_df["Readmission_Risk_Flag"].mean() * 100
)

print("\n" + "=" * 60)
print("KPI 6 : ESTIMATED READMISSION RATE")
print("=" * 60)

print(f"Estimated Readmission Rate : {estimated_readmission_rate:.2f}%")
# ============================================
# KPI SUMMARY
# ============================================

kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Average Length of Stay",
        "Occupancy Rate (%)",
        "Bed Utilization Rate (%)",
        "Department Efficiency Score",
        "Estimated Readmission Rate (%)"
    ],
    "Value": [
        total_admissions,
        round(avg_length_of_stay, 2),
        round(occupancy_rate, 2),
        round(bed_utilization_rate, 2),
        round(department_efficiency_score, 2),
        round(estimated_readmission_rate, 2)
    ]
})

print("\n" + "=" * 60)
print("KPI SUMMARY")
print("=" * 60)
print(kpi_summary)
# ============================================
# Add Department Efficiency to Final Dataset
# ============================================

department_lookup = department_df.set_index(
    "Based_On"
)["Department_Efficiency_Score"]

hospital_df["Department_Efficiency_Score"] = (
    hospital_df["APR MDC Description"]
    .map(department_lookup)
)

hospital_df["Department_Efficiency_Score"] = (
    hospital_df["Department_Efficiency_Score"]
    .fillna(round(department_efficiency_score, 2))
)
# ============================================
# VERIFY DEPARTMENT EFFICIENCY MAPPING
# ============================================

print("\n" + "=" * 60)
print("VERIFY DEPARTMENT EFFICIENCY MAPPING")
print("=" * 60)

print(
    hospital_df[
        [
            "APR MDC Description",
            "Department_Efficiency_Score"
        ]
    ].head(15)
)
# ============================================
# FINAL DATASET INFORMATION
# ============================================

print("\n" + "=" * 60)
print("FINAL DATASET INFORMATION")
print("=" * 60)

print(f"Dataset Shape : {hospital_df.shape}")

print("\nNew Feature Columns:")

print(
    hospital_df[
        [
            "Stay_Category",
            "Cost_Per_Day",
            "Charge_Per_Day",
            "Emergency_Flag",
            "Severity_Score",
            "Mortality_Risk_Score",
            "Readmission_Risk_Flag",
            "Department_Efficiency_Score"
        ]
    ].head()
)

print("\nTotal Columns :", hospital_df.shape[1])
# ======================================================
# ADD SUPPORTING KPI COLUMNS TO HOSPITAL DATASET
# ======================================================

# Total Beds in Hospital
total_beds = department_df["Total_Beds"].sum()

# Available Bed Days
available_bed_days = total_beds * 365

# Bed Utilization Rate
bed_utilization_rate = resource_df["Utilization_Rate"].mean()

# Average Resource Utilization
avg_resource_utilization = resource_df["Utilization_Rate"].mean() / 100

# Department Efficiency Score
department_df["Department_Efficiency_Score"] = (
    department_df["Total_Patients"] /
    (department_df["Total_Doctors"] + department_df["Total_Nurses"])
) * avg_resource_utilization





# ======================================================
# ADD SUPPORTING COLUMNS
# ======================================================

hospital_df["Total_Beds"] = total_beds
hospital_df["Available_Bed_Days"] = available_bed_days
hospital_df["Bed_Utilization_Rate"] = bed_utilization_rate




# ======================================================
# EXPORT FINAL DATASET
# ======================================================

hospital_df.to_excel(
    "hospital_final_dataset.xlsx",
    index=False
)

print("\nFinal dataset exported successfully.")
# ============================================
# EXPORT FINAL DATASET
# ============================================

output_path = r"C:\Users\manda\Healthcare_analytics_project\data\hospital_final_dataset.xlsx"

with pd.ExcelWriter(output_path) as writer:
    hospital_df.to_excel(
        writer,
        sheet_name="Hospital_Data",
        index=False
    )

    kpi_summary.to_excel(
        writer,
        sheet_name="KPI_Summary",
        index=False
    )

print("\n" + "=" * 60)
print("MODULE 3 COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Final Dataset Exported Successfully")
print(f"Location: {output_path}")