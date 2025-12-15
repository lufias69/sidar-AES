#!/usr/bin/env python3
"""
Deep dive analysis: Failed tasks, error patterns, and question difficulty
"""
import sqlite3
import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

def score_to_grade(score):
    """Convert GPA score to letter grade"""
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

def load_gold_standard():
    """Load gold standard grades"""
    gold_dir = Path('results/gold_standard')
    gold_data = {}
    
    for json_file in gold_dir.glob('student_*_gold.json'):
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
            student_name = data['student_name']
            student_num = ''.join(filter(str.isdigit, student_name))
            if student_num:
                student_id = f"student_{int(student_num):02d}"
            else:
                continue
                
            for q_idx, q in enumerate(data['questions'], start=1):
                score = q['weighted_score']
                gold_data[(student_id, q_idx)] = score
    
    return gold_data

def analyze_failed_tasks():
    """Investigate Gemini's 2 failed tasks"""
    print("\n" + "="*80)
    print("1. FAILED TASKS INVESTIGATION")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    # Find failed tasks
    df_failed = pd.read_sql_query("""
        SELECT experiment_id, student_id, question_number, 
               answer_text, error_message, timestamp
        FROM grading_results
        WHERE model = 'gemini' AND status = 'failed'
        ORDER BY timestamp
    """, conn)
    
    print(f"\nTotal failed tasks: {len(df_failed)}")
    
    if len(df_failed) > 0:
        print("\n" + "-"*80)
        for idx, row in df_failed.iterrows():
            print(f"\nFailed Task #{idx+1}:")
            print(f"  Experiment: {row['experiment_id']}")
            print(f"  Student: {row['student_id']}, Question: {row['question_number']}")
            print(f"  Timestamp: {row['timestamp']}")
            print(f"  Error: {row['error_message']}")
            print(f"\n  Answer preview:")
            answer = row['answer_text']
            print(f"  {answer[:300]}..." if len(answer) > 300 else f"  {answer}")
            print("-"*80)
    else:
        print("\n✓ No failed tasks found!")
    
    # Compare with ChatGPT success on same tasks
    if len(df_failed) > 0:
        print("\n" + "="*80)
        print("Checking ChatGPT performance on same tasks...")
        print("="*80)
        
        for idx, row in df_failed.iterrows():
            df_chatgpt = pd.read_sql_query(f"""
                SELECT experiment_id, status, weighted_score, error_message
                FROM grading_results
                WHERE model = 'chatgpt' 
                AND student_id = '{row['student_id']}'
                AND question_number = {row['question_number']}
                ORDER BY timestamp DESC
                LIMIT 1
            """, conn)
            
            print(f"\nTask: Student {row['student_id']}, Question {row['question_number']}")
            if len(df_chatgpt) > 0:
                chat_row = df_chatgpt.iloc[0]
                print(f"  ChatGPT status: {chat_row['status']}")
                if chat_row['status'] == 'completed':
                    print(f"  ChatGPT score: {chat_row['weighted_score']:.2f}")
                else:
                    print(f"  ChatGPT error: {chat_row['error_message']}")
            else:
                print("  ChatGPT: No data")
    
    conn.close()

def analyze_error_patterns():
    """Analyze which rubrics/questions have largest errors"""
    print("\n" + "="*80)
    print("2. ERROR PATTERN ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score, grades
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        # Add gold standard
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        
        # Calculate errors
        df['error'] = abs(df['weighted_score'] - df['gold_score'])
        df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
        df['gold_grade'] = df['gold_score'].apply(score_to_grade)
        
        # Overall statistics
        print(f"\n  Overall Error Statistics:")
        print(f"    Mean Absolute Error: {df['error'].mean():.3f}")
        print(f"    Median Absolute Error: {df['error'].median():.3f}")
        print(f"    Max Error: {df['error'].max():.3f}")
        print(f"    Std Dev: {df['error'].std():.3f}")
        
        # Error by question
        print(f"\n  Error by Question:")
        q_errors = df.groupby('question_number')['error'].agg(['mean', 'median', 'max', 'count'])
        q_errors = q_errors.sort_values('mean', ascending=False)
        print(f"    {'Q#':<5} {'Mean':<10} {'Median':<10} {'Max':<10} {'Count':<10}")
        print(f"    {'-'*50}")
        for q_num, row in q_errors.head(10).iterrows():
            print(f"    {q_num:<5} {row['mean']:<10.3f} {row['median']:<10.3f} {row['max']:<10.3f} {int(row['count']):<10}")
        
        print(f"\n  Per-Rubric Grade Distribution:")
        rubric_grades = {}
        
        for idx, row in df.iterrows():
            grades_data = json.loads(row['grades']) if isinstance(row['grades'], str) else row['grades']
            
            for rubric in grades_data.keys():
                if rubric not in rubric_grades:
                    rubric_grades[rubric] = []
                
                # Get AI grade for this rubric
                if model == 'chatgpt':
                    ai_rubric_grade = grades_data[rubric]
                else:
                    if isinstance(grades_data[rubric], dict):
                        ai_rubric_grade = grades_data[rubric].get('grade', 'C')
                    else:
                        ai_rubric_grade = grades_data[rubric]
                
                # Only add if it's a valid grade string
                if isinstance(ai_rubric_grade, str):
                    rubric_grades[rubric].append(ai_rubric_grade)
        
        print(f"    {'Rubric':<35} {'Grade Distribution'}")
        print(f"    {'-'*70}")
        for rubric, grades in rubric_grades.items():
            grade_counts = Counter(grades)
            dist = ', '.join([f"{g}:{count}" for g, count in sorted(grade_counts.items())])
            print(f"    {rubric:<35} {dist}")
    
    conn.close()

def analyze_question_difficulty():
    """Identify easy vs hard questions"""
    print("\n" + "="*80)
    print("3. QUESTION DIFFICULTY ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    # Combine both models
    df_all = pd.read_sql_query("""
        SELECT model, student_id, question_number, weighted_score
        FROM grading_results
        WHERE strategy = 'lenient' AND status = 'completed'
    """, conn)
    
    df_all['gold_score'] = df_all.apply(
        lambda row: gold_data.get((row['student_id'], row['question_number'])),
        axis=1
    )
    df_all = df_all.dropna()
    df_all['error'] = abs(df_all['weighted_score'] - df_all['gold_score'])
    df_all['exact_match'] = (df_all['weighted_score'].apply(score_to_grade) == 
                              df_all['gold_score'].apply(score_to_grade))
    
    # Group by question
    q_difficulty = df_all.groupby('question_number').agg({
        'error': ['mean', 'std'],
        'exact_match': 'mean',
        'model': 'count'
    }).round(3)
    
    q_difficulty.columns = ['Mean_Error', 'Std_Error', 'Exact_Match_%', 'N_Samples']
    q_difficulty['Exact_Match_%'] = (q_difficulty['Exact_Match_%'] * 100).round(1)
    q_difficulty = q_difficulty.sort_values('Mean_Error', ascending=False)
    
    print("\n  Question Difficulty Ranking (Hardest to Easiest):")
    print(f"  {'Q#':<5} {'Mean Error':<12} {'Std Dev':<12} {'Exact Match %':<15} {'Samples':<10}")
    print(f"  {'-'*60}")
    
    for q_num, row in q_difficulty.iterrows():
        difficulty = "HARD" if row['Mean_Error'] > 0.5 else "EASY" if row['Mean_Error'] < 0.3 else "MEDIUM"
        print(f"  {q_num:<5} {row['Mean_Error']:<12.3f} {row['Std_Error']:<12.3f} {row['Exact_Match_%']:<15.1f} {int(row['N_Samples']):<10} [{difficulty}]")
    
    # Categorize questions
    hard_questions = q_difficulty[q_difficulty['Mean_Error'] > 0.5].index.tolist()
    easy_questions = q_difficulty[q_difficulty['Mean_Error'] < 0.3].index.tolist()
    medium_questions = q_difficulty[(q_difficulty['Mean_Error'] >= 0.3) & 
                                   (q_difficulty['Mean_Error'] <= 0.5)].index.tolist()
    
    print(f"\n  Question Categories:")
    print(f"    Hard (MAE > 0.5): {len(hard_questions)} questions - {hard_questions}")
    print(f"    Medium (0.3 ≤ MAE ≤ 0.5): {len(medium_questions)} questions - {medium_questions}")
    print(f"    Easy (MAE < 0.3): {len(easy_questions)} questions - {easy_questions}")
    
    conn.close()

def analyze_grade_confusion():
    """Analyze most common grade confusions"""
    print("\n" + "="*80)
    print("4. GRADE CONFUSION ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        
        df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
        df['gold_grade'] = df['gold_score'].apply(score_to_grade)
        
        # Find mismatches
        mismatches = df[df['ai_grade'] != df['gold_grade']]
        
        print(f"\n  Total mismatches: {len(mismatches)} / {len(df)} ({len(mismatches)/len(df)*100:.1f}%)")
        
        if len(mismatches) > 0:
            print(f"\n  Most common confusions:")
            confusion_counts = mismatches.groupby(['gold_grade', 'ai_grade']).size().sort_values(ascending=False)
            
            print(f"    {'Gold → AI':<15} {'Count':<10} {'%'}")
            print(f"    {'-'*35}")
            for (gold, ai), count in confusion_counts.head(10).items():
                pct = count / len(mismatches) * 100
                print(f"    {gold} → {ai:<12} {count:<10} {pct:.1f}%")
    
    conn.close()

def analyze_overestimation_underestimation():
    """Analyze tendency to over/underestimate"""
    print("\n" + "="*80)
    print("5. OVER/UNDERESTIMATION ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        
        df['difference'] = df['weighted_score'] - df['gold_score']
        
        overestimated = df[df['difference'] > 0.3]
        underestimated = df[df['difference'] < -0.3]
        accurate = df[abs(df['difference']) <= 0.3]
        
        print(f"\n  Distribution:")
        print(f"    Overestimated (diff > +0.3): {len(overestimated)} ({len(overestimated)/len(df)*100:.1f}%)")
        print(f"    Accurate (|diff| ≤ 0.3): {len(accurate)} ({len(accurate)/len(df)*100:.1f}%)")
        print(f"    Underestimated (diff < -0.3): {len(underestimated)} ({len(underestimated)/len(df)*100:.1f}%)")
        
        print(f"\n  Mean difference: {df['difference'].mean():.3f}")
        if df['difference'].mean() > 0:
            print(f"    → Tendency to OVERESTIMATE")
        elif df['difference'].mean() < 0:
            print(f"    → Tendency to UNDERESTIMATE")
        else:
            print(f"    → Balanced estimation")
    
    conn.close()

def main():
    print("\n" + "="*80)
    print("DEEP DIVE ANALYSIS: ERRORS, FAILURES, AND PATTERNS")
    print("="*80)
    
    analyze_failed_tasks()
    analyze_error_patterns()
    analyze_question_difficulty()
    analyze_grade_confusion()
    analyze_overestimation_underestimation()
    
    print("\n" + "="*80)
    print("✓ DEEP DIVE ANALYSIS COMPLETED!")
    print("="*80)

if __name__ == "__main__":
    main()
