#!/usr/bin/env python3
"""
Test-retest reliability analysis: Consistency of grading across multiple trials
"""
import sqlite3
import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def grade_to_numeric(grade):
    """Convert letter grade to numeric for consistency calculation"""
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0, 'D/E': 0.5}
    if isinstance(grade, str):
        return grade_map.get(grade, 2)  # Default to C if unknown
    return grade

def analyze_consistency():
    """Analyze grading consistency across multiple trials"""
    print("\n" + "="*80)
    print("TEST-RETEST RELIABILITY ANALYSIS")
    print("Measuring consistency of grading across 10 lenient trials")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{'='*80}")
        print(f"{model.upper()} CONSISTENCY ANALYSIS")
        print('='*80)
        
        # Get all lenient trials for this model
        df = pd.read_sql_query(f"""
            SELECT experiment_id, student_id, question_number, 
                   weighted_score, grades
            FROM grading_results
            WHERE model = '{model}' 
            AND strategy = 'lenient'
            AND status = 'completed'
            AND experiment_id LIKE 'exp_{model}_lenient_%'
            ORDER BY student_id, question_number, experiment_id
        """, conn)
        
        print(f"\nTotal records: {len(df)}")
        print(f"Experiments: {df['experiment_id'].nunique()}")
        print(f"Unique students: {df['student_id'].nunique()}")
        print(f"Questions per student: {df['question_number'].nunique()}")
        
        # Group by student and question
        grouped = df.groupby(['student_id', 'question_number'])
        
        # Overall score consistency
        print(f"\n{'-'*80}")
        print("OVERALL WEIGHTED SCORE CONSISTENCY")
        print('-'*80)
        
        consistency_stats = []
        
        for (student, question), group in grouped:
            scores = group['weighted_score'].values
            
            if len(scores) >= 2:  # Need at least 2 trials
                consistency_stats.append({
                    'student': student,
                    'question': question,
                    'n_trials': len(scores),
                    'mean': np.mean(scores),
                    'std': np.std(scores, ddof=1) if len(scores) > 1 else 0,
                    'min': np.min(scores),
                    'max': np.max(scores),
                    'range': np.max(scores) - np.min(scores),
                    'cv': (np.std(scores, ddof=1) / np.mean(scores) * 100) if np.mean(scores) > 0 and len(scores) > 1 else 0
                })
        
        cons_df = pd.DataFrame(consistency_stats)
        
        print(f"\nSummary Statistics (n={len(cons_df)} student-question pairs):")
        print(f"  Mean SD across all pairs: {cons_df['std'].mean():.3f}")
        print(f"  Median SD: {cons_df['std'].median():.3f}")
        print(f"  Mean Range: {cons_df['range'].mean():.3f}")
        print(f"  Mean CV: {cons_df['cv'].mean():.2f}%")
        
        # Categorize consistency
        high_consistency = cons_df[cons_df['std'] <= 0.1]
        moderate_consistency = cons_df[(cons_df['std'] > 0.1) & (cons_df['std'] <= 0.3)]
        low_consistency = cons_df[cons_df['std'] > 0.3]
        
        print(f"\nConsistency Categories:")
        print(f"  High (SD ≤ 0.1):     {len(high_consistency):3d} ({len(high_consistency)/len(cons_df)*100:.1f}%)")
        print(f"  Moderate (0.1 < SD ≤ 0.3): {len(moderate_consistency):3d} ({len(moderate_consistency)/len(cons_df)*100:.1f}%)")
        print(f"  Low (SD > 0.3):      {len(low_consistency):3d} ({len(low_consistency)/len(cons_df)*100:.1f}%)")
        
        # Show examples
        print(f"\n{'Student':<12} {'Q#':<5} {'Trials':<8} {'Mean':<8} {'SD':<8} {'Range':<12} {'Category'}")
        print('-'*80)
        
        # Most consistent
        most_consistent = cons_df.nsmallest(5, 'std')
        print("\nMost Consistent (Top 5):")
        for _, row in most_consistent.iterrows():
            category = "High" if row['std'] <= 0.1 else "Moderate" if row['std'] <= 0.3 else "Low"
            print(f"{row['student']:<12} {int(row['question']):<5} {int(row['n_trials']):<8} {row['mean']:<8.2f} {row['std']:<8.3f} {row['min']:.2f}-{row['max']:.2f}    {category}")
        
        # Least consistent
        least_consistent = cons_df.nlargest(5, 'std')
        print("\nLeast Consistent (Bottom 5):")
        for _, row in least_consistent.iterrows():
            category = "High" if row['std'] <= 0.1 else "Moderate" if row['std'] <= 0.3 else "Low"
            print(f"{row['student']:<12} {int(row['question']):<5} {int(row['n_trials']):<8} {row['mean']:<8.2f} {row['std']:<8.3f} {row['min']:.2f}-{row['max']:.2f}    {category}")
        
        # Per-rubric consistency
        print(f"\n{'-'*80}")
        print("PER-RUBRIC CONSISTENCY")
        print('-'*80)
        
        rubric_consistency = {}
        rubric_names = ['Pemahaman Konten', 'Organisasi & Struktur', 'Argumen & Bukti', 'Gaya Bahasa & Mekanik']
        
        for rubric_name in rubric_names:
            rubric_consistency[rubric_name] = []
        
        for (student, question), group in grouped:
            if len(group) < 2:
                continue
                
            # Extract rubric grades from each trial
            rubric_scores = {rubric: [] for rubric in rubric_names}
            
            for _, row in group.iterrows():
                grades_data = json.loads(row['grades']) if isinstance(row['grades'], str) else row['grades']
                
                for rubric in rubric_names:
                    if rubric in grades_data:
                        if model == 'chatgpt':
                            grade = grades_data[rubric]
                        else:
                            if isinstance(grades_data[rubric], dict):
                                grade = grades_data[rubric].get('grade', 'C')
                            else:
                                grade = grades_data[rubric]
                        
                        rubric_scores[rubric].append(grade_to_numeric(grade))
            
            # Calculate consistency for each rubric
            for rubric in rubric_names:
                if len(rubric_scores[rubric]) >= 2:
                    scores = [s for s in rubric_scores[rubric] if isinstance(s, (int, float))]
                    if len(scores) >= 2:
                        std = np.std(scores, ddof=1)
                        rubric_consistency[rubric].append(std)
        
        print(f"\n{'Rubric':<35} {'Mean SD':<12} {'Median SD':<12} {'% High Consistency'}")
        print('-'*80)
        
        for rubric in rubric_names:
            if rubric_consistency[rubric]:
                mean_sd = np.mean(rubric_consistency[rubric])
                median_sd = np.median(rubric_consistency[rubric])
                high_pct = sum(1 for sd in rubric_consistency[rubric] if sd <= 0.5) / len(rubric_consistency[rubric]) * 100
                print(f"{rubric:<35} {mean_sd:<12.3f} {median_sd:<12.3f} {high_pct:.1f}%")
        
        # Intraclass Correlation Coefficient (ICC)
        print(f"\n{'-'*80}")
        print("INTRACLASS CORRELATION COEFFICIENT (ICC)")
        print('-'*80)
        
        # Prepare data for ICC calculation
        icc_data = []
        for (student, question), group in grouped:
            if len(group) >= 2:
                for idx, (_, row) in enumerate(group.iterrows()):
                    icc_data.append({
                        'subject': f"{student}_{question}",
                        'trial': idx + 1,
                        'score': row['weighted_score']
                    })
        
        icc_df = pd.DataFrame(icc_data)
        
        if len(icc_df) > 0:
            # Calculate ICC(2,1) - two-way random effects, single measurement
            pivot = icc_df.pivot(index='subject', columns='trial', values='score')
            
            # Remove subjects with missing trials
            pivot_clean = pivot.dropna()
            
            if len(pivot_clean) > 0 and len(pivot_clean.columns) > 1:
                # Calculate ICC using ANOVA approach
                n_subjects = len(pivot_clean)
                n_trials = len(pivot_clean.columns)
                
                # Grand mean
                grand_mean = pivot_clean.values.mean()
                
                # Between-subjects variance
                subject_means = pivot_clean.mean(axis=1)
                ss_between = n_trials * np.sum((subject_means - grand_mean) ** 2)
                df_between = n_subjects - 1
                ms_between = ss_between / df_between if df_between > 0 else 0
                
                # Within-subjects variance (error)
                ss_within = np.sum((pivot_clean.values - subject_means.values.reshape(-1, 1)) ** 2)
                df_within = n_subjects * (n_trials - 1)
                ms_within = ss_within / df_within if df_within > 0 else 0
                
                # ICC(2,1)
                icc = (ms_between - ms_within) / (ms_between + (n_trials - 1) * ms_within) if (ms_between + (n_trials - 1) * ms_within) > 0 else 0
                
                print(f"\nICC(2,1) - Two-way random effects, single measurement:")
                print(f"  ICC = {icc:.4f}")
                
                if icc >= 0.90:
                    interpretation = "Excellent reliability"
                elif icc >= 0.75:
                    interpretation = "Good reliability"
                elif icc >= 0.50:
                    interpretation = "Moderate reliability"
                else:
                    interpretation = "Poor reliability"
                
                print(f"  Interpretation: {interpretation}")
                print(f"  Subjects analyzed: {n_subjects}")
                print(f"  Trials per subject: {n_trials}")
            else:
                print("\n  Insufficient data for ICC calculation")
        
        # Sample detailed view
        print(f"\n{'-'*80}")
        print("SAMPLE DETAILED VIEW (First 3 students, Question 1)")
        print('-'*80)
        
        sample_students = df['student_id'].unique()[:3]
        
        for student in sample_students:
            student_q1 = df[(df['student_id'] == student) & (df['question_number'] == 1)]
            
            if len(student_q1) > 0:
                print(f"\n{student}, Question 1:")
                print(f"  {'Trial':<8} {'Score':<8} {'Rubric Grades'}")
                print(f"  {'-'*70}")
                
                for idx, row in student_q1.iterrows():
                    grades_data = json.loads(row['grades']) if isinstance(row['grades'], str) else row['grades']
                    
                    rubric_str = []
                    for rubric in rubric_names:
                        if rubric in grades_data:
                            if model == 'chatgpt':
                                grade = grades_data[rubric]
                            else:
                                if isinstance(grades_data[rubric], dict):
                                    grade = grades_data[rubric].get('grade', 'C')
                                else:
                                    grade = grades_data[rubric]
                            rubric_str.append(f"{rubric.split()[0][:4]}={grade}")
                    
                    trial_num = row['experiment_id'].split('_')[-1]
                    print(f"  {trial_num:<8} {row['weighted_score']:<8.2f} {', '.join(rubric_str)}")
                
                scores = student_q1['weighted_score'].values
                print(f"\n  Statistics: Mean={np.mean(scores):.2f}, SD={np.std(scores, ddof=1):.3f}, Range=[{np.min(scores):.2f}-{np.max(scores):.2f}]")
    
    conn.close()
    
    print("\n" + "="*80)
    print("✓ CONSISTENCY ANALYSIS COMPLETED!")
    print("="*80)

if __name__ == "__main__":
    analyze_consistency()
