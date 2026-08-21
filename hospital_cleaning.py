import pandas as pd

# Load cleaned dataset
df = pd.read_excel("hospital_cleaned.xlsx")

# Check duplicates
duplicates = df.duplicated().sum()
print("Duplicate Records:", duplicates)

# Check missing values
missing = df.isnull().sum()
print("\nMissing Values:")
print(missing)

# Save final cleaned dataset
df.to_csv("hospital_cleaned.csv", index=False)

print("\nData Cleaning Completed Successfully")