"""
Extract and organize all experimental data for comprehensive analysis.
Creates structured analysis folder with baseline, experiments, and metrics.
"""

import sqlite3
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
import numpy as np

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "results" / "grading_results.db"
BASELINE_DIR = PROJECT_ROOT / "results" / "baseline_batch"
ANALYSIS_DIR = PROJECT_ROOT / "analysis"

# Grade conversion
def score_to_grade(score):
    """Convert numerical score to letter grade (Indonesian system)"""
    if score >= 3.6: return 'A'
    elif score >= 3.0: return 'B'
    elif score >= 2.0: return 'C'
    elif score >= 1.0: return 'D'
    else: return 'E'

def load_gold_standard():
    """Load baseline gold standard from JSON files"""
    print("Loading baseline gold standard...")
    
    baseline_data = []
    student_files = sorted(BASELINE_DIR.glob("student_*.json"))
    
    for file in student_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        student_name = data['student_name']
        
        for idx, q in enumerate(data['questions'], start=1):
            # Get weighted score from either chatgpt or gemini
            weighted_score = q.get('chatgpt', {}).get('weighted_score') or q.get('gemini', {}).get('weighted_score')
            
            if weighted_score is None:
                continue  # Skip if no score available
            
            baseline_data.append({
                'student_name': student_name,
                'question_number': idx,
                'question_text': q['question'],
                'answer': q['answer'],
                'weighted_score': weighted_score,
                'grade': score_to_grade(weighted_score)
            })
    
    df = pd.DataFrame(baseline_data)
    print(f"  ✅ Loaded {len(df)} baseline tasks from {len(student_files)} students")
    return df

def extract_experiment_data(conn):
    """Extract all experiment data from database"""
    print("\nExtracting experiment data from database...")
    
    query = """
    SELECT 
        experiment_id,
        model,
        strategy,
        student_name,
        question_number,
        weighted_score,
        status,
        timestamp
    FROM grading_results
    WHERE status = 'completed'
    ORDER BY experiment_id, student_name, question_number
    """
    
    df = pd.read_sql_query(query, conn)
    df['grade'] = df['weighted_score'].apply(score_to_grade)
    
    print(f"  ✅ Extracted {len(df)} completed tasks")
    return df

def get_experiment_metadata(conn):
    """Get metadata for all experiments"""
    query = """
    SELECT DISTINCT
        experiment_id,
        model,
        strategy,
        COUNT(*) as total_tasks,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_tasks
    FROM grading_results
    GROUP BY experiment_id, model, strategy
    ORDER BY experiment_id
    """
    
    df = pd.read_sql_query(query, conn)
    return df

def save_baseline_data(baseline_df):
    """Save baseline/gold standard data"""
    print("\nSaving baseline data...")
    
    # Save as CSV
    csv_path = ANALYSIS_DIR / "baseline" / "gold_standard_70_tasks.csv"
    baseline_df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"  ✅ Saved: {csv_path}")
    
    # Save as JSON
    json_path = ANALYSIS_DIR / "baseline" / "gold_standard_70_tasks.json"
    baseline_df.to_json(json_path, orient='records', indent=2, force_ascii=False)
    print(f"  ✅ Saved: {json_path}")
    
    # Save summary statistics
    summary = {
        'total_tasks': len(baseline_df),
        'total_students': baseline_df['student_name'].nunique(),
        'questions_per_student': baseline_df.groupby('student_name')['question_number'].count().tolist(),
        'grade_distribution': baseline_df['grade'].value_counts().to_dict(),
        'score_statistics': {
            'mean': float(baseline_df['weighted_score'].mean()),
            'std': float(baseline_df['weighted_score'].std()),
            'min': float(baseline_df['weighted_score'].min()),
            'max': float(baseline_df['weighted_score'].max())
        }
    }
    
    summary_path = ANALYSIS_DIR / "baseline" / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Saved: {summary_path}")

def save_experiment_data(exp_df, metadata_df, baseline_df):
    """Save data for each experiment with baseline comparison"""
    print("\nSaving experiment data...")
    
    experiments_saved = 0
    
    for _, meta in metadata_df.iterrows():
        exp_id = meta['experiment_id']
        model = meta['model']
        strategy = meta['strategy']
        
        # Filter data for this experiment
        exp_data = exp_df[exp_df['experiment_id'] == exp_id].copy()
        
        if len(exp_data) == 0:
            continue
        
        # Create experiment folder
        exp_name = f"exp_{exp_id}_{model}_{strategy}"
        exp_dir = ANALYSIS_DIR / "experiments" / exp_name
        exp_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        metadata = {
            'experiment_id': str(exp_id),
            'model': model,
            'strategy': strategy,
            'total_tasks': int(meta['total_tasks']),
            'completed_tasks': int(meta['completed_tasks']),
            'failed_tasks': int(meta['failed_tasks']),
            'success_rate': float(meta['completed_tasks'] / meta['total_tasks'] * 100) if meta['total_tasks'] > 0 else 0
        }
        
        with open(exp_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save predictions
        exp_data.to_csv(exp_dir / "predictions.csv", index=False)
        
        # Compare with baseline (match by student_name and question_number)
        comparison = exp_data.merge(
            baseline_df[['student_name', 'question_number', 'weighted_score', 'grade']],
            on=['student_name', 'question_number'],
            how='inner',
            suffixes=('_pred', '_gold')
        )
        
        if len(comparison) > 0:
            comparison['score_diff'] = comparison['weighted_score_pred'] - comparison['weighted_score_gold']
            comparison['grade_match'] = comparison['grade_pred'] == comparison['grade_gold']
            
            baseline_comparison = {
                'matched_tasks': len(comparison),
                'accuracy': float(comparison['grade_match'].mean() * 100),
                'mean_score_difference': float(comparison['score_diff'].mean()),
                'mae': float(np.abs(comparison['score_diff']).mean()),
                'rmse': float(np.sqrt((comparison['score_diff'] ** 2).mean())),
                'correlation': float(comparison['weighted_score_pred'].corr(comparison['weighted_score_gold']))
            }
            
            with open(exp_dir / "vs_baseline.json", 'w') as f:
                json.dump(baseline_comparison, f, indent=2)
            
            comparison.to_csv(exp_dir / "baseline_comparison.csv", index=False)
        
        experiments_saved += 1
        print(f"  ✅ Saved: {exp_name} ({len(exp_data)} tasks)")
    
    print(f"\n  Total experiments saved: {experiments_saved}")

def generate_overall_summary(metadata_df, baseline_df):
    """Generate overall summary of all data"""
    print("\nGenerating overall summary...")
    
    summary = {
        'baseline': {
            'total_tasks': len(baseline_df),
            'total_students': int(baseline_df['student_name'].nunique()),
            'grade_distribution': baseline_df['grade'].value_counts().to_dict()
        },
        'experiments': {
            'total_experiments': len(metadata_df),
            'total_tasks_attempted': int(metadata_df['total_tasks'].sum()),
            'total_tasks_completed': int(metadata_df['completed_tasks'].sum()),
            'total_tasks_failed': int(metadata_df['failed_tasks'].sum()),
            'overall_success_rate': float(metadata_df['completed_tasks'].sum() / metadata_df['total_tasks'].sum() * 100)
        },
        'by_model': {},
        'by_strategy': {}
    }
    
    # Group by model
    for model in metadata_df['model'].unique():
        model_data = metadata_df[metadata_df['model'] == model]
        summary['by_model'][model] = {
            'experiments': len(model_data),
            'completed_tasks': int(model_data['completed_tasks'].sum()),
            'failed_tasks': int(model_data['failed_tasks'].sum())
        }
    
    # Group by strategy
    for strategy in metadata_df['strategy'].unique():
        strategy_data = metadata_df[metadata_df['strategy'] == strategy]
        summary['by_strategy'][strategy] = {
            'experiments': len(strategy_data),
            'completed_tasks': int(strategy_data['completed_tasks'].sum()),
            'failed_tasks': int(strategy_data['failed_tasks'].sum())
        }
    
    summary_path = ANALYSIS_DIR / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Saved: {summary_path}")
    
    # Print summary
    print("\n" + "="*70)
    print("EXTRACTION SUMMARY")
    print("="*70)
    print(f"\nBaseline: {summary['baseline']['total_tasks']} tasks from {summary['baseline']['total_students']} students")
    print(f"\nExperiments:")
    print(f"  Total experiments: {summary['experiments']['total_experiments']}")
    print(f"  Total tasks: {summary['experiments']['total_tasks_attempted']}")
    print(f"  Completed: {summary['experiments']['total_tasks_completed']} ({summary['experiments']['overall_success_rate']:.1f}%)")
    print(f"  Failed: {summary['experiments']['total_tasks_failed']}")
    print(f"\nBy Model:")
    for model, data in summary['by_model'].items():
        print(f"  {model}: {data['completed_tasks']} completed, {data['failed_tasks']} failed")
    print(f"\nBy Strategy:")
    for strategy, data in summary['by_strategy'].items():
        print(f"  {strategy}: {data['completed_tasks']} completed, {data['failed_tasks']} failed")
    print("\n" + "="*70)

def main():
    print("="*70)
    print("EXTRACTING ALL EXPERIMENTAL DATA FOR ANALYSIS")
    print("="*70)
    
    # Load baseline
    baseline_df = load_gold_standard()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Extract experiment data
    exp_df = extract_experiment_data(conn)
    metadata_df = get_experiment_metadata(conn)
    
    conn.close()
    
    # Save all data
    save_baseline_data(baseline_df)
    save_experiment_data(exp_df, metadata_df, baseline_df)
    generate_overall_summary(metadata_df, baseline_df)
    
    print("\n✅ ALL DATA EXTRACTED SUCCESSFULLY!")
    print(f"\nData tersedia di: {ANALYSIS_DIR}")

if __name__ == "__main__":
    main()
