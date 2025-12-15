"""
RQ1: Validity Analysis - Agreement with Gold Standard

Calculates agreement metrics between LLM grading and gold standard (baseline):
- Exact Agreement (EA): Exact match of final grades
- Adjacent Agreement (AA): Within ±1 grade point
- Cohen's Kappa: Agreement accounting for chance
- Quadratic Weighted Kappa (QWK): Agreement with distance weighting
- Per-grade Precision, Recall, F1
- Confusion matrices
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import confusion_matrix, cohen_kappa_score, precision_recall_fscore_support
from collections import defaultdict
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
OUTPUT_DIR = Path("results_experiment_final/rq1_validity")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("RQ1: VALIDITY ANALYSIS - AGREEMENT WITH GOLD STANDARD")
print("="*80 + "\n")

# Load data
print("Loading data...")
df_experiment = pd.read_csv(DATA_DIR / "experiment_data_complete.csv")
df_gold = pd.read_csv(DATA_DIR / "gold_standard.csv")
print(f"  ✓ Experiment data: {len(df_experiment)} records")
print(f"  ✓ Gold standard: {len(df_gold)} records")

# Map grades to numeric values
grade_mapping = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
reverse_mapping = {v: k for k, v in grade_mapping.items()}

# ============================================================================
# Prepare merged dataset
# ============================================================================
print("\nPreparing merged dataset...")

# Both use weighted scores (0-5 scale)
# Experiment data already has numeric weighted_score
df_experiment['llm_numeric'] = df_experiment['weighted_score']

# Gold standard already has numeric scores
df_gold['gold_numeric'] = df_gold['gold_score']

# Fix student_id mismatch: experiment uses "student_01", gold uses 0
# Convert gold standard student_id to match experiment format
df_gold['student_id'] = 'student_' + df_gold['student_id'].astype(str).str.zfill(2)

# Ensure student_id is string
df_experiment['student_id'] = df_experiment['student_id'].astype(str)

# Ensure question_number is consistent type
df_experiment['question_number'] = df_experiment['question_number'].astype(int)
df_gold['question_number'] = df_gold['question_number'].astype(int)

# Merge on student_id and question_number
df_merged = df_experiment.merge(
    df_gold[['student_id', 'question_number', 'gold_numeric']],
    on=['student_id', 'question_number'],
    how='inner'
)

print(f"  ✓ Merged dataset: {len(df_merged)} records")
print(f"  ✓ Models: {df_merged['model'].unique()}")
print(f"  ✓ Strategies: {df_merged['strategy'].unique()}")

# ============================================================================
# Function: Quadratic Weighted Kappa
# ============================================================================
def quadratic_weighted_kappa(y_true, y_pred, min_rating=1, max_rating=5):
    """Calculate Quadratic Weighted Kappa"""
    
    # Confusion matrix
    conf_mat = confusion_matrix(y_true, y_pred, labels=list(range(min_rating, max_rating + 1)))
    num_ratings = max_rating - min_rating + 1
    
    # Weight matrix
    weights = np.zeros((num_ratings, num_ratings))
    for i in range(num_ratings):
        for j in range(num_ratings):
            weights[i, j] = ((i - j) ** 2) / ((num_ratings - 1) ** 2)
    
    # Expected and observed agreement
    hist_true = np.zeros(num_ratings)
    hist_pred = np.zeros(num_ratings)
    
    for i in range(num_ratings):
        hist_true[i] = np.sum(conf_mat[i, :])
        hist_pred[i] = np.sum(conf_mat[:, i])
    
    expected_mat = np.outer(hist_true, hist_pred)
    expected_mat = expected_mat / expected_mat.sum()
    
    observed_mat = conf_mat / conf_mat.sum()
    
    numerator = np.sum(weights * observed_mat)
    denominator = np.sum(weights * expected_mat)
    
    if denominator == 0:
        return 0.0
    
    return 1.0 - (numerator / denominator)

# ============================================================================
# Calculate metrics per model-strategy combination
# ============================================================================
print("\nCalculating agreement metrics...")

results = []

for model in df_merged['model'].unique():
    for strategy in df_merged['strategy'].unique():
        
        # Filter data
        data = df_merged[(df_merged['model'] == model) & (df_merged['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        y_true = data['gold_numeric'].values
        y_pred = data['llm_numeric'].values
        
        # Round scores to nearest integer grade (1-5) for classification metrics
        y_true_rounded = np.round(y_true).astype(int)
        y_pred_rounded = np.round(y_pred).astype(int)
        
        # Exact Agreement (on rounded grades)
        exact_agreement = np.mean(y_true_rounded == y_pred_rounded) * 100
        
        # Adjacent Agreement (±1 grade on rounded grades)
        adjacent_agreement = np.mean(np.abs(y_true_rounded - y_pred_rounded) <= 1) * 100
        
        # Cohen's Kappa (on rounded grades)
        kappa = cohen_kappa_score(y_true_rounded, y_pred_rounded)
        
        # Quadratic Weighted Kappa (on rounded grades)
        qwk = quadratic_weighted_kappa(y_true_rounded, y_pred_rounded)
        
        # Mean Absolute Error (on continuous scores)
        mae = np.mean(np.abs(y_true - y_pred))
        
        # RMSE (on continuous scores)
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        
        # Bias (over-grading vs under-grading, on continuous scores)
        bias = np.mean(y_pred - y_true)
        
        results.append({
            'model': model,
            'strategy': strategy,
            'n_samples': len(data),
            'exact_agreement_pct': round(exact_agreement, 2),
            'adjacent_agreement_pct': round(adjacent_agreement, 2),
            'cohen_kappa': round(kappa, 4),
            'qwk': round(qwk, 4),
            'mae': round(mae, 4),
            'rmse': round(rmse, 4),
            'bias': round(bias, 4)
        })
        
        print(f"  ✓ {model.upper()} {strategy}: EA={exact_agreement:.1f}%, AA={adjacent_agreement:.1f}%, κ={kappa:.3f}, QWK={qwk:.3f}")

# Save summary
df_validity = pd.DataFrame(results)
df_validity.to_csv(OUTPUT_DIR / "validity_summary.csv", index=False)
print(f"\n  ✓ Saved validity_summary.csv")

# ============================================================================
# Per-grade metrics (Precision, Recall, F1)
# ============================================================================
print("\nCalculating per-grade metrics...")

per_grade_results = []

for model in df_merged['model'].unique():
    for strategy in df_merged['strategy'].unique():
        
        data = df_merged[(df_merged['model'] == model) & (df_merged['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        y_true = data['gold_numeric'].values
        y_pred = data['llm_numeric'].values
        
        # Round to integer grades for classification
        y_true_rounded = np.round(y_true).astype(int)
        y_pred_rounded = np.round(y_pred).astype(int)
        
        # Calculate precision, recall, F1 per grade
        precision, recall, f1, support = precision_recall_fscore_support(
            y_true_rounded, y_pred_rounded, labels=[1, 2, 3, 4, 5], average=None, zero_division=0
        )
        
        for grade_num, (p, r, f, s) in enumerate(zip(precision, recall, f1, support), start=1):
            grade_letter = reverse_mapping.get(grade_num, str(grade_num))
            per_grade_results.append({
                'model': model,
                'strategy': strategy,
                'grade': grade_letter,
                'grade_numeric': grade_num,
                'precision': round(p, 4),
                'recall': round(r, 4),
                'f1_score': round(f, 4),
                'support': int(s)
            })

df_per_grade = pd.DataFrame(per_grade_results)
df_per_grade.to_csv(OUTPUT_DIR / "per_grade_metrics.csv", index=False)
print(f"  ✓ Saved per_grade_metrics.csv")

# ============================================================================
# Confusion matrices
# ============================================================================
print("\nGenerating confusion matrices...")

for model in df_merged['model'].unique():
    for strategy in df_merged['strategy'].unique():
        
        data = df_merged[(df_merged['model'] == model) & (df_merged['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        y_true = data['gold_numeric'].values
        y_pred = data['llm_numeric'].values
        
        # Round to integer grades
        y_true_rounded = np.round(y_true).astype(int)
        y_pred_rounded = np.round(y_pred).astype(int)
        
        # Confusion matrix
        cm = confusion_matrix(y_true_rounded, y_pred_rounded, labels=[1, 2, 3, 4, 5])
        
        # Convert to DataFrame with grade labels
        cm_df = pd.DataFrame(
            cm,
            index=[f"True_{reverse_mapping.get(i, i)}" for i in range(1, 6)],
            columns=[f"Pred_{reverse_mapping.get(i, i)}" for i in range(1, 6)]
        )
        
        # Save
        filename = f"confusion_matrix_{model}_{strategy}.csv"
        cm_df.to_csv(OUTPUT_DIR / filename)
        print(f"  ✓ Saved {filename}")

# ============================================================================
# Summary statistics
# ============================================================================
print("\nGenerating summary statistics...")

summary_stats = {
    'overall': {
        'total_samples': int(len(df_merged)),
        'models': list(df_merged['model'].unique()),
        'strategies': list(df_merged['strategy'].unique()),
        'grade_distribution_gold': df_merged['gold_numeric'].value_counts().to_dict()
    },
    'by_model': {}
}

for model in df_merged['model'].unique():
    model_data = df_merged[df_merged['model'] == model]
    
    summary_stats['by_model'][model] = {
        'n_samples': int(len(model_data)),
        'mean_exact_agreement': float(df_validity[df_validity['model'] == model]['exact_agreement_pct'].mean()),
        'mean_adjacent_agreement': float(df_validity[df_validity['model'] == model]['adjacent_agreement_pct'].mean()),
        'mean_qwk': float(df_validity[df_validity['model'] == model]['qwk'].mean()),
        'best_strategy': df_validity[df_validity['model'] == model].nlargest(1, 'qwk')['strategy'].values[0]
    }

with open(OUTPUT_DIR / "validity_summary.json", 'w') as f:
    json.dump(summary_stats, f, indent=2)

print(f"  ✓ Saved validity_summary.json")

# ============================================================================
# Display Summary
# ============================================================================
print("\n" + "="*80)
print("VALIDITY ANALYSIS SUMMARY")
print("="*80 + "\n")

print("Top Performers by QWK:")
top_performers = df_validity.nlargest(5, 'qwk')[['model', 'strategy', 'qwk', 'exact_agreement_pct', 'adjacent_agreement_pct']]
print(top_performers.to_string(index=False))

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nOutput files:")
print(f"  • validity_summary.csv - Agreement metrics per model-strategy")
print(f"  • per_grade_metrics.csv - Precision/Recall/F1 per grade")
print(f"  • confusion_matrix_*.csv - Confusion matrices")
print(f"  • validity_summary.json - Summary statistics")
print("="*80 + "\n")
