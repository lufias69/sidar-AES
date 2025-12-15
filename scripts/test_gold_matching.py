import sqlite3
import pandas as pd
from pathlib import Path
import json

def load_gold_by_name():
    gold_dir = Path('results/gold_standard')
    name_to_scores = {}
    
    for file in gold_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            student_name = data['student_name']
            
            name_to_scores[student_name] = {}
            # Use array index + 1 as question number
            for idx, q in enumerate(data['questions'], start=1):
                name_to_scores[student_name][idx] = q['weighted_score']
    
    return name_to_scores

# Test
gold = load_gold_by_name()
print("Gold standard loaded:")
for name, scores in gold.items():
    print(f"  {name}: {len(scores)} questions")

# Query database
conn = sqlite3.connect('results/grading_results.db')
df = pd.read_sql_query("""
    SELECT student_name, question_number, weighted_score
    FROM grading_results
    WHERE experiment_id = 'exp_chatgpt_lenient_01'
    LIMIT 5
""", conn)

print("\nDatabase sample:")
print(df)

# Test matching
df['gold_score'] = df.apply(
    lambda row: gold.get(row['student_name'], {}).get(row['question_number']),
    axis=1
)

print("\nMatching test:")
print(df[['student_name', 'question_number', 'weighted_score', 'gold_score']])

nulls = df['gold_score'].isna().sum()
print(f"\nNull matches: {nulls}/{len(df)}")

conn.close()
