import sqlite3

conn = sqlite3.connect('results/grading_results.db')
c = conn.cursor()

c.execute("""
    SELECT DISTINCT student_id, student_name 
    FROM grading_results 
    WHERE experiment_id = 'exp_chatgpt_lenient_01' 
    ORDER BY student_id
""")

rows = c.fetchall()
print("Database mapping:")
for r in rows:
    print(f"  {r[0]}: {r[1]}")

conn.close()

# Now check gold standard
import json
from pathlib import Path

gold_dir = Path('results/gold_standard')
print("\nGold standard mapping:")
for file in sorted(gold_dir.glob('*.json')):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        file_prefix = file.stem.split('_Mahasiswa')[0]  # e.g., "student_01"
        print(f"  {file_prefix}: {data['student_name']}")

print("\nMapping analysis:")
print("Database has: student_01, student_02, student_03, student_05, student_08, student_12, student_13, student_14, student_15, student_16")
print("Gold has: student_00, student_01, student_02, student_04, student_07, student_11, student_12, student_13, student_14, student_15")
print("\nThey match by STUDENT NAME, not by student_id number!")
