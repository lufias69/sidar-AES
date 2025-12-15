"""
RQ2d: Consistency Visualizations

Create publication-ready visualizations for consistency analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DATA_DIR = Path("results_experiment_final/data")
INPUT_DIR = Path("results_experiment_final/rq2_consistency")
OUTPUT_DIR = Path("results_experiment_final/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("\n" + "="*80)
print("RQ2d: CONSISTENCY VISUALIZATIONS")
print("="*80 + "\n")

# Load data
df_variance = pd.read_csv(INPUT_DIR / "per_item_variance.csv")
df_scores = pd.read_csv(DATA_DIR / "per_item_scores.csv")

# ============================================================================
# Figure 1: Variance Heatmap
# ============================================================================
print("[1/5] Creating variance heatmap...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Per-Item Variance Heatmap Across Models and Strategies', fontsize=16, fontweight='bold')

strategies = [('chatgpt', 'zero'), ('chatgpt', 'few'), ('chatgpt', 'lenient'),
              ('gemini', 'zero'), ('gemini', 'few'), ('gemini', 'lenient')]

for idx, (model, strategy) in enumerate(strategies):
    ax = axes[idx // 3, idx % 3]
    
    # Filter data
    data = df_variance[
        (df_variance['model'] == model) & 
        (df_variance['strategy'] == strategy)
    ].copy()
    
    if len(data) == 0:
        continue
    
    # Pivot for heatmap
    pivot = data.pivot_table(
        index='student_id',
        columns='question_number',
        values='std_dev',
        aggfunc='first'
    )
    
    # Create heatmap
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r', 
                vmin=0, vmax=0.6, cbar_kws={'label': 'Std Dev'},
                ax=ax, linewidths=0.5)
    
    ax.set_title(f'{model.upper()} - {strategy.capitalize()}', fontweight='bold')
    ax.set_xlabel('Question Number')
    ax.set_ylabel('Student ID')

plt.tight_layout()
output_file = OUTPUT_DIR / "consistency_variance_heatmap.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_file}")
plt.close()

# ============================================================================
# Figure 2: Box Plot - Score Distribution by Strategy
# ============================================================================
print("[2/5] Creating box plots...")

fig, ax = plt.subplots(figsize=(12, 6))

# Prepare data
df_scores['model_strategy'] = df_scores['model'] + '_' + df_scores['strategy']

sns.boxplot(data=df_scores, x='model_strategy', y='score', ax=ax)
ax.set_title('Score Distribution Across Models and Strategies', fontsize=14, fontweight='bold')
ax.set_xlabel('Model - Strategy', fontsize=12)
ax.set_ylabel('Weighted Score', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = OUTPUT_DIR / "consistency_boxplot_by_strategy.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_file}")
plt.close()

# ============================================================================
# Figure 3: Standard Deviation Comparison
# ============================================================================
print("[3/5] Creating SD comparison bar chart...")

summary = df_variance.groupby(['model', 'strategy']).agg({
    'std_dev': ['mean', 'median'],
    'range': 'mean'
}).round(4)

summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary = summary.reset_index()
summary['model_strategy'] = summary['model'] + '_' + summary['strategy']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Mean SD
ax1.bar(range(len(summary)), summary['std_dev_mean'], color=sns.color_palette("husl", len(summary)))
ax1.set_xticks(range(len(summary)))
ax1.set_xticklabels(summary['model_strategy'], rotation=45, ha='right')
ax1.set_ylabel('Mean Standard Deviation', fontsize=12)
ax1.set_title('Mean SD per Item (Lower = More Consistent)', fontsize=13, fontweight='bold')
ax1.axhline(y=0.2, color='green', linestyle='--', label='Excellent (SD≤0.2)', alpha=0.7)
ax1.axhline(y=0.4, color='orange', linestyle='--', label='Good (SD≤0.4)', alpha=0.7)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Mean Range
ax2.bar(range(len(summary)), summary['range_mean'], color=sns.color_palette("husl", len(summary)))
ax2.set_xticks(range(len(summary)))
ax2.set_xticklabels(summary['model_strategy'], rotation=45, ha='right')
ax2.set_ylabel('Mean Score Range', fontsize=12)
ax2.set_title('Mean Range per Item (Lower = More Consistent)', fontsize=13, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = OUTPUT_DIR / "consistency_sd_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_file}")
plt.close()

# ============================================================================
# Figure 4: Reliability Coefficients Comparison
# ============================================================================
print("[4/5] Creating reliability coefficients chart...")

df_reliability = pd.read_csv(INPUT_DIR / "reliability_coefficients.csv")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

metrics = [('icc_2_1', 'ICC(2,1)', 'Intraclass Correlation'),
           ('cronbach_alpha', 'Cronbach\'s Alpha', 'Internal Consistency'),
           ('fleiss_kappa', 'Fleiss\' Kappa', 'Multi-Rater Agreement')]

for idx, (col, title, subtitle) in enumerate(metrics):
    ax = axes[idx]
    
    # Filter out NaN values
    data = df_reliability[['model', 'strategy', col]].dropna()
    data['model_strategy'] = data['model'] + '_' + data['strategy']
    
    colors = sns.color_palette("husl", len(data))
    bars = ax.bar(range(len(data)), data[col], color=colors)
    
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data['model_strategy'], rotation=45, ha='right')
    ax.set_ylabel(title, fontsize=12)
    ax.set_title(f'{title}\n{subtitle}', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1.0)
    
    # Add threshold lines
    if 'icc' in col or 'alpha' in col:
        ax.axhline(y=0.90, color='green', linestyle='--', alpha=0.5, label='Excellent')
        ax.axhline(y=0.75, color='orange', linestyle='--', alpha=0.5, label='Good')
    elif 'kappa' in col:
        ax.axhline(y=0.80, color='green', linestyle='--', alpha=0.5, label='Substantial')
        ax.axhline(y=0.60, color='orange', linestyle='--', alpha=0.5, label='Moderate')
    
    ax.legend(fontsize=8)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = OUTPUT_DIR / "reliability_coefficients_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_file}")
plt.close()

# ============================================================================
# Figure 5: Consistency Distribution
# ============================================================================
print("[5/5] Creating consistency distribution chart...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Consistency Distribution Across Models and Strategies', fontsize=16, fontweight='bold')

for idx, (model, strategy) in enumerate(strategies):
    ax = axes[idx // 3, idx % 3]
    
    data = df_variance[
        (df_variance['model'] == model) & 
        (df_variance['strategy'] == strategy)
    ]
    
    if len(data) == 0:
        continue
    
    # Count by consistency category
    consistency_counts = data['consistency'].value_counts()
    categories = ['Excellent', 'Good', 'Fair', 'Poor']
    counts = [consistency_counts.get(cat, 0) for cat in categories]
    colors = ['green', 'lightgreen', 'orange', 'red']
    
    bars = ax.bar(categories, counts, color=colors, alpha=0.7, edgecolor='black')
    
    # Add percentages
    total = sum(counts)
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}\n({count/total*100:.1f}%)',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title(f'{model.upper()} - {strategy.capitalize()}', fontweight='bold')
    ax.set_ylabel('Number of Items', fontsize=10)
    ax.set_ylim(0, max(counts) * 1.2)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = OUTPUT_DIR / "consistency_distribution.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_file}")
plt.close()

print("\n" + "="*80)
print("VISUALIZATIONS COMPLETE")
print("="*80)
print("\nOutput files in:", OUTPUT_DIR)
print("  1. consistency_variance_heatmap.png")
print("  2. consistency_boxplot_by_strategy.png")
print("  3. consistency_sd_comparison.png")
print("  4. reliability_coefficients_comparison.png")
print("  5. consistency_distribution.png")
print("="*80 + "\n")
