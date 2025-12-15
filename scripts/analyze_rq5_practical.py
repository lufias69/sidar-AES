"""
RQ5: Practical Implications

Analyzes practical deployment considerations:
- Cost analysis (API tokens and pricing)
- Processing speed and throughput
- Best strategy recommendations
- Trade-offs between accuracy, cost, and speed
- Deployment guidelines
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
INPUT_RQ1 = Path("results_experiment_final/rq1_validity")
INPUT_RQ2 = Path("results_experiment_final/rq2_consistency")
INPUT_RQ4 = Path("results_experiment_final/rq4_error_analysis")
OUTPUT_DIR = Path("results_experiment_final/rq5_practical")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# API Pricing (as of December 2024)
PRICING = {
    'chatgpt': {
        'input': 2.50 / 1_000_000,   # $2.50 per 1M input tokens (GPT-4o)
        'output': 10.00 / 1_000_000  # $10.00 per 1M output tokens
    },
    'gemini': {
        'input': 0.075 / 1_000_000,   # $0.075 per 1M input tokens (Gemini 2.5 Flash)
        'output': 0.30 / 1_000_000    # $0.30 per 1M output tokens
    }
}

print("\n" + "="*80)
print("RQ5: PRACTICAL IMPLICATIONS ANALYSIS")
print("="*80 + "\n")

# Load data
print("Loading data...")
df_experiment = pd.read_csv(DATA_DIR / "experiment_data_complete.csv")
df_validity = pd.read_csv(INPUT_RQ1 / "validity_summary.csv")
df_reliability = pd.read_csv(INPUT_RQ2 / "reliability_coefficients.csv")
df_error = pd.read_csv(INPUT_RQ4 / "error_summary.csv")

print(f"  ✓ Experiment data: {len(df_experiment)} records")
print(f"  ✓ Validity metrics loaded")
print(f"  ✓ Reliability metrics loaded")
print(f"  ✓ Error metrics loaded")

# ============================================================================
# 1. Cost Analysis
# ============================================================================
print("\n[1/4] Calculating cost metrics...")

cost_analysis = []

for model in df_experiment['model'].unique():
    for strategy in df_experiment['strategy'].unique():
        
        data = df_experiment[(df_experiment['model'] == model) & (df_experiment['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        # Token statistics
        total_tokens = data['tokens_used'].sum()
        mean_tokens = data['tokens_used'].mean()
        median_tokens = data['tokens_used'].median()
        
        # Estimate input/output split (typically 60/40 for grading tasks)
        input_tokens = total_tokens * 0.6
        output_tokens = total_tokens * 0.4
        
        # Calculate costs
        input_cost = input_tokens * PRICING[model]['input']
        output_cost = output_tokens * PRICING[model]['output']
        total_cost = input_cost + output_cost
        
        # Per-essay cost
        n_essays = len(data)
        cost_per_essay = total_cost / n_essays if n_essays > 0 else 0
        
        cost_analysis.append({
            'model': model,
            'strategy': strategy,
            'n_essays': int(n_essays),
            'total_tokens': int(total_tokens),
            'mean_tokens_per_essay': round(mean_tokens, 0),
            'median_tokens_per_essay': round(median_tokens, 0),
            'total_cost_usd': round(total_cost, 4),
            'cost_per_essay_usd': round(cost_per_essay, 6),
            'cost_per_100_essays_usd': round(cost_per_essay * 100, 4)
        })
        
        print(f"  {model.upper()} {strategy}: ${cost_per_essay:.6f}/essay, ${cost_per_essay*100:.4f}/100 essays")

df_cost = pd.DataFrame(cost_analysis)
df_cost.to_csv(OUTPUT_DIR / "cost_analysis.csv", index=False)
print(f"\n  ✓ Saved cost_analysis.csv")

# ============================================================================
# 2. Performance Analysis (Speed)
# ============================================================================
print("\n[2/4] Analyzing processing speed...")

performance_analysis = []

for model in df_experiment['model'].unique():
    for strategy in df_experiment['strategy'].unique():
        
        data = df_experiment[(df_experiment['model'] == model) & (df_experiment['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        # Time statistics
        mean_time = data['api_call_time'].mean()
        median_time = data['api_call_time'].median()
        std_time = data['api_call_time'].std()
        
        # Throughput (essays per hour)
        essays_per_hour = 3600 / mean_time if mean_time > 0 else 0
        
        performance_analysis.append({
            'model': model,
            'strategy': strategy,
            'mean_time_seconds': round(mean_time, 2),
            'median_time_seconds': round(median_time, 2),
            'std_time_seconds': round(std_time, 2),
            'essays_per_hour': round(essays_per_hour, 1),
            'time_for_100_essays_minutes': round(mean_time * 100 / 60, 1)
        })
        
        print(f"  {model.upper()} {strategy}: {mean_time:.2f}s/essay, {essays_per_hour:.0f} essays/hour")

df_performance = pd.DataFrame(performance_analysis)
df_performance.to_csv(OUTPUT_DIR / "performance_analysis.csv", index=False)
print(f"\n  ✓ Saved performance_analysis.csv")

# ============================================================================
# 3. Comprehensive Comparison & Recommendations
# ============================================================================
print("\n[3/4] Generating comprehensive comparison...")

# Merge all metrics - ensure consistent formatting
df_validity['model'] = df_validity['model'].str.strip().str.lower()
df_validity['strategy'] = df_validity['strategy'].str.strip().str.lower()
df_reliability['model'] = df_reliability['model'].str.strip().str.lower()
df_reliability['strategy'] = df_reliability['strategy'].str.strip().str.lower()
df_error['model'] = df_error['model'].str.strip().str.lower()
df_error['strategy'] = df_error['strategy'].str.strip().str.lower()

# Start with validity but drop mae/rmse/bias - use error analysis versions instead
df_comprehensive = df_validity.drop(columns=['mae', 'rmse', 'bias'], errors='ignore')

df_comprehensive = df_comprehensive.merge(
    df_reliability[['model', 'strategy', 'icc_2_1', 'cronbach_alpha', 'fleiss_kappa']],
    on=['model', 'strategy'],
    how='left'
)

df_comprehensive = df_comprehensive.merge(
    df_error[['model', 'strategy', 'mae', 'bias']],
    on=['model', 'strategy'],
    how='left'
)

df_comprehensive = df_comprehensive.merge(
    df_cost[['model', 'strategy', 'cost_per_essay_usd', 'mean_tokens_per_essay']],
    on=['model', 'strategy'],
    how='left'
)

df_comprehensive = df_comprehensive.merge(
    df_performance[['model', 'strategy', 'mean_time_seconds', 'essays_per_hour']],
    on=['model', 'strategy'],
    how='left'
)

# Calculate composite scores (normalize and weight)
def normalize(series):
    """Min-max normalization"""
    return (series - series.min()) / (series.max() - series.min())

# Higher is better for these
df_comprehensive['norm_qwk'] = normalize(df_comprehensive['qwk'].fillna(0))
df_comprehensive['norm_icc'] = normalize(df_comprehensive['icc_2_1'].fillna(0))

# Lower is better for these (invert)
df_comprehensive['norm_mae'] = 1 - normalize(df_comprehensive['mae'].fillna(0))
df_comprehensive['norm_cost'] = 1 - normalize(df_comprehensive['cost_per_essay_usd'].fillna(0))
df_comprehensive['norm_time'] = 1 - normalize(df_comprehensive['mean_time_seconds'].fillna(0))

# Composite scores with different priorities
df_comprehensive['score_accuracy_focused'] = (
    df_comprehensive['norm_qwk'] * 0.4 +
    df_comprehensive['norm_icc'] * 0.3 +
    df_comprehensive['norm_mae'] * 0.3
)

df_comprehensive['score_balanced'] = (
    df_comprehensive['norm_qwk'] * 0.25 +
    df_comprehensive['norm_icc'] * 0.25 +
    df_comprehensive['norm_mae'] * 0.20 +
    df_comprehensive['norm_cost'] * 0.15 +
    df_comprehensive['norm_time'] * 0.15
)

df_comprehensive['score_cost_focused'] = (
    df_comprehensive['norm_qwk'] * 0.20 +
    df_comprehensive['norm_mae'] * 0.20 +
    df_comprehensive['norm_cost'] * 0.40 +
    df_comprehensive['norm_time'] * 0.20
)

# Select key columns for output
output_cols = ['model', 'strategy', 'qwk', 'exact_agreement_pct', 'icc_2_1', 'mae', 'bias',
               'cost_per_essay_usd', 'mean_time_seconds', 'essays_per_hour',
               'score_accuracy_focused', 'score_balanced', 'score_cost_focused']

df_comprehensive[output_cols].to_csv(OUTPUT_DIR / "comprehensive_comparison.csv", index=False)
print(f"  ✓ Saved comprehensive_comparison.csv")

# ============================================================================
# 4. Recommendations
# ============================================================================
print("\n[4/4] Generating recommendations...")

recommendations = {
    'best_overall': df_comprehensive.loc[df_comprehensive['score_balanced'].idxmax(), ['model', 'strategy']].to_dict(),
    'best_accuracy': df_comprehensive.loc[df_comprehensive['score_accuracy_focused'].idxmax(), ['model', 'strategy']].to_dict(),
    'best_cost_effective': df_comprehensive.loc[df_comprehensive['score_cost_focused'].idxmax(), ['model', 'strategy']].to_dict(),
    'lowest_cost': df_comprehensive.loc[df_comprehensive['cost_per_essay_usd'].idxmin(), ['model', 'strategy', 'cost_per_essay_usd']].to_dict(),
    'fastest': df_comprehensive.loc[df_comprehensive['mean_time_seconds'].idxmin(), ['model', 'strategy', 'mean_time_seconds', 'essays_per_hour']].to_dict(),
    'most_reliable': df_comprehensive.loc[df_comprehensive['icc_2_1'].idxmax(), ['model', 'strategy', 'icc_2_1']].to_dict(),
    'most_valid': df_comprehensive.loc[df_comprehensive['qwk'].idxmax(), ['model', 'strategy', 'qwk']].to_dict(),
    
    'use_cases': {
        'high_stakes_assessment': {
            'recommended': 'ChatGPT zero-shot',
            'reason': 'Highest validity (QWK), good reliability, lowest bias, acceptable cost'
        },
        'formative_feedback': {
            'recommended': 'Gemini zero-shot',
            'reason': 'Best cost-effectiveness, fastest processing, acceptable accuracy'
        },
        'large_scale_grading': {
            'recommended': 'Gemini lenient',
            'reason': 'Lowest cost, reasonable reliability, but watch for over-grading bias'
        },
        'research_validation': {
            'recommended': 'ChatGPT few-shot',
            'reason': 'High reliability (ICC), good validity, consistent performance'
        }
    },
    
    'warnings': {
        'lenient_strategy': 'Shows significant over-grading bias (+0.44 to +0.47). Use with caution for summative assessment.',
        'gemini_few_shot': 'Low consistency with high variance items. Requires multiple trials or avoid.',
        'cost_consideration': f'ChatGPT costs ~{df_cost[df_cost["model"]=="chatgpt"]["cost_per_essay_usd"].mean()/df_cost[df_cost["model"]=="gemini"]["cost_per_essay_usd"].mean():.1f}x more than Gemini per essay.'
    }
}

with open(OUTPUT_DIR / "recommendations.json", 'w', encoding='utf-8') as f:
    json.dump(recommendations, f, indent=2, ensure_ascii=False)

print(f"  ✓ Saved recommendations.json")

# ============================================================================
# Cost-Benefit Matrix
# ============================================================================
print("\nCreating cost-benefit matrix...")

cost_benefit = df_comprehensive[['model', 'strategy', 'qwk', 'mae', 'cost_per_essay_usd', 
                                 'mean_time_seconds', 'score_balanced']].copy()

# Add rankings
cost_benefit['accuracy_rank'] = cost_benefit['qwk'].rank(ascending=False)
cost_benefit['cost_rank'] = cost_benefit['cost_per_essay_usd'].rank(ascending=True)
cost_benefit['speed_rank'] = cost_benefit['mean_time_seconds'].rank(ascending=True)
cost_benefit['overall_rank'] = cost_benefit['score_balanced'].rank(ascending=False)

cost_benefit.to_csv(OUTPUT_DIR / "cost_benefit_matrix.csv", index=False)
print(f"  ✓ Saved cost_benefit_matrix.csv")

# ============================================================================
# Display Summary
# ============================================================================
print("\n" + "="*80)
print("PRACTICAL IMPLICATIONS SUMMARY")
print("="*80 + "\n")

print("Recommendations by Use Case:")
for use_case, rec in recommendations['use_cases'].items():
    print(f"\n{use_case.replace('_', ' ').title()}:")
    print(f"  → {rec['recommended']}")
    print(f"     Reason: {rec['reason']}")

print("\n" + "-"*80)
print("Cost Comparison (per essay):")
for _, row in df_cost[['model', 'strategy', 'cost_per_essay_usd', 'cost_per_100_essays_usd']].iterrows():
    print(f"  {row['model'].upper()} {row['strategy']}: ${row['cost_per_essay_usd']:.6f} (${row['cost_per_100_essays_usd']:.2f}/100)")

print("\n" + "-"*80)
print("Speed Comparison (throughput):")
for _, row in df_performance[['model', 'strategy', 'essays_per_hour', 'time_for_100_essays_minutes']].iterrows():
    print(f"  {row['model'].upper()} {row['strategy']}: {row['essays_per_hour']:.0f} essays/hour ({row['time_for_100_essays_minutes']:.1f} min/100)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nOutput files:")
print(f"  • cost_analysis.csv - Token usage and costs")
print(f"  • performance_analysis.csv - Speed and throughput")
print(f"  • comprehensive_comparison.csv - All metrics combined")
print(f"  • cost_benefit_matrix.csv - Rankings and trade-offs")
print(f"  • recommendations.json - Strategic recommendations")
print("="*80 + "\n")
