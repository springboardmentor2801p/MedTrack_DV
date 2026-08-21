# MedTrack DV
## Hospital Operations & Patient Analytics Dashboard

<p align="center">
  <b>Data Engineering • KPI Analytics • Data Visualization</b>
</p>

---

## 📌 Project Overview

**MedTrack DV** is a hospital operations and patient analytics project designed to transform raw hospital data into meaningful business insights through data processing, KPI engineering, and interactive Tableau dashboards.

The project follows a structured data workflow that includes data collection, integration, cleaning, KPI generation, processed datasets, and visualization.

The final dashboards provide an interactive view of hospital admissions, patient flow, department performance, disease patterns, readmissions, and resource utilization.

---

## 🎯 Project Objectives

- Analyze hospital admission patterns and trends
- Understand patient and department-level performance
- Develop meaningful healthcare KPIs
- Analyze admission types and readmission patterns
- Identify diseases with the highest number of admissions
- Analyze ward and resource utilization
- Transform raw datasets into analysis-ready data
- Build interactive dashboards for data-driven decision-making

---

## 🏗️ Project Architecture

```text
                    Raw Hospital Data
                           │
                           ▼
              Data Collection & Integration
                           │
                           ▼
                    Data Cleaning
                           │
                           ▼
                  KPI Engineering
                           │
                           ▼
                  Processed Datasets
                           │
                           ▼
                    KPI Datasets
                           │
                           ▼
                 Tableau Dashboards
                           │
                           ▼
              Hospital Analytics & Insights

## Repository structure

MedTrack_DV/
│
├── Code/
│   ├── 01_Data_Collection_and_Integration.ipynb
│   └── KPI Engineering.ipynb
│
├── Dashboard/
│   └── MedTrack_DV.twbx
│
├── Data Set/
│   └── Raw and source hospital datasets
│
├── Docs/
│   ├── Dashboard Testing Report
│   ├── Final Project Documentation
│   └── Final QA Testing Report
│
├── KPI_Data/
│   ├── KPI_Summary.csv
│   ├── Department_Admissions.csv
│   ├── Monthly_Admissions.csv
│   ├── Readmission_Summary.csv
│   ├── Disease_Analysis.csv
│   └── Ward_Utilization.csv
│
├── Processed_Data/
│   ├── Fact_Admissions_Clean.csv
│   ├── Dim_Doctor.csv
│   ├── Dim_Ward.csv
│   └── bed.csv
│
├── .gitignore
└── README.md
🛠️ Technologies & Tools
| Technology           | Purpose                                   |
| -------------------- | ----------------------------------------- |
| **Python**           | Data processing and analysis              |
| **Pandas**           | Data cleaning and transformation          |
| **Jupyter Notebook** | Data engineering and KPI development      |
| **Tableau**          | Interactive dashboard development         |
| **CSV**              | Data storage and exchange                 |
| **Git & GitHub**     | Version control and project collaboration |

🔄 Data Processing

The project processes hospital datasets through multiple stages:

1. Data Collection & Integration

Raw hospital datasets are collected and integrated to create a structured data foundation.

2. Data Cleaning

The datasets are cleaned and prepared for analytical use.

3. KPI Engineering

Key performance indicators are generated to measure hospital operations and patient-related metrics.

4. Data Preparation

Cleaned fact and dimension datasets are stored in the Processed_Data directory.

5. KPI Data Generation

Analytical datasets are generated and stored in the KPI_Data directory for dashboard development.

📊 Dashboard Modules

The Tableau workbook contains multiple analytical views.

🏥 Hospital Overview

Provides a high-level summary of hospital operations, including:

Total Admissions
Total Patients
Total Departments
Total Wards
Average Length of Stay
Readmission Rate
Department Admissions
Monthly Admissions Trend
Admission Type Distribution
Readmission Summary
Top Diseases by Admissions
🏢 Department Analytics

Provides department-level analysis of hospital admissions and performance.

👥 Patient Flow Analytics

Provides insights into patient admission and flow patterns.

🛏️ Resource Utilization

Provides analysis related to hospital wards and resource utilization.

📈 Key Analytical Areas

The project focuses on:

Hospital Admissions
Patient Analytics
Department Performance
Disease Analysis
Readmission Analysis
Admission Type Analysis
Monthly Trends
Ward Utilization
Hospital KPIs
📋 Project Deliverables

The repository contains:

Data collection and integration notebooks
KPI engineering notebook
Raw datasets
Processed datasets
KPI datasets
Tableau dashboard workbook
Dashboard testing documentation
Final project documentation
QA testing report
🚀 How to Use
1. Clone the repository
git clone <repository-url>
2. Navigate to the project
cd MedTrack_DV
3. Explore the data

Review the datasets available in:

Data Set/
Processed_Data/
KPI_Data/
4. Review the notebooks

Open the notebooks in:

Code/

using Jupyter Notebook or JupyterLab.

5. Explore the dashboard

Open the Tableau workbook:

Dashboard/MedTrack_DV.twbx

using Tableau Desktop or Tableau Public.

📌 Project Outcome

MedTrack DV provides a structured approach for converting hospital operational data into actionable analytical insights.

The combination of data engineering, KPI development, and interactive visualization enables users to explore hospital performance and identify important trends across admissions, patients, departments, diseases, readmissions, and resource utilization.

👩‍💻 Project Information

Project: MedTrack DV
Domain: Healthcare Analytics
Focus: Hospital Operations & Patient Analytics
Tools: Python, Pandas, Jupyter Notebook, Tableau, Git & GitHub

📄 Documentation

Detailed project documentation, dashboard testing results, and QA testing reports are available in the:

Docs/

directory.