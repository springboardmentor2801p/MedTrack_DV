# MedTrack DV – KPI Definitions

## 1. KPI Overview

MedTrack DV contains 19 Key Performance Indicators (KPIs) across four Tableau dashboards.

The KPIs are designed to provide a quick view of hospital performance, patient flow, department performance, and resource utilization.

All KPIs were created using Tableau Calculated Fields.

---

## 2. Hospital Overview KPIs

### 2.1 Total Patients

- Value: 2,238
- Definition: Total number of patient records represented in the dataset.
- Purpose: Measures the overall patient volume.
- Dashboard: Hospital Overview Dashboard

### 2.2 Total Billing

- Value: $56,610,270
- Definition: Total billing amount across the patient records.
- Purpose: Provides an overall view of the billing value represented in the dataset.
- Dashboard: Hospital Overview Dashboard

### 2.3 Bed Occupancy Rate

- Value: 80.83%
- Definition: Percentage of hospital bed capacity that is occupied.
- Purpose: Helps evaluate hospital capacity utilization and bed demand.
- Dashboard: Hospital Overview Dashboard

### 2.4 Average Length of Stay

- Value: 15.53 Days
- Definition: Average number of days patients stay in the hospital.
- Purpose: Helps analyze patient stay duration and hospital resource utilization.
- Dashboard: Hospital Overview Dashboard

### 2.5 Readmission Rate

- Value: 9.12%
- Definition: Percentage of patient records identified as readmissions.
- Purpose: Helps monitor the frequency of patient readmissions.
- Dashboard: Hospital Overview Dashboard

### 2.6 Discharge Rate

- Value: 34.1%
- Definition: Percentage of patient records associated with the discharge status used in the dashboard calculation.
- Purpose: Helps understand patient discharge activity.
- Dashboard: Hospital Overview Dashboard

---

## 3. Patient Flow KPIs

### 3.1 Total Admissions

- Value: 2,238
- Definition: Total number of patient admission records.
- Purpose: Measures overall hospital admission volume.
- Dashboard: Patient Flow Dashboard

### 3.2 Occupied Beds

- Value: 1,809
- Definition: Number of beds identified as occupied in the dataset.
- Purpose: Helps monitor bed usage and hospital capacity.
- Dashboard: Patient Flow Dashboard

### 3.3 Severe Cases %

- Value: 23.95%
- Definition: Percentage of patient cases classified as severe.
- Purpose: Helps understand the proportion of patients requiring higher levels of clinical attention.
- Dashboard: Patient Flow Dashboard

### 3.4 ICU Admissions

- Value: 339
- Definition: Number of patient records identified as ICU admissions.
- Purpose: Helps monitor critical-care demand and ICU utilization.
- Dashboard: Patient Flow Dashboard

### 3.5 Emergency Cases

- Value: 472
- Definition: Number of patient records identified as emergency cases.
- Purpose: Helps evaluate emergency-care demand.
- Dashboard: Patient Flow Dashboard

### 3.6 Average Billing per Patient

- Value: $25,295
- Definition: Average billing amount associated with each patient record.
- Purpose: Provides an overview of average billing per patient.
- Dashboard: Patient Flow Dashboard

---

## 4. Department Analytics KPIs

### 4.1 Total Departments

- Value: 6
- Definition: Number of departments represented in the dataset.
- Purpose: Provides an overview of the departments included in the analysis.
- Dashboard: Department Analytics Dashboard

### 4.2 Average Patients per Department

- Value: 373
- Definition: Average number of patients represented per department.
- Purpose: Helps compare patient workload across departments.
- Dashboard: Department Analytics Dashboard

### 4.3 Average Billing per Department

- Value: $9,435,045
- Definition: Average billing amount represented per department.
- Purpose: Helps compare billing activity across departments.
- Dashboard: Department Analytics Dashboard

---

## 5. Resource Utilization KPIs

### 5.1 Total Nurses

- Value: 50
- Definition: Total number of nurses represented in the dataset.
- Purpose: Provides an overview of nursing resources.
- Dashboard: Resource Utilization Dashboard

### 5.2 Available Beds

- Value: 429
- Definition: Number of beds identified as available.
- Purpose: Helps monitor remaining hospital bed capacity.
- Dashboard: Resource Utilization Dashboard

### 5.3 Average Patients per Doctor

- Value: 1.015
- Definition: Average number of patient records associated with each doctor.
- Purpose: Provides an indication of the patient workload represented per doctor.
- Dashboard: Resource Utilization Dashboard

### 5.4 Total Wards

- Value: 5
- Definition: Number of wards represented in the dataset.
- Purpose: Provides an overview of the hospital ward structure represented in the data.
- Dashboard: Resource Utilization Dashboard

---

## 6. KPI Summary

| # | KPI | Dashboard | Value |
|---:|---|---|---:|
| 1 | Total Patients | Hospital Overview | 2,238 |
| 2 | Total Billing | Hospital Overview | $56,610,270 |
| 3 | Bed Occupancy Rate | Hospital Overview | 80.83% |
| 4 | Average Length of Stay | Hospital Overview | 15.53 Days |
| 5 | Readmission Rate | Hospital Overview | 9.12% |
| 6 | Discharge Rate | Hospital Overview | 34.1% |
| 7 | Total Admissions | Patient Flow | 2,238 |
| 8 | Occupied Beds | Patient Flow | 1,809 |
| 9 | Severe Cases % | Patient Flow | 23.95% |
| 10 | ICU Admissions | Patient Flow | 339 |
| 11 | Emergency Cases | Patient Flow | 472 |
| 12 | Average Billing per Patient | Patient Flow | $25,295 |
| 13 | Total Departments | Department Analytics | 6 |
| 14 | Average Patients per Department | Department Analytics | 373 |
| 15 | Average Billing per Department | Department Analytics | $9,435,045 |
| 16 | Total Nurses | Resource Utilization | 50 |
| 17 | Available Beds | Resource Utilization | 429 |
| 18 | Average Patients per Doctor | Resource Utilization | 1.015 |
| 19 | Total Wards | Resource Utilization | 5 |

---

## 7. KPI Categories

The 19 KPIs are grouped into four operational areas:

### Hospital Performance

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

### Department Performance

- Total Departments
- Average Patients per Department
- Average Billing per Department

### Resource Utilization

- Total Nurses
- Available Beds
- Average Patients per Doctor
- Total Wards

---

## 8. KPI Purpose

The KPIs provide a concise summary of important hospital operations and support deeper analysis through Tableau charts and interactive dashboards.

They help users understand:

- Patient volume
- Hospital billing
- Bed occupancy
- Patient stay duration
- Readmissions
- Discharge activity
- Patient admissions
- Critical-care demand
- Emergency-care demand
- Department workload
- Department billing
- Staff resources
- Bed availability
- Ward utilization

---

## 9. KPI Development

The KPIs were developed as part of the MedTrack DV healthcare analytics workflow.

The KPI development process involved:

1. Preparing the hospital dataset.
2. Identifying relevant healthcare fields.
3. Creating calculated fields in Tableau.
4. Building KPI cards.
5. Validating KPI values.
6. Integrating KPIs into the four dashboards.

---

## 10. KPI Validation

The project included validation of all 19 KPIs.

Testing results:

- Total KPIs Validated: 19
- Test Cases Executed: 26
- Passed: 26
- Failed: 0
- Pass Rate: 100%

The validated KPIs are used throughout the four Tableau dashboards to support healthcare operations analysis.