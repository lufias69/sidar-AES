import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# List all production experiments to delete
prod_experiments = [
    'exp_chatgpt_lenient_01', 'exp_chatgpt_lenient_02', 'exp_chatgpt_lenient_03',
    'exp_chatgpt_lenient_04', 'exp_chatgpt_lenient_05', 'exp_chatgpt_lenient_06',
    'exp_chatgpt_lenient_07', 'exp_chatgpt_lenient_08', 'exp_chatgpt_lenient_09',
    'exp_chatgpt_lenient_10', 'exp_chatgpt_zero', 'exp_chatgpt_few',
    'exp_gemini_lenient_01', 'exp_gemini_lenient_02', 'exp_gemini_lenient_03',
    'exp_gemini_lenient_04', 'exp_gemini_lenient_05', 'exp_gemini_lenient_06',
    'exp_gemini_lenient_07', 'exp_gemini_lenient_08', 'exp_gemini_lenient_09',
    'exp_gemini_lenient_10', 'exp_gemini_zero', 'exp_gemini_few',
    'test_reproduce_bug'
]

print("DELETING BUGGY PRODUCTION EXPERIMENTS")
print("="*70)

total_deleted = 0

for exp_id in prod_experiments:
    # Count tasks
    cur.execute('SELECT COUNT(*) FROM grading_results WHERE experiment_id = ?', (exp_id,))
    count = cur.fetchone()[0]
    
    if count > 0:
        # Delete
        cur.execute('DELETE FROM grading_results WHERE experiment_id = ?', (exp_id,))
        total_deleted += count
        print(f"✓ Deleted {exp_id}: {count} tasks")
    else:
        print(f"  Skip {exp_id}: 0 tasks")

# Commit changes
conn.commit()

print(f"\n{'='*70}")
print(f"TOTAL DELETED: {total_deleted} tasks")
print(f"{'='*70}")

# Verify deletion
cur.execute("SELECT COUNT(*) FROM grading_results WHERE experiment_id LIKE 'exp_%'")
remaining = cur.fetchone()[0]
print(f"Remaining production tasks: {remaining}")

conn.close()

print("\n[OK] Database cleaned. Ready to re-run experiments.")
