import pandas as pd
import numpy as np
import os

def generate_hospital_kpis():
    print("="*60)
    print(" HOSPITAL KPI ENGINEERING & DASHBOARD PLANNING ")
    print("="*60)
    
    # 1. Load the cleaned dataset
    if os.path.exists('hospital_cleaned.csv'):
        df = pd.read_csv('hospital_cleaned.csv')
        print("[✓] Cleaned dataset loaded successfully.")
    else:
        # Search for any file with 'hospital_cleaned' in the name
        matched_files = [f for f in os.listdir('.') if 'hospital_cleaned' in f and f.endswith('.csv')]
        if matched_files:
            df = pd.read_csv(matched_files[0])
            print(f"[✓] Cleaned dataset loaded successfully from: {matched_files[0]}")
        else:
            print("[X] Error: Could not find hospital_cleaned.csv in this folder!")
            return

    # Convert date columns to datetime objects
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
    df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

    # 2. KPI CALCULATIONS & ENGINEERING
    
    # KPI 1: Total Admissions
    total_admissions = df['Admission_ID'].nunique()
    
    # KPI 2: Occupancy Rate (%)
    avg_occupancy_rate = df['Occupancy_Rate_%'].mean()
    
    # KPI 3: Average Length of Stay (Days)
    avg_los = df['Length_of_Stay_Days'].mean()
    
    # KPI 4: Readmission Rate (%)
    df = df.sort_values(by=['Patient_ID', 'Admission_Date'])
    df['Is_Readmission'] = df.duplicated(subset=['Patient_ID'], keep='first').astype(int)
    readmission_rate = (df['Is_Readmission'].sum() / len(df)) * 100
    
    # KPI 5: Bed Utilization Rate (%)
    df['Bed_Utilization_Rate'] = (df['Occupied_Beds'] / df['Total_Beds']) * 100
    avg_bed_utilization = df['Bed_Utilization_Rate'].mean()
    
    # KPI 6: Department Efficiency Score
    dept_metrics = df.groupby('Department').agg(
        Total_Admissions=('Admission_ID', 'count'),
        Avg_LOS=('Length_of_Stay_Days', 'mean'),
        Avg_Occupancy=('Occupancy_Rate_%', 'mean')
    ).reset_index()
    
    dept_metrics['Efficiency_Score'] = ((dept_metrics['Avg_Occupancy'] / dept_metrics['Avg_LOS']) * np.log1p(dept_metrics['Total_Admissions']))
    max_score = dept_metrics['Efficiency_Score'].max()
    min_score = dept_metrics['Efficiency_Score'].min()
    dept_metrics['Department_Efficiency_Score'] = (((dept_metrics['Efficiency_Score'] - min_score) / (max_score - min_score)) * 40 + 60).round(2)
    
    df = df.merge(dept_metrics[['Department', 'Department_Efficiency_Score']], on='Department', how='left')

    # 3. TERMINAL REPORT DISPLAY
    print("\n" + "-"*45)
    print(" METRIC RESULTS (OVERALL SUMMARY)")
    print("-"*45)
    print(f" • Total Admissions          : {total_admissions:,}")
    print(f" • Average Occupancy Rate    : {avg_occupancy_rate:.2f}%")
    print(f" • Average Length of Stay    : {avg_los:.2f} Days")
    print(f" • Readmission Rate          : {readmission_rate:.2f}%")
    print(f" • Bed Utilization Rate      : {avg_bed_utilization:.2f}%")
    print("-"*45)
    
    print("\nDEPARTMENT PERFORMANCE & EFFICIENCY SCORE:")
    print(dept_metrics[['Department', 'Total_Admissions', 'Avg_LOS', 'Avg_Occupancy', 'Department_Efficiency_Score']].to_string(index=False))
    print("-"*60)
    
    # 4. EXPORT OPTIMIZED TABLEAU DATASET
    try:
        with pd.ExcelWriter('hospital_final_dataset.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='KPI_Final_Dataset', index=False)
            dept_metrics.to_excel(writer, sheet_name='Department_KPI_Summary', index=False)
        print("[✓] Optimization Complete! 'hospital_final_dataset.xlsx' generated.")
    except Exception as e:
        print(f"[X] Export Error: {e}")
    print("="*60)

if __name__ == "__main__":
    generate_hospital_kpis()