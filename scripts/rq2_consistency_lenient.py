"""
RQ2: Inter-Rater Reliability Analysis

Analyzes consistency of AES across 10 trials (treating each trial as a "rater").

Metrics calculated:
- Intraclass Correlation Coefficient (ICC)
  - ICC(2,1) for single measures
  - ICC(2,k) for average measures
- Cronbach's Alpha (internal consistency)
- Fleiss' Kappa (multi-rater agreement)
- Variance decomposition (between vs within trial variance)

Analysis per:
- Overall (all questions combined)
- Per question
- Per model (ChatGPT vs Gemini)
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


def calculate_icc(data):
    """
    Calculate ICC(2,1) and ICC(2,k) for consistency.
    
    Data should be: rows=subjects (student-question pairs), columns=trials (raters)
    """
    # Remove rows with any NaN
    data = data.dropna()
    
    if len(data) == 0 or data.shape[1] < 2:
        return {'icc_single': np.nan, 'icc_average': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan}
    
    n = data.shape[0]  # number of subjects
    k = data.shape[1]  # number of raters (trials)
    
    # Convert grades to numeric
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    data_numeric = data.applymap(lambda x: grade_map.get(x, np.nan))
    data_numeric = data_numeric.dropna()
    
    if len(data_numeric) == 0:
        return {'icc_single': np.nan, 'icc_average': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan}
    
    n = data_numeric.shape[0]
    k = data_numeric.shape[1]
    
    # Mean for each subject
    subject_means = data_numeric.mean(axis=1)
    # Grand mean
    grand_mean = data_numeric.values.mean()
    
    # Sum of squares
    # Between subjects
    ss_between = k * np.sum((subject_means - grand_mean) ** 2)
    # Within subjects (residual)
    ss_within = np.sum((data_numeric.values - subject_means.values.reshape(-1, 1)) ** 2)
    # Total
    ss_total = np.sum((data_numeric.values - grand_mean) ** 2)
    
    # Mean squares
    ms_between = ss_between / (n - 1)
    ms_within = ss_within / (n * (k - 1))
    
    # ICC(2,1) - single measure
    icc_single = (ms_between - ms_within) / (ms_between + (k - 1) * ms_within)
    
    # ICC(2,k) - average measures
    icc_average = (ms_between - ms_within) / ms_between
    
    # Confidence interval (95%) for ICC(2,1)
    f_stat = ms_between / ms_within
    df1 = n - 1
    df2 = n * (k - 1)
    
    f_lower = f_stat / stats.f.ppf(0.975, df1, df2)
    f_upper = f_stat / stats.f.ppf(0.025, df1, df2)
    
    ci_lower = (f_lower - 1) / (f_lower + k - 1)
    ci_upper = (f_upper - 1) / (f_upper + k - 1)
    
    return {
        'icc_single': max(0, icc_single),  # ICC can't be negative
        'icc_average': max(0, icc_average),
        'ci_lower': max(0, ci_lower),
        'ci_upper': min(1, ci_upper),
        'n_subjects': n,
        'n_raters': k
    }


def calculate_cronbach_alpha(data):
    """Calculate Cronbach's Alpha for internal consistency."""
    # Remove rows with any NaN
    data = data.dropna()
    
    if len(data) == 0 or data.shape[1] < 2:
        return np.nan
    
    # Convert to numeric
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    data_numeric = data.applymap(lambda x: grade_map.get(x, np.nan))
    data_numeric = data_numeric.dropna()
    
    if len(data_numeric) == 0:
        return np.nan
    
    k = data_numeric.shape[1]  # number of items (trials)
    
    # Variance of each item (trial)
    item_variances = data_numeric.var(axis=0, ddof=1)
    # Variance of total scores
    total_variance = data_numeric.sum(axis=1).var(ddof=1)
    
    # Cronbach's Alpha
    alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
    
    return alpha


def calculate_fleiss_kappa(data):
    """Calculate Fleiss' Kappa for multi-rater agreement."""
    # Remove rows with any NaN
    data = data.dropna()
    
    if len(data) == 0 or data.shape[1] < 2:
        return np.nan
    
    n = len(data)  # number of subjects
    k = data.shape[1]  # number of raters
    
    # Get all unique categories
    categories = ['A', 'B', 'C', 'D', 'E']
    
    # Count matrix: n subjects × c categories
    count_matrix = np.zeros((n, len(categories)))
    
    for i, row in enumerate(data.values):
        for rating in row:
            if rating in categories:
                cat_idx = categories.index(rating)
                count_matrix[i, cat_idx] += 1
    
    # Proportion of all assignments in each category
    p_j = count_matrix.sum(axis=0) / (n * k)
    
    # Calculate P_i (extent of agreement for subject i)
    P_i = []
    for i in range(n):
        sum_n_ij_squared = np.sum(count_matrix[i] ** 2)
        P_i.append((sum_n_ij_squared - k) / (k * (k - 1)))
    
    # Mean agreement
    P_bar = np.mean(P_i)
    
    # Expected agreement
    P_e = np.sum(p_j ** 2)
    
    # Fleiss' Kappa
    if P_e == 1:
        return 0
    
    kappa = (P_bar - P_e) / (1 - P_e)
    
    return kappa


def analyze_variance_decomposition(data):
    """Decompose variance into between-trial and within-trial components."""
    # Remove rows with any NaN
    data = data.dropna()
    
    if len(data) == 0:
        return {'between_trial': np.nan, 'within_trial': np.nan, 'total': np.nan}
    
    # Convert to numeric
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    data_numeric = data.applymap(lambda x: grade_map.get(x, np.nan))
    data_numeric = data_numeric.dropna()
    
    if len(data_numeric) == 0:
        return {'between_trial': np.nan, 'within_trial': np.nan, 'total': np.nan}
    
    # Total variance
    total_var = data_numeric.values.var()
    
    # Between-trial variance (variance of trial means)
    trial_means = data_numeric.mean(axis=0)
    between_var = trial_means.var()
    
    # Within-trial variance (average of trial variances)
    within_var = data_numeric.var(axis=0).mean()
    
    return {
        'between_trial': between_var,
        'within_trial': within_var,
        'total': total_var,
        'between_pct': (between_var / total_var * 100) if total_var > 0 else 0,
        'within_pct': (within_var / total_var * 100) if total_var > 0 else 0
    }


def prepare_trial_matrix(df, model=None):
    """Prepare data matrix: rows=subjects, columns=trials."""
    if model:
        df = df[df['model'] == model].copy()
    
    # Create unique subject identifier
    df['subject_id'] = df['student_id'] + '_Q' + df['question_number'].astype(str)
    
    # Pivot: subjects × trials
    matrix = df.pivot_table(
        index='subject_id',
        columns='trial_number',
        values='aes_grade',
        aggfunc='first'
    )
    
    return matrix


def plot_icc_by_question(df, model_name, save_path):
    """Plot ICC scores for each question."""
    questions = sorted(df['question_number'].unique())
    
    icc_singles = []
    icc_averages = []
    ci_lowers = []
    ci_uppers = []
    
    for q in questions:
        q_data = df[df['question_number'] == q].copy()
        q_data['subject_id'] = q_data['student_id']
        
        matrix = q_data.pivot_table(
            index='subject_id',
            columns='trial_number',
            values='aes_grade',
            aggfunc='first'
        )
        
        icc_result = calculate_icc(matrix)
        icc_singles.append(icc_result['icc_single'])
        icc_averages.append(icc_result['icc_average'])
        ci_lowers.append(icc_result['ci_lower'])
        ci_uppers.append(icc_result['ci_upper'])
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    x = np.arange(len(questions))
    
    # ICC(2,1) - Single measures
    ax1.errorbar(x, icc_singles, 
                 yerr=[np.array(icc_singles) - np.array(ci_lowers),
                       np.array(ci_uppers) - np.array(icc_singles)],
                 fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8)
    ax1.set_xlabel('Question Number', fontsize=12, fontweight='bold')
    ax1.set_ylabel('ICC(2,1)', fontsize=12, fontweight='bold')
    ax1.set_title('ICC - Single Measures', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'Q{q}' for q in questions])
    ax1.axhline(y=0.75, color='green', linestyle='--', alpha=0.3, label='Excellent (0.75)')
    ax1.axhline(y=0.60, color='orange', linestyle='--', alpha=0.3, label='Good (0.60)')
    ax1.legend()
    ax1.set_ylim(0, 1)
    ax1.grid(alpha=0.3)
    
    # ICC(2,k) - Average measures
    ax2.bar(x, icc_averages, color='steelblue', alpha=0.7)
    ax2.set_xlabel('Question Number', fontsize=12, fontweight='bold')
    ax2.set_ylabel('ICC(2,k)', fontsize=12, fontweight='bold')
    ax2.set_title('ICC - Average Measures', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'Q{q}' for q in questions])
    ax2.axhline(y=0.75, color='green', linestyle='--', alpha=0.3, label='Excellent (0.75)')
    ax2.axhline(y=0.90, color='red', linestyle='--', alpha=0.3, label='Outstanding (0.90)')
    ax2.legend()
    ax2.set_ylim(0, 1)
    ax2.grid(alpha=0.3)
    
    # Add values on bars
    for i, v in enumerate(icc_averages):
        ax2.text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold', fontsize=9)
    
    plt.suptitle(f'Intraclass Correlation Coefficient - {model_name}',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_consistency_heatmap(df, model_name, save_path):
    """Plot trial-to-trial consistency heatmap."""
    matrix = prepare_trial_matrix(df)
    
    # Calculate pairwise agreement between trials
    trials = sorted(matrix.columns)
    n_trials = len(trials)
    agreement_matrix = np.zeros((n_trials, n_trials))
    
    for i, trial_i in enumerate(trials):
        for j, trial_j in enumerate(trials):
            if i == j:
                agreement_matrix[i, j] = 1.0
            else:
                # Calculate agreement
                valid_pairs = matrix[[trial_i, trial_j]].dropna()
                if len(valid_pairs) > 0:
                    agreement = (valid_pairs[trial_i] == valid_pairs[trial_j]).sum() / len(valid_pairs)
                    agreement_matrix[i, j] = agreement
                else:
                    agreement_matrix[i, j] = np.nan
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(agreement_matrix * 100, annot=True, fmt='.1f', cmap='RdYlGn',
                xticklabels=[f'T{t}' for t in trials],
                yticklabels=[f'T{t}' for t in trials],
                cbar_kws={'label': 'Agreement (%)'},
                vmin=50, vmax=100, ax=ax)
    
    ax.set_xlabel('Trial', fontsize=12, fontweight='bold')
    ax.set_ylabel('Trial', fontsize=12, fontweight='bold')
    ax.set_title(f'Trial-to-Trial Agreement Heatmap - {model_name}',
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_variance_decomposition(variance_results, save_path):
    """Plot variance decomposition."""
    models = list(variance_results.keys())
    between_pcts = [variance_results[m]['between_pct'] for m in models]
    within_pcts = [variance_results[m]['within_pct'] for m in models]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, between_pcts, width, label='Between-Trial', color='steelblue')
    bars2 = ax.bar(x + width/2, within_pcts, width, label='Within-Trial', color='coral')
    
    ax.set_ylabel('Percentage of Total Variance (%)', fontsize=12, fontweight='bold')
    ax.set_title('Variance Decomposition: Between-Trial vs Within-Trial',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.set_ylim(0, 100)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_reliability_summary(reliability_metrics, save_path):
    """Plot summary of all reliability metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    models = list(reliability_metrics.keys())
    
    # 1. ICC Single
    ax = axes[0, 0]
    icc_singles = [reliability_metrics[m]['icc_single'] for m in models]
    bars = ax.bar(models, icc_singles, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel('ICC(2,1)', fontsize=11, fontweight='bold')
    ax.set_title('ICC - Single Measures', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.75, color='green', linestyle='--', alpha=0.3, label='Excellent')
    ax.legend()
    for bar, val in zip(bars, icc_singles):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    # 2. ICC Average
    ax = axes[0, 1]
    icc_averages = [reliability_metrics[m]['icc_average'] for m in models]
    bars = ax.bar(models, icc_averages, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel('ICC(2,k)', fontsize=11, fontweight='bold')
    ax.set_title('ICC - Average Measures', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.90, color='green', linestyle='--', alpha=0.3, label='Outstanding')
    ax.legend()
    for bar, val in zip(bars, icc_averages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    # 3. Cronbach's Alpha
    ax = axes[1, 0]
    alphas = [reliability_metrics[m]['cronbach_alpha'] for m in models]
    bars = ax.bar(models, alphas, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel("Cronbach's Alpha", fontsize=11, fontweight='bold')
    ax.set_title('Internal Consistency', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.70, color='orange', linestyle='--', alpha=0.3, label='Acceptable (0.70)')
    ax.axhline(y=0.80, color='green', linestyle='--', alpha=0.3, label='Good (0.80)')
    ax.legend()
    for bar, val in zip(bars, alphas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    # 4. Fleiss' Kappa
    ax = axes[1, 1]
    kappas = [reliability_metrics[m]['fleiss_kappa'] for m in models]
    bars = ax.bar(models, kappas, color=['#2E86AB', '#A23B72'])
    ax.set_ylabel("Fleiss' Kappa", fontsize=11, fontweight='bold')
    ax.set_title('Multi-Rater Agreement', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.axhline(y=0.60, color='orange', linestyle='--', alpha=0.3, label='Substantial (0.60)')
    ax.axhline(y=0.80, color='green', linestyle='--', alpha=0.3, label='Almost Perfect (0.80)')
    ax.legend()
    for bar, val in zip(bars, kappas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.3f}', ha='center', fontweight='bold')
    
    plt.suptitle('Inter-Rater Reliability Metrics Summary',
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_summary_table(reliability_metrics, variance_results, save_path):
    """Generate comprehensive summary table."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ2: INTER-RATER RELIABILITY ANALYSIS - SUMMARY TABLE\n")
        f.write("="*80 + "\n\n")
        
        f.write("OVERALL RELIABILITY METRICS\n")
        f.write("-"*80 + "\n\n")
        
        f.write(f"{'Model':<20} {'ICC(2,1)':<12} {'ICC(2,k)':<12} {'Alpha':<12} {'Fleiss κ':<12}\n")
        f.write("-"*80 + "\n")
        
        for model, metrics in reliability_metrics.items():
            f.write(f"{model:<20} "
                   f"{metrics['icc_single']:<12.3f} "
                   f"{metrics['icc_average']:<12.3f} "
                   f"{metrics['cronbach_alpha']:<12.3f} "
                   f"{metrics['fleiss_kappa']:<12.3f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("VARIANCE DECOMPOSITION\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"{'Model':<20} {'Between-Trial':<15} {'Within-Trial':<15} {'Total':<15}\n")
        f.write("-"*80 + "\n")
        
        for model, var in variance_results.items():
            f.write(f"{model:<20} "
                   f"{var['between_pct']:<15.1f}% "
                   f"{var['within_pct']:<15.1f}% "
                   f"100.0%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("INTERPRETATION GUIDELINES\n")
        f.write("="*80 + "\n\n")
        
        f.write("ICC (Intraclass Correlation Coefficient):\n")
        f.write("  ICC(2,1) - Single measure consistency\n")
        f.write("  ICC(2,k) - Average of k measures consistency\n")
        f.write("  < 0.50: Poor reliability\n")
        f.write("  0.50-0.75: Moderate reliability\n")
        f.write("  0.75-0.90: Good reliability\n")
        f.write("  > 0.90: Excellent reliability\n\n")
        
        f.write("Cronbach's Alpha:\n")
        f.write("  Measures internal consistency\n")
        f.write("  < 0.60: Unacceptable\n")
        f.write("  0.60-0.70: Questionable\n")
        f.write("  0.70-0.80: Acceptable\n")
        f.write("  0.80-0.90: Good\n")
        f.write("  > 0.90: Excellent\n\n")
        
        f.write("Fleiss' Kappa:\n")
        f.write("  Multi-rater agreement (10 trials as raters)\n")
        f.write("  < 0.00: Poor agreement\n")
        f.write("  0.00-0.20: Slight agreement\n")
        f.write("  0.21-0.40: Fair agreement\n")
        f.write("  0.41-0.60: Moderate agreement\n")
        f.write("  0.61-0.80: Substantial agreement\n")
        f.write("  0.81-1.00: Almost perfect agreement\n\n")
        
        f.write("Variance Decomposition:\n")
        f.write("  Between-Trial: Variance due to differences between trials\n")
        f.write("  Within-Trial: Variance within each trial (student/question differences)\n")
        f.write("  Lower between-trial % = Higher consistency across trials\n\n")
        
        f.write("="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("RQ2: INTER-RATER RELIABILITY ANALYSIS")
    print("="*80)
    
    # Paths
    data_dir = project_root / "results" / "lenient_analysis"
    output_dir = project_root / "results" / "rq2_consistency"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nInput: {data_dir}")
    print(f"Output: {output_dir}")
    
    # Load data
    print("\n[1/6] Loading data...")
    df_chatgpt = pd.read_csv(data_dir / "lenient_chatgpt.csv")
    df_gemini = pd.read_csv(data_dir / "lenient_gemini.csv")
    
    # Filter only valid expert grades
    df_chatgpt = df_chatgpt[df_chatgpt['expert_grade'].notna()].copy()
    df_gemini = df_gemini[df_gemini['expert_grade'].notna()].copy()
    
    print(f"  ChatGPT: {len(df_chatgpt)} records, {len(df_chatgpt['trial_number'].unique())} trials")
    print(f"  Gemini: {len(df_gemini)} records, {len(df_gemini['trial_number'].unique())} trials")
    
    # Calculate reliability metrics
    print("\n[2/6] Calculating reliability metrics...")
    
    reliability_metrics = {}
    
    for model_name, df in [('ChatGPT-Lenient', df_chatgpt), ('Gemini-Lenient', df_gemini)]:
        matrix = prepare_trial_matrix(df)
        
        icc_result = calculate_icc(matrix)
        alpha = calculate_cronbach_alpha(matrix)
        fleiss = calculate_fleiss_kappa(matrix)
        
        reliability_metrics[model_name] = {
            'icc_single': icc_result['icc_single'],
            'icc_average': icc_result['icc_average'],
            'cronbach_alpha': alpha,
            'fleiss_kappa': fleiss
        }
        
        print(f"  ✓ {model_name}: ICC(2,1)={icc_result['icc_single']:.3f}, "
              f"Alpha={alpha:.3f}, Fleiss κ={fleiss:.3f}")
    
    # Variance decomposition
    print("\n[3/6] Analyzing variance decomposition...")
    
    variance_results = {}
    for model_name, df in [('ChatGPT-Lenient', df_chatgpt), ('Gemini-Lenient', df_gemini)]:
        matrix = prepare_trial_matrix(df)
        var_result = analyze_variance_decomposition(matrix)
        variance_results[model_name] = var_result
        
        print(f"  ✓ {model_name}: Between={var_result['between_pct']:.1f}%, "
              f"Within={var_result['within_pct']:.1f}%")
    
    # Generate visualizations
    print("\n[4/6] Generating ICC plots...")
    plot_icc_by_question(df_chatgpt, 'ChatGPT-Lenient', 
                         output_dir / "icc_by_question_chatgpt.png")
    plot_icc_by_question(df_gemini, 'Gemini-Lenient',
                         output_dir / "icc_by_question_gemini.png")
    
    print("\n[5/6] Generating consistency heatmaps...")
    plot_consistency_heatmap(df_chatgpt, 'ChatGPT-Lenient',
                            output_dir / "consistency_heatmap_chatgpt.png")
    plot_consistency_heatmap(df_gemini, 'Gemini-Lenient',
                            output_dir / "consistency_heatmap_gemini.png")
    
    plot_variance_decomposition(variance_results,
                               output_dir / "variance_decomposition.png")
    
    plot_reliability_summary(reliability_metrics,
                            output_dir / "reliability_summary.png")
    
    # Generate summary table
    print("\n[6/6] Generating summary table...")
    generate_summary_table(reliability_metrics, variance_results,
                          output_dir / "summary_table.txt")
    
    # Final summary
    print("\n" + "="*80)
    print("RQ2 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  1. icc_by_question_chatgpt.png")
    print("  2. icc_by_question_gemini.png")
    print("  3. consistency_heatmap_chatgpt.png")
    print("  4. consistency_heatmap_gemini.png")
    print("  5. variance_decomposition.png")
    print("  6. reliability_summary.png")
    print("  7. summary_table.txt")
    
    print("\nKey Findings:")
    for model, metrics in reliability_metrics.items():
        print(f"  • {model}:")
        print(f"    - ICC(2,k): {metrics['icc_average']:.3f}")
        print(f"    - Cronbach's Alpha: {metrics['cronbach_alpha']:.3f}")
        print(f"    - Fleiss' Kappa: {metrics['fleiss_kappa']:.3f}")
    
    print("\nNext step: RQ3 - Model Comparison Analysis")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
