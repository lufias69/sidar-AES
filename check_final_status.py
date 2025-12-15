import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

print("\n" + "="*80)
print("FINAL DATABASE STATUS")
print("="*80 + "\n")

# Total by model and strategy
result = cur.execute("""
    SELECT model, strategy, 
           COUNT(DISTINCT experiment_id) as experiments,
           COUNT(*) as total_gradings,
           SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
           SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) as failed
    FROM grading_results 
    GROUP BY model, strategy
    ORDER BY model, strategy
""").fetchall()

print("Model    | Strategy  | Experiments | Total | Completed | Failed")
print("-" * 75)
for r in result:
    print(f"{r[0]:8} | {r[1]:9} | {r[2]:11} | {r[3]:5} | {r[4]:9} | {r[5]:6}")

# Overall summary
overall = cur.execute("""
    SELECT COUNT(DISTINCT experiment_id) as exp,
           COUNT(*) as total,
           SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
           SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) as failed
    FROM grading_results
""").fetchone()

print("\n" + "="*80)
print("OVERALL SUMMARY")
print("="*80)
print(f"Total Experiments: {overall[0]}")
print(f"Total Gradings: {overall[1]}")
print(f"Completed: {overall[2]} ({overall[2]/overall[1]*100:.1f}%)")
print(f"Failed: {overall[3]} ({overall[3]/overall[1]*100:.2f}%)")
print("="*80 + "\n")

conn.close()
