"""
Strategy Comparison Analysis
Compare effectiveness of different prompting strategies
"""
import sqlite3
import pandas as pd
import numpy as np
from scipy import stats
import argparse

def load_experiment(experiment_id: str):
    """Load single experiment from database"""
    conn = sqlite3.connect('results/grading_results.db')
    
    query = """
        SELECT 
            student_id,
            question_number,
            grades,
            weighted_score
        FROM grading_results
        WHERE experiment_id = ? AND status = 'completed'
        ORDER BY student_id, question_number
    """
    
    df = pd.read_sql_query(query, conn, params=(experiment_id,))
    conn.close()
    
    # Convert weighted_score (GPA scale 0-4) to letter grade
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
    
    df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
    
    # Load gold standard from JSON files
    import json
    from pathlib import Path
    
    gold_data = {}
    gold_path = Path('results/gold_standard')
    if gold_path.exists():
        for json_file in gold_path.glob('student_*_gold.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            student_name = data.get('student_name', 'unknown')
            if 'Mahasiswa ' in student_name:
                num = student_name.replace('Mahasiswa ', '').strip()
                student_id = f"student_{num.zfill(2)}"
            else:
                continue
            
            for q_idx, result in enumerate(data.get('questions', []), 1):
                key = (student_id, q_idx)
                gold_data[key] = score_to_grade(result.get('weighted_score', 0))
    
    # Add gold standard grades to dataframe
    df['gold_standard_grade'] = df.apply(
        lambda row: gold_data.get((row['student_id'], row['question_number']), 'C'),
        axis=1
    )
    
    return df

def grade_to_numeric(grade):
    """Convert letter grade to numeric"""
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    return grade_map.get(grade, 0)

def calculate_metrics(df):
    """Calculate performance metrics"""
    # Convert grades to numeric
    df['ai_numeric'] = df['ai_grade'].apply(grade_to_numeric)
    df['gold_numeric'] = df['gold_standard_grade'].apply(grade_to_numeric)
    
    # Calculate metrics
    mae = np.mean(np.abs(df['ai_numeric'] - df['gold_numeric']))
    rmse = np.sqrt(np.mean((df['ai_numeric'] - df['gold_numeric']) ** 2))
    
    # Alignment error (mean signed error)
    alignment_error = np.mean(df['ai_numeric'] - df['gold_numeric'])
    
    # Correlation
    correlation, p_value = stats.pearsonr(df['ai_numeric'], df['gold_numeric'])
    
    # Exact match rate
    exact_matches = np.sum(df['ai_grade'] == df['gold_standard_grade'])
    exact_match_rate = exact_matches / len(df)
    
    return {
        'mae': mae,
        'rmse': rmse,
        'alignment_error': alignment_error,
        'correlation': correlation,
        'p_value': p_value,
        'exact_match_rate': exact_match_rate,
        'n_tasks': len(df)
    }

def compare_strategies(*experiment_ids):
    """Compare multiple strategies"""
    print(f"\n{'='*70}")
    print(f"STRATEGY COMPARISON ANALYSIS")
    print(f"{'='*70}\n")
    
    results = {}
    
    # Load and analyze each experiment
    for exp_id in experiment_ids:
        df = load_experiment(exp_id)
        
        if df.empty:
            print(f"⚠️ {exp_id}: No data found")
            continue
        
        metrics = calculate_metrics(df)
        results[exp_id] = metrics
        
        # Determine strategy name from experiment_id
        if 'lenient' in exp_id:
            strategy = 'Lenient'
        elif 'zero' in exp_id:
            strategy = 'Zero-shot'
        elif 'few' in exp_id:
            strategy = 'Few-shot'
        else:
            strategy = 'Unknown'
        
        print(f"{strategy} Strategy ({exp_id}):")
        print(f"  Tasks: {metrics['n_tasks']}")
        print(f"  MAE: {metrics['mae']:.3f}")
        print(f"  RMSE: {metrics['rmse']:.3f}")
        print(f"  Alignment Error: {metrics['alignment_error']:+.3f}")
        print(f"  Correlation: {metrics['correlation']:.3f} (p={metrics['p_value']:.4f})")
        print(f"  Exact Match: {metrics['exact_match_rate']:.1%}")
        print()
    
    if len(results) < 2:
        print("⚠️ Need at least 2 strategies for comparison")
        return
    
    # Rank strategies
    print(f"{'='*70}")
    print(f"RANKING BY MAE (Lower is Better)")
    print(f"{'='*70}\n")
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['mae'])
    
    for rank, (exp_id, metrics) in enumerate(sorted_results, 1):
        if 'lenient' in exp_id:
            strategy = 'Lenient'
        elif 'zero' in exp_id:
            strategy = 'Zero-shot'
        elif 'few' in exp_id:
            strategy = 'Few-shot'
        else:
            strategy = exp_id
        
        medal = '🥇' if rank == 1 else '🥈' if rank == 2 else '🥉' if rank == 3 else '  '
        print(f"{medal} Rank {rank}: {strategy}")
        print(f"   MAE: {metrics['mae']:.3f}")
        print(f"   Correlation: {metrics['correlation']:.3f}")
        print(f"   Exact Match: {metrics['exact_match_rate']:.1%}")
        print()
    
    # Statistical significance test (if 3 strategies)
    if len(results) == 3:
        print(f"{'='*70}")
        print(f"STATISTICAL SIGNIFICANCE (ANOVA)")
        print(f"{'='*70}\n")
        
        # Load full data for ANOVA
        all_errors = []
        strategy_names = []
        
        for exp_id in experiment_ids:
            df = load_experiment(exp_id)
            if not df.empty:
                df['ai_numeric'] = df['ai_grade'].apply(grade_to_numeric)
                df['gold_numeric'] = df['gold_standard_grade'].apply(grade_to_numeric)
                errors = np.abs(df['ai_numeric'] - df['gold_numeric'])
                
                all_errors.append(errors)
                
                if 'lenient' in exp_id:
                    strategy_names.append('Lenient')
                elif 'zero' in exp_id:
                    strategy_names.append('Zero-shot')
                elif 'few' in exp_id:
                    strategy_names.append('Few-shot')
        
        if len(all_errors) == 3:
            f_stat, p_value = stats.f_oneway(*all_errors)
            
            print(f"F-statistic: {f_stat:.3f}")
            print(f"p-value: {p_value:.4f}")
            
            if p_value < 0.05:
                print(f"\n✅ Significant difference between strategies (p < 0.05)")
            else:
                print(f"\n⚠️ No significant difference between strategies (p >= 0.05)")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}\n")
    
    best_exp, best_metrics = sorted_results[0]
    best_strategy = 'Lenient' if 'lenient' in best_exp else 'Zero-shot' if 'zero' in best_exp else 'Few-shot'
    
    print(f"🏆 Best Strategy: {best_strategy}")
    print(f"   - Lowest MAE: {best_metrics['mae']:.3f}")
    print(f"   - Best Correlation: {best_metrics['correlation']:.3f}")
    print(f"   - Highest Exact Match: {best_metrics['exact_match_rate']:.1%}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare prompting strategies")
    parser.add_argument("experiments", nargs='+', help="Experiment IDs to compare")
    
    args = parser.parse_args()
    
    compare_strategies(*args.experiments)
