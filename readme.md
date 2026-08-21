# MedTrack_DV — Hospital Operations & Patient Analytics Dashboard

A Power BI-based analytics suite for hospital operations, patient flow, department performance, and resource utilization — built as part of the **Infosys Springboard Internship 2026**.

---

## Overview

**MedTrack_DV** turns raw hospital operational data into a set of interactive Power BI dashboards. It walks the full pipeline — data collection → cleaning → KPI engineering → dashboard development — and delivers four connected views of how a hospital is performing.

**Dashboards included:**
1. Executive Hospital Performance
2. Patient Flow Analytics
3. Department Analytics
4. Resource Utilization

## Dashboard Previews



**1. Executive Hospital Performance**
<img width="1305" height="737" alt="Executive Hospital Performance dashboard" src="https://github.com/user-attachments/assets/d2b4761c-932d-4aae-8943-1c224f2e04d0" />


**2. Patient Flow Analytics**
<img width="1306" height="738" alt="Patient Flow Analytics dashboard" src="https://github.com/user-attachments/assets/3c516fa7-6724-4d4b-a18d-2eb924970f9b" />


**3. Department Analytics**
<img width="1309" height="737" alt="Department Analytics dashboard" src="https://github.com/user-attachments/assets/f06e43e6-8c6f-488f-a52a-a3266c479b4e" />


**4. Resource Utilization**
<img width="1307" height="740" alt="Resource Utilization dashboard" src="https://github.com/user-attachments/assets/eb787b30-01bb-40cb-8478-4cbd4964b6a5" />

## Objectives

- Analyze hospital admissions and patient activity
- Monitor key hospital performance indicators (KPIs)
- Understand admission, discharge, and readmission patterns
- Compare departmental performance and patient volumes
- Track doctors, nurses, and staffing by department
- Monitor beds, wards, rooms, and equipment utilization
- Provide interactive, filterable dashboards for operational decision-making

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data collection, cleaning, and transformation |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical data processing |
| Microsoft Excel | Storage of cleaned and final datasets |
| Microsoft Power BI | Dashboard development and visualization |
| DAX | KPI and calculated measure development |
| Git & GitHub | Version control and project management |
| Microsoft Word | Documentation and testing reports |

---

## Dashboard Suite

### 1. Executive Hospital Performance
Total Patients · Total Admissions · Total Revenue · Average Length of Stay · Occupancy Rate · Bed Utilization Rate · Monthly Admission Trends · Revenue Trends · Readmission Trends · Department-wise Analysis

### 2. Patient Flow Analytics
Admissions & Discharges · Average Length of Stay · Readmission Analysis · Admissions/Discharges by Department · Patient Distribution by Gender & Age Group · Admissions vs Discharges

### 3. Department Analytics
Doctors & Nurses by Department · Patient Volume by Department · Department Efficiency · Equipment Count · Rooms by Department

### 4. Resource Utilization
Total Beds, Wards, Rooms · Bed Occupancy · Equipment Type Distribution & Status · Staff Allocation · Equipment Usage Hours · Maintenance Flag Distribution

---

## Key KPIs

- Total Admissions
- Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Bed Utilization Rate
- Department Efficiency

---

## Data Preparation

Processed with Python and Pandas before dashboard development:

- Removed duplicate records
- Handled missing values
- Standardized department names
- Corrected data formats and validated key fields
- Assembled the cleaned data into an Excel workbook used as the Power BI data source

## Dashboard Development

Built in Microsoft Power BI using KPI cards, bar/column/line charts, donut charts, treemaps, and interactive slicers (department, date, gender, and equipment filters). DAX measures calculate each KPI dynamically.

## Testing & Validation

A separate **Dashboard Testing Report** covers KPI calculation validation, dashboard functionality, filter behavior, interactivity, navigation, visual consistency, and data accuracy — completed before final submission.

---

## Getting Started

**Prerequisites**
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free) to open and explore the `.pbix` file
- Python 3.x with `pandas` and `numpy` if you want to re-run the data pipeline

**Steps**
1. Clone the repository
   ```bash
   git clone https://github.com/jettisrineshreddy-cpu/MedTrack_DV.git
   ```
2. Open `Hospital_Management_Analytics.pbix` in Power BI Desktop to explore the dashboards directly, **or**
3. Re-run the pipeline from source:
   ```bash
   python 00_Data_Collection.ipynb      # data collection
   python generate_hospital_kpis.py     # KPI generation from hospital_cleaned_data.xlsx
   ```
4. Refresh the data source in Power BI to point at your generated `hospital_final_dataset.xlsx`

## Data Source

14 of the 16 source tables come from the open-source [Hospital Management System dataset](https://www.kaggle.com/datasets/mshamoonbutt/hospital-management-system/data?select=Hospital+Management+System.xlsx) on Kaggle. The remaining 2 — `equipment` and `equipment_usage` — are synthetically generated to support the Resource Utilization dashboard's equipment tracking metrics.

---

## Repository Structure

```text
MedTrack_DV/
│
├── 00_Data_Collection.ipynb
├── data_cleaning.zip
├── hospital_raw_data.xlsx
├── hospital_cleaned_data.xlsx
├── hospital_final_dataset.xlsx
├── generate_hospital_kpis.py
├── Hospital_Management_Analytics.pbix
├── Dashboard_Testing_Report.pdf
├── Final_Project_Documentation_Enhanced.pdf
├── storyboard1.1.pdf
├── README.md
└── LICENSE
```

## Project Workflow

```text
Healthcare Data
      ↓
Data Collection
      ↓
Data Cleaning & Transformation
      ↓
KPI Engineering
      ↓
Power BI Data Model
      ↓
Dashboard Development
      ↓
Dashboard Integration
      ↓
Testing & Validation
      ↓
Final Documentation
```

---

## Outcome

A centralized BI solution combining **Hospital Performance + Patient Flow + Department Analytics + Resource Utilization** into four interactive Power BI dashboards, supporting data-driven hospital operations decisions.

## Internship

- **Program:** Infosys Springboard Internship
- **Year:** 2026
- **Domain:** Healthcare Analytics & Business Intelligence
- **Platform:** Microsoft Power BI *(originally scoped for Tableau; switched to Power BI with mentor approval)*

## Author

**Jetti Srinesh Reddy**
B.Tech – Artificial Intelligence, Amrita Vishwa Vidyapeetham, Amaravati

## License

This project is licensed under the [MIT License](LICENSE).
