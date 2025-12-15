"""
RQ4: Model Comparison - ChatGPT vs Gemini

This script compares:
1. Quality metrics (agreement, accuracy, error)
2. Performance across strategies
3. Efficiency and cost considerations
4. Statistical significance testing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
METRICS_DIR = ANALYSIS_DIR / "metrics"
TABLES_DIR = ANALYSIS_DIR / "tables"
FIGURES_DIR = ANALYSIS_DIR / "figures" / "model_comparison"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_reliability_metrics():
    """Load reliability metrics from RQ1 analysis"""
    print("\n" + "="*70)
    print("LOADING RELIABILITY METRICS")
    print("="*70)
    
    reliability_file = METRICS_DIR / "reliability_vs_expert.csv"
    df = pd.read_csv(reliability_file)
    
    print(f"✅ Loaded {len(df)} strategy comparisons")
    print(f"   Models: {df['model'].unique()}")
    print(f"   Strategies: {df['strategy'].unique()}")
    
    return df

def calculate_effect_size(group1, group2, metric='cohens_d'):
    """Calculate effect size between two groups"""
    
    if metric == 'cohens_d':
        # Cohen's d
        mean_diff = group1.mean() - group2.mean()
        pooled_std = np.sqrt((group1.std()**2 + group2.std()**2) / 2)
        return mean_diff / pooled_std if pooled_std > 0 else 0
    
    elif metric == 'cliff_delta':
        # Cliff's Delta (non-parametric)
        n1, n2 = len(group1), len(group2)
        if n1 == 0 or n2 == 0:
            return 0
        
        greater = sum(1 for x in group1 for y in group2 if x > y)
        lesser = sum(1 for x in group1 for y in group2 if x < y)
        
        return (greater - lesser) / (n1 * n2)

def interpret_cohens_d(d):
    """Interpret Cohen's d effect size"""
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"

def interpret_cliff_delta(delta):
    """Interpret Cliff's Delta effect size"""
    delta = abs(delta)
    if delta < 0.147:
        return "negligible"
    elif delta < 0.33:
        return "small"
    elif delta < 0.474:
        return "medium"
    else:
        return "large"

def compare_models_by_strategy(df):
    """Compare ChatGPT vs Gemini for each strategy"""
    
    print("\n" + "="*70)
    print("MODEL COMPARISON BY STRATEGY")
    print("="*70)
    
    strategies = df['strategy'].unique()
    results = []
    
    for strategy in strategies:
        print(f"\n{'─'*70}")
        print(f"STRATEGY: {strategy.upper()}")
        print(f"{'─'*70}")
        
        chatgpt = df[(df['model'] == 'chatgpt') & (df['strategy'] == strategy)]
        gemini = df[(df['model'] == 'gemini') & (df['strategy'] == strategy)]
        
        if len(chatgpt) == 0 or len(gemini) == 0:
            print("  ⚠️  Missing data for comparison")
            continue
        
        # Get metrics
        metrics = ['mae', 'exact_match', 'cohens_kappa', 'pearson_r']
        
        for metric in metrics:
            chat_val = chatgpt[metric].values[0]
            gem_val = gemini[metric].values[0]
            
            # Calculate difference
            if metric == 'mae':
                diff = chat_val - gem_val  # Lower is better
                pct_diff = ((chat_val - gem_val) / gem_val) * 100
                winner = 'ChatGPT' if chat_val < gem_val else 'Gemini'
            else:
                diff = chat_val - gem_val  # Higher is better
                pct_diff = ((chat_val - gem_val) / gem_val) * 100
                winner = 'ChatGPT' if chat_val > gem_val else 'Gemini'
            
            results.append({
                'strategy': strategy,
                'metric': metric,
                'chatgpt': chat_val,
                'gemini': gem_val,
                'difference': diff,
                'percent_diff': pct_diff,
                'winner': winner
            })
            
            print(f"\n  {metric.upper()}:")
            print(f"    ChatGPT: {chat_val:.4f}")
            print(f"    Gemini:  {gem_val:.4f}")
            print(f"    Diff:    {diff:+.4f} ({pct_diff:+.1f}%)")
            print(f"    Winner:  {winner}")
    
    return pd.DataFrame(results)

def create_model_comparison_plots(comparison_df):
    """Create visualization comparing models across strategies"""
    
    print("\n" + "="*70)
    print("CREATING MODEL COMPARISON VISUALIZATIONS")
    print("="*70)
    
    metrics = comparison_df['metric'].unique()
    strategies = comparison_df['strategy'].unique()
    
    # 1. Bar chart comparing models for each metric
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        data = comparison_df[comparison_df['metric'] == metric]
        
        x = np.arange(len(strategies))
        width = 0.35
        
        chatgpt_vals = [data[data['strategy'] == s]['chatgpt'].values[0] for s in strategies]
        gemini_vals = [data[data['strategy'] == s]['gemini'].values[0] for s in strategies]
        
        bars1 = ax.bar(x - width/2, chatgpt_vals, width, label='ChatGPT', color='#2ecc71', alpha=0.8)
        bars2 = ax.bar(x + width/2, gemini_vals, width, label='Gemini', color='#3498db', alpha=0.8)
        
        ax.set_xlabel('Strategy', fontsize=12, fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(f'{metric.replace("_", " ").title()} Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(strategies, rotation=45, ha='right')
        ax.legend(loc='best', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_13_model_metrics_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()
    
    # 2. Percentage difference heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pivot_data = comparison_df.pivot(index='metric', columns='strategy', values='percent_diff')
    
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                cbar_kws={'label': 'Percentage Difference (ChatGPT vs Gemini)'},
                linewidths=1, linecolor='white', ax=ax)
    
    ax.set_title('Model Performance Difference (% Change)\nPositive = ChatGPT Better, Negative = Gemini Better',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Metric', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_14_model_difference_heatmap.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()
    
    # 3. Winner summary
    fig, ax = plt.subplots(figsize=(10, 6))
    
    winner_counts = comparison_df.groupby(['strategy', 'winner']).size().unstack(fill_value=0)
    winner_counts.plot(kind='bar', stacked=True, ax=ax, 
                      color=['#2ecc71', '#3498db'], alpha=0.8)
    
    ax.set_title('Model Wins by Strategy (across 4 metrics)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Metrics Won', fontsize=12, fontweight='bold')
    ax.legend(title='Winner', fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add count labels
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_15_model_wins_summary.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()

def overall_model_comparison(df):
    """Overall comparison across all strategies"""
    
    print("\n" + "="*70)
    print("OVERALL MODEL COMPARISON (ALL STRATEGIES)")
    print("="*70)
    
    chatgpt_data = df[df['model'] == 'chatgpt']
    gemini_data = df[df['model'] == 'gemini']
    
    metrics = ['mae', 'exact_match', 'cohens_kappa', 'pearson_r']
    
    results = []
    
    for metric in metrics:
        chat_vals = chatgpt_data[metric].values
        gem_vals = gemini_data[metric].values
        
        chat_mean = chat_vals.mean()
        chat_std = chat_vals.std()
        gem_mean = gem_vals.mean()
        gem_std = gem_vals.std()
        
        # Statistical test
        t_stat, p_value = stats.ttest_ind(chat_vals, gem_vals)
        
        # Effect size
        cohens_d = calculate_effect_size(chat_vals, gem_vals, 'cohens_d')
        cliff_delta = calculate_effect_size(chat_vals, gem_vals, 'cliff_delta')
        
        results.append({
            'metric': metric,
            'chatgpt_mean': chat_mean,
            'chatgpt_std': chat_std,
            'gemini_mean': gem_mean,
            'gemini_std': gem_std,
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'cohens_d_interpretation': interpret_cohens_d(cohens_d),
            'cliff_delta': cliff_delta,
            'cliff_delta_interpretation': interpret_cliff_delta(cliff_delta)
        })
        
        print(f"\n  {metric.upper()}:")
        print(f"    ChatGPT: {chat_mean:.4f} ± {chat_std:.4f}")
        print(f"    Gemini:  {gem_mean:.4f} ± {gem_std:.4f}")
        print(f"    t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
        print(f"    Cohen's d: {cohens_d:.4f} ({interpret_cohens_d(cohens_d)})")
        print(f"    Cliff's Δ: {cliff_delta:.4f} ({interpret_cliff_delta(cliff_delta)})")
        
        if p_value < 0.05:
            winner = 'ChatGPT' if (metric == 'mae' and chat_mean < gem_mean) or \
                                 (metric != 'mae' and chat_mean > gem_mean) else 'Gemini'
            print(f"    ✅ Significant difference (p < 0.05): {winner} is better")
        else:
            print(f"    ⚠️  No significant difference (p ≥ 0.05)")
    
    return pd.DataFrame(results)

def create_overall_comparison_plot(overall_df):
    """Create overall model comparison visualization"""
    
    print("\n" + "="*70)
    print("CREATING OVERALL COMPARISON VISUALIZATION")
    print("="*70)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, row in overall_df.iterrows():
        ax = axes[idx]
        metric = row['metric']
        
        # Bar plot with error bars
        models = ['ChatGPT', 'Gemini']
        means = [row['chatgpt_mean'], row['gemini_mean']]
        stds = [row['chatgpt_std'], row['gemini_std']]
        
        colors = ['#2ecc71', '#3498db']
        bars = ax.bar(models, means, yerr=stds, capsize=10, 
                     color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        # Highlight winner
        if row['p_value'] < 0.05:
            if (metric == 'mae' and row['chatgpt_mean'] < row['gemini_mean']) or \
               (metric != 'mae' and row['chatgpt_mean'] > row['gemini_mean']):
                bars[0].set_edgecolor('gold')
                bars[0].set_linewidth(4)
            else:
                bars[1].set_edgecolor('gold')
                bars[1].set_linewidth(4)
        
        ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=12, fontweight='bold')
        ax.set_title(f'{metric.replace("_", " ").title()}\n(Cohen\'s d={row["cohens_d"]:.3f}, p={row["p_value"]:.4f})',
                    fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, mean, std in zip(bars, means, stds):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std,
                   f'{mean:.3f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.suptitle('Overall Model Comparison (Averaged Across Strategies)\nGold Border = Significantly Better (p < 0.05)',
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    output_file = FIGURES_DIR / "figure_16_overall_model_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()

def main():
    """Main execution"""
    
    print("\n" + "="*70)
    print("RQ4: MODEL COMPARISON - CHATGPT VS GEMINI")
    print("="*70)
    
    # Load data
    reliability_df = load_reliability_metrics()
    
    # Strategy-by-strategy comparison
    comparison_df = compare_models_by_strategy(reliability_df)
    
    # Save comparison table
    output_file = TABLES_DIR / "table_09_model_comparison_by_strategy.csv"
    comparison_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved: {output_file.name}")
    
    # Create visualizations
    create_model_comparison_plots(comparison_df)
    
    # Overall comparison
    overall_df = overall_model_comparison(reliability_df)
    
    # Save overall comparison table
    output_file = TABLES_DIR / "table_10_overall_model_comparison.csv"
    overall_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved: {output_file.name}")
    
    # Create overall visualization
    create_overall_comparison_plot(overall_df)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    # Count wins
    chatgpt_wins = (comparison_df['winner'] == 'ChatGPT').sum()
    gemini_wins = (comparison_df['winner'] == 'Gemini').sum()
    
    print(f"\n  Strategy-level wins (across 4 metrics × 3 strategies):")
    print(f"    ChatGPT: {chatgpt_wins} wins")
    print(f"    Gemini:  {gemini_wins} wins")
    
    # Significant differences
    sig_diffs = (overall_df['p_value'] < 0.05).sum()
    print(f"\n  Overall comparison (averaged across strategies):")
    print(f"    Significant differences: {sig_diffs}/4 metrics")
    
    print("\n" + "="*70)
    print("✅ RQ4 MODEL COMPARISON COMPLETE!")
    print("="*70)
    print(f"\n📊 Generated:")
    print(f"   - 3 figures (model comparison)")
    print(f"   - 2 tables (by-strategy, overall)")

if __name__ == "__main__":
    main()
