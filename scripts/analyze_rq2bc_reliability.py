"""
RQ2b & RQ2c: Trial Correlation & Reliability Coefficients

RQ2b: Trial-to-trial correlation analysis
RQ2c: ICC, Cronbach's Alpha, SEM, Fleiss' Kappa
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from scipy import stats
from sklearn.metrics import cohen_kappa_score
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = Path("results_experiment_final/data")
OUTPUT_DIR = Path("results_experiment_final/rq2_consistency")

print("\n" + "="*80)
print("RQ2b: TRIAL-TO-TRIAL CORRELATION ANALYSIS")
print("="*80 + "\n")

# Load data
df = pd.read_csv(DATA_DIR / "per_item_scores.csv")

# Pivot for correlation analysis
print("[1/2] Calculating trial-to-trial correlations...")

correlation_results = []

for (model, strategy), group in df.groupby(['model', 'strategy']):
    # Pivot to get trials as columns
    pivot = group.pivot_table(
        index=['student_id', 'question_number'],
        columns='trial_number',
        values='score'
    )
    
    n_trials = pivot.shape[1]
    
    if n_trials < 2:
        continue
    
    # Calculate correlation matrix
    corr_matrix = pivot.corr()
    
    # Calculate mean correlation (excluding diagonal)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    correlations = corr_matrix.where(mask).stack().values
    
    mean_corr = np.mean(correlations)
    median_corr = np.median(correlations)
    min_corr = np.min(correlations)
    max_corr = np.max(correlations)
    
    correlation_results.append({
        'model': model,
        'strategy': strategy,
        'n_trials': n_trials,
        'mean_correlation': mean_corr,
        'median_correlation': median_corr,
        'min_correlation': min_corr,
        'max_correlation': max_corr,
        'std_correlation': np.std(correlations)
    })
    
    # Save correlation matrix
    output_file = OUTPUT_DIR / f"correlation_matrix_{model}_{strategy}.csv"
    corr_matrix.to_csv(output_file)
    print(f"   ✓ {model.capitalize()} {strategy}: Mean r = {mean_corr:.4f}")

df_corr = pd.DataFrame(correlation_results)
output_file = OUTPUT_DIR / "trial_correlation_summary.csv"
df_corr.to_csv(output_file, index=False)
print(f"\n   ✓ Saved to: {output_file}")

# ============================================================================
print("\n" + "="*80)
print("RQ2c: RELIABILITY COEFFICIENTS")
print("="*80 + "\n")

print("[2/2] Calculating ICC, Cronbach's Alpha, SEM...")

def calculate_icc_2_1(data):
    """
    Calculate ICC(2,1) - Two-way random effects, absolute agreement, single rater
    """
    n_items = data.shape[0]
    n_raters = data.shape[1]
    
    # Mean squares
    grand_mean = np.mean(data)
    
    # Between items variance
    item_means = np.mean(data, axis=1)
    ms_rows = np.sum((item_means - grand_mean)**2) * n_raters / (n_items - 1)
    
    # Between raters variance
    rater_means = np.mean(data, axis=0)
    ms_cols = np.sum((rater_means - grand_mean)**2) * n_items / (n_raters - 1)
    
    # Residual variance
    residuals = data - item_means[:, np.newaxis] - rater_means + grand_mean
    ms_error = np.sum(residuals**2) / ((n_items - 1) * (n_raters - 1))
    
    # ICC(2,1)
    icc = (ms_rows - ms_error) / (ms_rows + (n_raters - 1) * ms_error + n_raters * (ms_cols - ms_error) / n_items)
    
    return icc

def calculate_cronbach_alpha(data):
    """Calculate Cronbach's Alpha"""
    n_items = data.shape[0]
    n_raters = data.shape[1]
    
    # Variance of each rater
    rater_variances = np.var(data, axis=0, ddof=1)
    
    # Variance of total scores
    total_scores = np.sum(data, axis=1)
    total_variance = np.var(total_scores, ddof=1)
    
    # Cronbach's alpha
    alpha = (n_raters / (n_raters - 1)) * (1 - np.sum(rater_variances) / total_variance)
    
    return alpha

def calculate_sem(data):
    """Calculate Standard Error of Measurement"""
    # Pooled standard deviation
    pooled_std = np.std(data)
    
    # ICC for reliability
    icc = calculate_icc_2_1(data)
    
    # SEM = SD * sqrt(1 - reliability)
    sem = pooled_std * np.sqrt(1 - icc)
    
    return sem

def calculate_fleiss_kappa(data):
    """Calculate Fleiss' Kappa for multiple raters"""
    # Convert continuous scores to ordinal categories for kappa
    # Using 0.5 grade boundaries
    data_cat = np.round(data * 2) / 2  # Round to nearest 0.5
    
    n_items = data_cat.shape[0]
    n_raters = data_cat.shape[1]
    categories = np.unique(data_cat)
    n_categories = len(categories)
    
    # Create frequency matrix
    freq_matrix = np.zeros((n_items, n_categories))
    for i, cat in enumerate(categories):
        freq_matrix[:, i] = np.sum(data_cat == cat, axis=1)
    
    # Calculate p_j (proportion of all assignments to category j)
    p_j = np.sum(freq_matrix, axis=0) / (n_items * n_raters)
    
    # Calculate P_i (extent of agreement for item i)
    P_i = (np.sum(freq_matrix**2, axis=1) - n_raters) / (n_raters * (n_raters - 1))
    
    # Calculate P_bar (mean of P_i)
    P_bar = np.mean(P_i)
    
    # Calculate P_e_bar (expected proportion of agreement)
    P_e_bar = np.sum(p_j**2)
    
    # Fleiss' Kappa
    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    
    return kappa

# Calculate for each model-strategy
reliability_results = []

for (model, strategy), group in df.groupby(['model', 'strategy']):
    # Pivot to matrix format
    pivot = group.pivot_table(
        index=['student_id', 'question_number'],
        columns='trial_number',
        values='score'
    )
    
    data_matrix = pivot.values
    n_items = data_matrix.shape[0]
    n_trials = data_matrix.shape[1]
    
    if n_trials < 2:
        continue
    
    # Calculate metrics
    icc = calculate_icc_2_1(data_matrix)
    alpha = calculate_cronbach_alpha(data_matrix)
    sem = calculate_sem(data_matrix)
    fleiss_k = calculate_fleiss_kappa(data_matrix)
    
    # Mean and SD across all scores
    mean_score = np.mean(data_matrix)
    sd_score = np.std(data_matrix)
    
    reliability_results.append({
        'model': model,
        'strategy': strategy,
        'n_items': n_items,
        'n_trials': n_trials,
        'icc_2_1': icc,
        'cronbach_alpha': alpha,
        'sem': sem,
        'fleiss_kappa': fleiss_k,
        'mean_score': mean_score,
        'sd_score': sd_score
    })
    
    print(f"   {model.upper():8} {strategy.capitalize():10}")
    print(f"      ICC(2,1): {icc:.4f}")
    print(f"      Cronbach's α: {alpha:.4f}")
    print(f"      SEM: {sem:.4f}")
    print(f"      Fleiss' κ: {fleiss_k:.4f}")
    print()

df_reliability = pd.DataFrame(reliability_results)
output_file = OUTPUT_DIR / "reliability_coefficients.csv"
df_reliability.to_csv(output_file, index=False)
print(f"   ✓ Saved to: {output_file}")

# Create comparison JSON
comparison = {}
for _, row in df_reliability.iterrows():
    key = f"{row['model']}_{row['strategy']}"
    comparison[key] = {
        'n_items': int(row['n_items']),
        'n_trials': int(row['n_trials']),
        'icc_2_1': float(row['icc_2_1']),
        'cronbach_alpha': float(row['cronbach_alpha']),
        'sem': float(row['sem']),
        'fleiss_kappa': float(row['fleiss_kappa']),
        'interpretation': {
            'icc': 'Excellent' if row['icc_2_1'] > 0.90 else 'Good' if row['icc_2_1'] > 0.75 else 'Fair',
            'alpha': 'Excellent' if row['cronbach_alpha'] > 0.90 else 'Good' if row['cronbach_alpha'] > 0.80 else 'Fair',
            'kappa': 'Substantial' if row['fleiss_kappa'] > 0.80 else 'Moderate' if row['fleiss_kappa'] > 0.60 else 'Fair'
        }
    }

output_file = OUTPUT_DIR / "reliability_comparison.json"
with open(output_file, 'w') as f:
    json.dump(comparison, f, indent=2)
print(f"   ✓ Saved comparison to: {output_file}")

# ============================================================================
print("\n" + "="*80)
print("RELIABILITY SUMMARY")
print("="*80 + "\n")

print("ICC(2,1) Interpretation:")
print("  > 0.90: Excellent reliability")
print("  > 0.75: Good reliability")
print("  > 0.50: Moderate reliability")
print()

print("Cronbach's Alpha Interpretation:")
print("  > 0.90: Excellent internal consistency")
print("  > 0.80: Good internal consistency")
print("  > 0.70: Acceptable")
print()

print("="*80)
print("OUTPUT FILES:")
print("="*80)
print(f"1. {OUTPUT_DIR}/trial_correlation_summary.csv")
print(f"2. {OUTPUT_DIR}/correlation_matrix_*.csv (per strategy)")
print(f"3. {OUTPUT_DIR}/reliability_coefficients.csv")
print(f"4. {OUTPUT_DIR}/reliability_comparison.json")
print("="*80 + "\n")
