"""Generate synthetic hospital operational data for analytics projects."""

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = "hospital_raw_data.csv"
TOTAL_PATIENTS = 300
DUPLICATE_RECORDS = 18
NULL_RATE_BY_COLUMN = {
    "Blood_Group": 0.04,
    "Doctor_Name": 0.03,
    "Insurance_Provider": 0.05,
    "Bill_Amount": 0.02,
    "Medicine": 0.04,
    "Test_Result": 0.06,
    "Follow_Up_Date": 0.05,
    "Patient_Feedback": 0.10,
    "Hospital_Rating": 0.02,
    "Contact_Number": 0.08,
}
RANDOM_SEED = 42

fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


DEPARTMENTS = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Oncology",
    "Pediatrics",
    "Emergency",
    "ICU",
    "General Medicine",
    "Gynecology",
    "Radiology",
]

DEPARTMENT_PROFILES = {
    "Cardiology": {
        "diagnoses": ["Coronary Artery Disease", "Hypertension", "Arrhythmia"],
        "category": "Cardiovascular",
        "treatments": ["Angioplasty", "Cardiac Monitoring", "Medication Therapy"],
        "medicines": ["Atorvastatin", "Amlodipine", "Metoprolol"],
        "tests": ["ECG", "Troponin Test", "Echocardiogram"],
        "equipment": ["ECG Machine", "Cardiac Monitor"],
        "base_bill": 45000,
    },
    "Neurology": {
        "diagnoses": ["Migraine", "Epilepsy", "Stroke"],
        "category": "Neurological",
        "treatments": ["Neurological Observation", "Thrombolysis", "Seizure Control"],
        "medicines": ["Levetiracetam", "Aspirin", "Sumatriptan"],
        "tests": ["MRI Brain", "EEG", "CT Head"],
        "equipment": ["MRI Scanner", "EEG Machine"],
        "base_bill": 52000,
    },
    "Orthopedics": {
        "diagnoses": ["Fracture", "Osteoarthritis", "Ligament Tear"],
        "category": "Musculoskeletal",
        "treatments": ["Fracture Fixation", "Physiotherapy", "Joint Care"],
        "medicines": ["Ibuprofen", "Calcium Supplement", "Diclofenac"],
        "tests": ["X-Ray", "MRI Joint", "Bone Density Test"],
        "equipment": ["X-Ray Machine", "Traction Unit"],
        "base_bill": 38000,
    },
    "Oncology": {
        "diagnoses": ["Breast Cancer", "Lung Cancer", "Lymphoma"],
        "category": "Cancer",
        "treatments": ["Chemotherapy", "Radiation Therapy", "Targeted Therapy"],
        "medicines": ["Paclitaxel", "Cisplatin", "Imatinib"],
        "tests": ["Biopsy", "PET-CT", "Tumor Marker Test"],
        "equipment": ["Linear Accelerator", "Infusion Pump"],
        "base_bill": 90000,
    },
    "Pediatrics": {
        "diagnoses": ["Pneumonia", "Dengue Fever", "Gastroenteritis"],
        "category": "Pediatric",
        "treatments": ["Pediatric Care", "IV Fluids", "Antibiotic Therapy"],
        "medicines": ["Paracetamol Syrup", "ORS", "Amoxicillin"],
        "tests": ["CBC", "Dengue NS1", "Chest X-Ray"],
        "equipment": ["Pediatric Nebulizer", "Infusion Pump"],
        "base_bill": 18000,
    },
    "Emergency": {
        "diagnoses": ["Road Traffic Injury", "Acute Appendicitis", "Severe Dehydration"],
        "category": "Emergency Care",
        "treatments": ["Emergency Stabilization", "Wound Care", "Resuscitation"],
        "medicines": ["Normal Saline", "Ceftriaxone", "Tramadol"],
        "tests": ["FAST Scan", "CBC", "Serum Electrolytes"],
        "equipment": ["Defibrillator", "Emergency Trolley"],
        "base_bill": 30000,
    },
    "ICU": {
        "diagnoses": ["Sepsis", "Respiratory Failure", "Multi-Organ Dysfunction"],
        "category": "Critical Care",
        "treatments": ["Ventilator Support", "Critical Monitoring", "Vasopressor Therapy"],
        "medicines": ["Meropenem", "Noradrenaline", "Midazolam"],
        "tests": ["ABG", "Blood Culture", "Renal Function Test"],
        "equipment": ["Ventilator", "Multiparameter Monitor"],
        "base_bill": 120000,
    },
    "General Medicine": {
        "diagnoses": ["Type 2 Diabetes", "Typhoid Fever", "Viral Fever"],
        "category": "General Illness",
        "treatments": ["Medical Management", "Hydration Therapy", "Observation"],
        "medicines": ["Metformin", "Azithromycin", "Paracetamol"],
        "tests": ["CBC", "HbA1c", "Liver Function Test"],
        "equipment": ["Glucometer", "Infusion Pump"],
        "base_bill": 22000,
    },
    "Gynecology": {
        "diagnoses": ["High-Risk Pregnancy", "PCOS", "Fibroid Uterus"],
        "category": "Women Health",
        "treatments": ["Antenatal Care", "Hormonal Therapy", "Surgical Management"],
        "medicines": ["Folic Acid", "Progesterone", "Iron Supplement"],
        "tests": ["Ultrasound Pelvis", "Hormone Panel", "CBC"],
        "equipment": ["Ultrasound Machine", "Fetal Monitor"],
        "base_bill": 35000,
    },
    "Radiology": {
        "diagnoses": ["Pulmonary Nodule", "Kidney Stone", "Disc Prolapse"],
        "category": "Diagnostic Imaging",
        "treatments": ["Diagnostic Imaging", "Image-Guided Procedure", "Reporting"],
        "medicines": ["Contrast Agent", "Analgesic", "Sedative"],
        "tests": ["CT Scan", "MRI", "Ultrasound"],
        "equipment": ["CT Scanner", "MRI Scanner"],
        "base_bill": 16000,
    },
}


def create_hospitals() -> pd.DataFrame:
    """Create master data for 20 Indian hospitals."""
    hospital_locations = [
        ("Apollo Speciality Hospital", "Chennai", "Tamil Nadu", "Private"),
        ("AIIMS Delhi", "New Delhi", "Delhi", "Government"),
        ("Fortis Memorial Research Institute", "Gurugram", "Haryana", "Private"),
        ("Kokilaben Dhirubhai Ambani Hospital", "Mumbai", "Maharashtra", "Private"),
        ("Narayana Health City", "Bengaluru", "Karnataka", "Private"),
        ("CMC Vellore", "Vellore", "Tamil Nadu", "Trust"),
        ("KIMS Hospital", "Hyderabad", "Telangana", "Private"),
        ("Ruby Hall Clinic", "Pune", "Maharashtra", "Private"),
        ("Medanta The Medicity", "Gurugram", "Haryana", "Private"),
        ("PGIMER Chandigarh", "Chandigarh", "Chandigarh", "Government"),
        ("Manipal Hospital", "Jaipur", "Rajasthan", "Private"),
        ("AMRI Hospital", "Kolkata", "West Bengal", "Private"),
        ("Sawai Man Singh Hospital", "Jaipur", "Rajasthan", "Government"),
        ("Ganga Hospital", "Coimbatore", "Tamil Nadu", "Private"),
        ("Max Super Speciality Hospital", "Saket", "Delhi", "Private"),
        ("Kalinga Institute Hospital", "Bhubaneswar", "Odisha", "Trust"),
        ("Civil Hospital Ahmedabad", "Ahmedabad", "Gujarat", "Government"),
        ("Lisie Hospital", "Kochi", "Kerala", "Trust"),
        ("King George Medical University", "Lucknow", "Uttar Pradesh", "Government"),
        ("SevenHills Hospital", "Visakhapatnam", "Andhra Pradesh", "Private"),
    ]

    hospitals = []
    for index, (name, city, state, hospital_type) in enumerate(hospital_locations, 1):
        hospitals.append(
            {
                "Hospital_ID": f"HOSP{index:03d}",
                "Hospital_Name": name,
                "City": city,
                "State": state,
                "Hospital_Type": hospital_type,
                "Hospital_Rating": round(random.uniform(3.6, 4.9), 1),
            }
        )

    return pd.DataFrame(hospitals)


def create_patients(total_patients: int = TOTAL_PATIENTS) -> pd.DataFrame:
    """Create unique patient-level demographic records."""
    if total_patients <= 0:
        raise ValueError("total_patients must be greater than zero.")

    patients = []
    genders = ["Male", "Female", "Other"]
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    for index in range(1, total_patients + 1):
        gender = random.choices(genders, weights=[49, 49, 2], k=1)[0]
        name = fake.name_male() if gender == "Male" else fake.name_female()

        patients.append(
            {
                "Patient_ID": f"PAT{index:05d}",
                "Patient_Name": name,
                "Gender": gender,
                "Age": random.randint(1, 90),
                "Blood_Group": random.choice(blood_groups),
            }
        )

    return pd.DataFrame(patients)


def _choose_severity(department: str) -> str:
    """Choose severity with higher acuity for emergency and ICU records."""
    if department == "ICU":
        return random.choices(["Moderate", "Severe", "Critical"], [10, 45, 45], k=1)[0]
    if department == "Emergency":
        return random.choices(["Mild", "Moderate", "Severe", "Critical"], [10, 35, 40, 15], k=1)[0]
    return random.choices(["Mild", "Moderate", "Severe", "Critical"], [35, 40, 20, 5], k=1)[0]


def _calculate_bill(base_bill: int, severity: str, length_of_stay: int, surgery: str) -> float:
    """Calculate a realistic bill using department, severity, stay, and surgery."""
    severity_multiplier = {
        "Mild": 0.75,
        "Moderate": 1.0,
        "Severe": 1.55,
        "Critical": 2.25,
    }
    surgery_charge = 45000 if surgery == "Yes" else 0
    stay_charge = length_of_stay * random.randint(3500, 12000)
    diagnostics_charge = random.randint(3500, 25000)
    bill = (base_bill * severity_multiplier[severity]) + stay_charge + diagnostics_charge
    return round(bill + surgery_charge + random.uniform(-2500, 4500), 2)


def create_admissions(patients: pd.DataFrame, hospitals: pd.DataFrame) -> pd.DataFrame:
    """Create admission and operational records for each patient."""
    if patients.empty or hospitals.empty:
        raise ValueError("patients and hospitals dataframes cannot be empty.")

    admissions = []
    payment_statuses = ["Paid", "Pending", "Partially Paid", "Insurance Processing"]
    insurance_providers = ["Star Health", "HDFC ERGO", "ICICI Lombard", "Niva Bupa", "LIC", "None"]
    room_types = ["General", "Semi-Private", "Private", "Deluxe", "ICU"]
    outcomes = ["Recovered", "Improved", "Referred", "Under Observation", "Deceased"]
    feedback_options = ["Excellent", "Good", "Average", "Needs Improvement"]
    test_results = ["Normal", "Abnormal", "Borderline", "Critical", "Awaited"]
    wards = ["A", "B", "C", "D", "Emergency", "ICU"]

    for index, patient in patients.iterrows():
        hospital = hospitals.sample(n=1, random_state=RANDOM_SEED + index).iloc[0]
        department = random.choice(DEPARTMENTS)
        profile = DEPARTMENT_PROFILES[department]
        severity = _choose_severity(department)
        diagnosis = random.choice(profile["diagnoses"])

        admission_date = fake.date_between(
            start_date="-18M",
            end_date="-2d",
        )
        length_of_stay = max(1, int(np.random.poisson(lam=4)))
        if severity == "Severe":
            length_of_stay += random.randint(2, 5)
        elif severity == "Critical":
            length_of_stay += random.randint(5, 12)

        discharge_date = admission_date + timedelta(days=length_of_stay)
        is_icu = department == "ICU" or severity == "Critical"
        room_type = "ICU" if is_icu else random.choice(room_types[:-1])
        surgery = random.choices(["Yes", "No"], weights=[28, 72], k=1)[0]
        if department in ["Radiology", "General Medicine", "Pediatrics"]:
            surgery = random.choices(["Yes", "No"], weights=[8, 92], k=1)[0]

        insurance_status = random.choices(["Insured", "Not Insured"], [68, 32], k=1)[0]
        insurance_provider = (
            random.choice(insurance_providers[:-1]) if insurance_status == "Insured" else "None"
        )
        bill_amount = _calculate_bill(
            profile["base_bill"],
            severity,
            length_of_stay,
            surgery,
        )

        follow_up_date = discharge_date + timedelta(days=random.randint(7, 45))
        emergency_flag = department == "Emergency" or random.random() < 0.18
        outcome_weights = [48, 34, 8, 8, 2]
        if severity == "Critical":
            outcome_weights = [18, 35, 12, 25, 10]

        admissions.append(
            {
                "Admission_ID": f"ADM{index + 1:06d}",
                "Patient_ID": patient["Patient_ID"],
                "Hospital_ID": hospital["Hospital_ID"],
                "Department": department,
                "Admission_Date": admission_date.strftime("%Y-%m-%d"),
                "Discharge_Date": discharge_date.strftime("%Y-%m-%d"),
                "Length_of_Stay": length_of_stay,
                "Diagnosis": diagnosis,
                "Disease_Category": profile["category"],
                "Severity": severity,
                "Doctor_ID": f"DOC{random.randint(1, 85):04d}",
                "Doctor_Name": f"Dr. {fake.name()}",
                "Nurse_ID": f"NUR{random.randint(1, 160):04d}",
                "Bed_Number": f"{random.choice(wards)}-{random.randint(1, 60):02d}",
                "Ward": "ICU" if is_icu else random.choice(wards[:-1]),
                "Room_Type": room_type,
                "Insurance_Status": insurance_status,
                "Insurance_Provider": insurance_provider,
                "Bill_Amount": bill_amount,
                "Payment_Status": random.choice(payment_statuses),
                "Treatment": random.choice(profile["treatments"]),
                "Surgery": surgery,
                "Medicine": random.choice(profile["medicines"]),
                "Lab_Test": random.choice(profile["tests"]),
                "Test_Result": random.choice(test_results),
                "Resource_Used": random.choice(
                    ["Bed", "Oxygen", "Blood Unit", "Dialysis Slot", "Ambulance", "OT Slot"]
                ),
                "Equipment_Used": random.choice(profile["equipment"]),
                "Emergency_Flag": "Yes" if emergency_flag else "No",
                "ICU_Admission": "Yes" if is_icu else "No",
                "Follow_Up_Date": follow_up_date.strftime("%Y-%m-%d"),
                "Patient_Outcome": random.choices(outcomes, outcome_weights, k=1)[0],
                "Patient_Feedback": random.choice(feedback_options),
                "Readmission_Risk": random.choice(["Low", "Medium", "High"]),
                "Admission_Type": "Emergency" if emergency_flag else random.choice(["Planned", "Referral"]),
                "Discharge_Mode": random.choice(["Routine", "Against Medical Advice", "Transferred"]),
                "Attendant_Name": fake.name(),
                "Contact_Number": fake.phone_number(),
                "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return pd.DataFrame(admissions)


def merge_data(
    hospitals: pd.DataFrame,
    patients: pd.DataFrame,
    admissions: pd.DataFrame,
) -> pd.DataFrame:
    """Merge hospital, patient, and admission data into a final flat dataset."""
    try:
        patient_admissions = patients.merge(admissions, on="Patient_ID", how="inner")
        final_data = patient_admissions.merge(hospitals, on="Hospital_ID", how="left")

        ordered_columns = [
            "Hospital_ID",
            "Hospital_Name",
            "City",
            "State",
            "Hospital_Type",
            "Department",
            "Patient_ID",
            "Patient_Name",
            "Gender",
            "Age",
            "Blood_Group",
            "Admission_ID",
            "Admission_Date",
            "Discharge_Date",
            "Length_of_Stay",
            "Diagnosis",
            "Disease_Category",
            "Severity",
            "Doctor_ID",
            "Doctor_Name",
            "Nurse_ID",
            "Bed_Number",
            "Ward",
            "Room_Type",
            "Insurance_Status",
            "Insurance_Provider",
            "Bill_Amount",
            "Payment_Status",
            "Treatment",
            "Surgery",
            "Medicine",
            "Lab_Test",
            "Test_Result",
            "Resource_Used",
            "Equipment_Used",
            "Emergency_Flag",
            "ICU_Admission",
            "Follow_Up_Date",
            "Patient_Outcome",
            "Patient_Feedback",
            "Hospital_Rating",
            "Readmission_Risk",
            "Admission_Type",
            "Discharge_Mode",
            "Attendant_Name",
            "Contact_Number",
            "Created_At",
        ]
        return final_data[ordered_columns]
    except KeyError as error:
        raise KeyError(f"Missing expected merge column: {error}") from error


def add_data_quality_issues(
    data: pd.DataFrame,
    duplicate_records: int = DUPLICATE_RECORDS,
) -> pd.DataFrame:
    """Add controlled duplicates and nulls for cleaning and BI practice."""
    if data.empty:
        raise ValueError("Cannot add quality issues to an empty dataset.")
    if duplicate_records < 0 or duplicate_records >= len(data):
        raise ValueError("duplicate_records must be between 0 and total rows - 1.")

    data_with_issues = data.copy()

    # Add nulls only to non-key analytical columns so joins remain usable.
    for column, null_rate in NULL_RATE_BY_COLUMN.items():
        if column not in data_with_issues.columns:
            raise KeyError(f"Column configured for nulls does not exist: {column}")
        null_count = max(1, int(round(len(data_with_issues) * null_rate)))
        null_indices = data_with_issues.sample(
            n=null_count,
            random_state=RANDOM_SEED + len(column),
        ).index
        data_with_issues.loc[null_indices, column] = np.nan

    if duplicate_records:
        available_source_rows = data_with_issues.iloc[:-duplicate_records]
        source_rows = data_with_issues.sample(
            n=duplicate_records,
            random_state=RANDOM_SEED + 500,
        ) if available_source_rows.empty else available_source_rows.sample(
            n=duplicate_records,
            random_state=RANDOM_SEED + 500,
        )
        source_rows = source_rows.reset_index(drop=True)
        target_indices = data_with_issues.tail(duplicate_records).index
        data_with_issues.loc[target_indices, :] = source_rows.to_numpy()

    return data_with_issues


def save_dataset(data: pd.DataFrame, output_file: str = OUTPUT_FILE) -> None:
    """Save the final dataset as CSV."""
    if data.empty:
        raise ValueError("Cannot save an empty dataset.")

    output_path = BASE_DIR / output_file
    temporary_path = output_path.with_suffix(".tmp.csv")
    data.to_csv(temporary_path, index=False)
    temporary_path.replace(output_path)


def main() -> None:
    """Run the full synthetic data generation workflow."""
    try:
        print("Generating hospital master data...")
        hospitals = create_hospitals()

        print("Generating patient records...")
        patients = create_patients()

        print("Generating admissions and operational details...")
        admissions = create_admissions(patients, hospitals)

        print("Merging data...")
        final_data = merge_data(hospitals, patients, admissions)

        print("Adding duplicate rows and null values for analysis practice...")
        final_data = add_data_quality_issues(final_data)

        print("Saving dataset...")
        save_dataset(final_data)

        print("\nGeneration complete.")
        print(f"Number of hospitals generated: {hospitals['Hospital_ID'].nunique()}")
        print(f"Number of patient records generated: {patients['Patient_ID'].nunique()}")
        print(f"Intentional duplicate rows added: {DUPLICATE_RECORDS}")
        print(f"Total null values added: {int(final_data.isna().sum().sum())}")
        print(f"Output file name: {OUTPUT_FILE}")
        print(f"Total records: {len(final_data)}")
        print(f"Total columns: {len(final_data.columns)}")
    except (ValueError, KeyError, OSError) as error:
        print(f"Data generation failed: {error}")
        raise


if __name__ == "__main__":
    main()
