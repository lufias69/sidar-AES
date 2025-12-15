"""
RQ2a: Per-Item Consistency Analysis

Untuk setiap (student, question) combination:
- Hitung consistency metrics across trials
- Identify high-variance items (inconsistent scoring)
- Compare ChatGPT vs Gemini consistency
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
OUTPUT_DIR = Path("results_experiment_final/rq2_consistency")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("RQ2a: PER-ITEM CONSISTENCY ANALYSIS")
print("="*80 + "\n")

# Load per-item scores
print("[1/4] Loading per-item scores...")
df = pd.read_csv(DATA_DIR / "per_item_scores.csv")
print(f"   ✓ Loaded {len(df)} scores")
print(f"   ✓ Models: {df['model'].unique().tolist()}")
print(f"   ✓ Strategies: {df['strategy'].unique().tolist()}")

# Calculate per-item statistics
print("\n[2/4] Calculating per-item consistency metrics...")

results = []

# Group by model, strategy, student, question
grouped = df.groupby(['model', 'strategy', 'student_id', 'student_name', 'question_number'])

for (model, strategy, student_id, student_name, question_number), group in grouped:
    scores = group['score'].values
    n_trials = len(scores)
    
    if n_trials < 2:
        continue
    
    # Calculate statistics
    mean_score = np.mean(scores)
    std_dev = np.std(scores, ddof=1) if n_trials > 1 else 0
    variance = np.var(scores, ddof=1) if n_trials > 1 else 0
    min_score = np.min(scores)
    max_score = np.max(scores)
    score_range = max_score - min_score
    
    # Coefficient of variation (CV) - only if mean > 0
    cv = (std_dev / mean_score * 100) if mean_score > 0 else 0
    
    # Classify consistency
    if std_dev <= 0.2:
        consistency = "Excellent"
    elif std_dev <= 0.4:
        consistency = "Good"
    elif std_dev <= 0.6:
        consistency = "Fair"
    else:
        consistency = "Poor"
    
    results.append({
        'model': model,
        'strategy': strategy,
        'student_id': student_id,
        'student_name': student_name,
        'question_number': question_number,
        'n_trials': n_trials,
        'mean_score': mean_score,
        'std_dev': std_dev,
        'variance': variance,
        'min_score': min_score,
        'max_score': max_score,
        'range': score_range,
        'cv_percent': cv,
        'consistency': consistency,
        'all_scores': ','.join([f"{s:.2f}" for s in scores])
    })

df_results = pd.DataFrame(results)
print(f"   ✓ Analyzed {len(df_results)} items")

# Save per-item variance
output_file = OUTPUT_DIR / "per_item_variance.csv"
df_results.to_csv(output_file, index=False)
print(f"   ✓ Saved to: {output_file}")

# Identify high-variance items
print("\n[3/4] Identifying high-variance items...")

# High variance: SD > 0.5 OR Range > 1.5
high_variance = df_results[
    (df_results['std_dev'] > 0.5) | (df_results['range'] > 1.5)
].sort_values('std_dev', ascending=False)

output_file = OUTPUT_DIR / "high_variance_items.csv"
high_variance.to_csv(output_file, index=False)
print(f"   ✓ Found {len(high_variance)} high-variance items")
print(f"   ✓ Saved to: {output_file}")

if len(high_variance) > 0:
    print(f"\n   Top 5 Most Inconsistent Items:")
    for i, row in high_variance.head().iterrows():
        print(f"   {row['model']:8} {row['strategy']:10} Student {row['student_id']} Q{row['question_number']}: "
              f"SD={row['std_dev']:.3f}, Range={row['range']:.2f}")

# Compare models and strategies
print("\n[4/4] Comparing consistency across models and strategies...")

# Summary by model and strategy
summary = df_results.groupby(['model', 'strategy']).agg({
    'std_dev': ['mean', 'median', 'std'],
    'range': ['mean', 'median', 'max'],
    'cv_percent': ['mean', 'median'],
    'n_trials': 'first'
}).round(4)

summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary = summary.reset_index()

output_file = OUTPUT_DIR / "consistency_summary_by_strategy.csv"
summary.to_csv(output_file, index=False)
print(f"   ✓ Saved summary to: {output_file}")

# Create comparison JSON
comparison = {}

for (model, strategy), group in df_results.groupby(['model', 'strategy']):
    key = f"{model}_{strategy}"
    comparison[key] = {
        'n_items': len(group),
        'n_trials': int(group['n_trials'].iloc[0]),
        'mean_std_dev': float(group['std_dev'].mean()),
        'median_std_dev': float(group['std_dev'].median()),
        'mean_range': float(group['range'].mean()),
        'max_range': float(group['range'].max()),
        'mean_cv': float(group['cv_percent'].mean()),
        'excellent_count': int((group['consistency'] == 'Excellent').sum()),
        'good_count': int((group['consistency'] == 'Good').sum()),
        'fair_count': int((group['consistency'] == 'Fair').sum()),
        'poor_count': int((group['consistency'] == 'Poor').sum()),
        'high_variance_count': int(((group['std_dev'] > 0.5) | (group['range'] > 1.5)).sum())
    }

output_file = OUTPUT_DIR / "consistency_comparison.json"
with open(output_file, 'w') as f:
    json.dump(comparison, f, indent=2)
print(f"   ✓ Saved comparison to: {output_file}")

# Print summary
print("\n" + "="*80)
print("CONSISTENCY SUMMARY")
print("="*80 + "\n")

for (model, strategy), group in df_results.groupby(['model', 'strategy']):
    print(f"{model.upper()} - {strategy.capitalize()}:")
    print(f"  Items analyzed: {len(group)}")
    print(f"  Trials per item: {group['n_trials'].iloc[0]}")
    print(f"  Mean SD: {group['std_dev'].mean():.4f}")
    print(f"  Median SD: {group['std_dev'].median():.4f}")
    print(f"  Mean Range: {group['range'].mean():.4f}")
    print(f"  High variance items: {((group['std_dev'] > 0.5) | (group['range'] > 1.5)).sum()}")
    print(f"  Consistency distribution:")
    print(f"    Excellent (SD≤0.2): {(group['consistency'] == 'Excellent').sum()}")
    print(f"    Good (SD≤0.4): {(group['consistency'] == 'Good').sum()}")
    print(f"    Fair (SD≤0.6): {(group['consistency'] == 'Fair').sum()}")
    print(f"    Poor (SD>0.6): {(group['consistency'] == 'Poor').sum()}")
    print()

print("="*80)
print("OUTPUT FILES:")
print("="*80)
print(f"1. {OUTPUT_DIR}/per_item_variance.csv")
print(f"2. {OUTPUT_DIR}/high_variance_items.csv")
print(f"3. {OUTPUT_DIR}/consistency_summary_by_strategy.csv")
print(f"4. {OUTPUT_DIR}/consistency_comparison.json")
print("="*80 + "\n")
