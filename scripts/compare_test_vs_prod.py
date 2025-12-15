import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Compare test experiments vs production experiments
test_experiments = ['test_01', 'test_lenient', 'test_fewshot']
prod_experiments = ['exp_chatgpt_lenient_01', 'exp_chatgpt_lenient_02']

print("="*70)
print("TEST EXPERIMENTS (yang berhasil dengan 70 tasks)")
print("="*70)

for exp_id in test_experiments:
    cur.execute('''
        SELECT DISTINCT student_name 
        FROM grading_results 
        WHERE experiment_id = ?
        ORDER BY student_name
    ''', (exp_id,))
    
    students = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT COUNT(*) FROM grading_results WHERE experiment_id = ?', (exp_id,))
    count = cur.fetchone()[0]
    
    print(f"\n{exp_id}: {count} tasks, {len(students)} students")
    if len(students) <= 10:
        print(f"  Students: {students}")

print("\n" + "="*70)
print("PRODUCTION EXPERIMENTS (yang cuma 7 tasks)")
print("="*70)

for exp_id in prod_experiments:
    cur.execute('''
        SELECT DISTINCT student_name 
        FROM grading_results 
        WHERE experiment_id = ?
        ORDER BY student_name
    ''', (exp_id,))
    
    students = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT COUNT(*) FROM grading_results WHERE experiment_id = ?', (exp_id,))
    count = cur.fetchone()[0]
    
    print(f"\n{exp_id}: {count} tasks, {len(students)} students")
    if len(students) <= 10:
        print(f"  Students: {students}")

conn.close()
