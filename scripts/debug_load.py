"""
Debug script to check what run_experiment.py actually processes
"""
import pandas as pd
import os

def load_student_data(excel_path):
    """Load student answers from Excel file."""
    print(f"[DEBUG] Loading data from: {excel_path}")
    
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    df = pd.read_excel(excel_path)
    print(f"[DEBUG] Initial dataframe: {len(df)} rows")
    
    # Use 'Nama' for student name column
    if 'Nama' not in df.columns:
        raise ValueError(f"Column 'Nama' not found. Available columns: {df.columns.tolist()}")
    
    # Filter to selected students if file exists
    selected_file = "selected_students.txt"
    if os.path.exists(selected_file):
        with open(selected_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        
        selected_names = [line.split(',')[1] for line in lines if ',' in line]
        print(f"[DEBUG] Selected names: {selected_names}")
        
        df = df[df['Nama'].isin(selected_names)].copy()
        print(f"[DEBUG] After filtering: {len(df)} rows")
        print(f"[DEBUG] Filtered names: {df['Nama'].tolist()}")
    else:
        print(f"[DEBUG] Using all {len(df)} students")
    
    return df

# Test the function
excel_path = "data/Jawaban/jawaban UTS  Capstone Project.xlsx"
df = load_student_data(excel_path)

print("\n" + "="*60)
print("FINAL DATAFRAME:")
print("="*60)
print(f"Total rows: {len(df)}")
print(f"Students: {df['Nama'].tolist()}")

print("\n" + "="*60)
print("ITERATION TEST:")
print("="*60)
for idx, row in df.iterrows():
    print(f"Row {idx}: {row['Nama']}")
