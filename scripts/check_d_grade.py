"""
Check why D grade doesn't appear in AI predictions for lenient strategy
"""

import sqlite3
import pandas as pd
import json

def score_to_grade(score):
    """Convert weighted score to letter grade"""
    if score >= 3.5:
        return 'A'
    elif score >= 2.5:
        return 'B'
    elif score >= 1.5:
        return 'C'
    elif score >= 0.5:
        return 'D'
    else:
        return 'E'

# Connect to database
conn = sqlite3.connect('results/grading_results.db')

# Query ChatGPT lenient scores
query = """
SELECT weighted_score
FROM grading_results
WHERE experiment_id LIKE 'exp_chatgpt_lenient%'
AND status = 'completed'
"""

print("=" * 60)
print("CHATGPT LENIENT - GRADE DISTRIBUTION")
print("=" * 60)
df_chatgpt = pd.read_sql_query(query, conn)
df_chatgpt['grade'] = df_chatgpt['weighted_score'].apply(score_to_grade)
print(df_chatgpt['grade'].value_counts().sort_index())
print(f"\nTotal: {len(df_chatgpt)}")

# Query Gemini lenient scores
query_gemini = """
SELECT weighted_score
FROM grading_results
WHERE experiment_id LIKE 'exp_gemini_lenient%'
AND status = 'completed'
"""

print("\n" + "=" * 60)
print("GEMINI LENIENT - GRADE DISTRIBUTION")
print("=" * 60)
df_gemini = pd.read_sql_query(query_gemini, conn)
df_gemini['grade'] = df_gemini['weighted_score'].apply(score_to_grade)
print(df_gemini['grade'].value_counts().sort_index())
print(f"\nTotal: {len(df_gemini)}")

# Get gold standard distribution
print("\n" + "=" * 60)
print("GOLD STANDARD - GRADE DISTRIBUTION")
print("=" * 60)

import os
gold_path = 'scripts/gold_standard'
gold_grades = []

if os.path.exists(gold_path):
    for file in os.listdir(gold_path):
        if file.endswith('.json'):
            with open(os.path.join(gold_path, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'weighted_score' in data:
                    grade = score_to_grade(data['weighted_score'])
                    gold_grades.append(grade)

if gold_grades:
    gold_df = pd.Series(gold_grades).value_counts().sort_index()
    print(gold_df)
    print(f"\nTotal: {len(gold_grades)}")
else:
    print("Could not find gold standard grades in files")
    
# Check weighted scores to understand distribution
print("\n" + "=" * 60)
print("SCORE DISTRIBUTION ANALYSIS")
print("=" * 60)

query_scores = """
SELECT 
    weighted_score,
    COUNT(*) as count
FROM grading_results
WHERE experiment_id LIKE 'exp_chatgpt_lenient%'
AND status = 'completed'
GROUP BY weighted_score
ORDER BY weighted_score DESC
"""

df_scores = pd.read_sql_query(query_scores, conn)
df_scores['grade'] = df_scores['weighted_score'].apply(score_to_grade)
print("\nChatGPT Lenient - Score Distribution (top 20):")
print(df_scores.head(20))

# Score range analysis
query_range = """
SELECT 
    MIN(weighted_score) as min_score,
    MAX(weighted_score) as max_score,
    AVG(weighted_score) as avg_score,
    COUNT(*) as total
FROM grading_results
WHERE experiment_id LIKE 'exp_chatgpt_lenient%'
AND status = 'completed'
"""

df_range = pd.read_sql_query(query_range, conn)
print("\n" + "=" * 60)
print("SCORE RANGE ANALYSIS - ChatGPT Lenient")
print("=" * 60)
print(df_range)

# Count by grade ranges
print("\n" + "=" * 60)
print("DISTRIBUTION BY SCORE RANGES")
print("=" * 60)

grade_counts = df_chatgpt['grade'].value_counts().sort_index()
for grade in ['A', 'B', 'C', 'D', 'E']:
    count = grade_counts.get(grade, 0)
    pct = (count / len(df_chatgpt) * 100) if len(df_chatgpt) > 0 else 0
    
    if grade == 'A':
        range_str = '3.5-4.0'
    elif grade == 'B':
        range_str = '2.5-3.4'
    elif grade == 'C':
        range_str = '1.5-2.4'
    elif grade == 'D':
        range_str = '0.5-1.4'
    else:
        range_str = '0.0-0.4'
    
    print(f"{grade} ({range_str}): {count:4d} ({pct:5.1f}%)")

# Check how many scores are below 1.5 (C threshold)
low_scores = df_chatgpt[df_chatgpt['weighted_score'] < 1.5]
print(f"\nScores below 1.5 (would be D or E): {len(low_scores)} out of {len(df_chatgpt)} ({len(low_scores)/len(df_chatgpt)*100:.1f}%)")

if len(low_scores) > 0:
    print("\nLowest scores:")
    print(low_scores['weighted_score'].sort_values().head(10).tolist())

conn.close()

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
print("\nIf D grade is missing from confusion matrix, possible reasons:")
print("1. Lenient strategy tends to give higher grades (minimum score > 1.5)")
print("2. AI models avoid giving very low scores even for poor answers")
print("3. The 'lenient' prompt explicitly biases toward higher grades")
print("4. Gold standard may not have D grades in the 70 test cases")
print("\nThis is actually EXPECTED behavior for 'lenient' strategy!")
print("The strategy is designed to be forgiving and constructive.")

