import pandas as pd

df = pd.read_csv("Hospital_dataset.csv")

print(df.head(5))
print(df.info())

print(df.isnull().sum())

print(" Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

print(" Duplicate rows after cleaning:", df.duplicated().sum())
df = df.dropna()

print("Missing values after cleaning:", df.isnull().sum())

df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], dayfirst=True)  
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], dayfirst=True)
text_columns = df.select_dtypes(include="object").columns
for col in text_columns:
    df[col] = df[col].str.strip()


    print(df.columns)
    print("Number of Columns:", len(df.columns))

    df.columns = [
        "Name New",
        "Age",
        "Gender",
        "Blood Type",
        "Medical Condition",
        "Date of Admission",
        "Doctor",
        "Hospital",
        "Insurance Provider",
        "Billing Amount",
        "Room Number",
        "Admission Type",
        "Discharge Date",
        "Medication",
        "Test Results",
        "Length of Stay",
    ]
df["Admission Month"]= df["Date of Admission"].dt.month_name()

df["Admission Year"] = df["Date of Admission"].dt.year

df["Billing Category"] = pd.cut( df["Billing Amount"], bins=[0, 10000, 30000, 50000 ], labels=["Low", "Medium", "High"])

print("KPI columns created successfully.")

df.to_csv("Hospital_Cleaned.csv", index=False)
print("Dataset cleaned and saved successfully.")