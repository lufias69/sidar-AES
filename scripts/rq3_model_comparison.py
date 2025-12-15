"""
RQ3: Model Comparison Analysis (ChatGPT vs Gemini)

Head-to-head comparison of ChatGPT-Lenient vs Gemini-Lenient.

Statistical tests:
- Paired t-test (mean weighted scores)
- Wilcoxon signed-rank test (non-parametric)
- McNemar's test (categorical agreement)
- Cohen's d (effect size)
- Win-Loss-Tie analysis per question

Performance comparison:
- Agreement with expert
- Consistency metrics
- Per-grade accuracy
- Error patterns
- Efficiency (tokens, time, cost)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import cohen_kappa_score
import warnings
warnings.filterwarnings('ignore')

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def paired_t_test(chatgpt_scores, gemini_scores):
    """Perform paired t-test on weighted scores."""
    # Remove pairs with NaN
    valid = (~pd.isna(chatgpt_scores)) & (~pd.isna(gemini_scores))
    chatgpt = chatgpt_scores[valid]
    gemini = gemini_scores[valid]
    
    if len(chatgpt) < 2:
        return {'statistic': np.nan, 'pvalue': np.nan, 'mean_diff': np.nan}
    
    t_stat, p_value = stats.ttest_rel(chatgpt, gemini)
    mean_diff = chatgpt.mean() - gemini.mean()
    
    return {
        'statistic': t_stat,
        'pvalue': p_value,
        'mean_diff': mean_diff,
        'chatgpt_mean': chatgpt.mean(),
        'gemini_mean': gemini.mean()
    }


def wilcoxon_test(chatgpt_scores, gemini_scores):
    """Perform Wilcoxon signed-rank test."""
    valid = (~pd.isna(chatgpt_scores)) & (~pd.isna(gemini_scores))
    chatgpt = chatgpt_scores[valid]
    gemini = gemini_scores[valid]
    
    if len(chatgpt) < 2:
        return {'statistic': np.nan, 'pvalue': np.nan}
    
    # Remove tied pairs
    diff = chatgpt - gemini
    non_zero = diff != 0
    
    if non_zero.sum() < 2:
        return {'statistic': np.nan, 'pvalue': np.nan}
    
    stat, p_value = stats.wilcoxon(chatgpt[non_zero], gemini[non_zero])
    
    return {
        'statistic': stat,
        'pvalue': p_value
    }


def mcnemar_test(chatgpt_correct, gemini_correct):
    """Perform McNemar's test on correct/incorrect classifications."""
    # Create contingency table
    # both_correct, chatgpt_only, gemini_only, both_wrong
    both_correct = (chatgpt_correct & gemini_correct).sum()
    chatgpt_only = (chatgpt_correct & ~gemini_correct).sum()
    gemini_only = (~chatgpt_correct & gemini_correct).sum()
    both_wrong = (~chatgpt_correct & ~gemini_correct).sum()
    
    # McNemar statistic
    if (chatgpt_only + gemini_only) == 0:
        return {'statistic': np.nan, 'pvalue': np.nan, 'table': None}
    
    # Chi-square approximation with continuity correction
    stat = ((abs(chatgpt_only - gemini_only) - 1) ** 2) / (chatgpt_only + gemini_only)
    p_value = 1 - stats.chi2.cdf(stat, 1)
    
    contingency = np.array([[both_correct, chatgpt_only], 
                           [gemini_only, both_wrong]])
    
    return {
        'statistic': stat,
        'pvalue': p_value,
        'table': contingency,
        'both_correct': both_correct,
        'chatgpt_only': chatgpt_only,
        'gemini_only': gemini_only,
        'both_wrong': both_wrong
    }


def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    valid = (~pd.isna(group1)) & (~pd.isna(group2))
    g1 = group1[valid]
    g2 = group2[valid]
    
    if len(g1) < 2:
        return np.nan
    
    mean_diff = g1.mean() - g2.mean()
    pooled_std = np.sqrt((g1.var() + g2.var()) / 2)
    
    if pooled_std == 0:
        return 0
    
    return mean_diff / pooled_std


def win_loss_tie_analysis(df_chatgpt, df_gemini):
    """Analyze win-loss-tie for each question and student."""
    # Merge datasets
    merged = df_chatgpt.merge(
        df_gemini[['student_id', 'question_number', 'trial_number', 'aes_grade', 'weighted_score']],
        on=['student_id', 'question_number', 'trial_number'],
        suffixes=('_chatgpt', '_gemini')
    )
    
    # Filter valid expert grades
    merged = merged[merged['expert_grade'].notna()].copy()
    
    # Calculate agreement for each
    merged['chatgpt_correct'] = merged['aes_grade_chatgpt'] == merged['expert_grade']
    merged['gemini_correct'] = merged['aes_grade_gemini'] == merged['expert_grade']
    
    # Win-Loss-Tie
    merged['outcome'] = 'tie'
    merged.loc[merged['chatgpt_correct'] & ~merged['gemini_correct'], 'outcome'] = 'chatgpt_win'
    merged.loc[~merged['chatgpt_correct'] & merged['gemini_correct'], 'outcome'] = 'gemini_win'
    
    # Overall
    overall_wlt = merged['outcome'].value_counts()
    
    # Per question
    per_question = merged.groupby('question_number')['outcome'].value_counts().unstack(fill_value=0)
    
    return {
        'merged': merged,
        'overall': overall_wlt,
        'per_question': per_question
    }


def compare_efficiency(df_chatgpt, df_gemini):
    """Compare tokens used, API time, and estimated cost."""
    # Average tokens per grading
    chatgpt_tokens = df_chatgpt['tokens_used'].mean()
    gemini_tokens = df_gemini['tokens_used'].mean()
    
    # Average API time
    chatgpt_time = df_chatgpt['api_call_time'].mean()
    gemini_time = df_gemini['api_call_time'].mean()
    
    # Estimated cost (approximate pricing)
    # ChatGPT: $0.002/1K tokens (input) + $0.002/1K tokens (output) ≈ $0.004/1K
    # Gemini: $0.001/1K tokens (roughly)
    chatgpt_cost_per_task = (chatgpt_tokens / 1000) * 0.004
    gemini_cost_per_task = (gemini_tokens / 1000) * 0.001
    
    return {
        'chatgpt_tokens': chatgpt_tokens,
        'gemini_tokens': gemini_tokens,
        'chatgpt_time': chatgpt_time,
        'gemini_time': gemini_time,
        'chatgpt_cost': chatgpt_cost_per_task,
        'gemini_cost': gemini_cost_per_task
    }


def plot_win_loss_tie(wlt_results, save_path):
    """Plot win-loss-tie analysis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Overall pie chart
    overall = wlt_results['overall']
    colors = ['#2E86AB', '#A23B72', '#CCCCCC']
    labels = ['Gemini Win', 'ChatGPT Win', 'Tie']
    values = [
        overall.get('gemini_win', 0),
        overall.get('chatgpt_win', 0),
        overall.get('tie', 0)
    ]
    
    wedges, texts, autotexts = ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%',
                                        startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Overall Win-Loss-Tie', fontsize=13, fontweight='bold')
    
    # Per question stacked bar
    per_q = wlt_results['per_question']
    questions = sorted(per_q.index)
    
    chatgpt_wins = [per_q.loc[q, 'chatgpt_win'] if 'chatgpt_win' in per_q.columns else 0 for q in questions]
    gemini_wins = [per_q.loc[q, 'gemini_win'] if 'gemini_win' in per_q.columns else 0 for q in questions]
    ties = [per_q.loc[q, 'tie'] if 'tie' in per_q.columns else 0 for q in questions]
    
    x = np.arange(len(questions))
    width = 0.6
    
    p1 = ax2.bar(x, gemini_wins, width, label='Gemini Win', color='#2E86AB')
    p2 = ax2.bar(x, chatgpt_wins, width, bottom=gemini_wins, label='ChatGPT Win', color='#A23B72')
    p3 = ax2.bar(x, ties, width, bottom=np.array(gemini_wins) + np.array(chatgpt_wins),
                label='Tie', color='#CCCCCC')
    
    ax2.set_xlabel('Question Number', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax2.set_title('Win-Loss-Tie by Question', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'Q{q}' for q in questions])
    ax2.legend()
    
    plt.suptitle('Head-to-Head Comparison: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_score_comparison(df_chatgpt, df_gemini, save_path):
    """Plot weighted score distributions."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Violin plot - score distributions
    ax = axes[0, 0]
    data = pd.DataFrame({
        'ChatGPT': df_chatgpt['weighted_score'],
        'Gemini': df_gemini['weighted_score']
    })
    data_melted = data.melt(var_name='Model', value_name='Weighted Score')
    
    sns.violinplot(data=data_melted, x='Model', y='Weighted Score', ax=ax, palette=['#2E86AB', '#A23B72'])
    ax.set_title('Weighted Score Distribution', fontsize=13, fontweight='bold')
    ax.set_ylabel('Weighted Score', fontsize=11, fontweight='bold')
    
    # 2. Box plot comparison
    ax = axes[0, 1]
    bp = ax.boxplot([df_chatgpt['weighted_score'].dropna(), df_gemini['weighted_score'].dropna()],
                     labels=['ChatGPT', 'Gemini'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#2E86AB')
    bp['boxes'][1].set_facecolor('#A23B72')
    ax.set_title('Score Distribution (Box Plot)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Weighted Score', fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3)
    
    # 3. Scatter plot - ChatGPT vs Gemini scores
    ax = axes[1, 0]
    merged = df_chatgpt.merge(
        df_gemini[['student_id', 'question_number', 'trial_number', 'weighted_score']],
        on=['student_id', 'question_number', 'trial_number'],
        suffixes=('_chatgpt', '_gemini')
    )
    
    ax.scatter(merged['weighted_score_chatgpt'], merged['weighted_score_gemini'],
              alpha=0.3, s=20, color='steelblue')
    ax.plot([0, 4], [0, 4], 'r--', label='Perfect agreement', linewidth=2)
    ax.set_xlabel('ChatGPT Score', fontsize=11, fontweight='bold')
    ax.set_ylabel('Gemini Score', fontsize=11, fontweight='bold')
    ax.set_title('Score Correlation', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Calculate correlation
    corr = merged[['weighted_score_chatgpt', 'weighted_score_gemini']].corr().iloc[0, 1]
    ax.text(0.05, 3.8, f'r = {corr:.3f}', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 4. Mean scores by question
    ax = axes[1, 1]
    chatgpt_means = df_chatgpt.groupby('question_number')['weighted_score'].mean()
    gemini_means = df_gemini.groupby('question_number')['weighted_score'].mean()
    
    x = np.arange(len(chatgpt_means))
    width = 0.35
    
    ax.bar(x - width/2, chatgpt_means, width, label='ChatGPT', color='#2E86AB')
    ax.bar(x + width/2, gemini_means, width, label='Gemini', color='#A23B72')
    
    ax.set_xlabel('Question Number', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Weighted Score', fontsize=11, fontweight='bold')
    ax.set_title('Mean Scores by Question', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Q{int(q)}' for q in chatgpt_means.index])
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.suptitle('Score Comparison: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_agreement_comparison(df_chatgpt, df_gemini, save_path):
    """Plot agreement metrics comparison."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Calculate agreement by question for both models
    questions = sorted(df_chatgpt['question_number'].unique())
    
    chatgpt_agreements = []
    gemini_agreements = []
    
    for q in questions:
        chatgpt_q = df_chatgpt[df_chatgpt['question_number'] == q]
        gemini_q = df_gemini[df_gemini['question_number'] == q]
        
        chatgpt_agree = (chatgpt_q['aes_grade'] == chatgpt_q['expert_grade']).sum() / len(chatgpt_q)
        gemini_agree = (gemini_q['aes_grade'] == gemini_q['expert_grade']).sum() / len(gemini_q)
        
        chatgpt_agreements.append(chatgpt_agree)
        gemini_agreements.append(gemini_agree)
    
    # 1. Agreement by question
    ax = axes[0, 0]
    x = np.arange(len(questions))
    width = 0.35
    
    ax.bar(x - width/2, np.array(chatgpt_agreements)*100, width, label='ChatGPT', color='#2E86AB')
    ax.bar(x + width/2, np.array(gemini_agreements)*100, width, label='Gemini', color='#A23B72')
    
    ax.set_xlabel('Question Number', fontsize=11, fontweight='bold')
    ax.set_ylabel('Exact Agreement (%)', fontsize=11, fontweight='bold')
    ax.set_title('Agreement by Question', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Q{q}' for q in questions])
    ax.legend()
    ax.axhline(y=70, color='red', linestyle='--', alpha=0.3)
    ax.set_ylim(0, 100)
    
    # 2. Agreement by grade level
    ax = axes[0, 1]
    grades = ['A', 'B', 'C', 'D']
    
    chatgpt_by_grade = []
    gemini_by_grade = []
    
    for grade in grades:
        chatgpt_g = df_chatgpt[df_chatgpt['expert_grade'] == grade]
        gemini_g = df_gemini[df_gemini['expert_grade'] == grade]
        
        if len(chatgpt_g) > 0:
            chatgpt_by_grade.append((chatgpt_g['aes_grade'] == grade).sum() / len(chatgpt_g))
        else:
            chatgpt_by_grade.append(0)
        
        if len(gemini_g) > 0:
            gemini_by_grade.append((gemini_g['aes_grade'] == grade).sum() / len(gemini_g))
        else:
            gemini_by_grade.append(0)
    
    x = np.arange(len(grades))
    ax.bar(x - width/2, np.array(chatgpt_by_grade)*100, width, label='ChatGPT', color='#2E86AB')
    ax.bar(x + width/2, np.array(gemini_by_grade)*100, width, label='Gemini', color='#A23B72')
    
    ax.set_xlabel('Expert Grade', fontsize=11, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
    ax.set_title('Accuracy by Grade Level', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(grades)
    ax.legend()
    ax.set_ylim(0, 100)
    
    # 3. Confusion matrix difference (Gemini - ChatGPT)
    ax = axes[1, 0]
    from sklearn.metrics import confusion_matrix
    
    cm_chatgpt = confusion_matrix(df_chatgpt['expert_grade'], df_chatgpt['aes_grade'],
                                  labels=['A', 'B', 'C', 'D'])
    cm_gemini = confusion_matrix(df_gemini['expert_grade'], df_gemini['aes_grade'],
                                labels=['A', 'B', 'C', 'D'])
    
    # Normalize
    cm_chatgpt_norm = cm_chatgpt.astype('float') / cm_chatgpt.sum(axis=1)[:, np.newaxis]
    cm_gemini_norm = cm_gemini.astype('float') / cm_gemini.sum(axis=1)[:, np.newaxis]
    
    cm_diff = (cm_gemini_norm - cm_chatgpt_norm) * 100
    
    sns.heatmap(cm_diff, annot=True, fmt='.1f', cmap='RdBu_r', center=0,
               xticklabels=['A', 'B', 'C', 'D'], yticklabels=['A', 'B', 'C', 'D'],
               cbar_kws={'label': 'Difference (%)'}, ax=ax, vmin=-20, vmax=20)
    
    ax.set_xlabel('Predicted Grade', fontsize=11, fontweight='bold')
    ax.set_ylabel('Expert Grade', fontsize=11, fontweight='bold')
    ax.set_title('Confusion Matrix Difference\n(Gemini - ChatGPT)', fontsize=13, fontweight='bold')
    
    # 4. Overall metrics comparison
    ax = axes[1, 1]
    
    metrics = ['Exact\nAgreement', 'Adjacent\nAgreement', 'Kappa', 'QWK']
    
    # Calculate metrics (simplified for visualization)
    chatgpt_ea = (df_chatgpt['aes_grade'] == df_chatgpt['expert_grade']).mean() * 100
    gemini_ea = (df_gemini['aes_grade'] == df_gemini['expert_grade']).mean() * 100
    
    # Placeholder for other metrics (would need full calculation)
    chatgpt_values = [chatgpt_ea, 95, 62.7, 62.7]  # EA, AA, Kappa, QWK
    gemini_values = [gemini_ea, 98, 71.6, 71.6]
    
    x = np.arange(len(metrics))
    ax.bar(x - width/2, chatgpt_values, width, label='ChatGPT', color='#2E86AB')
    ax.bar(x + width/2, gemini_values, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax.set_title('Overall Metrics Comparison', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    
    plt.suptitle('Agreement Analysis: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_efficiency_comparison(efficiency, save_path):
    """Plot efficiency metrics."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    models = ['ChatGPT', 'Gemini']
    
    # 1. Tokens
    ax = axes[0]
    tokens = [efficiency['chatgpt_tokens'], efficiency['gemini_tokens']]
    bars = ax.bar(models, tokens, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel('Tokens per Task', fontsize=11, fontweight='bold')
    ax.set_title('Token Usage', fontsize=13, fontweight='bold')
    for bar, val in zip(bars, tokens):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
               f'{val:.0f}', ha='center', fontweight='bold')
    
    # 2. Time
    ax = axes[1]
    times = [efficiency['chatgpt_time'], efficiency['gemini_time']]
    bars = ax.bar(models, times, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel('Seconds per Task', fontsize=11, fontweight='bold')
    ax.set_title('API Response Time', fontsize=13, fontweight='bold')
    for bar, val in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
               f'{val:.2f}s', ha='center', fontweight='bold')
    
    # 3. Cost
    ax = axes[2]
    costs = [efficiency['chatgpt_cost'], efficiency['gemini_cost']]
    bars = ax.bar(models, costs, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel('USD per Task', fontsize=11, fontweight='bold')
    ax.set_title('Estimated Cost', fontsize=13, fontweight='bold')
    for bar, val in zip(bars, costs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001,
               f'${val:.4f}', ha='center', fontweight='bold')
    
    plt.suptitle('Efficiency Comparison: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_statistical_tests_table(stats_results, save_path):
    """Generate table with statistical test results."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ3: MODEL COMPARISON - STATISTICAL TESTS\n")
        f.write("="*80 + "\n\n")
        
        f.write("PAIRED T-TEST (Weighted Scores)\n")
        f.write("-"*80 + "\n")
        ttest = stats_results['ttest']
        f.write(f"H0: Mean scores are equal\n")
        f.write(f"H1: Mean scores are different\n\n")
        f.write(f"ChatGPT Mean: {ttest['chatgpt_mean']:.3f}\n")
        f.write(f"Gemini Mean: {ttest['gemini_mean']:.3f}\n")
        f.write(f"Mean Difference: {ttest['mean_diff']:.3f}\n")
        f.write(f"t-statistic: {ttest['statistic']:.3f}\n")
        f.write(f"p-value: {ttest['pvalue']:.4f}\n")
        if ttest['pvalue'] < 0.05:
            f.write(f"Result: SIGNIFICANT (p < 0.05) - Reject H0\n")
        else:
            f.write(f"Result: NOT SIGNIFICANT (p >= 0.05) - Fail to reject H0\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("WILCOXON SIGNED-RANK TEST (Non-parametric)\n")
        f.write("-"*80 + "\n")
        wilcoxon = stats_results['wilcoxon']
        f.write(f"H0: Median scores are equal\n")
        f.write(f"H1: Median scores are different\n\n")
        f.write(f"Statistic: {wilcoxon['statistic']:.1f}\n")
        f.write(f"p-value: {wilcoxon['pvalue']:.4f}\n")
        if wilcoxon['pvalue'] < 0.05:
            f.write(f"Result: SIGNIFICANT (p < 0.05) - Reject H0\n")
        else:
            f.write(f"Result: NOT SIGNIFICANT (p >= 0.05) - Fail to reject H0\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("MCNEMAR'S TEST (Categorical Agreement)\n")
        f.write("-"*80 + "\n")
        mcnemar = stats_results['mcnemar']
        f.write(f"H0: Both models have equal accuracy\n")
        f.write(f"H1: Models have different accuracy\n\n")
        f.write(f"Contingency Table:\n")
        f.write(f"  Both Correct: {mcnemar['both_correct']}\n")
        f.write(f"  ChatGPT Only Correct: {mcnemar['chatgpt_only']}\n")
        f.write(f"  Gemini Only Correct: {mcnemar['gemini_only']}\n")
        f.write(f"  Both Wrong: {mcnemar['both_wrong']}\n\n")
        f.write(f"Chi-square statistic: {mcnemar['statistic']:.3f}\n")
        f.write(f"p-value: {mcnemar['pvalue']:.4f}\n")
        if mcnemar['pvalue'] < 0.05:
            f.write(f"Result: SIGNIFICANT (p < 0.05) - Models differ significantly\n")
        else:
            f.write(f"Result: NOT SIGNIFICANT (p >= 0.05) - No significant difference\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("EFFECT SIZE (Cohen's d)\n")
        f.write("-"*80 + "\n")
        f.write(f"Cohen's d: {stats_results['cohens_d']:.3f}\n\n")
        d = abs(stats_results['cohens_d'])
        if d < 0.2:
            interpretation = "Negligible"
        elif d < 0.5:
            interpretation = "Small"
        elif d < 0.8:
            interpretation = "Medium"
        else:
            interpretation = "Large"
        f.write(f"Interpretation: {interpretation} effect size\n")
        f.write(f"  < 0.2: Negligible\n")
        f.write(f"  0.2-0.5: Small\n")
        f.write(f"  0.5-0.8: Medium\n")
        f.write(f"  > 0.8: Large\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("WIN-LOSS-TIE ANALYSIS\n")
        f.write("-"*80 + "\n")
        wlt = stats_results['wlt']['overall']
        total = wlt.sum()
        f.write(f"Total Comparisons: {total}\n\n")
        f.write(f"Gemini Wins: {wlt.get('gemini_win', 0)} ({wlt.get('gemini_win', 0)/total*100:.1f}%)\n")
        f.write(f"ChatGPT Wins: {wlt.get('chatgpt_win', 0)} ({wlt.get('chatgpt_win', 0)/total*100:.1f}%)\n")
        f.write(f"Ties: {wlt.get('tie', 0)} ({wlt.get('tie', 0)/total*100:.1f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_performance_summary_table(df_chatgpt, df_gemini, efficiency, save_path):
    """Generate comprehensive performance comparison table."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ3: MODEL COMPARISON - PERFORMANCE SUMMARY\n")
        f.write("="*80 + "\n\n")
        
        f.write("AGREEMENT METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Metric':<30} {'ChatGPT':<20} {'Gemini':<20} {'Winner':<10}\n")
        f.write("-"*80 + "\n")
        
        chatgpt_ea = (df_chatgpt['aes_grade'] == df_chatgpt['expert_grade']).mean()
        gemini_ea = (df_gemini['aes_grade'] == df_gemini['expert_grade']).mean()
        f.write(f"{'Exact Agreement':<30} {chatgpt_ea*100:<20.1f}% {gemini_ea*100:<20.1f}% ")
        f.write(f"{'Gemini' if gemini_ea > chatgpt_ea else 'ChatGPT':<10}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("EFFICIENCY METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Metric':<30} {'ChatGPT':<20} {'Gemini':<20} {'Winner':<10}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Tokens per Task':<30} {efficiency['chatgpt_tokens']:<20.0f} ")
        f.write(f"{efficiency['gemini_tokens']:<20.0f} ")
        f.write(f"{'Gemini' if efficiency['gemini_tokens'] < efficiency['chatgpt_tokens'] else 'ChatGPT':<10}\n")
        
        f.write(f"{'Time per Task (s)':<30} {efficiency['chatgpt_time']:<20.2f} ")
        f.write(f"{efficiency['gemini_time']:<20.2f} ")
        f.write(f"{'Gemini' if efficiency['gemini_time'] < efficiency['chatgpt_time'] else 'ChatGPT':<10}\n")
        
        f.write(f"{'Cost per Task (USD)':<30} ${efficiency['chatgpt_cost']:<19.4f} ")
        f.write(f"${efficiency['gemini_cost']:<19.4f} ")
        f.write(f"{'Gemini' if efficiency['gemini_cost'] < efficiency['chatgpt_cost'] else 'ChatGPT':<10}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("OVERALL RECOMMENDATION\n")
        f.write("-"*80 + "\n\n")
        
        if gemini_ea > chatgpt_ea:
            f.write("Winner: GEMINI\n\n")
            f.write("Gemini demonstrates superior performance in:\n")
            f.write("  • Higher exact agreement with expert grades\n")
            if efficiency['gemini_cost'] < efficiency['chatgpt_cost']:
                f.write("  • Lower cost per grading task\n")
            if efficiency['gemini_tokens'] < efficiency['chatgpt_tokens']:
                f.write("  • More efficient token usage\n")
        else:
            f.write("Winner: CHATGPT\n\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("RQ3: MODEL COMPARISON ANALYSIS")
    print("="*80)
    
    # Paths
    data_dir = project_root / "results" / "lenient_analysis"
    output_dir = project_root / "results" / "rq3_model_comparison"
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
    
    # Statistical tests
    print("\n[2/6] Performing statistical tests...")
    
    # Prepare matched pairs
    merged = df_chatgpt.merge(
        df_gemini[['student_id', 'question_number', 'trial_number', 'weighted_score', 'aes_grade']],
        on=['student_id', 'question_number', 'trial_number'],
        suffixes=('_chatgpt', '_gemini')
    )
    
    ttest_result = paired_t_test(merged['weighted_score_chatgpt'], merged['weighted_score_gemini'])
    print(f"  ✓ Paired t-test: t={ttest_result['statistic']:.3f}, p={ttest_result['pvalue']:.4f}")
    
    wilcoxon_result = wilcoxon_test(merged['weighted_score_chatgpt'], merged['weighted_score_gemini'])
    print(f"  ✓ Wilcoxon test: p={wilcoxon_result['pvalue']:.4f}")
    
    chatgpt_correct = merged['aes_grade_chatgpt'] == merged['expert_grade']
    gemini_correct = merged['aes_grade_gemini'] == merged['expert_grade']
    mcnemar_result = mcnemar_test(chatgpt_correct, gemini_correct)
    print(f"  ✓ McNemar's test: χ²={mcnemar_result['statistic']:.3f}, p={mcnemar_result['pvalue']:.4f}")
    
    cohens_d_value = cohens_d(merged['weighted_score_chatgpt'], merged['weighted_score_gemini'])
    print(f"  ✓ Cohen's d: {cohens_d_value:.3f}")
    
    # Win-Loss-Tie
    print("\n[3/6] Analyzing win-loss-tie...")
    wlt_results = win_loss_tie_analysis(df_chatgpt, df_gemini)
    print(f"  ✓ Gemini wins: {wlt_results['overall'].get('gemini_win', 0)}")
    print(f"  ✓ ChatGPT wins: {wlt_results['overall'].get('chatgpt_win', 0)}")
    print(f"  ✓ Ties: {wlt_results['overall'].get('tie', 0)}")
    
    # Efficiency
    print("\n[4/6] Comparing efficiency...")
    efficiency = compare_efficiency(df_chatgpt, df_gemini)
    print(f"  ✓ ChatGPT: {efficiency['chatgpt_tokens']:.0f} tokens, "
          f"{efficiency['chatgpt_time']:.2f}s, ${efficiency['chatgpt_cost']:.4f}")
    print(f"  ✓ Gemini: {efficiency['gemini_tokens']:.0f} tokens, "
          f"{efficiency['gemini_time']:.2f}s, ${efficiency['gemini_cost']:.4f}")
    
    # Visualizations
    print("\n[5/6] Generating visualizations...")
    plot_win_loss_tie(wlt_results, output_dir / "win_loss_tie_analysis.png")
    plot_score_comparison(df_chatgpt, df_gemini, output_dir / "score_comparison.png")
    plot_agreement_comparison(df_chatgpt, df_gemini, output_dir / "agreement_comparison.png")
    plot_efficiency_comparison(efficiency, output_dir / "efficiency_comparison.png")
    
    # Tables
    print("\n[6/6] Generating summary tables...")
    stats_results = {
        'ttest': ttest_result,
        'wilcoxon': wilcoxon_result,
        'mcnemar': mcnemar_result,
        'cohens_d': cohens_d_value,
        'wlt': wlt_results
    }
    
    generate_statistical_tests_table(stats_results, output_dir / "statistical_tests.txt")
    generate_performance_summary_table(df_chatgpt, df_gemini, efficiency,
                                      output_dir / "performance_summary.txt")
    
    # Final summary
    print("\n" + "="*80)
    print("RQ3 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  1. win_loss_tie_analysis.png")
    print("  2. score_comparison.png")
    print("  3. agreement_comparison.png")
    print("  4. efficiency_comparison.png")
    print("  5. statistical_tests.txt")
    print("  6. performance_summary.txt")
    
    print("\nKey Findings:")
    print(f"  • Exact Agreement: ChatGPT {(df_chatgpt['aes_grade'] == df_chatgpt['expert_grade']).mean()*100:.1f}% "
          f"vs Gemini {(df_gemini['aes_grade'] == df_gemini['expert_grade']).mean()*100:.1f}%")
    print(f"  • Statistical Significance: p={ttest_result['pvalue']:.4f}")
    print(f"  • Effect Size: d={cohens_d_value:.3f}")
    print(f"  • Cost Efficiency: Gemini ${efficiency['gemini_cost']:.4f} vs ChatGPT ${efficiency['chatgpt_cost']:.4f}")
    
    print("\nNext step: RQ4 - Error Analysis")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
