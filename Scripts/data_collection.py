import pandas as pd

healthcare = pd.read_csv("Data/healthcare_dataset.csv")
patient = pd.read_csv("Data/patient.csv")
admission = pd.read_csv("Data/admission.csv")
department = pd.read_csv("Data/department.csv")
doctor = pd.read_csv("Data/doctor.csv")
employee = pd.read_csv("Data/employee.csv")
bed = pd.read_csv("Data/bed.csv")
disease = pd.read_csv("Data/disease.csv")
patient_diagnostic = pd.read_csv("Data/patient_diagnostic.csv")
patient_insurance = pd.read_csv("Data/patient_insurance.csv")
insurance_provider = pd.read_csv("Data/insurance_provider.csv")

print("All datasets loaded successfully!")

print("Healthcare:", healthcare.shape)
print("Patient:", patient.shape)
print("Admission:", admission.shape)
print("Department:", department.shape)
print("Doctor:", doctor.shape)
print("Employee:", employee.shape)
print("Bed:", bed.shape)
print("Disease:", disease.shape)
print("Patient Diagnostic:", patient_diagnostic.shape)
print("Patient Insurance:", patient_insurance.shape)
print("Insurance Provider:", insurance_provider.shape)

print("\nHealthcare Columns:")
print(healthcare.columns.tolist())

print("\nPatient Columns:")
print(patient.columns.tolist())

print("\nAdmission Columns:")
print(admission.columns.tolist())

print("\nDepartment Columns:")
print(department.columns.tolist())

print("\nDisease Columns:")
print(disease.columns.tolist())

print("\nBed Columns:")
print(bed.columns.tolist())

print("\nEmployee Columns:")
print(employee.columns.tolist())

print("\nDoctor Columns:")
print(doctor.columns.tolist())

print("\nDuplicate Patient IDs:", patient["patient_id"].duplicated().sum())
print("Duplicate Admission IDs:", admission["admission_id"].duplicated().sum())
print("Duplicate Department IDs:", department["department_id"].duplicated().sum())
print("Duplicate Disease IDs:", disease["disease_id"].duplicated().sum())
print("Duplicate Bed IDs:", bed["bed_id"].duplicated().sum())

# Merge Patient and Admission datasets
patient_admission = pd.merge(
    patient,
    admission,
    on="patient_id",
    how="inner"
)

print("\nPatient + Admission Dataset Shape:")
print(patient_admission.shape)

print("\nColumns:")
print(patient_admission.columns.tolist())

print("\nFirst 5 Rows:")
print(patient_admission.head())

# Merge Department

patient_admission_department = pd.merge(
    patient_admission,
    department,
    on="department_id",
    how="left"
)

print("\nPatient + Admission + Department Shape:")
print(patient_admission_department.shape)

print("\nColumns:")
print(patient_admission_department.columns.tolist())

print("\nFirst 5 Rows:")
print(
    patient_admission_department[
        [
            "patient_id",
            "admission_id",
            "department_name",
            "department_type",
            "floor_number"
        ]
    ].head()
)

# Merge Disease

patient_admission_department_disease = pd.merge(
    patient_admission_department,
    disease,
    on="disease_id",
    how="left"
)

print("\nPatient + Admission + Department + Disease Shape:")
print(patient_admission_department_disease.shape)

print("\nFirst 5 Rows:")
print(
    patient_admission_department_disease[
        [
            "patient_id",
            "admission_id",
            "department_name",
            "disease_name",
            "disease_category"
        ]
    ].head()
)

# Merge Bed

patient_admission_department_disease_bed = pd.merge(
    patient_admission_department_disease,
    bed,
    on="bed_id",
    how="left"
)

print("\nPatient + Admission + Department + Disease + Bed Shape:")
print(patient_admission_department_disease_bed.shape)

print("\nFirst 5 Rows:")
print(
    patient_admission_department_disease_bed[
        [
            "patient_id",
            "admission_id",
            "department_name",
            "bed_number",
            "bed_status"
        ]
    ].head()
)

patient_admission_department_disease_bed_insurance = pd.merge(
    patient_admission_department_disease_bed,
    patient_insurance,
    on="patient_id",
    how="left"
)

print(
    patient_admission_department_disease_bed_insurance.shape
)

print(
    patient_admission_department_disease_bed_insurance[
        [
            "patient_id",
            "policy_number",
            "coverage_percentage",
            "insurance_provider_id"
        ]
    ].head()
)

patient_admission_department_disease_bed_insurance_provider = pd.merge(
    patient_admission_department_disease_bed_insurance,
    insurance_provider,
    on="insurance_provider_id",
    how="left"
)

print(
    patient_admission_department_disease_bed_insurance_provider.shape
)

print(
    patient_admission_department_disease_bed_insurance_provider[
        [
            "patient_id",
            "provider_name",
            "provider_type",
            "coverage_limit"
        ]
    ].head()
)

patient_admission_department_disease_bed_insurance_provider_diagnostic = pd.merge(
    patient_admission_department_disease_bed_insurance_provider,
    patient_diagnostic,
    on="admission_id",
    how="left"
)

print(
    patient_admission_department_disease_bed_insurance_provider_diagnostic.shape
)

print(
    patient_admission_department_disease_bed_insurance_provider_diagnostic[
        [
            "patient_id",
            "admission_id",
            "doctor_id",
            "test_date",
            "result_status"
        ]
    ].head()
)

patient_admission_department_disease_bed_insurance_provider_diagnostic_doctor = pd.merge(
    patient_admission_department_disease_bed_insurance_provider_diagnostic,
    doctor,
    on="doctor_id",
    how="left"
)

print(
    patient_admission_department_disease_bed_insurance_provider_diagnostic_doctor.shape
)

print(
    patient_admission_department_disease_bed_insurance_provider_diagnostic_doctor[
        [
            "patient_id",
            "doctor_id",
            "employee_id",
            "specialization",
            "experience_years"
        ]
    ].head()
)

final_hmis = pd.merge(
    patient_admission_department_disease_bed_insurance_provider_diagnostic_doctor,
    employee,
    on="employee_id",
    how="left"
)

print("\nFinal HMIS Shape:")
print(final_hmis.shape)

print("\nFirst 5 Rows:")
print(
    final_hmis[
        [
            "patient_id",
            "doctor_id",
            "employee_name",
            "role",
            "employment_type",
            "specialization",
            "experience_years"
        ]
    ].head()
)

final_hmis.to_csv(
    "Data/hospital_raw_data.csv",
    index=False
)

print("hospital_raw_data.csv created successfully!")