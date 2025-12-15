"""
Analyze AI grading reliability using ALL lenient trials (aggregated).

This script:
1. Loads all 10 lenient trials per model
2. Aggregates scores (mean, median, mode) per student-question
3. Compares aggregated AI scores vs expert grades
4. Provides more robust estimates than single-trial analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
BASELINE_FILE = ANALYSIS_DIR / "baseline" / "gold_standard_70_tasks.csv"
EXPERIMENTS_DIR = ANALYSIS_DIR / "experiments"
OUTPUT_DIR = ANALYSIS_DIR / "metrics"
TABLES_DIR = ANALYSIS_DIR / "tables"
FIGURES_DIR = ANALYSIS_DIR / "figures" / "reliability"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def score_to_grade(score):
    """Convert numerical score to letter grade"""
    if score >= 3.6: return 'A'
    elif score >= 3.0: return 'B'
    elif score >= 2.0: return 'C'
    elif score >= 1.0: return 'D'
    else: return 'E'

def load_baseline():
    """Load expert gold standard grades"""
    print("\n" + "="*70)
    print("LOADING BASELINE GOLD STANDARD")
    print("="*70)
    
    df = pd.read_csv(BASELINE_FILE)
    
    # Remove duplicates (baseline has 140 records = 70 tasks × 2 AI sources)
    # Keep only unique student-question pairs
    df_unique = df.drop_duplicates(subset=['student_name', 'question_number'])
    
    print(f"✅ Loaded {len(df)} baseline records")
    print(f"✅ Unique tasks: {len(df_unique)} (after deduplication)")
    
    return df_unique

def load_all_lenient_trials(model_name):
    """Load and aggregate all 10 lenient trials for a model"""
    
    print(f"\n{'='*70}")
    print(f"LOADING ALL LENIENT TRIALS: {model_name.upper()}")
    print(f"{'='*70}")
    
    all_data = []
    trial_count = 0
    
    # Try to load trials 01-10
    for trial in range(1, 11):
        exp_name = f"exp_exp_{model_name}_lenient_{trial:02d}_{model_name}_lenient"
        exp_dir = EXPERIMENTS_DIR / exp_name
        pred_file = exp_dir / "predictions.csv"
        
        if not pred_file.exists():
            continue
        
        df = pd.read_csv(pred_file)
        df['trial'] = trial
        all_data.append(df)
        trial_count += 1
        print(f"  ✅ Trial {trial:02d}: {len(df)} tasks")
    
    if len(all_data) == 0:
        print(f"  ⚠️  No lenient trials found for {model_name}")
        return None
    
    # Concatenate all trials
    combined = pd.concat(all_data, ignore_index=True)
    
    print(f"\n  📊 Summary:")
    print(f"     Total trials: {trial_count}")
    print(f"     Total records: {len(combined)}")
    print(f"     Unique tasks: {combined.groupby(['student_name', 'question_number']).ngroups}")
    
    return combined

def aggregate_scores(df):
    """Aggregate scores across trials per student-question"""
    
    print(f"\n{'─'*70}")
    print("AGGREGATING SCORES ACROSS TRIALS")
    print(f"{'─'*70}")
    
    # Group by student_name and question_number
    grouped = df.groupby(['student_name', 'question_number'])
    
    aggregated = grouped.agg({
        'weighted_score': ['mean', 'median', 'std', 'min', 'max', 'count']
    }).reset_index()
    
    # Flatten column names
    aggregated.columns = ['student_name', 'question_number', 
                         'score_mean', 'score_median', 'score_std', 
                         'score_min', 'score_max', 'trial_count']
    
    # Calculate mode grade (most common grade across trials)
    def get_mode_grade(group):
        grades = group['grade']
        mode_val = grades.mode()
        return mode_val.iloc[0] if len(mode_val) > 0 else grades.iloc[0]
    
    aggregated['grade_mode'] = grouped.apply(get_mode_grade).values
    
    # Also calculate grade from mean score
    aggregated['grade_from_mean'] = aggregated['score_mean'].apply(score_to_grade)
    aggregated['grade_from_median'] = aggregated['score_median'].apply(score_to_grade)
    
    print(f"\n  📊 Aggregation Statistics:")
    print(f"     Unique tasks: {len(aggregated)}")
    print(f"     Avg trials per task: {aggregated['trial_count'].mean():.1f}")
    print(f"     Mean score SD: {aggregated['score_std'].mean():.3f}")
    print(f"     Score range: [{aggregated['score_min'].min():.2f}, {aggregated['score_max'].max():.2f}]")
    
    return aggregated

def compare_with_baseline(aggregated_df, baseline_df, model_name, aggregation_method='mean'):
    """Compare aggregated AI scores with baseline"""
    
    print(f"\n{'='*70}")
    print(f"COMPARING WITH BASELINE: {model_name.upper()} ({aggregation_method.upper()})")
    print(f"{'='*70}")
    
    # Select score column based on aggregation method
    if aggregation_method == 'mean':
        score_col = 'score_mean'
        grade_col = 'grade_from_mean'
    elif aggregation_method == 'median':
        score_col = 'score_median'
        grade_col = 'grade_from_median'
    elif aggregation_method == 'mode':
        score_col = 'score_mean'  # Still use mean for score metrics
        grade_col = 'grade_mode'
    
    # Merge with baseline
    merged = baseline_df.merge(
        aggregated_df[['student_name', 'question_number', score_col, grade_col, 'trial_count', 'score_std']],
        on=['student_name', 'question_number'],
        suffixes=('_expert', '_ai')
    )
    
    print(f"  Matched tasks: {len(merged)}")
    
    if len(merged) == 0:
        print("  ⚠️  No matching tasks found!")
        return None
    
    # Calculate metrics
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    
    expert_scores = merged['weighted_score'].values
    ai_scores = merged[score_col].values
    expert_grades = merged['grade'].values
    ai_grades = merged[grade_col].values
    
    results = {
        'model': model_name,
        'aggregation': aggregation_method,
        'n_tasks': len(merged),
        'n_trials': int(merged['trial_count'].mean()),
        'mae': mean_absolute_error(expert_scores, ai_scores),
        'rmse': np.sqrt(mean_squared_error(expert_scores, ai_scores)),
        'bias': np.mean(ai_scores - expert_scores),
        'exact_match': np.mean(expert_grades == ai_grades) * 100,
        'cohens_kappa': cohen_kappa_score(expert_grades, ai_grades),
        'pearson_r': pearsonr(expert_scores, ai_scores)[0],
        'mean_consistency_sd': merged['score_std'].mean()
    }
    
    # Confusion matrix
    all_grades = ['A', 'B', 'C', 'D', 'E']
    cm = confusion_matrix(expert_grades, ai_grades, labels=all_grades)
    
    # Print results
    print(f"\n  📊 Score Metrics:")
    print(f"     MAE: {results['mae']:.3f}")
    print(f"     RMSE: {results['rmse']:.3f}")
    print(f"     Bias: {results['bias']:.3f}")
    print(f"     Pearson r: {results['pearson_r']:.3f}")
    
    print(f"\n  📋 Grade Metrics:")
    print(f"     Exact match: {results['exact_match']:.1f}%")
    print(f"     Cohen's κ: {results['cohens_kappa']:.3f}")
    
    print(f"\n  🔄 Consistency:")
    print(f"     Avg trials/task: {results['n_trials']}")
    print(f"     Mean SD: {results['mean_consistency_sd']:.3f}")
    
    return {
        'metrics': results,
        'confusion_matrix': cm,
        'merged_data': merged
    }

def create_comparison_table(single_trial_results, aggregated_results):
    """Create comparison table between single trial and aggregated analysis"""
    
    print(f"\n{'='*70}")
    print("COMPARISON: SINGLE TRIAL vs AGGREGATED (ALL 10 TRIALS)")
    print(f"{'='*70}")
    
    data = []
    
    for model in ['chatgpt', 'gemini']:
        # Single trial
        single = single_trial_results[model]
        
        # Aggregated (try all methods)
        for method in ['mean', 'median', 'mode']:
            if model in aggregated_results and method in aggregated_results[model]:
                agg = aggregated_results[model][method]['metrics']
                
                data.append({
                    'model': model,
                    'method': f'single_trial',
                    'n_samples': single['n_tasks'],
                    'mae': single['mae'],
                    'exact_match': single['exact_match'],
                    'cohens_kappa': single['cohens_kappa'],
                    'pearson_r': single['pearson_r']
                })
                
                data.append({
                    'model': model,
                    'method': f'aggregated_{method}',
                    'n_samples': agg['n_tasks'],
                    'mae': agg['mae'],
                    'exact_match': agg['exact_match'],
                    'cohens_kappa': agg['cohens_kappa'],
                    'pearson_r': agg['pearson_r']
                })
    
    df = pd.DataFrame(data)
    
    print("\n" + df.to_string(index=False))
    
    return df

def main():
    print("\n" + "="*70)
    print("RELIABILITY ANALYSIS: ALL LENIENT TRIALS AGGREGATED")
    print("="*70)
    
    # Load baseline
    baseline_df = load_baseline()
    
    # Load single trial results for comparison
    single_trial_metrics = {}
    
    for model in ['chatgpt', 'gemini']:
        exp_name = f"exp_exp_{model}_lenient_01_{model}_lenient"
        pred_file = EXPERIMENTS_DIR / exp_name / "predictions.csv"
        
        if pred_file.exists():
            pred_df = pd.read_csv(pred_file)
            merged = baseline_df.merge(
                pred_df,
                on=['student_name', 'question_number'],
                suffixes=('_expert', '_ai')
            )
            
            single_trial_metrics[model] = {
                'n_tasks': len(merged),
                'mae': np.abs(merged['weighted_score_ai'] - merged['weighted_score_expert']).mean(),
                'exact_match': (merged['grade_expert'] == merged['grade_ai']).mean() * 100,
                'cohens_kappa': cohen_kappa_score(merged['grade_expert'], merged['grade_ai']),
                'pearson_r': pearsonr(merged['weighted_score_expert'], merged['weighted_score_ai'])[0]
            }
    
    # Analyze all lenient trials
    aggregated_results = {}
    
    for model in ['chatgpt', 'gemini']:
        # Load all trials
        all_trials = load_all_lenient_trials(model)
        
        if all_trials is None:
            continue
        
        # Aggregate scores
        aggregated = aggregate_scores(all_trials)
        
        aggregated_results[model] = {}
        
        # Compare using different aggregation methods
        for method in ['mean', 'median', 'mode']:
            result = compare_with_baseline(aggregated, baseline_df, model, method)
            if result:
                aggregated_results[model][method] = result
    
    # Create comparison table
    print("\n" + "="*70)
    print("CREATING COMPARISON TABLES")
    print("="*70)
    
    comparison_df = create_comparison_table(single_trial_metrics, aggregated_results)
    comparison_df.to_csv(TABLES_DIR / "table_03_lenient_single_vs_aggregated.csv", index=False)
    print(f"✅ Saved: table_03_lenient_single_vs_aggregated.csv")
    
    # Summary
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    
    print("\n🎯 IMPACT OF AGGREGATION:")
    print("  Using all 10 trials (mean/median) provides:")
    print("  1. More stable estimates (reduces random variation)")
    print("  2. Better representation of model behavior")
    print("  3. Allows assessment of consistency (via SD)")
    
    print("\n📊 AGGREGATION METHOD COMPARISON:")
    print("  - MEAN: Best for continuous score metrics (MAE, Pearson r)")
    print("  - MEDIAN: Robust to outliers")
    print("  - MODE: Best for categorical grades (Cohen's Kappa)")
    
    print("\n" + "="*70)
    print("✅ AGGREGATED LENIENT ANALYSIS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()
