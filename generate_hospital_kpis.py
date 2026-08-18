import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

hospital_df = pd.read_csv("../data/cleaned/hospital_cleaned.csv")

patient_df = pd.read_csv("../data/cleaned/patient_cleaned.csv")

total_admissions = patient_df["Patient_ID"].count()

print("Total Admissions:", total_admissions)

average_los = patient_df["Length_of_Stay_Days"].mean()

print("Average Length of Stay:", round(average_los,2),"Days")

readmission_rate = (
    patient_df["Readmission_Flag"].mean()
) * 100

print(f"Readmission Rate: {readmission_rate:.2f}%")

TOTAL_BEDS = 500

occupancy_rate = (

    patient_df["Length_of_Stay_Days"].sum()

    /

    (TOTAL_BEDS * 365)

)*100

print("Occupancy Rate:",round(occupancy_rate,2),"%")


bed_utilization = (

    patient_df["Length_of_Stay_Days"].sum()

    /

    (500*365)

)*100

print("Bed Utilization Rate:",round(bed_utilization,2),"%")

department_efficiency = (

    patient_df

    .groupby("Department")

    .agg(

        Avg_Wait_Time=("Wait_Time_Minutes","mean"),

        Avg_LOS=("Length_of_Stay_Days","mean"),

        Avg_Cost=("Treatment_Cost_USD","mean")

    )

)

department_efficiency["Efficiency_Score"]=(

100-

department_efficiency["Avg_Wait_Time"]

)

department_efficiency

kpi_summary = pd.DataFrame({

"KPI":[

"Total Admissions",

"Average Length of Stay",

"Readmission Rate",

"Occupancy Rate",

"Bed Utilization Rate"

],

"Value":[

total_admissions,

round(average_los,2),

round(readmission_rate,2),

round(occupancy_rate,2),

round(bed_utilization,2)

]

})

kpi_summary