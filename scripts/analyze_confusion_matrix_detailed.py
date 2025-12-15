"""
Detailed Confusion Matrix Analysis with Classification Metrics

Generates comprehensive confusion matrix analysis including:
- Heatmap visualizations
- Per-class metrics (Precision, Recall, F1, Specificity)
- Overall metrics (Accuracy, Balanced Accuracy, Macro/Micro averages)
- Error pattern analysis
- Misclassification insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report,
    balanced_accuracy_score
)
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
INPUT_DIR = Path("results_experiment_final/rq1_validity")
OUTPUT_DIR = Path("results_experiment_final/rq1_validity")
FIGURES_DIR = Path("results_experiment_final/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("DETAILED CONFUSION MATRIX ANALYSIS")
print("="*80 + "\n")

# Load data
print("Loading data...")
df_gold = pd.read_csv(DATA_DIR / "gold_standard.csv")
df_experiment = pd.read_csv(DATA_DIR / "experiment_data_complete.csv")

# Fix student_id format
df_gold['student_id'] = 'student_' + df_gold['student_id'].astype(str).str.zfill(2)
df_gold['question_number'] = df_gold['question_number'].astype(int)
df_experiment['student_id'] = df_experiment['student_id'].astype(str)
df_experiment['question_number'] = df_experiment['question_number'].astype(int)

# Merge
df = df_experiment.merge(
    df_gold[['student_id', 'question_number', 'gold_score']],
    on=['student_id', 'question_number'],
    how='inner'
)

# Convert to grades
df['gold_grade'] = np.round(df['gold_score']).astype(int)
df['llm_grade'] = np.round(df['weighted_score']).astype(int)

print(f"  ✓ Loaded {len(df)} graded essays\n")

# Grade labels
grade_labels = ['E (1)', 'D (2)', 'C (3)', 'B (4)', 'A (5)']
grade_nums = [1, 2, 3, 4, 5]

# ============================================================================
# Function: Calculate detailed per-class metrics
# ============================================================================
def calculate_detailed_metrics(y_true, y_pred, labels=[1,2,3,4,5]):
    """Calculate comprehensive classification metrics"""
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    metrics = {}
    
    for i, label in enumerate(labels):
        # True Positives, False Positives, False Negatives, True Negatives
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        tn = cm.sum() - tp - fp - fn
        
        # Metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0  # Sensitivity
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        # Support
        support = (y_true == label).sum()
        
        metrics[label] = {
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'specificity': round(specificity, 4),
            'f1_score': round(f1, 4),
            'support': int(support),
            'tp': int(tp),
            'fp': int(fp),
            'fn': int(fn),
            'tn': int(tn)
        }
    
    # Overall metrics
    accuracy = accuracy_score(y_true, y_pred)
    balanced_acc = balanced_accuracy_score(y_true, y_pred)
    
    # Macro averages
    precisions = [m['precision'] for m in metrics.values()]
    recalls = [m['recall'] for m in metrics.values()]
    f1s = [m['f1_score'] for m in metrics.values()]
    
    metrics['overall'] = {
        'accuracy': round(accuracy, 4),
        'balanced_accuracy': round(balanced_acc, 4),
        'macro_precision': round(np.mean(precisions), 4),
        'macro_recall': round(np.mean(recalls), 4),
        'macro_f1': round(np.mean(f1s), 4)
    }
    
    return metrics, cm

# ============================================================================
# Calculate metrics for each model-strategy
# ============================================================================
print("Calculating detailed metrics per model-strategy...\n")

all_metrics = []
confusion_matrices = {}

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        
        data = df[(df['model'] == model) & (df['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        y_true = data['gold_grade'].values
        y_pred = data['llm_grade'].values
        
        # Calculate metrics
        metrics, cm = calculate_detailed_metrics(y_true, y_pred)
        
        # Store confusion matrix
        confusion_matrices[f"{model}_{strategy}"] = cm
        
        # Print summary
        print(f"{model.upper()} {strategy}:")
        print(f"  Accuracy: {metrics['overall']['accuracy']:.2%}")
        print(f"  Balanced Accuracy: {metrics['overall']['balanced_accuracy']:.2%}")
        print(f"  Macro F1: {metrics['overall']['macro_f1']:.4f}")
        
        # Store per-grade metrics
        for grade in grade_nums:
            all_metrics.append({
                'model': model,
                'strategy': strategy,
                'grade': grade,
                'grade_label': grade_labels[grade-1],
                'precision': metrics[grade]['precision'],
                'recall': metrics[grade]['recall'],
                'specificity': metrics[grade]['specificity'],
                'f1_score': metrics[grade]['f1_score'],
                'support': metrics[grade]['support'],
                'tp': metrics[grade]['tp'],
                'fp': metrics[grade]['fp'],
                'fn': metrics[grade]['fn'],
                'tn': metrics[grade]['tn']
            })
        
        # Store overall metrics
        all_metrics.append({
            'model': model,
            'strategy': strategy,
            'grade': 'Overall',
            'grade_label': 'Overall',
            'precision': metrics['overall']['macro_precision'],
            'recall': metrics['overall']['macro_recall'],
            'specificity': np.nan,
            'f1_score': metrics['overall']['macro_f1'],
            'support': len(data),
            'tp': np.nan,
            'fp': np.nan,
            'fn': np.nan,
            'tn': np.nan
        })
        
        print()

# Save detailed metrics
df_metrics = pd.DataFrame(all_metrics)
df_metrics.to_csv(OUTPUT_DIR / "detailed_classification_metrics.csv", index=False)
print(f"✓ Saved detailed_classification_metrics.csv\n")

# ============================================================================
# Create Confusion Matrix Heatmaps
# ============================================================================
print("Generating confusion matrix heatmaps...\n")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Confusion Matrices: True Grade vs LLM-Predicted Grade', 
             fontsize=16, fontweight='bold', y=0.995)

strategies = [('chatgpt', 'zero-shot'), ('chatgpt', 'few-shot'), ('chatgpt', 'lenient'),
              ('gemini', 'zero-shot'), ('gemini', 'few-shot'), ('gemini', 'lenient')]

for idx, (model, strategy) in enumerate(strategies):
    ax = axes[idx // 3, idx % 3]
    
    key = f"{model}_{strategy}"
    if key not in confusion_matrices:
        ax.axis('off')
        continue
    
    cm = confusion_matrices[key]
    
    # Calculate percentages
    cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    # Create heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=grade_labels, yticklabels=grade_labels,
                ax=ax, cbar_kws={'label': 'Count'}, 
                linewidths=0.5, linecolor='gray')
    
    # Add percentage annotations
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if cm[i, j] > 0:
                text = ax.texts[i * cm.shape[1] + j]
                text.set_text(f'{cm[i, j]}\n({cm_percent[i, j]:.1f}%)')
    
    ax.set_title(f'{model.upper()} - {strategy.capitalize()}', 
                fontweight='bold', fontsize=12)
    ax.set_xlabel('Predicted Grade', fontsize=10)
    ax.set_ylabel('True Grade', fontsize=10)
    
    # Calculate accuracy for this matrix
    accuracy = np.trace(cm) / cm.sum()
    ax.text(0.02, 0.98, f'Accuracy: {accuracy:.1%}', 
           transform=ax.transAxes, fontsize=10, 
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
output_file = FIGURES_DIR / "confusion_matrices_heatmap.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved {output_file.name}")
plt.close()

# ============================================================================
# Create Per-Class Performance Visualization
# ============================================================================
print("Generating per-class performance charts...\n")

# Filter out overall rows
df_per_grade = df_metrics[df_metrics['grade'] != 'Overall'].copy()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Per-Grade Classification Performance', fontsize=16, fontweight='bold')

metrics_to_plot = [
    ('precision', 'Precision', 'Higher is Better'),
    ('recall', 'Recall (Sensitivity)', 'Higher is Better'),
    ('f1_score', 'F1-Score', 'Higher is Better'),
    ('specificity', 'Specificity', 'Higher is Better')
]

for idx, (metric, title, subtitle) in enumerate(metrics_to_plot):
    ax = axes[idx // 2, idx % 2]
    
    # Pivot for grouped bar chart
    pivot = df_per_grade.pivot_table(
        index='grade',
        columns=['model', 'strategy'],
        values=metric,
        aggfunc='first'
    )
    
    pivot.plot(kind='bar', ax=ax, width=0.8)
    
    ax.set_title(f'{title}\n{subtitle}', fontweight='bold', fontsize=12)
    ax.set_xlabel('Grade', fontsize=11)
    ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=11)
    ax.set_xticklabels(['E (1)', 'D (2)', 'C (3)', 'B (4)', 'A (5)'], rotation=0)
    ax.legend(title='Model-Strategy', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 1.0)
    
    # Add reference lines
    ax.axhline(y=0.7, color='green', linestyle='--', alpha=0.3, label='Good (0.7)')
    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.3, label='Moderate (0.5)')

plt.tight_layout()
output_file = FIGURES_DIR / "per_grade_classification_metrics.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved {output_file.name}")
plt.close()

# ============================================================================
# Create Overall Performance Comparison
# ============================================================================
print("Generating overall performance comparison...\n")

# Filter overall metrics
df_overall = df_metrics[df_metrics['grade'] == 'Overall'].copy()
df_overall['model_strategy'] = df_overall['model'] + '_' + df_overall['strategy']

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Overall Classification Performance Comparison', fontsize=16, fontweight='bold')

# Accuracy (from validity summary)
df_validity = pd.read_csv(INPUT_DIR / "validity_summary.csv")
df_validity['model_strategy'] = df_validity['model'] + '_' + df_validity['strategy']

# Plot 1: Exact vs Adjacent Agreement
ax = axes[0]
x = np.arange(len(df_validity))
width = 0.35

bars1 = ax.bar(x - width/2, df_validity['exact_agreement_pct'], width, 
               label='Exact Agreement', alpha=0.8)
bars2 = ax.bar(x + width/2, df_validity['adjacent_agreement_pct'], width, 
               label='Adjacent Agreement (±1)', alpha=0.8)

ax.set_ylabel('Agreement (%)', fontsize=11)
ax.set_title('Agreement Rates', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_validity['model_strategy'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}',
               ha='center', va='bottom', fontsize=8)

# Plot 2: Precision-Recall-F1
ax = axes[1]
x = np.arange(len(df_overall))
width = 0.25

bars1 = ax.bar(x - width, df_overall['precision'], width, label='Precision', alpha=0.8)
bars2 = ax.bar(x, df_overall['recall'], width, label='Recall', alpha=0.8)
bars3 = ax.bar(x + width, df_overall['f1_score'], width, label='F1-Score', alpha=0.8)

ax.set_ylabel('Score', fontsize=11)
ax.set_title('Macro-Averaged Metrics', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_overall['model_strategy'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 1.0)

# Plot 3: QWK vs Balanced Accuracy
ax = axes[2]
# Get balanced accuracy from overall metrics (would need to recalculate, use existing data)
scatter_data = df_validity.merge(df_overall[['model_strategy', 'f1_score']], on='model_strategy')

for idx, row in scatter_data.iterrows():
    ax.scatter(row['qwk'], row['f1_score'], s=200, alpha=0.6)
    ax.annotate(row['model_strategy'], 
               (row['qwk'], row['f1_score']),
               fontsize=8, ha='center')

ax.set_xlabel('QWK (Agreement with Gold)', fontsize=11)
ax.set_ylabel('Macro F1-Score', fontsize=11)
ax.set_title('Validity vs Classification Performance', fontweight='bold')
ax.grid(alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Add diagonal reference line
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Perfect correlation')

plt.tight_layout()
output_file = FIGURES_DIR / "overall_performance_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved {output_file.name}")
plt.close()

# ============================================================================
# Misclassification Analysis
# ============================================================================
print("Analyzing misclassification patterns...\n")

misclass_analysis = []

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        
        data = df[(df['model'] == model) & (df['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        y_true = data['gold_grade'].values
        y_pred = data['llm_grade'].values
        
        # Misclassification patterns
        diff = y_pred - y_true
        
        # Over-prediction by severity
        over_1 = (diff == 1).sum()
        over_2 = (diff == 2).sum()
        over_3_plus = (diff >= 3).sum()
        
        # Under-prediction by severity
        under_1 = (diff == -1).sum()
        under_2 = (diff == -2).sum()
        under_3_plus = (diff <= -3).sum()
        
        # Correct predictions
        correct = (diff == 0).sum()
        
        total = len(data)
        
        misclass_analysis.append({
            'model': model,
            'strategy': strategy,
            'total_predictions': total,
            'correct': correct,
            'correct_pct': round(correct / total * 100, 2),
            'over_by_1': over_1,
            'over_by_1_pct': round(over_1 / total * 100, 2),
            'over_by_2': over_2,
            'over_by_2_pct': round(over_2 / total * 100, 2),
            'over_by_3plus': over_3_plus,
            'over_by_3plus_pct': round(over_3_plus / total * 100, 2),
            'under_by_1': under_1,
            'under_by_1_pct': round(under_1 / total * 100, 2),
            'under_by_2': under_2,
            'under_by_2_pct': round(under_2 / total * 100, 2),
            'under_by_3plus': under_3_plus,
            'under_by_3plus_pct': round(under_3_plus / total * 100, 2),
            'total_overgrading': over_1 + over_2 + over_3_plus,
            'total_overgrading_pct': round((over_1 + over_2 + over_3_plus) / total * 100, 2),
            'total_undergrading': under_1 + under_2 + under_3_plus,
            'total_undergrading_pct': round((under_1 + under_2 + under_3_plus) / total * 100, 2)
        })

df_misclass = pd.DataFrame(misclass_analysis)
df_misclass.to_csv(OUTPUT_DIR / "misclassification_analysis.csv", index=False)
print(f"✓ Saved misclassification_analysis.csv\n")

# ============================================================================
# Summary Statistics
# ============================================================================
print("="*80)
print("SUMMARY STATISTICS")
print("="*80 + "\n")

print("Best Overall Performance (by Accuracy):")
best_accuracy = df_validity.nlargest(3, 'exact_agreement_pct')[['model', 'strategy', 'exact_agreement_pct', 'qwk']]
print(best_accuracy.to_string(index=False))

print("\n" + "-"*80)
print("Best Per-Grade Performance (by F1-Score):")
best_f1_per_grade = df_per_grade.loc[df_per_grade.groupby('grade')['f1_score'].idxmax()]
print(best_f1_per_grade[['grade', 'grade_label', 'model', 'strategy', 'f1_score', 'precision', 'recall']].to_string(index=False))

print("\n" + "-"*80)
print("Misclassification Summary:")
print(df_misclass[['model', 'strategy', 'correct_pct', 'total_overgrading_pct', 'total_undergrading_pct']].to_string(index=False))

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nOutput files:")
print(f"  • detailed_classification_metrics.csv - Precision/Recall/F1/Specificity per grade")
print(f"  • misclassification_analysis.csv - Error pattern breakdown")
print(f"  • confusion_matrices_heatmap.png - Heatmaps for all 6 configurations")
print(f"  • per_grade_classification_metrics.png - Performance by grade level")
print(f"  • overall_performance_comparison.png - Aggregate metrics comparison")
print("="*80 + "\n")
