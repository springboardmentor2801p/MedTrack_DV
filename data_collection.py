import pandas as pd

# Load dataset
df = pd.read_excel("hospital_raw_data.xlsx")

# Display basic information
print("Dataset Loaded Successfully")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# Save as CSV
df.to_csv("hospital_raw_data.csv", index=False)

print("\nCSV file created successfully.")