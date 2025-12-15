#!/usr/bin/env python3
"""Check weighted_score range in database"""

import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

cur.execute("""
    SELECT MIN(weighted_score), MAX(weighted_score), AVG(weighted_score)
    FROM grading_results
    WHERE experiment_id LIKE 'exp_chatgpt_%'
""")

print("weighted_score statistics:")
print(f"  MIN: {cur.fetchone()}")

cur.execute("""
    SELECT weighted_score, COUNT(*) 
    FROM grading_results
    WHERE experiment_id LIKE 'exp_chatgpt_lenient_%'
    GROUP BY weighted_score
    ORDER BY weighted_score DESC
    LIMIT 20
""")

print("\nTop weighted_score values:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} tasks")

conn.close()
