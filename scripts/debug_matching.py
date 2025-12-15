import sqlite3
import pandas as pd

conn = sqlite3.connect('results/grading_results.db')

# Check student IDs
df = pd.read_sql_query("""
    SELECT DISTINCT student_id 
    FROM grading_results 
    WHERE experiment_id = 'exp_chatgpt_lenient_01' 
    ORDER BY student_id
""", conn)

print("Student IDs in database:")
print(df['student_id'].tolist())

# Check gold standard files
from pathlib import Path
gold_dir = Path('results/gold_standard')
files = sorted(gold_dir.glob('*.json'))
print(f"\nGold standard files ({len(files)}):")
for f in files:
    print(f"  {f.name}")

# Check sample mapping
import json
sample_file = files[0]
with open(sample_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"\nSample gold standard file: {sample_file.name}")
    print(f"  student_name: {data['student_name']}")
    print(f"  Number of questions: {len(data['questions'])}")
    if data['questions']:
        print(f"  First question number: {data['questions'][0]['question'].split('.')[0].strip()}")

conn.close()
