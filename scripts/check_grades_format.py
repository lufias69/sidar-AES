import sqlite3
import json

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

cur.execute("""
    SELECT grades 
    FROM grading_results 
    WHERE experiment_id = 'exp_chatgpt_lenient_01' 
    AND student_name = 'Mahasiswa 1' 
    AND question_number = 1 
    LIMIT 1
""")

row = cur.fetchone()
if row:
    grades_dict = json.loads(row[0])
    print("Grades JSON structure:")
    print(json.dumps(grades_dict, indent=2))

conn.close()
