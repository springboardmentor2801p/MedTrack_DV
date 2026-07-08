import pandas as pd

# Load hospital datasets
patient_df = pd.read_excel('Sunrise_Hospital_Dataset Reall.xlsx', sheet_name='Patient_Admissions')
dept_df = pd.read_excel('Sunrise_Hospital_Dataset Reall.xlsx', sheet_name='Department_Resources')
ops_df = pd.read_excel('Sunrise_Hospital_Dataset Reall.xlsx', sheet_name='Hospital_Operations')

# Integrate datasets
hospital_raw_data = patient_df.merge(dept_df, on='Department', how='left')
hospital_raw_data = hospital_raw_data.merge(ops_df, on='Department', how='left')

# Save integrated dataset
hospital_raw_data.to_csv('hospital_raw_data.csv', index=False)

print('Dataset integration completed successfully.')
print(f'Total records: {len(hospital_raw_data)}')
print(f'Completeness: {(1 - hospital_raw_data.isnull().sum().sum()/(hospital_raw_data.shape[0]*hospital_raw_data.shape[1]))*100:.2f}%')
