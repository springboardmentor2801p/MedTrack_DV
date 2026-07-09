import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 10)

hospital_df = pd.read_csv("../data/raw/hospital_operations.csv")

patient_df = pd.read_csv("../data/raw/patient_operations.csv")

print("="*60)
print("Hospital Operations Dataset")
print("="*60)
print(hospital_df.shape)

print()

print("="*60)
print("Patient Operations Dataset")
print("="*60)
print(patient_df.shape)

hospital_df.head()
patient_df.head()

print(hospital_df.columns.tolist())
print(patient_df.columns.tolist())

hospital_df.info()
patient_df.info()

hospital_df.describe(include="all")
patient_df.describe(include="all")

hospital_df.isnull().sum()
patient_df.isnull().sum()

print("Hospital Dataset:", hospital_df.duplicated().sum())
print("Patient Dataset:", patient_df.duplicated().sum())

hospital_df.dtypes
patient_df.dtypes

hospital_df.to_csv(
    "../data/raw/hospital_raw_data.csv",
    index=False
)

patient_df.to_csv(
    "../data/raw/patient_raw_data.csv",
    index=False
)