import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='grading_results'")
schema = cur.fetchone()[0]

print("DATABASE SCHEMA:")
print("="*70)
print(schema)

conn.close()
