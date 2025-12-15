"""
RQ4: Error Analysis

Comprehensive error pattern analysis for ChatGPT and Gemini.

Analyses:
- Error distribution by grade level
- Over-grading vs under-grading patterns
- Critical errors (2+ grade differences)
- Confusion patterns (which grades confused most)
- Error severity comparison
- Comparative error analysis between models
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def calculate_error_magnitude(expert_grade, aes_grade):
    """Calculate numeric error magnitude."""
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    
    if pd.isna(expert_grade) or pd.isna(aes_grade):
        return np.nan
    
    expert_val = grade_map.get(expert_grade, np.nan)
    aes_val = grade_map.get(aes_grade, np.nan)
    
    return aes_val - expert_val


def classify_error(error_magnitude):
    """Classify error into categories."""
    if pd.isna(error_magnitude):
        return 'Unknown'
    elif error_magnitude == 0:
        return 'Correct'
    elif error_magnitude > 0:
        return 'Over-grade'
    else:
        return 'Under-grade'


def classify_error_severity(error_magnitude):
    """Classify error severity."""
    if pd.isna(error_magnitude):
        return 'Unknown'
    
    abs_error = abs(error_magnitude)
    
    if abs_error == 0:
        return 'Correct'
    elif abs_error == 1:
        return 'Minor (±1)'
    elif abs_error == 2:
        return 'Major (±2)'
    else:
        return 'Critical (±3+)'


def analyze_error_patterns(df, model_name):
    """Analyze error patterns for a model."""
    # Calculate errors
    df['error_magnitude'] = df.apply(
        lambda row: calculate_error_magnitude(row['expert_grade'], row['aes_grade']),
        axis=1
    )
    df['error_type'] = df['error_magnitude'].apply(classify_error)
    df['error_severity'] = df['error_magnitude'].apply(classify_error_severity)
    
    # Error distribution
    error_dist = df['error_type'].value_counts()
    
    # Severity distribution
    severity_dist = df['error_severity'].value_counts()
    
    # By grade level
    error_by_grade = df.groupby('expert_grade')['error_type'].value_counts().unstack(fill_value=0)
    
    # Critical errors
    critical_errors = df[df['error_severity'].isin(['Major (±2)', 'Critical (±3+)'])].copy()
    
    # Statistics
    total = len(df)
    correct = (df['error_type'] == 'Correct').sum()
    over_grade = (df['error_type'] == 'Over-grade').sum()
    under_grade = (df['error_type'] == 'Under-grade').sum()
    minor = (df['error_severity'] == 'Minor (±1)').sum()
    major = (df['error_severity'] == 'Major (±2)').sum()
    critical = (df['error_severity'] == 'Critical (±3+)').sum()
    
    stats = {
        'model': model_name,
        'total': total,
        'correct': correct,
        'correct_pct': correct / total * 100,
        'over_grade': over_grade,
        'over_grade_pct': over_grade / total * 100,
        'under_grade': under_grade,
        'under_grade_pct': under_grade / total * 100,
        'minor': minor,
        'minor_pct': minor / total * 100,
        'major': major,
        'major_pct': major / total * 100,
        'critical': critical,
        'critical_pct': critical / total * 100,
        'mean_error': df['error_magnitude'].mean(),
        'std_error': df['error_magnitude'].std()
    }
    
    return {
        'df': df,
        'error_dist': error_dist,
        'severity_dist': severity_dist,
        'error_by_grade': error_by_grade,
        'critical_errors': critical_errors,
        'stats': stats
    }


def plot_error_distribution(chatgpt_analysis, gemini_analysis, save_path):
    """Plot error type and severity distributions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Error type distribution - ChatGPT
    ax = axes[0, 0]
    error_types = ['Correct', 'Over-grade', 'Under-grade']
    chatgpt_vals = [chatgpt_analysis['stats']['correct'],
                    chatgpt_analysis['stats']['over_grade'],
                    chatgpt_analysis['stats']['under_grade']]
    
    colors = ['#2ECC71', '#E74C3C', '#3498DB']
    bars = ax.bar(error_types, chatgpt_vals, color=colors)
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('ChatGPT - Error Type Distribution', fontsize=13, fontweight='bold')
    
    # Add percentages
    for bar, val in zip(bars, chatgpt_vals):
        pct = val / chatgpt_analysis['stats']['total'] * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
               f'{val}\n({pct:.1f}%)', ha='center', fontweight='bold')
    
    # 2. Error type distribution - Gemini
    ax = axes[0, 1]
    gemini_vals = [gemini_analysis['stats']['correct'],
                   gemini_analysis['stats']['over_grade'],
                   gemini_analysis['stats']['under_grade']]
    
    bars = ax.bar(error_types, gemini_vals, color=colors)
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Gemini - Error Type Distribution', fontsize=13, fontweight='bold')
    
    for bar, val in zip(bars, gemini_vals):
        pct = val / gemini_analysis['stats']['total'] * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
               f'{val}\n({pct:.1f}%)', ha='center', fontweight='bold')
    
    # 3. Error severity - Stacked bar comparison
    ax = axes[1, 0]
    
    categories = ['Correct', 'Minor (±1)', 'Major (±2)', 'Critical (±3+)']
    chatgpt_severity = [
        chatgpt_analysis['stats']['correct'],
        chatgpt_analysis['stats']['minor'],
        chatgpt_analysis['stats']['major'],
        chatgpt_analysis['stats']['critical']
    ]
    gemini_severity = [
        gemini_analysis['stats']['correct'],
        gemini_analysis['stats']['minor'],
        gemini_analysis['stats']['major'],
        gemini_analysis['stats']['critical']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    colors_sev = ['#2ECC71', '#F39C12', '#E67E22', '#C0392B']
    bars1 = ax.bar(x - width/2, chatgpt_severity, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_severity, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Error Severity Comparison', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    ax.legend()
    
    # 4. Mean error by grade level
    ax = axes[1, 1]
    
    chatgpt_df = chatgpt_analysis['df']
    gemini_df = gemini_analysis['df']
    
    grades = ['A', 'B', 'C', 'D']
    chatgpt_mean_errors = [chatgpt_df[chatgpt_df['expert_grade'] == g]['error_magnitude'].mean() 
                           for g in grades]
    gemini_mean_errors = [gemini_df[gemini_df['expert_grade'] == g]['error_magnitude'].mean() 
                          for g in grades]
    
    x = np.arange(len(grades))
    bars1 = ax.bar(x - width/2, chatgpt_mean_errors, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_mean_errors, width, label='Gemini', color='#A23B72')
    
    ax.set_xlabel('Expert Grade', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Error Magnitude', fontsize=11, fontweight='bold')
    ax.set_title('Average Error by Grade Level', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(grades)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    plt.suptitle('Error Analysis: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_confusion_heatmap(chatgpt_analysis, gemini_analysis, save_path):
    """Plot detailed confusion matrices with error highlighting."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    grades = ['A', 'B', 'C', 'D']
    
    # ChatGPT confusion matrix
    ax = axes[0]
    chatgpt_df = chatgpt_analysis['df']
    cm_chatgpt = confusion_matrix(chatgpt_df['expert_grade'], chatgpt_df['aes_grade'],
                                  labels=grades)
    cm_chatgpt_norm = cm_chatgpt.astype('float') / cm_chatgpt.sum(axis=1)[:, np.newaxis] * 100
    
    sns.heatmap(cm_chatgpt_norm, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
               xticklabels=grades, yticklabels=grades, cbar_kws={'label': 'Percentage (%)'},
               ax=ax, vmin=0, vmax=100)
    
    ax.set_xlabel('Predicted Grade', fontsize=11, fontweight='bold')
    ax.set_ylabel('Expert Grade', fontsize=11, fontweight='bold')
    ax.set_title(f'ChatGPT Confusion Matrix\n(Accuracy: {chatgpt_analysis["stats"]["correct_pct"]:.1f}%)',
                fontsize=13, fontweight='bold')
    
    # Gemini confusion matrix
    ax = axes[1]
    gemini_df = gemini_analysis['df']
    cm_gemini = confusion_matrix(gemini_df['expert_grade'], gemini_df['aes_grade'],
                                labels=grades)
    cm_gemini_norm = cm_gemini.astype('float') / cm_gemini.sum(axis=1)[:, np.newaxis] * 100
    
    sns.heatmap(cm_gemini_norm, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
               xticklabels=grades, yticklabels=grades, cbar_kws={'label': 'Percentage (%)'},
               ax=ax, vmin=0, vmax=100)
    
    ax.set_xlabel('Predicted Grade', fontsize=11, fontweight='bold')
    ax.set_ylabel('Expert Grade', fontsize=11, fontweight='bold')
    ax.set_title(f'Gemini Confusion Matrix\n(Accuracy: {gemini_analysis["stats"]["correct_pct"]:.1f}%)',
                fontsize=13, fontweight='bold')
    
    plt.suptitle('Confusion Matrices: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_error_by_question(chatgpt_analysis, gemini_analysis, save_path):
    """Plot error rates by question."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    chatgpt_df = chatgpt_analysis['df']
    gemini_df = gemini_analysis['df']
    
    questions = sorted(chatgpt_df['question_number'].unique())
    
    # 1. Error rate by question
    ax = axes[0]
    
    chatgpt_error_rates = []
    gemini_error_rates = []
    
    for q in questions:
        chatgpt_q = chatgpt_df[chatgpt_df['question_number'] == q]
        gemini_q = gemini_df[gemini_df['question_number'] == q]
        
        chatgpt_error = (chatgpt_q['error_type'] != 'Correct').sum() / len(chatgpt_q) * 100
        gemini_error = (gemini_q['error_type'] != 'Correct').sum() / len(gemini_q) * 100
        
        chatgpt_error_rates.append(chatgpt_error)
        gemini_error_rates.append(gemini_error)
    
    x = np.arange(len(questions))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, chatgpt_error_rates, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_error_rates, width, label='Gemini', color='#A23B72')
    
    ax.set_xlabel('Question Number', fontsize=11, fontweight='bold')
    ax.set_ylabel('Error Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('Overall Error Rate by Question', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Q{q}' for q in questions])
    ax.legend()
    ax.set_ylim(0, 50)
    ax.grid(alpha=0.3, axis='y')
    
    # 2. Critical error rate by question
    ax = axes[1]
    
    chatgpt_critical_rates = []
    gemini_critical_rates = []
    
    for q in questions:
        chatgpt_q = chatgpt_df[chatgpt_df['question_number'] == q]
        gemini_q = gemini_df[gemini_df['question_number'] == q]
        
        chatgpt_crit = (chatgpt_q['error_severity'].isin(['Major (±2)', 'Critical (±3+)'])).sum() / len(chatgpt_q) * 100
        gemini_crit = (gemini_q['error_severity'].isin(['Major (±2)', 'Critical (±3+)'])).sum() / len(gemini_q) * 100
        
        chatgpt_critical_rates.append(chatgpt_crit)
        gemini_critical_rates.append(gemini_crit)
    
    bars1 = ax.bar(x - width/2, chatgpt_critical_rates, width, label='ChatGPT', color='#E74C3C')
    bars2 = ax.bar(x + width/2, gemini_critical_rates, width, label='Gemini', color='#C0392B')
    
    ax.set_xlabel('Question Number', fontsize=11, fontweight='bold')
    ax.set_ylabel('Critical Error Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('Critical Error Rate by Question (±2 grades or more)', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Q{q}' for q in questions])
    ax.legend()
    ax.set_ylim(0, 15)
    ax.grid(alpha=0.3, axis='y')
    
    plt.suptitle('Error Analysis by Question',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_error_magnitude_distribution(chatgpt_analysis, gemini_analysis, save_path):
    """Plot error magnitude distributions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    chatgpt_df = chatgpt_analysis['df']
    gemini_df = gemini_analysis['df']
    
    # 1. Histogram - ChatGPT error magnitude
    ax = axes[0, 0]
    chatgpt_errors = chatgpt_df['error_magnitude'].dropna()
    
    bins = np.arange(-3.5, 4.5, 1)
    ax.hist(chatgpt_errors, bins=bins, color='#2E86AB', alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Correct')
    ax.set_xlabel('Error Magnitude', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_title(f'ChatGPT Error Distribution\n(Mean: {chatgpt_errors.mean():.3f}, SD: {chatgpt_errors.std():.3f})',
                fontsize=13, fontweight='bold')
    ax.set_xticks(range(-3, 4))
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # 2. Histogram - Gemini error magnitude
    ax = axes[0, 1]
    gemini_errors = gemini_df['error_magnitude'].dropna()
    
    ax.hist(gemini_errors, bins=bins, color='#A23B72', alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Correct')
    ax.set_xlabel('Error Magnitude', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_title(f'Gemini Error Distribution\n(Mean: {gemini_errors.mean():.3f}, SD: {gemini_errors.std():.3f})',
                fontsize=13, fontweight='bold')
    ax.set_xticks(range(-3, 4))
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # 3. Box plot comparison
    ax = axes[1, 0]
    data = [chatgpt_errors, gemini_errors]
    bp = ax.boxplot(data, labels=['ChatGPT', 'Gemini'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#2E86AB')
    bp['boxes'][1].set_facecolor('#A23B72')
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5)
    ax.set_ylabel('Error Magnitude', fontsize=11, fontweight='bold')
    ax.set_title('Error Magnitude Distribution', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    # 4. Cumulative distribution
    ax = axes[1, 1]
    
    chatgpt_sorted = np.sort(np.abs(chatgpt_errors))
    gemini_sorted = np.sort(np.abs(gemini_errors))
    
    chatgpt_cum = np.arange(1, len(chatgpt_sorted) + 1) / len(chatgpt_sorted) * 100
    gemini_cum = np.arange(1, len(gemini_sorted) + 1) / len(gemini_sorted) * 100
    
    ax.plot(chatgpt_sorted, chatgpt_cum, label='ChatGPT', color='#2E86AB', linewidth=2)
    ax.plot(gemini_sorted, gemini_cum, label='Gemini', color='#A23B72', linewidth=2)
    
    ax.set_xlabel('Absolute Error Magnitude', fontsize=11, fontweight='bold')
    ax.set_ylabel('Cumulative Percentage (%)', fontsize=11, fontweight='bold')
    ax.set_title('Cumulative Error Distribution', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 3)
    
    plt.suptitle('Error Magnitude Analysis',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_error_summary_table(chatgpt_analysis, gemini_analysis, save_path):
    """Generate comprehensive error analysis table."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ4: ERROR ANALYSIS - SUMMARY TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("ERROR TYPE DISTRIBUTION\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Error Type':<25} {'ChatGPT':<20} {'Gemini':<20} {'Difference':<15}\n")
        f.write("-"*80 + "\n")
        
        chatgpt_stats = chatgpt_analysis['stats']
        gemini_stats = gemini_analysis['stats']
        
        f.write(f"{'Correct':<25} {chatgpt_stats['correct']:<10} ({chatgpt_stats['correct_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['correct']:<10} ({gemini_stats['correct_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['correct_pct'] - chatgpt_stats['correct_pct']:>+6.1f}%\n")
        
        f.write(f"{'Over-grading':<25} {chatgpt_stats['over_grade']:<10} ({chatgpt_stats['over_grade_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['over_grade']:<10} ({gemini_stats['over_grade_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['over_grade_pct'] - chatgpt_stats['over_grade_pct']:>+6.1f}%\n")
        
        f.write(f"{'Under-grading':<25} {chatgpt_stats['under_grade']:<10} ({chatgpt_stats['under_grade_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['under_grade']:<10} ({gemini_stats['under_grade_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['under_grade_pct'] - chatgpt_stats['under_grade_pct']:>+6.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ERROR SEVERITY DISTRIBUTION\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Severity':<25} {'ChatGPT':<20} {'Gemini':<20} {'Difference':<15}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Correct':<25} {chatgpt_stats['correct']:<10} ({chatgpt_stats['correct_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['correct']:<10} ({gemini_stats['correct_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['correct_pct'] - chatgpt_stats['correct_pct']:>+6.1f}%\n")
        
        f.write(f"{'Minor (±1 grade)':<25} {chatgpt_stats['minor']:<10} ({chatgpt_stats['minor_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['minor']:<10} ({gemini_stats['minor_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['minor_pct'] - chatgpt_stats['minor_pct']:>+6.1f}%\n")
        
        f.write(f"{'Major (±2 grades)':<25} {chatgpt_stats['major']:<10} ({chatgpt_stats['major_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['major']:<10} ({gemini_stats['major_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['major_pct'] - chatgpt_stats['major_pct']:>+6.1f}%\n")
        
        f.write(f"{'Critical (±3+ grades)':<25} {chatgpt_stats['critical']:<10} ({chatgpt_stats['critical_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['critical']:<10} ({gemini_stats['critical_pct']:>5.1f}%) ")
        f.write(f"{gemini_stats['critical_pct'] - chatgpt_stats['critical_pct']:>+6.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ERROR STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Metric':<30} {'ChatGPT':<20} {'Gemini':<20}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Mean Error':<30} {chatgpt_stats['mean_error']:<20.3f} {gemini_stats['mean_error']:<20.3f}\n")
        f.write(f"{'Std Dev Error':<30} {chatgpt_stats['std_error']:<20.3f} {gemini_stats['std_error']:<20.3f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("CRITICAL ERROR ANALYSIS\n")
        f.write("-"*80 + "\n")
        
        chatgpt_critical = chatgpt_analysis['critical_errors']
        gemini_critical = gemini_analysis['critical_errors']
        
        f.write(f"\nChatGPT Critical Errors: {len(chatgpt_critical)} cases\n")
        if len(chatgpt_critical) > 0:
            f.write("Sample cases:\n")
            for idx, row in chatgpt_critical.head(5).iterrows():
                f.write(f"  Student {row['student_id']}, Q{row['question_number']}: "
                       f"Expert={row['expert_grade']}, AES={row['aes_grade']}, "
                       f"Error={row['error_magnitude']:+.0f}\n")
        
        f.write(f"\nGemini Critical Errors: {len(gemini_critical)} cases\n")
        if len(gemini_critical) > 0:
            f.write("Sample cases:\n")
            for idx, row in gemini_critical.head(5).iterrows():
                f.write(f"  Student {row['student_id']}, Q{row['question_number']}: "
                       f"Expert={row['expert_grade']}, AES={row['aes_grade']}, "
                       f"Error={row['error_magnitude']:+.0f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ERROR PATTERN INTERPRETATION\n")
        f.write("-"*80 + "\n\n")
        
        if chatgpt_stats['mean_error'] > 0:
            f.write("ChatGPT Tendency: OVER-GRADING (positive mean error)\n")
        elif chatgpt_stats['mean_error'] < 0:
            f.write("ChatGPT Tendency: UNDER-GRADING (negative mean error)\n")
        else:
            f.write("ChatGPT Tendency: BALANCED (zero mean error)\n")
        
        if gemini_stats['mean_error'] > 0:
            f.write("Gemini Tendency: OVER-GRADING (positive mean error)\n")
        elif gemini_stats['mean_error'] < 0:
            f.write("Gemini Tendency: UNDER-GRADING (negative mean error)\n")
        else:
            f.write("Gemini Tendency: BALANCED (zero mean error)\n")
        
        f.write("\n")
        
        if gemini_stats['correct_pct'] > chatgpt_stats['correct_pct']:
            f.write(f"Overall Winner: GEMINI (accuracy advantage: {gemini_stats['correct_pct'] - chatgpt_stats['correct_pct']:.1f}%)\n")
        else:
            f.write(f"Overall Winner: CHATGPT (accuracy advantage: {chatgpt_stats['correct_pct'] - gemini_stats['correct_pct']:.1f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_detailed_error_table(chatgpt_analysis, gemini_analysis, save_path):
    """Generate detailed error breakdown by grade and question."""
    
    chatgpt_df = chatgpt_analysis['df']
    gemini_df = gemini_analysis['df']
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ4: ERROR ANALYSIS - DETAILED BREAKDOWN\n")
        f.write("="*80 + "\n\n")
        
        f.write("ERROR RATE BY GRADE LEVEL\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Grade':<10} {'ChatGPT Error %':<20} {'Gemini Error %':<20} {'Difference':<15}\n")
        f.write("-"*80 + "\n")
        
        grades = ['A', 'B', 'C', 'D']
        for grade in grades:
            chatgpt_g = chatgpt_df[chatgpt_df['expert_grade'] == grade]
            gemini_g = gemini_df[gemini_df['expert_grade'] == grade]
            
            if len(chatgpt_g) > 0:
                chatgpt_error_rate = (chatgpt_g['error_type'] != 'Correct').sum() / len(chatgpt_g) * 100
            else:
                chatgpt_error_rate = 0
            
            if len(gemini_g) > 0:
                gemini_error_rate = (gemini_g['error_type'] != 'Correct').sum() / len(gemini_g) * 100
            else:
                gemini_error_rate = 0
            
            diff = gemini_error_rate - chatgpt_error_rate
            
            f.write(f"{grade:<10} {chatgpt_error_rate:<20.1f} {gemini_error_rate:<20.1f} {diff:>+6.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ERROR RATE BY QUESTION\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Question':<10} {'ChatGPT Error %':<20} {'Gemini Error %':<20} {'Difference':<15}\n")
        f.write("-"*80 + "\n")
        
        questions = sorted(chatgpt_df['question_number'].unique())
        for q in questions:
            chatgpt_q = chatgpt_df[chatgpt_df['question_number'] == q]
            gemini_q = gemini_df[gemini_df['question_number'] == q]
            
            chatgpt_error_rate = (chatgpt_q['error_type'] != 'Correct').sum() / len(chatgpt_q) * 100
            gemini_error_rate = (gemini_q['error_type'] != 'Correct').sum() / len(gemini_q) * 100
            
            diff = gemini_error_rate - chatgpt_error_rate
            
            f.write(f"Q{q:<9} {chatgpt_error_rate:<20.1f} {gemini_error_rate:<20.1f} {diff:>+6.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("CRITICAL ERROR RATE BY QUESTION\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Question':<10} {'ChatGPT Critical %':<20} {'Gemini Critical %':<20} {'Difference':<15}\n")
        f.write("-"*80 + "\n")
        
        for q in questions:
            chatgpt_q = chatgpt_df[chatgpt_df['question_number'] == q]
            gemini_q = gemini_df[gemini_df['question_number'] == q]
            
            chatgpt_crit_rate = (chatgpt_q['error_severity'].isin(['Major (±2)', 'Critical (±3+)'])).sum() / len(chatgpt_q) * 100
            gemini_crit_rate = (gemini_q['error_severity'].isin(['Major (±2)', 'Critical (±3+)'])).sum() / len(gemini_q) * 100
            
            diff = gemini_crit_rate - chatgpt_crit_rate
            
            f.write(f"Q{q:<9} {chatgpt_crit_rate:<20.1f} {gemini_crit_rate:<20.1f} {diff:>+6.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("RQ4: ERROR ANALYSIS")
    print("="*80)
    
    # Paths
    data_dir = project_root / "results" / "lenient_analysis"
    output_dir = project_root / "results" / "rq4_error_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nInput: {data_dir}")
    print(f"Output: {output_dir}")
    
    # Load data
    print("\n[1/6] Loading data...")
    df_chatgpt = pd.read_csv(data_dir / "lenient_chatgpt.csv")
    df_gemini = pd.read_csv(data_dir / "lenient_gemini.csv")
    
    # Filter valid expert grades
    df_chatgpt = df_chatgpt[df_chatgpt['expert_grade'].notna()].copy()
    df_gemini = df_gemini[df_gemini['expert_grade'].notna()].copy()
    
    print(f"  ChatGPT: {len(df_chatgpt)} records")
    print(f"  Gemini: {len(df_gemini)} records")
    
    # Analyze errors
    print("\n[2/6] Analyzing error patterns...")
    chatgpt_analysis = analyze_error_patterns(df_chatgpt, 'ChatGPT')
    gemini_analysis = analyze_error_patterns(df_gemini, 'Gemini')
    
    print(f"  ✓ ChatGPT: {chatgpt_analysis['stats']['correct_pct']:.1f}% correct, "
          f"{chatgpt_analysis['stats']['major'] + chatgpt_analysis['stats']['critical']} critical errors")
    print(f"  ✓ Gemini: {gemini_analysis['stats']['correct_pct']:.1f}% correct, "
          f"{gemini_analysis['stats']['major'] + gemini_analysis['stats']['critical']} critical errors")
    
    # Visualizations
    print("\n[3/6] Generating error distribution plots...")
    plot_error_distribution(chatgpt_analysis, gemini_analysis, 
                           output_dir / "error_distribution.png")
    
    print("[4/6] Generating confusion matrices...")
    plot_confusion_heatmap(chatgpt_analysis, gemini_analysis,
                          output_dir / "confusion_matrices.png")
    
    print("[5/6] Generating error by question plots...")
    plot_error_by_question(chatgpt_analysis, gemini_analysis,
                          output_dir / "error_by_question.png")
    
    print("[6/6] Generating error magnitude plots...")
    plot_error_magnitude_distribution(chatgpt_analysis, gemini_analysis,
                                     output_dir / "error_magnitude.png")
    
    # Tables
    print("\n[7/8] Generating error summary table...")
    generate_error_summary_table(chatgpt_analysis, gemini_analysis,
                                output_dir / "error_summary.txt")
    
    print("[8/8] Generating detailed error breakdown...")
    generate_detailed_error_table(chatgpt_analysis, gemini_analysis,
                                 output_dir / "detailed_breakdown.txt")
    
    # Final summary
    print("\n" + "="*80)
    print("RQ4 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  1. error_distribution.png")
    print("  2. confusion_matrices.png")
    print("  3. error_by_question.png")
    print("  4. error_magnitude.png")
    print("  5. error_summary.txt")
    print("  6. detailed_breakdown.txt")
    
    print("\nKey Findings:")
    print(f"  • ChatGPT: {chatgpt_analysis['stats']['correct_pct']:.1f}% accuracy, "
          f"Mean error: {chatgpt_analysis['stats']['mean_error']:+.3f}")
    print(f"  • Gemini: {gemini_analysis['stats']['correct_pct']:.1f}% accuracy, "
          f"Mean error: {gemini_analysis['stats']['mean_error']:+.3f}")
    print(f"  • Critical errors: ChatGPT {chatgpt_analysis['stats']['major'] + chatgpt_analysis['stats']['critical']}, "
          f"Gemini {gemini_analysis['stats']['major'] + gemini_analysis['stats']['critical']}")
    
    print("\nNext step: RQ5 - Practical Implications")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
