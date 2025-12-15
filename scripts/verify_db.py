import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Check all production experiments
experiments = ['exp_chatgpt_lenient_01', 'exp_chatgpt_lenient_02', 'exp_gemini_lenient_01']

for exp_id in experiments:
    cur.execute('''
        SELECT DISTINCT student_name 
        FROM grading_results 
        WHERE experiment_id = ?
        ORDER BY student_name
    ''', (exp_id,))
    
    students = [row[0] for row in cur.fetchall()]
    
    cur.execute('''
        SELECT COUNT(*) 
        FROM grading_results 
        WHERE experiment_id = ?
    ''', (exp_id,))
    
    count = cur.fetchone()[0]
    
    print(f"\n{exp_id}:")
    print(f"  Students ({len(students)}): {students}")
    print(f"  Total tasks: {count}")

conn.close()
