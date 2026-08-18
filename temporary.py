import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 10)
hospital_df = pd.read_csv("../data/raw/hospital_raw_data.csv")

patient_df = pd.read_csv("../data/raw/patient_raw_data.csv")

print("Hospital Dataset Duplicates:", hospital_df.duplicated().sum())

print("Patient Dataset Duplicates:", patient_df.duplicated().sum())

hospital_df.isnull().sum()

patient_df.isnull().sum()

hospital_df[
    [
        "Discharge Time",
        "Discharge Before 12PM"
    ]
].head(20)

hospital_df["Discharge Time"] = hospital_df["Discharge Time"].fillna("Not Recorded")

hospital_df["Discharge Before 12PM"] = hospital_df["Discharge Before 12PM"].fillna("Unknown")

hospital_df.isnull().sum()

patient_df["Department"].unique()
patient_df["Department"] = (
    patient_df["Department"]
    .str.strip()
    .str.title()
)

patient_df["Department"].value_counts()


scaler = MinMaxScaler()

columns = [

    "Length_of_Stay_Days",

    "Wait_Time_Minutes",

    "Treatment_Cost_USD"

]

patient_df[columns] = scaler.fit_transform(
    patient_df[columns]
)
patient_df[
    [

        "Length_of_Stay_Days",

        "Wait_Time_Minutes",

        "Treatment_Cost_USD"

    ]

].head()