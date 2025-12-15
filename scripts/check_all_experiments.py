import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Get all production experiments
cur.execute('''
    SELECT DISTINCT experiment_id 
    FROM grading_results 
    WHERE experiment_id LIKE 'exp_%'
    ORDER BY experiment_id
''')

experiments = [row[0] for row in cur.fetchall()]

print(f"Total eksperimen produksi: {len(experiments)}\n")

for exp_id in experiments:
    # Count students
    cur.execute('''
        SELECT DISTINCT student_name 
        FROM grading_results 
        WHERE experiment_id = ?
    ''', (exp_id,))
    students = [row[0] for row in cur.fetchall()]
    
    # Count tasks
    cur.execute('''
        SELECT COUNT(*) 
        FROM grading_results 
        WHERE experiment_id = ?
    ''', (exp_id,))
    task_count = cur.fetchone()[0]
    
    print(f"{exp_id}:")
    print(f"  Mahasiswa: {', '.join(students)}")
    print(f"  Jumlah tasks: {task_count}")
    print()

conn.close()
