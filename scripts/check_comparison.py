import sqlite3
import json
import pandas as pd

# Get ChatGPT grades for Mahasiswa 1
conn = sqlite3.connect('results/grading_results.db')
cur = conn.cursor()

print("\n" + "="*70)
print("COMPARISON: ChatGPT vs Gold Standard")
print("="*70)

# Get ChatGPT grades from exp_chatgpt_lenient_01
cur.execute("""
    SELECT student_name, question_number, weighted_score 
    FROM grading_results 
    WHERE experiment_id = 'exp_chatgpt_lenient_01' 
    AND student_name = 'Mahasiswa 1'
    ORDER BY question_number
""")

chatgpt_grades = {}
def score_to_grade(score):
    if score >= 85: return 'A'
    elif score >= 70: return 'B'
    elif score >= 55: return 'C'
    elif score >= 40: return 'D'
    else: return 'E'

for row in cur.fetchall():
    q_num = row[1]
    score = row[2]
    chatgpt_grades[q_num] = score_to_grade(score)

conn.close()

# Load gold standard from JSON
try:
    import glob
    gold_files = glob.glob('results/gold_standard/*.json')
    
    # Find Mahasiswa 1 gold standard
    gold_file = None
    for f in gold_files:
        if 'Mahasiswa_1' in f:
            gold_file = f
            break
    
    if not gold_file:
        print("\n⚠️ Gold standard for Mahasiswa 1 not found")
    else:
        with open(gold_file, 'r', encoding='utf-8') as f:
            gold_data = json.load(f)
        
        print("\nMahasiswa 1 - Grade Comparison:")
        print("-" * 70)
        print(f"{'Question':<12} {'ChatGPT':<15} {'Gold Standard':<15} {'Match':<10}")
        print("-" * 70)
        
        for q in range(1, 8):
            chatgpt = chatgpt_grades.get(q, 'N/A')
            
            # Find gold standard for this question
            gold = 'N/A'
            for item in gold_data.get('grading_results', []):
                if item.get('question_number') == q:
                    gold_score = item.get('weighted_score', 0)
                    gold = score_to_grade(gold_score)
                    break
            
            match = '✓' if chatgpt == gold else '✗'
            print(f"Q{q:<11} {chatgpt:<15} {gold:<15} {match:<10}")
        
        # Calculate overall match rate
        matches = sum(1 for q in range(1, 8) if chatgpt_grades.get(q) == next((score_to_grade(item.get('weighted_score', 0)) for item in gold_data.get('grading_results', []) if item.get('question_number') == q), None))
        match_rate = matches / 7 * 100
        print("-" * 70)
        print(f"Match Rate: {matches}/7 ({match_rate:.1f}%)")
    
    # Check all 10 trials for Q1 to see if identical
    print("\n" + "="*70)
    print("CHECKING CONSISTENCY: All 10 trials for Mahasiswa 1, Q1")
    print("="*70)
    
    conn = sqlite3.connect('results/grading_results.db')
    cur = conn.cursor()
    
    cur.execute("""
        SELECT experiment_id, weighted_score 
        FROM grading_results 
        WHERE experiment_id LIKE 'exp_chatgpt_lenient_%' 
        AND student_name = 'Mahasiswa 1'
        AND question_number = 1
        ORDER BY experiment_id
    """)
    
    print("\nGrades across 10 trials:")
    trials_grades = []
    for row in cur.fetchall():
        exp_id = row[0]
        score = row[1]
        grade = score_to_grade(score)
        trials_grades.append(grade)
        print(f"  {exp_id}: {grade} (score: {score:.1f})")
    
    conn.close()
    
    # Check if all identical
    unique_grades = set(trials_grades)
    print(f"\nUnique grades: {unique_grades}")
    
    if len(unique_grades) == 1:
        print("PERFECTLY CONSISTENT - All 10 trials gave IDENTICAL grade")
    else:
        print(f"VARIABLE - {len(unique_grades)} different grades across trials")

except FileNotFoundError as e:
    print(f"\nFile not found: {e}")
except Exception as e:
    print(f"\nError: {e}")
