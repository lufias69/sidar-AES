import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Check student_id for different experiments
experiments = ['test_lenient', 'exp_chatgpt_lenient_01', 'test_reproduce_bug']

for exp_id in experiments:
    print(f"\n{exp_id}:")
    print("="*60)
    
    cur.execute('''
        SELECT DISTINCT student_id, student_name 
        FROM grading_results 
        WHERE experiment_id = ?
        ORDER BY student_name
    ''', (exp_id,))
    
    for student_id, student_name in cur.fetchall():
        print(f"  {student_name}: student_id = '{student_id}'")

conn.close()
