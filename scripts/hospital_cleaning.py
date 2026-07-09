import pandas as pd

# Load raw dataset
df = pd.read_csv("data/hospital_raw_data.csv")

print("=" * 50)
print("HOSPITAL DATA CLEANING")
print("=" * 50)

print("\nOriginal Shape:", df.shape)

# Missing values before cleaning
missing_before = df.isnull().sum().sum()
total_cells = df.size

print(f"\nMissing Values Before Cleaning: {missing_before}")

# Remove duplicates
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print(f"Duplicate Rows Removed: {duplicates}")

# Clean every column
for col in df.columns:

    if df[col].dtype == "object":
        df[col] = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    else:
        df[col] = df[col].fillna(df[col].median())

# Missing values after cleaning
missing_after = df.isnull().sum().sum()
missing_percentage = (missing_after / df.size) * 100

print(f"\nMissing Values After Cleaning: {missing_after}")
print(f"Missing Percentage: {missing_percentage:.2f}%")

# Save cleaned data
df.to_csv("data/hospital_cleaned.csv", index=False)

print("\nCleaned Dataset Shape:", df.shape)

print("\nOperational Metrics")
print("--------------------------")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])

print("\nData Types")
print(df.dtypes)

print("\n✅ hospital_cleaned.csv created successfully.")

# Verify cleaned data
print("\n========== AFTER CLEANING ==========")

print("Missing Values:")
print(df.isnull().sum())

total_missing = df.isnull().sum().sum()
missing_percentage = (total_missing / df.size) * 100

print(f"\nTotal Missing Values: {total_missing}")
print(f"Missing Percentage: {missing_percentage:.2f}%")