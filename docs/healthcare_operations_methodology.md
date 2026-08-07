# MedTrack DV – Healthcare Operations Methodology

## 1. Overview

MedTrack DV is a healthcare operations analytics project designed to transform hospital data into meaningful business insights using data processing, KPI engineering, and Tableau visualization.

The methodology follows a structured process from raw data preparation to interactive dashboard development.

---

## 2. Project Objective

The main objective of MedTrack DV is to analyze hospital operations and provide a clear view of:

- Patient activity
- Hospital performance
- Patient flow
- Department performance
- Hospital resource utilization
- Billing and financial activity
- Bed occupancy
- Readmissions
- Emergency cases
- ICU admissions

The final output is a four-dashboard Tableau analytics suite.

---

## 3. Healthcare Data Workflow

The project follows this workflow:

Raw Hospital Dataset
↓
Data Inspection
↓
Data Cleaning
↓
Data Validation
↓
KPI Engineering
↓
Tableau Data Connection
↓
Calculated Fields
↓
Visualizations
↓
Interactive Dashboards
↓
Healthcare Insights

---

## 4. Data Collection

The hospital dataset contains:

- 2,238 patient records
- 37 columns

The dataset contains patient, medical, admission, discharge, financial, department, staffing, equipment, and hospital resource information.

Important fields include:

- Patient_ID
- Age
- Gender
- Medical Condition
- Date of Admission
- Discharge Date
- Billing Amount
- Department
- Length_of_stay
- Readmission_Flag
- Severity
- Ward
- Bed_ID
- Nurse_ID
- Emergency_Case
- ICU_Admission
- Discharge_Status
- Hospital_Region
- Occupancy_Status
- Bed_Capacity

---

## 5. Data Preparation

Python and Pandas were used during the data preparation stage.

The preparation process included:

1. Loading the hospital dataset.
2. Inspecting the dataset structure.
3. Checking the number of records and columns.
4. Reviewing column names.
5. Checking missing values.
6. Checking duplicate records.
7. Reviewing data types.
8. Validating important fields.
9. Preparing the dataset for KPI generation and Tableau analysis.

---

## 6. KPI Engineering

The project contains 19 KPIs.

The KPIs were designed to measure different aspects of hospital operations.

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

The KPIs are used to provide quick summaries and support deeper analysis through the dashboard visualizations.

---

## 7. Tableau Analysis

Tableau is used as the primary data visualization platform for the project.

The processed hospital dataset is connected to Tableau and used to create:

- Calculated fields
- KPI cards
- Charts
- Filters
- Tooltips
- Dashboard navigation
- Interactive visualizations

The dashboards are designed to allow users to explore hospital operations interactively.

---

## 8. Dashboard Methodology

The analysis is divided into four dashboards.

### 8.1 Hospital Overview Dashboard

Provides a high-level view of overall hospital performance.

Focus areas:

- Patient volume
- Billing
- Bed occupancy
- Length of stay
- Readmissions
- Discharges
- Hospital trends
- Department distribution

### 8.2 Patient Flow Dashboard

Focuses on patient movement and admission activity.

Focus areas:

- Admissions
- Occupied beds
- Severity
- ICU admissions
- Emergency cases
- Billing per patient
- Discharge status
- Readmissions
- Patient demographics
- Length of stay

### 8.3 Department Analytics Dashboard

Focuses on department-level performance.

Focus areas:

- Patient workload
- Department billing
- Medical conditions
- Admission types
- Readmissions
- Emergency cases
- Average stay
- Test results

### 8.4 Resource Utilization Dashboard

Focuses on hospital resource usage.

Focus areas:

- Nurses
- Beds
- Doctors
- Wards
- Room types
- Staff shifts
- Equipment
- Room occupancy
- ICU admissions
- Length of stay
- Emergency cases

---

## 9. Business Analysis Approach

The project uses the dashboards to answer practical healthcare operations questions.

### Hospital Performance

How is the hospital performing overall?

### Patient Flow

How many patients are being admitted, discharged, or requiring critical care?

### Department Performance

Which departments have higher patient loads or billing activity?

### Resource Utilization

How are beds, staff, wards, rooms, and equipment being utilized?

### Operational Planning

Where can hospital management investigate potential capacity or resource requirements?

---

## 10. Dashboard Interaction

The dashboards use Tableau interactive features to allow users to explore the data.

Users can:

- Apply filters
- Explore charts
- View KPI cards
- Hover over visualizations for details
- Navigate between dashboards
- Compare different hospital operational dimensions

This allows the dashboard to function as an interactive analytical tool rather than a static report.

---

## 11. Validation Methodology

The project includes validation of the generated KPIs and dashboard outputs.

Validation includes:

- Dataset validation
- KPI validation
- Chart validation
- Filter validation
- Dashboard navigation validation
- Visual consistency checks

The final project testing consisted of:

- 26 Test Cases
- 26 Passed
- 0 Failed
- 100% Pass Rate
- 19 KPIs Validated

---

## 12. Final Analytical Output

The methodology produces a complete healthcare analytics solution consisting of:

- Cleaned hospital dataset
- 19 healthcare KPIs
- Four Tableau dashboards
- Interactive filters
- Data visualizations
- Healthcare operational insights
- Project documentation

---

## 13. Methodology Summary

The MedTrack DV methodology converts raw hospital data into analytical information through the following process:

Data
↓
Preparation
↓
Validation
↓
KPI Engineering
↓
Visualization
↓
Dashboard Analysis
↓
Healthcare Operations Insights

The final solution provides a structured view of hospital performance, patient flow, department activity, and resource utilization.