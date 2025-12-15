import sqlite3
from datetime import datetime

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Get earliest and latest timestamps for test vs production
experiments = {
    'test': ['test_01', 'test_lenient', 'test_fewshot'],
    'prod': ['exp_chatgpt_lenient_01', 'exp_gemini_lenient_01']
}

for exp_type, exp_list in experiments.items():
    print(f"\n{'='*70}")
    print(f"{exp_type.upper()} EXPERIMENTS")
    print(f"{'='*70}")
    
    for exp_id in exp_list:
        cur.execute('''
            SELECT MIN(timestamp), MAX(timestamp), COUNT(*)
            FROM grading_results
            WHERE experiment_id = ?
        ''', (exp_id,))
        
        min_time, max_time, count = cur.fetchone()
        
        if min_time:
            print(f"\n{exp_id}:")
            print(f"  Started: {min_time}")
            print(f"  Ended: {max_time}")
            print(f"  Tasks: {count}")

conn.close()
