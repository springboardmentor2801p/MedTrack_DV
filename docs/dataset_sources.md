L# MedTrack DV – Dataset Sources

## 1. Dataset Overview

The MedTrack DV project uses a Hospital Operations Dataset for healthcare data analysis and visualization.

- Dataset: Hospital Operations Dataset
- Records: 2,238
- Columns: 37
- Domain: Healthcare Operations Analytics
- Data Processing: Python and Pandas
- Data Visualization: Tableau

---

## 2. Dataset Fields

The dataset contains the following 37 columns:

1. Name
2. Age
3. Gender
4. Blood Type
5. Medical Condition
6. Date of Admission
7. Doctor
8. Hospital
9. Insurance Provider
10. Billing Amount
11. Room Number
12. Admission Type
13. Discharge Date
14. Medication
15. Test Results
16. Patient_ID
17. Department
18. Length_of_stay
19. Readmission_Flag
20. Severity
21. Ward
22. Bed_ID
23. Room_Type
24. Nurse_ID
25. Staff_Shift
26. Equipment_Used
27. Equipment_status
28. Payment_Status
29. Payment_Method
30. Emergency_Case
31. ICU_Admission
32. Discharge_Status
33. Hospital_Region
34. Admission_Month
35. Admission_Year
36. Occupancy_Status
37. Bed_Capacity

---

## 3. Dataset Size

- Total Records: 2,238
- Total Columns: 37

Each row represents a patient record, while the columns contain patient, medical, admission, discharge, financial, departmental, staffing, equipment, and hospital resource information.

---

## 4. Data Categories

### Patient Information

- Name
- Age
- Gender
- Blood Type
- Patient_ID

### Medical Information

- Medical Condition
- Doctor
- Medication
- Test Results
- Severity

### Admission and Discharge Information

- Date of Admission
- Admission Type
- Discharge Date
- Length_of_stay
- Readmission_Flag
- Emergency_Case
- ICU_Admission
- Discharge_Status
- Admission_Month
- Admission_Year

### Hospital and Department Information

- Hospital
- Department
- Hospital_Region
- Ward
- Bed_ID
- Room Number
- Room_Type

### Financial Information

- Insurance Provider
- Billing Amount
- Payment_Status
- Payment_Method

### Staff and Resource Information

- Nurse_ID
- Staff_Shift
- Equipment_Used
- Equipment_status
- Occupancy_Status
- Bed_Capacity

---

## 5. Data Processing

The dataset was processed using Python and Pandas before being used for Tableau visualization.

The data processing workflow included:

- Loading the dataset
- Inspecting the dataset structure
- Checking the number of records and columns
- Reviewing column names
- Checking data quality
- Preparing the data for KPI generation
- Preparing the processed data for Tableau visualization

---

## 6. Data Usage

The dataset is used to analyze important healthcare operations such as:

- Patient admissions
- Patient flow
- Hospital occupancy
- Length of stay
- Readmissions
- Billing
- Department performance
- Emergency cases
- ICU admissions
- Bed utilization
- Staff resources
- Equipment utilization

---

## 7. KPI Generation

The dataset is used as the source for the 19 KPIs created for the MedTrack DV project.

The KPIs cover four major areas:

### Hospital Overview

- Total Patients
- Total Billing
- Bed Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Discharge Rate

### Patient Flow

- Total Admissions
- Occupied Beds
- Severe Cases %
- ICU Admissions
- Emergency Cases
- Average Billing per Patient

### Department Analytics

- Total Departments
- Average Patients per Department
- Average Billing per Department

### Resource Utilization

- Total Nurses
- Available Beds
- Average Patients per Doctor
- Total Wards

---

## 8. Tableau Dashboards

The processed dataset is used to create four Tableau dashboards:

1. Hospital Overview Dashboard
2. Patient Flow Dashboard
3. Department Analytics Dashboard
4. Resource Utilization Dashboard

These dashboards provide interactive analysis of hospital performance, patient flow, department activity, and resource utilization.

---

## 9. Tools Used

- Python
- Pandas
- Tableau
- Markdown
- GitHub

Python and Pandas were used for data processing and preparation, while Tableau was used to create the interactive healthcare dashboards.

---

## 10. Data Flow

The overall data flow is:

Hospital Operations Dataset
↓
Python and Pandas
↓
Data Processing
↓
KPI Generation
↓
Tableau
↓
Interactive Dashboards
↓
Healthcare Operations Insights

---

## 11. Dataset Summary

| Attribute | Details |
|---|---|
| Dataset | Hospital Operations Dataset |
| Records | 2,238 |
| Columns | 37 |
| Domain | Healthcare Operations Analytics |
| Data Processing | Python / Pandas |
| Visualization | Tableau |
| Dashboards | 4 |
| KPIs | 19 |