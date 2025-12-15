import sqlite3

# Connect to database
conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Get students from one experiment
experiment_id = 'exp_chatgpt_lenient_01'
cur.execute('''
    SELECT DISTINCT student_name 
    FROM grading_results 
    WHERE experiment_id = ? 
    ORDER BY student_name
''', (experiment_id,))

students = cur.fetchall()

print(f"Eksperimen: {experiment_id}")
print(f"Jumlah mahasiswa: {len(students)}")
print("\nDaftar mahasiswa:")
for i, (name,) in enumerate(students, 1):
    print(f"{i}. {name}")

# Count tasks per student
print("\nJumlah pertanyaan per mahasiswa:")
cur.execute('''
    SELECT student_name, COUNT(*) as num_questions
    FROM grading_results 
    WHERE experiment_id = ? 
    GROUP BY student_name
    ORDER BY student_name
''', (experiment_id,))

for name, count in cur.fetchall():
    print(f"  {name}: {count} pertanyaan")

# Total tasks
cur.execute('''
    SELECT COUNT(*) 
    FROM grading_results 
    WHERE experiment_id = ?
''', (experiment_id,))

total = cur.fetchone()[0]
print(f"\nTotal tasks di eksperimen ini: {total}")
print(f"Formula: {len(students)} mahasiswa × 7 pertanyaan = {len(students) * 7}")

conn.close()
