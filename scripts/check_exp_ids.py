import sqlite3
conn = sqlite3.connect('results/grading_results.db')
df = conn.execute("SELECT DISTINCT experiment_id FROM grading_results WHERE status = 'completed' ORDER BY experiment_id").fetchall()
for row in df:
    print(row[0])
