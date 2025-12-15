"""
RQ1: Reliability vs Expert Grading Analysis

Analyzes how well AES (lenient strategy) agrees with expert human grading.

Metrics calculated:
- Exact Agreement (EA)
- Adjacent Agreement (AA)
- Cohen's Kappa
- Quadratic Weighted Kappa (QWK)
- Per-grade Precision, Recall, F1
- Confusion matrices

Comparisons:
- ChatGPT-lenient vs Expert
- Gemini-lenient vs Expert
- Combined (all trials) vs Expert
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, cohen_kappa_score, accuracy_score,
    precision_recall_fscore_support, classification_report
)
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def quadratic_weighted_kappa(y_true, y_pred, labels):
    """Calculate Quadratic Weighted Kappa."""
    # Convert labels to numeric
    label_to_num = {label: i for i, label in enumerate(labels)}
    y_true_num = np.array([label_to_num[y] for y in y_true])
    y_pred_num = np.array([label_to_num[y] for y in y_pred])
    
    # Confusion matrix
    cm = confusion_matrix(y_true_num, y_pred_num, labels=range(len(labels)))
    
    # Weight matrix (quadratic)
    n = len(labels)
    weights = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            weights[i, j] = ((i - j) ** 2) / ((n - 1) ** 2)
    
    # Observed agreement
    observed = np.sum(weights * cm) / np.sum(cm)
    
    # Expected agreement
    row_sum = np.sum(cm, axis=1)
    col_sum = np.sum(cm, axis=0)
    expected_cm = np.outer(row_sum, col_sum) / np.sum(cm)
    expected = np.sum(weights * expected_cm) / np.sum(cm)
    
    # QWK
    if expected == 1:
        return 0
    return 1 - (observed / expected)


def adjacent_agreement(y_true, y_pred, labels):
    """Calculate adjacent agreement (within 1 grade level)."""
    label_to_num = {label: i for i, label in enumerate(labels)}
    
    adjacent = 0
    for true, pred in zip(y_true, y_pred):
        true_idx = label_to_num[true]
        pred_idx = label_to_num[pred]
        if abs(true_idx - pred_idx) <= 1:
            adjacent += 1
    
    return adjacent / len(y_true)


def calculate_agreement_metrics(expert, aes, model_name):
    """Calculate all agreement metrics."""
    
    # Grade order
    grade_labels = ['A', 'B', 'C', 'D', 'E']
    
    # Filter valid pairs
    valid = (expert.notna()) & (aes.notna())
    expert_valid = expert[valid].values
    aes_valid = aes[valid].values
    
    n = len(expert_valid)
    
    if n == 0:
        return None
    
    # Exact agreement
    exact_agreement = accuracy_score(expert_valid, aes_valid)
    
    # Adjacent agreement
    adj_agreement = adjacent_agreement(expert_valid, aes_valid, grade_labels)
    
    # Cohen's Kappa
    cohens_kappa = cohen_kappa_score(expert_valid, aes_valid, labels=grade_labels)
    
    # Quadratic Weighted Kappa
    qwk = quadratic_weighted_kappa(expert_valid, aes_valid, grade_labels)
    
    # Per-grade metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        expert_valid, aes_valid, labels=grade_labels, zero_division=0
    )
    
    metrics = {
        'model': model_name,
        'n_samples': n,
        'exact_agreement': exact_agreement,
        'adjacent_agreement': adj_agreement,
        'cohens_kappa': cohens_kappa,
        'qwk': qwk,
        'per_grade_precision': {grade: p for grade, p in zip(grade_labels, precision)},
        'per_grade_recall': {grade: r for grade, r in zip(grade_labels, recall)},
        'per_grade_f1': {grade: f for grade, f in zip(grade_labels, f1)},
        'per_grade_support': {grade: s for grade, s in zip(grade_labels, support)},
        'expert_grades': expert_valid,
        'aes_grades': aes_valid
    }
    
    return metrics


def plot_confusion_matrix(expert, aes, model_name, save_path):
    """Plot confusion matrix."""
    grade_labels = ['A', 'B', 'C', 'D', 'E']
    
    cm = confusion_matrix(expert, aes, labels=grade_labels)
    
    # Calculate percentages
    cm_pct = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot heatmap
    sns.heatmap(
        cm_pct, 
        annot=True, 
        fmt='.1f',
        cmap='Blues',
        xticklabels=grade_labels,
        yticklabels=grade_labels,
        cbar_kws={'label': 'Percentage (%)'},
        ax=ax,
        vmin=0,
        vmax=100
    )
    
    # Add counts
    for i in range(len(grade_labels)):
        for j in range(len(grade_labels)):
            count = cm[i, j]
            if count > 0:
                ax.text(j + 0.5, i + 0.7, f'n={count}', 
                       ha='center', va='center', fontsize=8, color='gray')
    
    ax.set_xlabel('AES Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expert Grade', fontsize=12, fontweight='bold')
    ax.set_title(f'Confusion Matrix: {model_name} vs Expert\n(Lenient Strategy)', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_agreement_comparison(metrics_list, save_path):
    """Plot agreement metrics comparison."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    models = [m['model'] for m in metrics_list]
    
    # 1. Exact Agreement
    ax = axes[0, 0]
    ea_values = [m['exact_agreement'] * 100 for m in metrics_list]
    bars = ax.bar(models, ea_values, color=['#2E86AB', '#A23B72', '#F18F01'])
    ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title('Exact Agreement', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(y=70, color='red', linestyle='--', alpha=0.3, label='70% threshold')
    ax.legend()
    for bar, val in zip(bars, ea_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
               f'{val:.1f}%', ha='center', fontweight='bold')
    
    # 2. Adjacent Agreement
    ax = axes[0, 1]
    aa_values = [m['adjacent_agreement'] * 100 for m in metrics_list]
    bars = ax.bar(models, aa_values, color=['#2E86AB', '#A23B72', '#F18F01'])
    ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title('Adjacent Agreement (±1 grade)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(y=90, color='red', linestyle='--', alpha=0.3, label='90% threshold')
    ax.legend()
    for bar, val in zip(bars, aa_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
               f'{val:.1f}%', ha='center', fontweight='bold')
    
    # 3. Cohen's Kappa
    ax = axes[1, 0]
    kappa_values = [m['cohens_kappa'] for m in metrics_list]
    bars = ax.bar(models, kappa_values, color=['#2E86AB', '#A23B72', '#F18F01'])
    ax.set_ylabel('Kappa Value', fontsize=11, fontweight='bold')
    ax.set_title("Cohen's Kappa", fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.6, color='orange', linestyle='--', alpha=0.3, label='Substantial (0.6)')
    ax.axhline(y=0.8, color='green', linestyle='--', alpha=0.3, label='Almost Perfect (0.8)')
    ax.legend()
    for bar, val in zip(bars, kappa_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    # 4. Quadratic Weighted Kappa
    ax = axes[1, 1]
    qwk_values = [m['qwk'] for m in metrics_list]
    bars = ax.bar(models, qwk_values, color=['#2E86AB', '#A23B72', '#F18F01'])
    ax.set_ylabel('QWK Value', fontsize=11, fontweight='bold')
    ax.set_title('Quadratic Weighted Kappa', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.6, color='orange', linestyle='--', alpha=0.3, label='Substantial (0.6)')
    ax.axhline(y=0.8, color='green', linestyle='--', alpha=0.3, label='Almost Perfect (0.8)')
    ax.legend()
    for bar, val in zip(bars, qwk_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    plt.suptitle('Agreement Metrics: AES vs Expert (Lenient Strategy)',
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_per_grade_performance(metrics_list, save_path):
    """Plot per-grade precision, recall, F1."""
    grade_labels = ['A', 'B', 'C', 'D']  # E usually has no samples
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    x = np.arange(len(grade_labels))
    width = 0.25
    
    for idx, metric_name in enumerate(['precision', 'recall', 'f1']):
        ax = axes[idx]
        
        for i, metrics in enumerate(metrics_list):
            values = [metrics[f'per_grade_{metric_name}'].get(g, 0) for g in grade_labels]
            ax.bar(x + i * width, values, width, label=metrics['model'])
        
        ax.set_xlabel('Grade Level', fontsize=11, fontweight='bold')
        ax.set_ylabel(metric_name.capitalize(), fontsize=11, fontweight='bold')
        ax.set_title(f'{metric_name.capitalize()} by Grade', fontsize=12, fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels(grade_labels)
        ax.legend()
        ax.set_ylim(0, 1.1)
        ax.axhline(y=0.7, color='red', linestyle='--', alpha=0.3)
    
    plt.suptitle('Per-Grade Performance Metrics',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_agreement_by_grade(metrics_list, save_path):
    """Plot agreement rates by expert grade level."""
    grade_labels = ['A', 'B', 'C', 'D']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(grade_labels))
    width = 0.25
    
    for i, metrics in enumerate(metrics_list):
        expert = metrics['expert_grades']
        aes = metrics['aes_grades']
        
        agreement_by_grade = []
        for grade in grade_labels:
            mask = expert == grade
            if mask.sum() > 0:
                agree = (expert[mask] == aes[mask]).sum() / mask.sum()
                agreement_by_grade.append(agree)
            else:
                agreement_by_grade.append(0)
        
        bars = ax.bar(x + i * width, agreement_by_grade, width, label=metrics['model'])
    
    ax.set_xlabel('Expert Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Agreement Rate', fontsize=12, fontweight='bold')
    ax.set_title('Agreement Rate by Expert Grade Level', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(grade_labels)
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.axhline(y=0.7, color='red', linestyle='--', alpha=0.3, label='70% threshold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_summary_table(metrics_list, save_path):
    """Generate summary table."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ1: RELIABILITY VS EXPERT GRADING - SUMMARY TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("OVERALL AGREEMENT METRICS\n")
        f.write("-"*80 + "\n\n")
        
        # Table header
        f.write(f"{'Model':<20} {'N':<8} {'EA (%)':<10} {'AA (%)':<10} {'Kappa':<10} {'QWK':<10}\n")
        f.write("-"*80 + "\n")
        
        for m in metrics_list:
            f.write(f"{m['model']:<20} {m['n_samples']:<8} "
                   f"{m['exact_agreement']*100:<10.1f} "
                   f"{m['adjacent_agreement']*100:<10.1f} "
                   f"{m['cohens_kappa']:<10.3f} "
                   f"{m['qwk']:<10.3f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("PER-GRADE PERFORMANCE\n")
        f.write("="*80 + "\n\n")
        
        for m in metrics_list:
            f.write(f"\n{m['model']}:\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Grade':<8} {'Support':<10} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}\n")
            f.write("-"*80 + "\n")
            
            for grade in ['A', 'B', 'C', 'D']:
                support = m['per_grade_support'].get(grade, 0)
                if support > 0:
                    prec = m['per_grade_precision'].get(grade, 0)
                    rec = m['per_grade_recall'].get(grade, 0)
                    f1 = m['per_grade_f1'].get(grade, 0)
                    f.write(f"{grade:<8} {support:<10} {prec:<12.3f} {rec:<12.3f} {f1:<12.3f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*80 + "\n\n")
        
        f.write("Exact Agreement (EA):\n")
        f.write("  - Percentage of exact matches between AES and expert grades\n")
        f.write("  - Benchmark: >70% is good for educational assessment\n\n")
        
        f.write("Adjacent Agreement (AA):\n")
        f.write("  - Percentage within ±1 grade level\n")
        f.write("  - Benchmark: >90% is acceptable\n\n")
        
        f.write("Cohen's Kappa:\n")
        f.write("  - 0.00-0.20: Slight agreement\n")
        f.write("  - 0.21-0.40: Fair agreement\n")
        f.write("  - 0.41-0.60: Moderate agreement\n")
        f.write("  - 0.61-0.80: Substantial agreement\n")
        f.write("  - 0.81-1.00: Almost perfect agreement\n\n")
        
        f.write("Quadratic Weighted Kappa (QWK):\n")
        f.write("  - Similar to Cohen's Kappa but penalizes larger disagreements more\n")
        f.write("  - Preferred for ordinal grades (A, B, C, D)\n")
        f.write("  - Same interpretation thresholds as Cohen's Kappa\n\n")
        
        f.write("="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("RQ1: RELIABILITY VS EXPERT GRADING ANALYSIS")
    print("="*80)
    
    # Paths
    data_dir = project_root / "results" / "lenient_analysis"
    output_dir = project_root / "results" / "rq1_reliability"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nInput: {data_dir}")
    print(f"Output: {output_dir}")
    
    # Load data
    print("\n[1/6] Loading data...")
    df_full = pd.read_csv(data_dir / "lenient_full_data.csv")
    df_chatgpt = pd.read_csv(data_dir / "lenient_chatgpt.csv")
    df_gemini = pd.read_csv(data_dir / "lenient_gemini.csv")
    
    print(f"  Full: {len(df_full)} records")
    print(f"  ChatGPT: {len(df_chatgpt)} records")
    print(f"  Gemini: {len(df_gemini)} records")
    
    # Calculate metrics
    print("\n[2/6] Calculating agreement metrics...")
    
    metrics_chatgpt = calculate_agreement_metrics(
        df_chatgpt['expert_grade'], 
        df_chatgpt['aes_grade'],
        'ChatGPT-Lenient'
    )
    print(f"  ✓ ChatGPT: EA={metrics_chatgpt['exact_agreement']*100:.1f}%, "
          f"QWK={metrics_chatgpt['qwk']:.3f}")
    
    metrics_gemini = calculate_agreement_metrics(
        df_gemini['expert_grade'],
        df_gemini['aes_grade'],
        'Gemini-Lenient'
    )
    print(f"  ✓ Gemini: EA={metrics_gemini['exact_agreement']*100:.1f}%, "
          f"QWK={metrics_gemini['qwk']:.3f}")
    
    metrics_combined = calculate_agreement_metrics(
        df_full['expert_grade'],
        df_full['aes_grade'],
        'Combined (All)'
    )
    print(f"  ✓ Combined: EA={metrics_combined['exact_agreement']*100:.1f}%, "
          f"QWK={metrics_combined['qwk']:.3f}")
    
    metrics_list = [metrics_chatgpt, metrics_gemini, metrics_combined]
    
    # Generate visualizations
    print("\n[3/6] Generating confusion matrices...")
    plot_confusion_matrix(
        metrics_chatgpt['expert_grades'],
        metrics_chatgpt['aes_grades'],
        'ChatGPT-Lenient',
        output_dir / "confusion_matrix_chatgpt.png"
    )
    
    plot_confusion_matrix(
        metrics_gemini['expert_grades'],
        metrics_gemini['aes_grades'],
        'Gemini-Lenient',
        output_dir / "confusion_matrix_gemini.png"
    )
    
    print("\n[4/6] Generating agreement comparison...")
    plot_agreement_comparison(
        metrics_list,
        output_dir / "agreement_comparison.png"
    )
    
    print("\n[5/6] Generating per-grade analysis...")
    plot_per_grade_performance(
        metrics_list,
        output_dir / "per_grade_performance.png"
    )
    
    plot_agreement_by_grade(
        metrics_list,
        output_dir / "agreement_by_grade.png"
    )
    
    print("\n[6/6] Generating summary table...")
    generate_summary_table(
        metrics_list,
        output_dir / "summary_table.txt"
    )
    
    # Final summary
    print("\n" + "="*80)
    print("RQ1 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  1. confusion_matrix_chatgpt.png")
    print("  2. confusion_matrix_gemini.png")
    print("  3. agreement_comparison.png")
    print("  4. per_grade_performance.png")
    print("  5. agreement_by_grade.png")
    print("  6. summary_table.txt")
    
    print("\nKey Findings:")
    print(f"  • ChatGPT Exact Agreement: {metrics_chatgpt['exact_agreement']*100:.1f}%")
    print(f"  • Gemini Exact Agreement: {metrics_gemini['exact_agreement']*100:.1f}%")
    print(f"  • ChatGPT QWK: {metrics_chatgpt['qwk']:.3f}")
    print(f"  • Gemini QWK: {metrics_gemini['qwk']:.3f}")
    
    print("\nNext step: RQ2 - Inter-Rater Reliability Analysis")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
