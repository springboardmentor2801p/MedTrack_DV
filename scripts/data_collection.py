"""
=========================================================
Healthcare Analytics Project
Module 1 : Hospital Data Collection

Author : Niharika

Datasets:
1. Hospital Inpatient Discharges
2. Health Facility General Information

Output Files:
-------------
1. hospital_raw_data.csv
2. hospital_profile.csv
3. department_data.csv
4. resource_data.csv
=========================================================
"""

import pandas as pd
import random
from sklearn.model_selection import train_test_split
from pathlib import Path
# --------------------------------------------------
# Project Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def main():

    print("=" * 60)
    print("Healthcare Analytics Project")
    print("Module 1 : Hospital Data Collection")
    print("=" * 60)
        # --------------------------------------------------
    # Load Hospital Inpatient Discharges Dataset
    # --------------------------------------------------

    hospital_df = pd.read_csv(
        DATA_DIR / "Hospital_Inpatient_Discharges__SPARCS_De-Identified___2021_20231012.csv",
        low_memory=False
    )

    print("\nHospital dataset loaded successfully.")
    print("Shape :", hospital_df.shape)
        # --------------------------------------------------
    # Filter Selected Hospital
    # --------------------------------------------------

    hospital_df = hospital_df[
        hospital_df["Facility Name"] ==
        "New York-Presbyterian Hospital - New York Weill Cornell Center"
    ]

    print("\nSelected Hospital Records")
    print(hospital_df.shape)
        # --------------------------------------------------
    # Representative Sampling (8000 Records)
    # --------------------------------------------------

    sample_df, _ = train_test_split(
        hospital_df,
        train_size=8000,
        stratify=hospital_df["Type of Admission"],
        random_state=42
    )

    sample_df = sample_df.sample(
        n=8000,
        random_state=42
    )

    print("\nRepresentative Sample Created")
    print(sample_df.shape)
        # --------------------------------------------------
    # Data Cleaning
    # --------------------------------------------------

    sample_df["Total Charges"] = (
        sample_df["Total Charges"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    sample_df["Total Costs"] = (
        sample_df["Total Costs"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    sample_df["Length of Stay"] = (
        sample_df["Length of Stay"]
        .str.strip()
        .replace("120 +", "120")
        .astype(int)
    )

    print("\nData Cleaning Completed")
        # --------------------------------------------------
    # Save Patient Dataset
    # --------------------------------------------------
    sample_df.to_csv(
        DATA_DIR / "hospital_raw_data.csv",
        index=False
    )

    print("\nhospital_raw_data.csv saved successfully.")
        # --------------------------------------------------
    # Load Health Facility Dataset
    # --------------------------------------------------

    facility_df = pd.read_csv(
        DATA_DIR / "Health_Facility_General_Information_20260705.csv"
    )

    print("\nHealth Facility dataset loaded successfully.")
    print("Shape :", facility_df.shape)
        # Clean Operating Certificate Number

    facility_df["Operating Certificate Number"] = (
        facility_df["Operating Certificate Number"]
        .astype(str)
        .str.extract(r'(\d+)')[0]
    )

    facility_df["Operating Certificate Number"] = pd.to_numeric(
        facility_df["Operating Certificate Number"],
        errors="coerce"
    )

    # Filter selected hospital
    hospital_profile = facility_df[
        facility_df["Operating Certificate Number"] == 7002054
    ]

    # Keep only required columns
    hospital_profile = hospital_profile[
        [
            "Facility ID",
            "Facility Name",
            "Description",
            "Facility Open Date",
            "Facility Address 1",
            "Facility City",
            "Facility State",
            "Facility Zip Code",
            "Facility County",
            "Operating Certificate Number",
            "Ownership Type",
            "Facility Website",
            "Facility Latitude",
            "Facility Longitude"
        ]
    ]
    hospital_profile.to_csv(
        DATA_DIR / "hospital_profile.csv",
        index=False
    )

    print("\nhospital_profile.csv saved successfully.")
        # --------------------------------------------------
    # Create Department Dataset
    # --------------------------------------------------

    department_df = (
        sample_df["APR MDC Description"]
        .value_counts()
        .reset_index()
    )

    department_df.columns = [
        "Based_On",
        "Total_Patients"
    ]

    print("\nDepartment summary created.")
        # --------------------------------------------------
    # Add Department IDs
    # --------------------------------------------------

    department_df["Department_ID"] = [
        f"D{i:03d}" for i in range(1, len(department_df) + 1)
    ]
    department_names = [
        "Obstetrics & Gynecology",
        "Pediatrics & Neonatal Care",
        "Cardiology",
        "Gastroenterology",
        "Neurology",
        "Pulmonology",
        "Orthopedics",
        "Nephrology & Urology",
        "Infectious Disease",
        "Endocrinology",
        "Oncology",
        "Hepatology",
        "Dermatology",
        "ENT",
        "Psychiatry",
        "Hematology",
        "General Medicine",
        "Emergency Medicine",
        "Urology",
        "Burn Care",
        "Gynecology",
        "Addiction Medicine",
        "Trauma Care",
        "Ophthalmology",
        "HIV Care",
        "Critical Care"
    ]

    department_df["Department_Name"] = department_names
    department_df["Department_Floor"] = [
        "3rd Floor","2nd Floor","5th Floor","4th Floor","5th Floor",
        "4th Floor","2nd Floor","3rd Floor","1st Floor","3rd Floor",
        "6th Floor","6th Floor","2nd Floor","2nd Floor","4th Floor",
        "5th Floor","1st Floor","Ground Floor","3rd Floor","Ground Floor",
        "3rd Floor","2nd Floor","Ground Floor","2nd Floor","5th Floor","ICU"
    ]

    department_df["Department_Extension"] = list(range(101,127))

    department_df["Head_Doctor"] = [
        "Head of Obstetrics & Gynecology",
        "Head of Pediatrics & Neonatal Care",
        "Chief Cardiologist",
        "Chief Gastroenterologist",
        "Chief Neurologist",
        "Chief Pulmonologist",
        "Chief Orthopedic Surgeon",
        "Chief Nephrologist & Urologist",
        "Chief Infectious Disease Specialist",
        "Chief Endocrinologist",
        "Chief Oncologist",
        "Chief Hepatologist",
        "Chief Dermatologist",
        "Chief ENT Specialist",
        "Chief Psychiatrist",
        "Chief Hematologist",
        "Chief General Physician",
        "Chief Emergency Physician",
        "Chief Urologist",
        "Chief Burn Surgeon",
        "Chief Gynecologist",
        "Chief Addiction Specialist",
        "Chief Trauma Surgeon",
        "Chief Ophthalmologist",
        "Chief HIV Specialist",
        "Chief Intensivist"
    ]
    department_df["Total_Doctors"] = [
        24,22,18,15,15,14,12,11,9,8,
        8,7,7,6,6,6,10,12,7,6,
        6,5,5,4,3,8
    ]

    department_df["Total_Nurses"] = [
        58,55,44,38,36,34,30,28,24,20,
        18,18,16,15,15,14,22,25,15,14,
        13,12,11,10,8,30
    ]

    department_df["Total_Beds"] = [
        75,70,60,48,45,42,35,30,25,22,
        20,18,18,15,15,15,30,35,18,18,
        15,12,12,10,8,40
    ]

    department_df["Department_Status"] = "Active"
    department_df = department_df[
        [
            "Department_ID",
            "Department_Name",
            "Based_On",
            "Department_Floor",
            "Department_Extension",
            "Total_Patients",
            "Head_Doctor",
            "Total_Doctors",
            "Total_Nurses",
            "Total_Beds",
            "Department_Status"
        ]
    ]

    department_df.to_csv(
        DATA_DIR / "department_data.csv",
        index=False
    )

    print("\ndepartment_data.csv saved successfully.")
        # --------------------------------------------------
    # Create Resource Dataset
    # --------------------------------------------------

    resource_mapping = {
        "Obstetrics & Gynecology": [
            ("Delivery Rooms", "Room"),
            ("Fetal Monitors", "Equipment"),
            ("Ultrasound Machines", "Equipment"),
            ("Labor Beds", "Bed")
        ],

        "Pediatrics & Neonatal Care": [
            ("Incubators", "Equipment"),
            ("NICU Beds", "Bed"),
            ("Infant Warmers", "Equipment"),
            ("Pediatric Ventilators", "Equipment")
        ],

        "Cardiology": [
            ("ECG Machines", "Equipment"),
            ("ICU Beds", "Bed"),
            ("Cardiac Monitors", "Equipment"),
            ("Catheterization Lab", "Room")
        ],

        "Gastroenterology": [
            ("Endoscopy Units", "Equipment"),
            ("Procedure Rooms", "Room"),
            ("Patient Beds", "Bed"),
            ("Ultrasound Machines", "Equipment")
        ],

        "Neurology": [
            ("EEG Machines", "Equipment"),
            ("MRI Access", "Equipment"),
            ("Neurology Beds", "Bed"),
            ("ICU Monitors", "Equipment")
        ],

        "Pulmonology": [
            ("Ventilators", "Equipment"),
            ("Respiratory Monitors", "Equipment"),
            ("Oxygen Beds", "Bed"),
            ("Pulmonary Function Lab", "Room")
        ],

        "Orthopedics": [
            ("Operation Theatres", "Room"),
            ("X-Ray Machines", "Equipment"),
            ("Orthopedic Beds", "Bed"),
            ("Wheelchairs", "Equipment")
        ],

        "Nephrology & Urology": [
            ("Dialysis Machines", "Equipment"),
            ("Dialysis Beds", "Bed"),
            ("Ultrasound Machines", "Equipment"),
            ("Procedure Rooms", "Room")
        ],

        "Infectious Disease": [
            ("Isolation Rooms", "Room"),
            ("Negative Pressure Beds", "Bed"),
            ("PPE Kits", "Equipment"),
            ("Disinfection Units", "Equipment")
        ],

        "Endocrinology": [
            ("Consultation Rooms", "Room"),
            ("Glucose Analyzers", "Equipment"),
            ("Patient Beds", "Bed"),
            ("Diagnostic Equipment", "Equipment")
        ]
    }
    resource_data = []
    resource_id = 1

    for _, dept in department_df.head(10).iterrows():

        dept_name = dept["Department_Name"]
        dept_id = dept["Department_ID"]

        for resource_name, category in resource_mapping[dept_name]:

            total_units = random.randint(8, 30)
            maintenance = random.randint(0, 2)

            in_use = random.randint(
                int(total_units * 0.5),
                total_units - maintenance
            )

            available = total_units - in_use - maintenance

            utilization = round(
                (in_use / total_units) * 100,
                2
            )

            resource_data.append([
                f"R{resource_id:03d}",
                dept_id,
                dept_name,
                resource_name,
                category,
                total_units,
                available,
                in_use,
                maintenance,
                utilization,
                "Active"
            ])

            resource_id += 1

    resource_df = pd.DataFrame(
        resource_data,
        columns=[
            "Resource_ID",
            "Department_ID",
            "Department_Name",
            "Resource_Name",
            "Resource_Category",
            "Total_Units",
            "Available_Units",
            "In_Use_Units",
            "Maintenance_Units",
            "Utilization_Rate",
            "Resource_Status"
        ]
    )

    resource_df.to_csv(
        DATA_DIR / "resource_data.csv",
        index=False
    )

    print("\nresource_data.csv saved successfully.")
    print("\n" + "=" * 60)
    print("Module 1 completed successfully!")
    print("=" * 60)
    print("Generated Files:")
    print("1. hospital_raw_data.csv")
    print("2. hospital_profile.csv")
    print("3. department_data.csv")
    print("4. resource_data.csv")
    print("=" * 60)
    
if __name__ == "__main__":
    main()