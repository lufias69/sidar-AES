"""
RQ3: Model Comparison - Statistical Testing

Performs head-to-head statistical comparisons between models:
- Paired t-tests (parametric)
- Wilcoxon signed-rank tests (non-parametric)
- McNemar's test (for categorical agreement)
- Effect sizes (Cohen's d)
- Win/tie/loss analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.stats import ttest_rel, wilcoxon
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
OUTPUT_DIR = Path("results_experiment_final/rq3_model_comparison")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("RQ3: MODEL COMPARISON - STATISTICAL TESTING")
print("="*80 + "\n")

# Load data
print("Loading data...")
df = pd.read_csv(DATA_DIR / "per_item_scores.csv")
df_gold = pd.read_csv(DATA_DIR / "gold_standard.csv")

# Fix student_id format
df_gold['student_id'] = 'student_' + df_gold['student_id'].astype(str).str.zfill(2)
df_gold['question_number'] = df_gold['question_number'].astype(int)

print(f"  ✓ Per-item scores: {len(df)} records")
print(f"  ✓ Gold standard: {len(df_gold)} records")

# ============================================================================
# Helper Functions
# ============================================================================

def cohens_d(x, y):
    """Calculate Cohen's d effect size"""
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1)**2 + (ny-1)*np.std(y, ddof=1)**2) / dof)

def interpret_cohen_d(d):
    """Interpret Cohen's d effect size"""
    d_abs = abs(d)
    if d_abs < 0.2:
        return "Negligible"
    elif d_abs < 0.5:
        return "Small"
    elif d_abs < 0.8:
        return "Medium"
    else:
        return "Large"

def mcnemar_test(correct1, correct2):
    """McNemar's test for comparing two binary classifiers"""
    # Create contingency table
    n_both_correct = np.sum((correct1 == 1) & (correct2 == 1))
    n_both_incorrect = np.sum((correct1 == 0) & (correct2 == 0))
    n_only_1_correct = np.sum((correct1 == 1) & (correct2 == 0))
    n_only_2_correct = np.sum((correct1 == 0) & (correct2 == 1))
    
    # McNemar's test statistic
    b, c = n_only_1_correct, n_only_2_correct
    if b + c == 0:
        return 1.0  # No disagreement
    
    # Chi-square with continuity correction
    chi2 = (abs(b - c) - 1)**2 / (b + c)
    p_value = 1 - stats.chi2.cdf(chi2, 1)
    
    return p_value

# ============================================================================
# 1. Within-Strategy Comparisons (ChatGPT vs Gemini)
# ============================================================================
print("\n[1/3] Within-strategy comparisons (ChatGPT vs Gemini)...")

within_strategy_results = []

for strategy in ['zero-shot', 'few-shot', 'lenient']:
    print(f"\n  Strategy: {strategy}")
    
    # Get data for both models
    chatgpt_data = df[(df['model'] == 'chatgpt') & (df['strategy'] == strategy)]
    gemini_data = df[(df['model'] == 'gemini') & (df['strategy'] == strategy)]
    
    # Merge on student_id and question_number to get paired data
    merged = chatgpt_data.merge(
        gemini_data,
        on=['student_id', 'question_number', 'trial_number'],
        suffixes=('_chatgpt', '_gemini')
    )
    
    if len(merged) == 0:
        print(f"    ⚠ No paired data for {strategy}")
        continue
    
    scores_chatgpt = merged['score_chatgpt'].values
    scores_gemini = merged['score_gemini'].values
    
    # Paired t-test
    t_stat, t_pval = ttest_rel(scores_chatgpt, scores_gemini)
    
    # Wilcoxon signed-rank test
    w_stat, w_pval = wilcoxon(scores_chatgpt, scores_gemini)
    
    # Effect size
    effect_size = cohens_d(scores_chatgpt, scores_gemini)
    effect_interpret = interpret_cohen_d(effect_size)
    
    # Win/tie/loss
    wins = np.sum(scores_chatgpt > scores_gemini)
    ties = np.sum(scores_chatgpt == scores_gemini)
    losses = np.sum(scores_chatgpt < scores_gemini)
    
    # Mean differences
    mean_diff = np.mean(scores_chatgpt - scores_gemini)
    
    within_strategy_results.append({
        'comparison': f'ChatGPT vs Gemini ({strategy})',
        'strategy': strategy,
        'n_pairs': len(merged),
        'chatgpt_mean': round(np.mean(scores_chatgpt), 4),
        'gemini_mean': round(np.mean(scores_gemini), 4),
        'mean_diff': round(mean_diff, 4),
        't_statistic': round(t_stat, 4),
        't_pvalue': round(t_pval, 6),
        'wilcoxon_statistic': round(w_stat, 4),
        'wilcoxon_pvalue': round(w_pval, 6),
        'cohens_d': round(effect_size, 4),
        'effect_size': effect_interpret,
        'wins': int(wins),
        'ties': int(ties),
        'losses': int(losses),
        'significant_t': 'Yes' if t_pval < 0.05 else 'No',
        'significant_w': 'Yes' if w_pval < 0.05 else 'No'
    })
    
    sig_marker = "***" if t_pval < 0.001 else "**" if t_pval < 0.01 else "*" if t_pval < 0.05 else "ns"
    print(f"    Mean diff: {mean_diff:.4f}, t={t_stat:.2f}, p={t_pval:.6f} {sig_marker}")
    print(f"    Cohen's d: {effect_size:.3f} ({effect_interpret})")
    print(f"    Wins/Ties/Losses: {wins}/{ties}/{losses}")

df_within_strategy = pd.DataFrame(within_strategy_results)
df_within_strategy.to_csv(OUTPUT_DIR / "within_strategy_comparison.csv", index=False)
print(f"\n  ✓ Saved within_strategy_comparison.csv")

# ============================================================================
# 2. Across-Strategy Comparisons (within each model)
# ============================================================================
print("\n[2/3] Across-strategy comparisons (within each model)...")

across_strategy_results = []

for model in ['chatgpt', 'gemini']:
    print(f"\n  Model: {model.upper()}")
    
    strategies = ['zero-shot', 'few-shot', 'lenient']
    
    for i, strat1 in enumerate(strategies):
        for strat2 in strategies[i+1:]:
            
            data1 = df[(df['model'] == model) & (df['strategy'] == strat1)]
            data2 = df[(df['model'] == model) & (df['strategy'] == strat2)]
            
            # Merge on student_id and question_number
            merged = data1.merge(
                data2,
                on=['student_id', 'question_number', 'trial_number'],
                suffixes=(f'_{strat1}', f'_{strat2}')
            )
            
            if len(merged) == 0:
                continue
            
            scores1 = merged[f'score_{strat1}'].values
            scores2 = merged[f'score_{strat2}'].values
            
            # Paired t-test
            t_stat, t_pval = ttest_rel(scores1, scores2)
            
            # Wilcoxon
            w_stat, w_pval = wilcoxon(scores1, scores2)
            
            # Effect size
            effect_size = cohens_d(scores1, scores2)
            effect_interpret = interpret_cohen_d(effect_size)
            
            # Mean difference
            mean_diff = np.mean(scores1 - scores2)
            
            across_strategy_results.append({
                'model': model,
                'comparison': f'{strat1} vs {strat2}',
                'strategy1': strat1,
                'strategy2': strat2,
                'n_pairs': len(merged),
                'strat1_mean': round(np.mean(scores1), 4),
                'strat2_mean': round(np.mean(scores2), 4),
                'mean_diff': round(mean_diff, 4),
                't_statistic': round(t_stat, 4),
                't_pvalue': round(t_pval, 6),
                'wilcoxon_statistic': round(w_stat, 4),
                'wilcoxon_pvalue': round(w_pval, 6),
                'cohens_d': round(effect_size, 4),
                'effect_size': effect_interpret,
                'significant': 'Yes' if t_pval < 0.05 else 'No'
            })
            
            sig_marker = "***" if t_pval < 0.001 else "**" if t_pval < 0.01 else "*" if t_pval < 0.05 else "ns"
            print(f"    {strat1} vs {strat2}: diff={mean_diff:.4f}, p={t_pval:.6f} {sig_marker}, d={effect_size:.3f}")

df_across_strategy = pd.DataFrame(across_strategy_results)
df_across_strategy.to_csv(OUTPUT_DIR / "across_strategy_comparison.csv", index=False)
print(f"\n  ✓ Saved across_strategy_comparison.csv")

# ============================================================================
# 3. Agreement with Gold Standard - McNemar's Test
# ============================================================================
print("\n[3/3] Agreement with gold standard (McNemar's test)...")

# Merge with gold standard
df_with_gold = df.merge(
    df_gold[['student_id', 'question_number', 'gold_score']],
    on=['student_id', 'question_number'],
    how='inner'
)

# Define "correct" as within ±0.5 of gold standard
threshold = 0.5
df_with_gold['correct'] = (np.abs(df_with_gold['score'] - df_with_gold['gold_score']) <= threshold).astype(int)

mcnemar_results = []

for strategy in ['zero-shot', 'few-shot', 'lenient']:
    
    chatgpt_data = df_with_gold[(df_with_gold['model'] == 'chatgpt') & (df_with_gold['strategy'] == strategy)]
    gemini_data = df_with_gold[(df_with_gold['model'] == 'gemini') & (df_with_gold['strategy'] == strategy)]
    
    # Merge to get paired correctness
    merged = chatgpt_data.merge(
        gemini_data,
        on=['student_id', 'question_number', 'trial_number'],
        suffixes=('_chatgpt', '_gemini')
    )
    
    if len(merged) == 0:
        continue
    
    correct_chatgpt = merged['correct_chatgpt'].values
    correct_gemini = merged['correct_gemini'].values
    
    # McNemar's test
    p_value = mcnemar_test(correct_chatgpt, correct_gemini)
    
    # Accuracy
    acc_chatgpt = np.mean(correct_chatgpt) * 100
    acc_gemini = np.mean(correct_gemini) * 100
    
    mcnemar_results.append({
        'strategy': strategy,
        'n_pairs': len(merged),
        'chatgpt_accuracy': round(acc_chatgpt, 2),
        'gemini_accuracy': round(acc_gemini, 2),
        'accuracy_diff': round(acc_chatgpt - acc_gemini, 2),
        'mcnemar_pvalue': round(p_value, 6),
        'significant': 'Yes' if p_value < 0.05 else 'No'
    })
    
    sig_marker = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    print(f"  {strategy}: ChatGPT={acc_chatgpt:.1f}%, Gemini={acc_gemini:.1f}%, p={p_value:.6f} {sig_marker}")

df_mcnemar = pd.DataFrame(mcnemar_results)
df_mcnemar.to_csv(OUTPUT_DIR / "mcnemar_test_results.csv", index=False)
print(f"\n  ✓ Saved mcnemar_test_results.csv")

# ============================================================================
# Summary Statistics
# ============================================================================
print("\nGenerating summary...")

summary = {
    'within_strategy': {
        'all_comparisons_significant': bool(df_within_strategy['significant_t'].eq('Yes').all()) if len(df_within_strategy) > 0 else None,
        'chatgpt_better_count': int(df_within_strategy[df_within_strategy['mean_diff'] > 0].shape[0]) if len(df_within_strategy) > 0 else 0,
        'mean_effect_size': float(df_within_strategy['cohens_d'].mean()) if len(df_within_strategy) > 0 else None,
        'largest_difference': {
            'strategy': df_within_strategy.loc[df_within_strategy['mean_diff'].abs().idxmax(), 'strategy'] if len(df_within_strategy) > 0 else None,
            'diff': float(df_within_strategy['mean_diff'].abs().max()) if len(df_within_strategy) > 0 else None
        }
    },
    'across_strategy': {
        'chatgpt': {
            'significant_differences': int(df_across_strategy[
                (df_across_strategy['model'] == 'chatgpt') & 
                (df_across_strategy['significant'] == 'Yes')
            ].shape[0]) if len(df_across_strategy) > 0 and 'model' in df_across_strategy.columns else 0
        },
        'gemini': {
            'significant_differences': int(df_across_strategy[
                (df_across_strategy['model'] == 'gemini') & 
                (df_across_strategy['significant'] == 'Yes')
            ].shape[0]) if len(df_across_strategy) > 0 and 'model' in df_across_strategy.columns else 0
        }
    },
    'agreement': {
        'mcnemar_significant_count': int(df_mcnemar[df_mcnemar['significant'] == 'Yes'].shape[0]) if len(df_mcnemar) > 0 else 0,
        'best_strategy_chatgpt': df_mcnemar.loc[df_mcnemar['chatgpt_accuracy'].idxmax(), 'strategy'] if len(df_mcnemar) > 0 else None,
        'best_strategy_gemini': df_mcnemar.loc[df_mcnemar['gemini_accuracy'].idxmax(), 'strategy'] if len(df_mcnemar) > 0 else None
    }
}

with open(OUTPUT_DIR / "comparison_summary.json", 'w') as f:
    json.dump(summary, f, indent=2)

print(f"  ✓ Saved comparison_summary.json")

# ============================================================================
# Display Summary
# ============================================================================
print("\n" + "="*80)
print("MODEL COMPARISON SUMMARY")
print("="*80 + "\n")

print("Within-Strategy Comparisons (ChatGPT vs Gemini):")
print(df_within_strategy[['strategy', 'mean_diff', 't_pvalue', 'cohens_d', 'effect_size', 'significant_t']].to_string(index=False))

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nOutput files:")
print(f"  • within_strategy_comparison.csv - ChatGPT vs Gemini per strategy")
print(f"  • across_strategy_comparison.csv - Strategy comparisons within models")
print(f"  • mcnemar_test_results.csv - Agreement comparison with gold standard")
print(f"  • comparison_summary.json - Summary statistics")
print("="*80 + "\n")
