"""
Analyze AI grading reliability compared to expert grading (RQ1).

This script:
1. Loads baseline gold standard (expert grades)
2. Loads AI predictions for each strategy
3. Calculates agreement metrics per strategy:
   - Exact match accuracy
   - Within-1-grade accuracy
   - Cohen's Kappa (categorical)
   - Weighted Kappa (ordinal)
   - Pearson correlation (continuous)
   - MAE, RMSE
4. Generates confusion matrices
5. Creates visualizations (scatter plots, Bland-Altman)
"""

import sqlite3
import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import cohen_kappa_score, confusion_matrix, mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
BASELINE_FILE = ANALYSIS_DIR / "baseline" / "gold_standard_70_tasks.csv"
EXPERIMENTS_DIR = ANALYSIS_DIR / "experiments"
OUTPUT_DIR = ANALYSIS_DIR / "metrics"
FIGURES_DIR = ANALYSIS_DIR / "figures" / "reliability"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Grade conversion
def score_to_grade(score):
    """Convert numerical score to letter grade"""
    if score >= 3.6: return 'A'
    elif score >= 3.0: return 'B'
    elif score >= 2.0: return 'C'
    elif score >= 1.0: return 'D'
    else: return 'E'

def grade_to_numeric(grade):
    """Convert letter grade to numeric for correlation"""
    mapping = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    return mapping.get(grade, np.nan)

def weighted_kappa(y_true, y_pred, weights='quadratic'):
    """Calculate weighted Cohen's Kappa for ordinal data"""
    from sklearn.metrics import cohen_kappa_score
    return cohen_kappa_score(y_true, y_pred, weights=weights)

def within_n_grade_accuracy(y_true, y_pred, n=1):
    """Calculate percentage of predictions within n grades of true grade"""
    grade_order = ['A', 'B', 'C', 'D', 'E']
    true_idx = [grade_order.index(g) if g in grade_order else -1 for g in y_true]
    pred_idx = [grade_order.index(g) if g in grade_order else -1 for g in y_pred]
    
    within_n = sum(1 for t, p in zip(true_idx, pred_idx) 
                   if t != -1 and p != -1 and abs(t - p) <= n)
    total = sum(1 for t in true_idx if t != -1)
    
    return (within_n / total * 100) if total > 0 else 0

def bland_altman_plot(true_scores, pred_scores, title, save_path):
    """Create Bland-Altman plot for agreement analysis"""
    mean_scores = (np.array(true_scores) + np.array(pred_scores)) / 2
    diff_scores = np.array(pred_scores) - np.array(true_scores)
    
    mean_diff = np.mean(diff_scores)
    std_diff = np.std(diff_scores)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(mean_scores, diff_scores, alpha=0.6, s=50)
    ax.axhline(mean_diff, color='red', linestyle='--', label=f'Mean: {mean_diff:.3f}')
    ax.axhline(mean_diff + 1.96*std_diff, color='gray', linestyle=':', 
               label=f'+1.96 SD: {mean_diff + 1.96*std_diff:.3f}')
    ax.axhline(mean_diff - 1.96*std_diff, color='gray', linestyle=':', 
               label=f'-1.96 SD: {mean_diff - 1.96*std_diff:.3f}')
    
    ax.set_xlabel('Mean Score (Expert + AI) / 2', fontsize=12)
    ax.set_ylabel('Difference (AI - Expert)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return mean_diff, std_diff

def load_baseline():
    """Load expert gold standard grades"""
    print("\n" + "="*70)
    print("LOADING BASELINE GOLD STANDARD")
    print("="*70)
    
    df = pd.read_csv(BASELINE_FILE)
    print(f"✅ Loaded {len(df)} baseline tasks")
    print(f"   Students: {df['student_name'].nunique()}")
    print(f"   Questions: {df['question_number'].nunique()}")
    
    return df

def load_experiment_predictions(experiment_name):
    """Load AI predictions for a specific experiment"""
    exp_dir = EXPERIMENTS_DIR / experiment_name
    predictions_file = exp_dir / "predictions.csv"
    
    if not predictions_file.exists():
        return None
    
    df = pd.read_csv(predictions_file)
    return df

def analyze_strategy(baseline_df, predictions_df, strategy_name, model_name):
    """Analyze single strategy vs baseline"""
    
    print(f"\n{'─'*70}")
    print(f"Analyzing: {model_name.upper()} - {strategy_name}")
    print(f"{'─'*70}")
    
    # Merge on student_name and question_number
    merged = baseline_df.merge(
        predictions_df,
        on=['student_name', 'question_number'],
        suffixes=('_expert', '_ai')
    )
    
    print(f"  Matched tasks: {len(merged)}")
    
    if len(merged) == 0:
        print("  ⚠️  No matching tasks found!")
        return None
    
    # Calculate metrics
    results = {
        'model': model_name,
        'strategy': strategy_name,
        'n_tasks': len(merged)
    }
    
    # Score-level metrics (continuous)
    expert_scores = merged['weighted_score_expert'].values
    ai_scores = merged['weighted_score_ai'].values
    
    results['mae'] = mean_absolute_error(expert_scores, ai_scores)
    results['rmse'] = np.sqrt(mean_squared_error(expert_scores, ai_scores))
    results['bias'] = np.mean(ai_scores - expert_scores)
    
    # Correlation
    pearson_r, pearson_p = pearsonr(expert_scores, ai_scores)
    spearman_r, spearman_p = spearmanr(expert_scores, ai_scores)
    
    results['pearson_r'] = pearson_r
    results['pearson_p'] = pearson_p
    results['spearman_r'] = spearman_r
    results['spearman_p'] = spearman_p
    
    # Grade-level metrics (categorical)
    expert_grades = merged['grade_expert'].values
    ai_grades = merged['grade_ai'].values
    
    results['exact_match'] = np.mean(expert_grades == ai_grades) * 100
    results['within_1_grade'] = within_n_grade_accuracy(expert_grades, ai_grades, n=1)
    
    # Cohen's Kappa
    try:
        results['cohens_kappa'] = cohen_kappa_score(expert_grades, ai_grades)
        results['weighted_kappa'] = weighted_kappa(expert_grades, ai_grades)
    except:
        results['cohens_kappa'] = np.nan
        results['weighted_kappa'] = np.nan
    
    # Confusion matrix
    all_grades = ['A', 'B', 'C', 'D', 'E']
    cm = confusion_matrix(expert_grades, ai_grades, labels=all_grades)
    
    # Print summary
    print(f"\n  📊 Score Metrics:")
    print(f"     MAE: {results['mae']:.3f}")
    print(f"     RMSE: {results['rmse']:.3f}")
    print(f"     Bias (AI - Expert): {results['bias']:.3f}")
    print(f"     Pearson r: {results['pearson_r']:.3f} (p={results['pearson_p']:.4f})")
    print(f"     Spearman ρ: {results['spearman_r']:.3f} (p={results['spearman_p']:.4f})")
    
    print(f"\n  📋 Grade Metrics:")
    print(f"     Exact match: {results['exact_match']:.1f}%")
    print(f"     Within-1-grade: {results['within_1_grade']:.1f}%")
    print(f"     Cohen's κ: {results['cohens_kappa']:.3f}")
    print(f"     Weighted κ: {results['weighted_kappa']:.3f}")
    
    return {
        'metrics': results,
        'confusion_matrix': cm,
        'merged_data': merged
    }

def create_confusion_matrix_plot(cm, title, save_path):
    """Create and save confusion matrix heatmap"""
    all_grades = ['A', 'B', 'C', 'D', 'E']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=all_grades, yticklabels=all_grades,
                cbar_kws={'label': 'Count'}, ax=ax, vmin=0)
    
    ax.set_xlabel('AI Predicted Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expert Gold Standard Grade', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add note
    note = "Note: Empty cells indicate grade combinations not present in data"
    fig.text(0.5, 0.02, note, ha='center', fontsize=9, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Saved confusion matrix: {save_path.name}")

def create_scatter_plot(expert_scores, ai_scores, title, save_path, show_regression=True):
    """Create scatter plot comparing AI vs Expert scores"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Scatter plot
    ax.scatter(expert_scores, ai_scores, alpha=0.6, s=80, edgecolors='black', linewidth=0.5)
    
    # Perfect agreement line
    min_val = min(expert_scores.min(), ai_scores.min())
    max_val = max(expert_scores.max(), ai_scores.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, 
            label='Perfect Agreement', alpha=0.7)
    
    # Regression line
    if show_regression:
        z = np.polyfit(expert_scores, ai_scores, 1)
        p = np.poly1d(z)
        ax.plot(expert_scores, p(expert_scores), 'b-', linewidth=2, 
                label=f'Regression: y={z[0]:.2f}x+{z[1]:.2f}', alpha=0.7)
    
    # Calculate metrics for annotation
    r, p_val = pearsonr(expert_scores, ai_scores)
    mae = mean_absolute_error(expert_scores, ai_scores)
    
    # Annotation
    textstr = f'Pearson r = {r:.3f} (p={p_val:.4f})\nMAE = {mae:.3f}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_xlabel('Expert Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('AI Predicted Score', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✅ Saved scatter plot: {save_path.name}")

def main():
    print("\n" + "="*70)
    print("RELIABILITY ANALYSIS: AI vs EXPERT GRADING (RQ1)")
    print("="*70)
    
    # Load baseline
    baseline_df = load_baseline()
    
    # Define strategies to analyze
    strategies = [
        # ChatGPT
        ('exp_exp_chatgpt_lenient_01_chatgpt_lenient', 'chatgpt', 'lenient'),
        ('exp_exp_chatgpt_zero_chatgpt_zero-shot', 'chatgpt', 'zero-shot'),
        ('exp_exp_chatgpt_few_chatgpt_few-shot', 'chatgpt', 'few-shot'),
        
        # Gemini
        ('exp_exp_gemini_lenient_01_gemini_lenient', 'gemini', 'lenient'),
        ('exp_exp_gemini_zero_gemini_zero-shot', 'gemini', 'zero-shot'),
        ('exp_exp_gemini_few_gemini_few-shot', 'gemini', 'few-shot'),
    ]
    
    all_results = []
    
    # Analyze each strategy
    for exp_name, model, strategy in strategies:
        print(f"\n{'='*70}")
        print(f"Loading: {exp_name}")
        
        predictions_df = load_experiment_predictions(exp_name)
        
        if predictions_df is None:
            print(f"  ⚠️  Experiment not found, skipping...")
            continue
        
        result = analyze_strategy(baseline_df, predictions_df, strategy, model)
        
        if result is None:
            continue
        
        all_results.append(result)
        
        # Save confusion matrix
        cm_filename = f"confusion_matrix_{model}_{strategy.replace('-', '')}.png"
        cm_path = FIGURES_DIR / cm_filename
        cm_title = f"Confusion Matrix: {model.upper()} - {strategy.capitalize()}"
        create_confusion_matrix_plot(result['confusion_matrix'], cm_title, cm_path)
        
        # Save confusion matrix as CSV
        cm_csv = OUTPUT_DIR / f"confusion_matrix_{model}_{strategy.replace('-', '')}.csv"
        cm_df = pd.DataFrame(result['confusion_matrix'], 
                            index=['A', 'B', 'C', 'D', 'E'],
                            columns=['A', 'B', 'C', 'D', 'E'])
        cm_df.to_csv(cm_csv)
        
        # Save scatter plot
        scatter_filename = f"scatter_{model}_{strategy.replace('-', '')}.png"
        scatter_path = FIGURES_DIR / scatter_filename
        scatter_title = f"AI vs Expert Scores: {model.upper()} - {strategy.capitalize()}"
        create_scatter_plot(
            result['merged_data']['weighted_score_expert'].values,
            result['merged_data']['weighted_score_ai'].values,
            scatter_title,
            scatter_path
        )
        
        # Save Bland-Altman plot
        ba_filename = f"bland_altman_{model}_{strategy.replace('-', '')}.png"
        ba_path = FIGURES_DIR / ba_filename
        ba_title = f"Bland-Altman Plot: {model.upper()} - {strategy.capitalize()}"
        bland_altman_plot(
            result['merged_data']['weighted_score_expert'].values,
            result['merged_data']['weighted_score_ai'].values,
            ba_title,
            ba_path
        )
    
    # Compile all metrics
    print("\n" + "="*70)
    print("COMPILING RESULTS")
    print("="*70)
    
    metrics_df = pd.DataFrame([r['metrics'] for r in all_results])
    
    # Save to CSV
    output_csv = OUTPUT_DIR / "reliability_vs_expert.csv"
    metrics_df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved metrics: {output_csv}")
    
    # Create summary tables
    print("\n" + "="*70)
    print("SUMMARY: AGREEMENT METRICS")
    print("="*70)
    print(metrics_df[['model', 'strategy', 'exact_match', 'within_1_grade', 
                     'cohens_kappa', 'weighted_kappa']].to_string(index=False))
    
    print("\n" + "="*70)
    print("SUMMARY: SCORE METRICS")
    print("="*70)
    print(metrics_df[['model', 'strategy', 'mae', 'rmse', 'bias', 
                     'pearson_r']].to_string(index=False))
    
    # Save summary tables
    table1 = metrics_df[['model', 'strategy', 'n_tasks', 'exact_match', 'within_1_grade', 
                        'cohens_kappa', 'weighted_kappa']]
    table1.to_csv(ANALYSIS_DIR / "tables" / "table_01_agreement_metrics.csv", index=False)
    
    table2 = metrics_df[['model', 'strategy', 'mae', 'rmse', 'bias', 
                        'pearson_r', 'pearson_p', 'spearman_r']]
    table2.to_csv(ANALYSIS_DIR / "tables" / "table_02_score_metrics.csv", index=False)
    
    print("\n" + "="*70)
    print("✅ RELIABILITY ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nOutputs:")
    print(f"  Metrics: {OUTPUT_DIR / 'reliability_vs_expert.csv'}")
    print(f"  Tables: {ANALYSIS_DIR / 'tables' / 'table_01_agreement_metrics.csv'}")
    print(f"  Tables: {ANALYSIS_DIR / 'tables' / 'table_02_score_metrics.csv'}")
    print(f"  Figures: {FIGURES_DIR}/ (18 files)")
    print(f"  - 6 confusion matrices")
    print(f"  - 6 scatter plots")
    print(f"  - 6 Bland-Altman plots")

if __name__ == "__main__":
    main()
