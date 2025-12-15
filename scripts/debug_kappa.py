#!/usr/bin/env python3
"""Debug why Fleiss Kappa is 0"""

import sqlite3
import pandas as pd

def score_to_grade(score):
    if pd.isna(score):
        return 'E'
    if score >= 3.5:  # A = 4
        return 'A'
    elif score >= 2.5:  # B = 3
        return 'B'
    elif score >= 1.5:  # C = 2
        return 'C'
    elif score >= 0.5:  # D = 1
        return 'D'
    else:  # E = 0
        return 'E'

# Load data
conn = sqlite3.connect('results/grading_results.db')

query = """
    SELECT 
        experiment_id,
        student_id,
        question_number,
        weighted_score
    FROM grading_results
    WHERE experiment_id LIKE 'exp_chatgpt_lenient_%' AND status = 'completed'
    ORDER BY student_id, question_number, experiment_id
"""

df = pd.read_sql_query(query, conn)
conn.close()

df['ai_grade'] = df['weighted_score'].apply(score_to_grade)

print("Total rows:", len(df))
print("\nGrade distribution:")
print(df['ai_grade'].value_counts().sort_index())

print("\n\nSample data for student_01, Q1:")
sample = df[(df['student_id'] == 'student_01') & (df['question_number'] == 1)]
print(sample[['experiment_id', 'weighted_score', 'ai_grade']])

print("\n\nGrades for student_01, Q1 across 10 trials:")
print(sample['ai_grade'].values)

print("\n\nUnique students:")
print(df['student_id'].nunique())

print("\nUnique questions:")
print(df['question_number'].nunique())

print("\nUnique experiments:")
print(df['experiment_id'].nunique())

# Create pivot table: rows=students*questions, columns=experiments
print("\n\nCreating ratings matrix...")
pivot = df.pivot_table(
    index=['student_id', 'question_number'],
    columns='experiment_id',
    values='ai_grade',
    aggfunc='first'
)

print("Pivot shape:", pivot.shape)
print("\nFirst few rows:")
print(pivot.head())

# Check if all trials give same grade (perfect consistency)
print("\n\nChecking consistency across trials:")
for idx in pivot.index[:5]:
    grades = pivot.loc[idx].values
    unique = set(grades)
    print(f"{idx}: {grades} -> Unique: {unique}")
