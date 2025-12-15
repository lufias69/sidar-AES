import sqlite3

conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

# Get all Gemini tasks
cur.execute("""
    SELECT experiment_id, trial_number, student_id, question_number 
    FROM grading_results 
    WHERE experiment_id LIKE 'exp_gemini%' OR experiment_id LIKE 'test_gemini%'
    ORDER BY experiment_id, trial_number, student_id, question_number
""")
results = cur.fetchall()

print(f"Total Gemini tasks: {len(results)}\n")

# Check each experiment
for exp in ['exp_gemini_lenient_01', 'exp_gemini_lenient_02', 'test_gemini_working']:
    exp_tasks = [r for r in results if r[0] == exp]
    if exp_tasks:
        students = sorted(set(r[2] for r in exp_tasks))
        questions = sorted(set(r[3] for r in exp_tasks))
        print(f"{exp}: {len(exp_tasks)} tasks")
        print(f"  Students: {students}")
        print(f"  Questions: {questions}")
        print()

# Check if test_gemini_working has different data than exp_gemini_lenient_01/02
print("\n" + "="*60)
print("COMPARISON: Are they the same tasks?")
print("="*60)

exp1_tasks = set((r[1], r[2], r[3]) for r in results if r[0] == 'exp_gemini_lenient_01')
exp2_tasks = set((r[1], r[2], r[3]) for r in results if r[0] == 'exp_gemini_lenient_02')
test_tasks = set((r[1], r[2], r[3]) for r in results if r[0] == 'test_gemini_working')

print(f"\nexp_gemini_lenient_01: {len(exp1_tasks)} unique (trial, student, question)")
print(f"exp_gemini_lenient_02: {len(exp2_tasks)} unique (trial, student, question)")
print(f"test_gemini_working: {len(test_tasks)} unique (trial, student, question)")

# Check overlap
overlap_1_test = exp1_tasks & test_tasks
overlap_2_test = exp2_tasks & test_tasks

print(f"\nOverlap exp1 & test: {len(overlap_1_test)} tasks")
print(f"Overlap exp2 & test: {len(overlap_2_test)} tasks")

if len(overlap_1_test) > 0 or len(overlap_2_test) > 0:
    print("\n⚠️ DUPLIKAT DITEMUKAN - test_gemini_working mengulang tasks yang sudah ada!")
else:
    print("\n✅ TIDAK ADA DUPLIKAT - test_gemini_working adalah eksperimen independen")

conn.close()
