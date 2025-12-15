#!/usr/bin/env python3
"""
Analyze per-rubric comparison between Gold Baseline and AI experiments.
Compares each of 4 rubrics separately for each student and question.
"""

import sqlite3
import json
import os
import argparse
from pathlib import Path

# Rubric names in order
RUBRICS = [
    "Pemahaman Konten",
    "Organisasi & Struktur", 
    "Argumen & Bukti",
    "Gaya Bahasa & Mekanik"
]

def load_gold_standard(gold_dir: str):
    """Load all gold standard grades from JSON files."""
    gold_data = {}
    
    gold_path = Path(gold_dir)
    if not gold_path.exists():
        raise FileNotFoundError(f"Gold standard directory not found: {gold_dir}")
    
    for json_file in gold_path.glob("student_*_gold.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        student_name = data.get('student_name', 'unknown')
        
        # Extract student number from name: "Mahasiswa 1" -> "student_01"
        if 'Mahasiswa ' in student_name:
            num = student_name.replace('Mahasiswa ', '').strip()
            student_id = f"student_{num.zfill(2)}"
        else:
            # Fallback: extract from filename
            filename = json_file.stem
            parts = filename.split('_')
            student_id = f"{parts[0]}_{parts[1]}"
        
        # Gold standard uses 'questions' array, not 'grading_results'
        for q_idx, result in enumerate(data.get('questions', []), 1):
            q_num = q_idx
            key = (student_id, q_num)
            
            # Extract grades for each rubric
            grades_json = result.get('grades', {})
            rubric_grades = {}
            for rubric in RUBRICS:
                if rubric in grades_json:
                    # Gold standard stores grade directly as string (e.g., "B")
                    rubric_grades[rubric] = grades_json[rubric]
                else:
                    rubric_grades[rubric] = 'N/A'
            
            gold_data[key] = {
                'student_name': student_name,
                'rubric_grades': rubric_grades
            }
    
    return gold_data

def load_experiment_grades(db_path: str, experiment_pattern: str):
    """Load AI experiment grades from database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Get all experiments matching pattern
    if '*' in experiment_pattern:
        pattern = experiment_pattern.replace('*', '%')
        cur.execute("""
            SELECT DISTINCT experiment_id 
            FROM grading_results 
            WHERE experiment_id LIKE ?
            ORDER BY experiment_id
        """, (pattern,))
    else:
        cur.execute("""
            SELECT DISTINCT experiment_id 
            FROM grading_results 
            WHERE experiment_id = ?
        """, (experiment_pattern,))
    
    experiments = [row[0] for row in cur.fetchall()]
    
    # Load grades for each experiment
    exp_data = {}
    for exp_id in experiments:
        cur.execute("""
            SELECT student_id, student_name, question_number, trial_number, grades
            FROM grading_results
            WHERE experiment_id = ?
            ORDER BY student_id, question_number, trial_number
        """, (exp_id,))
        
        exp_grades = {}
        for row in cur.fetchall():
            student_id, student_name, q_num, trial_num, grades_json_str = row
            
            try:
                grades_json = json.loads(grades_json_str)
            except:
                grades_json = {}
            
            # Extract rubric grades
            rubric_grades = {}
            for rubric in RUBRICS:
                if rubric in grades_json:
                    rubric_grades[rubric] = grades_json[rubric].get('grade', 'N/A')
                else:
                    rubric_grades[rubric] = 'N/A'
            
            key = (student_id, q_num, trial_num)
            exp_grades[key] = {
                'student_name': student_name,
                'rubric_grades': rubric_grades
            }
        
        exp_data[exp_id] = exp_grades
    
    conn.close()
    return experiments, exp_data

def compare_per_rubric(gold_data, experiments, exp_data):
    """Compare each rubric between gold and AI for each student/question."""
    
    # Get all unique student/question combinations
    all_keys = set(gold_data.keys())
    
    print("=" * 80)
    print("PER-RUBRIC ANALYSIS: Gold Baseline vs AI Experiments")
    print("=" * 80)
    print()
    
    # Statistics per rubric
    rubric_stats = {rubric: {'total': 0, 'match': 0} for rubric in RUBRICS}
    
    for student_id, q_num in sorted(all_keys):
        if (student_id, q_num) not in gold_data:
            continue
        
        gold_info = gold_data[(student_id, q_num)]
        student_name = gold_info['student_name']
        gold_rubrics = gold_info['rubric_grades']
        
        print(f"\n{'='*80}")
        print(f"{student_name} - Soal {q_num}")
        print(f"{'='*80}")
        
        # Compare each rubric
        for rubric in RUBRICS:
            gold_grade = gold_rubrics.get(rubric, 'N/A')
            print(f"\n{rubric}:")
            print(f"  Gold Baseline (Dosen): {gold_grade}")
            
            # Compare across all experiments and trials
            exp_grades = []
            for exp_id in experiments:
                exp_trials = exp_data[exp_id]
                
                # Find all trials for this student/question
                trial_grades = []
                for trial_num in range(1, 20):  # Check up to 20 trials
                    key = (student_id, q_num, trial_num)
                    if key in exp_trials:
                        ai_rubrics = exp_trials[key]['rubric_grades']
                        ai_grade = ai_rubrics.get(rubric, 'N/A')
                        trial_grades.append((trial_num, ai_grade))
                
                if trial_grades:
                    exp_grades.append((exp_id, trial_grades))
            
            # Print AI grades grouped by experiment
            if exp_grades:
                for exp_id, trial_grades in exp_grades:
                    # Count matches
                    matches = sum(1 for _, g in trial_grades if g == gold_grade)
                    total = len(trial_grades)
                    match_rate = (matches / total * 100) if total > 0 else 0
                    
                    # Print trial grades
                    grades_str = ", ".join([f"T{t}={g}{'[OK]' if g == gold_grade else '[X]'}" 
                                           for t, g in trial_grades])
                    print(f"  {exp_id}: {grades_str}")
                    print(f"    Match: {matches}/{total} ({match_rate:.1f}%)")
                    
                    # Update statistics
                    rubric_stats[rubric]['total'] += total
                    rubric_stats[rubric]['match'] += matches
            else:
                print(f"  No AI data found")
    
    # Print overall statistics per rubric
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS PER RUBRIC")
    print(f"{'='*80}")
    
    for rubric in RUBRICS:
        total = rubric_stats[rubric]['total']
        match = rubric_stats[rubric]['match']
        if total > 0:
            accuracy = (match / total) * 100
            print(f"\n{rubric}:")
            print(f"  Total comparisons: {total}")
            print(f"  Exact matches: {match}")
            print(f"  Accuracy: {accuracy:.2f}%")
        else:
            print(f"\n{rubric}:")
            print(f"  No data available")

def main():
    parser = argparse.ArgumentParser(description='Analyze per-rubric comparison with gold baseline')
    parser.add_argument('--db', default='results/grading_results.db', 
                       help='Path to database')
    parser.add_argument('--gold', default='results/gold_standard',
                       help='Path to gold standard directory')
    parser.add_argument('--pattern', required=True,
                       help='Experiment pattern (e.g., "exp_chatgpt_lenient_*" or specific experiment ID)')
    
    args = parser.parse_args()
    
    print(f"Loading gold standard from: {args.gold}")
    gold_data = load_gold_standard(args.gold)
    print(f"  Loaded {len(gold_data)} student-question pairs")
    
    print(f"\nLoading experiments matching: {args.pattern}")
    experiments, exp_data = load_experiment_grades(args.db, args.pattern)
    print(f"  Found {len(experiments)} experiments")
    for exp_id in experiments:
        exp_count = len(exp_data[exp_id])
        print(f"    {exp_id}: {exp_count} tasks")
    
    print()
    compare_per_rubric(gold_data, experiments, exp_data)

if __name__ == '__main__':
    main()
