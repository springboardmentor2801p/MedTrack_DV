import pandas as pd

print("Loading Integrated Dataset...")

# Load integrated dataset
df = pd.read_csv("data/hospital_raw_data.csv")

print("Original Shape :", df.shape)

# -------------------------------
# 1. Remove Duplicate Records
# -------------------------------
df = df.drop_duplicates()

# -------------------------------
# 2. Handle Missing Values
# -------------------------------
df = df.fillna({
    "Diagnosis": "Unknown",
    "Treatment": "Not Available",
    "Insurance_Status": "No"
})

# Numeric missing values
numeric_columns = df.select_dtypes(include=["number"]).columns

for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

# -------------------------------
# 3. Standardize Department Names
# -------------------------------
if "Department_Name" in df.columns:
    df["Department_Name"] = (
        df["Department_Name"]
        .str.strip()
        .str.title()
    )

# -------------------------------
# 4. Remove Extra Spaces
# -------------------------------
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

# -------------------------------
# 5. Save Clean Dataset
# -------------------------------
df.to_csv(
    "data/hospital_cleaned.csv",
    index=False
)

print("Cleaning Completed Successfully")
print("New Shape :", df.shape)