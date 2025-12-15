#!/usr/bin/env python3
"""
Comprehensive statistical tests for AES research paper
"""
import sqlite3
import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.proportion import proportion_confint
import warnings
warnings.filterwarnings('ignore')

def score_to_grade(score):
    """Convert GPA score to letter grade"""
    if score >= 3.5:
        return 'A'
    elif score >= 2.5:
        return 'B'
    elif score >= 1.5:
        return 'C'
    elif score >= 0.5:
        return 'D'
    else:
        return 'E'

def load_gold_standard():
    """Load gold standard grades"""
    gold_dir = Path('results/gold_standard')
    gold_data = {}
    
    for json_file in gold_dir.glob('student_*_gold.json'):
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
            student_name = data['student_name']
            student_num = ''.join(filter(str.isdigit, student_name))
            if student_num:
                student_id = f"student_{int(student_num):02d}"
            else:
                continue
                
            for q_idx, q in enumerate(data['questions'], start=1):
                score = q['weighted_score']
                gold_data[(student_id, q_idx)] = score
    
    return gold_data

def test_strategy_differences():
    """ANOVA: Test if strategies differ significantly"""
    print("\n" + "="*80)
    print("1. ANOVA: Strategy Differences")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        strategies_data = []
        strategy_names = []
        
        for strategy in ['lenient', 'few-shot', 'zero-shot']:
            # Find experiment ID
            if strategy == 'lenient':
                exp_pattern = f'exp_{model}_lenient'
            elif strategy == 'few-shot':
                exp_pattern = f'exp_{model}_few'
            else:
                exp_pattern = f'exp_{model}_zero'
            
            df = pd.read_sql_query(f"""
                SELECT student_id, question_number, weighted_score
                FROM grading_results
                WHERE experiment_id LIKE '{exp_pattern}%' AND status = 'completed'
            """, conn)
            
            # Calculate errors
            df['gold_score'] = df.apply(
                lambda row: gold_data.get((row['student_id'], row['question_number'])),
                axis=1
            )
            df = df.dropna()
            df['error'] = abs(df['weighted_score'] - df['gold_score'])
            
            strategies_data.append(df['error'].values)
            strategy_names.append(strategy)
        
        # ANOVA
        f_stat, p_value = stats.f_oneway(*strategies_data)
        
        print(f"  F-statistic: {f_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        
        if p_value < 0.001:
            print(f"  *** Highly significant difference (p < 0.001)")
        elif p_value < 0.01:
            print(f"  ** Very significant difference (p < 0.01)")
        elif p_value < 0.05:
            print(f"  * Significant difference (p < 0.05)")
        else:
            print(f"  No significant difference (p >= 0.05)")
        
        # Post-hoc pairwise t-tests
        print(f"\n  Post-hoc pairwise comparisons:")
        for i in range(len(strategies_data)):
            for j in range(i+1, len(strategies_data)):
                t_stat, p_val = stats.ttest_ind(strategies_data[i], strategies_data[j])
                print(f"    {strategy_names[i]} vs {strategy_names[j]}: t={t_stat:.3f}, p={p_val:.6f}")
    
    conn.close()

def test_model_differences():
    """Independent t-test: ChatGPT vs Gemini"""
    print("\n" + "="*80)
    print("2. Independent t-test: Model Comparison")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    for strategy in ['lenient', 'few-shot', 'zero-shot']:
        print(f"\n{strategy.upper()} Strategy:")
        
        # ChatGPT
        if strategy == 'lenient':
            exp_pattern_chat = 'exp_chatgpt_lenient'
            exp_pattern_gem = 'exp_gemini_lenient'
        elif strategy == 'few-shot':
            exp_pattern_chat = 'exp_chatgpt_few'
            exp_pattern_gem = 'exp_gemini_few'
        else:
            exp_pattern_chat = 'exp_chatgpt_zero'
            exp_pattern_gem = 'exp_gemini_zero'
        
        df_chat = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id LIKE '{exp_pattern_chat}%' AND status = 'completed'
        """, conn)
        
        df_gem = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id LIKE '{exp_pattern_gem}%' AND status = 'completed'
        """, conn)
        
        # Calculate errors
        df_chat['gold_score'] = df_chat.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df_chat = df_chat.dropna()
        df_chat['error'] = abs(df_chat['weighted_score'] - df_chat['gold_score'])
        
        df_gem['gold_score'] = df_gem.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df_gem = df_gem.dropna()
        df_gem['error'] = abs(df_gem['weighted_score'] - df_gem['gold_score'])
        
        # t-test
        t_stat, p_value = stats.ttest_ind(df_chat['error'], df_gem['error'])
        
        print(f"  ChatGPT MAE: {df_chat['error'].mean():.3f} (SD={df_chat['error'].std():.3f})")
        print(f"  Gemini MAE: {df_gem['error'].mean():.3f} (SD={df_gem['error'].std():.3f})")
        print(f"  t-statistic: {t_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(df_chat)-1)*df_chat['error'].std()**2 + 
                             (len(df_gem)-1)*df_gem['error'].std()**2) / 
                            (len(df_chat) + len(df_gem) - 2))
        cohens_d = (df_chat['error'].mean() - df_gem['error'].mean()) / pooled_std
        print(f"  Cohen's d: {cohens_d:.3f} ({'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'} effect)")
        
        if p_value < 0.001:
            print(f"  *** Highly significant difference (p < 0.001)")
        elif p_value < 0.01:
            print(f"  ** Very significant difference (p < 0.01)")
        elif p_value < 0.05:
            print(f"  * Significant difference (p < 0.05)")
        else:
            print(f"  No significant difference (p >= 0.05)")
    
    conn.close()

def test_kappa_confidence_intervals():
    """Bootstrap confidence intervals for Fleiss' Kappa"""
    print("\n" + "="*80)
    print("3. Fleiss' Kappa Confidence Intervals (Bootstrap)")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    # Load data from all raters
    experiments = {
        'ChatGPT-Lenient': 'exp_chatgpt_lenient_01',
        'ChatGPT-Few-shot': 'exp_chatgpt_few',
        'ChatGPT-Zero-shot': 'exp_chatgpt_zero',
        'Gemini-Lenient': 'exp_gemini_lenient_01',
    }
    
    all_data = []
    for name, exp_id in experiments.items():
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        df['grade'] = df['weighted_score'].apply(score_to_grade)
        df['rater'] = name
        all_data.append(df)
    
    combined = pd.concat(all_data, ignore_index=True)
    
    # Create rating matrix
    grades = ['A', 'B', 'C', 'D', 'E']
    items = combined.groupby(['student_id', 'question_number']).size().index
    
    rating_matrix = []
    for item in items:
        student_id, q_num = item
        item_data = combined[(combined['student_id'] == student_id) & 
                            (combined['question_number'] == q_num)]
        
        counts = [sum(item_data['grade'] == g) for g in grades]
        rating_matrix.append(counts)
    
    rating_matrix = np.array(rating_matrix)
    
    # Calculate Kappa
    kappa = fleiss_kappa(rating_matrix)
    print(f"\nFleiss' Kappa: {kappa:.4f}")
    
    # Bootstrap confidence interval
    n_bootstrap = 1000
    kappa_samples = []
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(len(rating_matrix), size=len(rating_matrix), replace=True)
        sample_matrix = rating_matrix[indices]
        try:
            k = fleiss_kappa(sample_matrix)
            kappa_samples.append(k)
        except:
            continue
    
    ci_lower = np.percentile(kappa_samples, 2.5)
    ci_upper = np.percentile(kappa_samples, 97.5)
    
    print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    # Interpretation
    if kappa >= 0.81:
        interpretation = "Almost Perfect Agreement"
    elif kappa >= 0.61:
        interpretation = "Substantial Agreement"
    elif kappa >= 0.41:
        interpretation = "Moderate Agreement"
    else:
        interpretation = "Fair to Poor Agreement"
    
    print(f"Interpretation: {interpretation}")
    
    conn.close()

def test_grade_distribution():
    """Chi-square test: Grade distribution differences"""
    print("\n" + "="*80)
    print("4. Chi-square: Grade Distribution Differences")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    # Compare ChatGPT vs Gemini (lenient)
    print("\nChatGPT vs Gemini (Lenient Strategy):")
    
    df_chat = pd.read_sql_query("""
        SELECT weighted_score
        FROM grading_results
        WHERE model = 'chatgpt' AND strategy = 'lenient' AND status = 'completed'
    """, conn)
    
    df_gem = pd.read_sql_query("""
        SELECT weighted_score
        FROM grading_results
        WHERE model = 'gemini' AND strategy = 'lenient' AND status = 'completed'
    """, conn)
    
    df_chat['grade'] = df_chat['weighted_score'].apply(score_to_grade)
    df_gem['grade'] = df_gem['weighted_score'].apply(score_to_grade)
    
    grades = ['A', 'B', 'C', 'D', 'E']
    chat_counts = [sum(df_chat['grade'] == g) for g in grades]
    gem_counts = [sum(df_gem['grade'] == g) for g in grades]
    
    # Remove grades with zero frequency in both
    filtered_grades = []
    filtered_chat_counts = []
    filtered_gem_counts = []
    for i, g in enumerate(grades):
        if chat_counts[i] > 0 or gem_counts[i] > 0:
            filtered_grades.append(g)
            filtered_chat_counts.append(chat_counts[i])
            filtered_gem_counts.append(gem_counts[i])
    
    contingency_table = np.array([filtered_chat_counts, filtered_gem_counts])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    print(f"\n  Observed frequencies:")
    print(f"    ChatGPT: {dict(zip(filtered_grades, filtered_chat_counts))}")
    print(f"    Gemini:  {dict(zip(filtered_grades, filtered_gem_counts))}")
    
    print(f"\n  Chi-square statistic: {chi2:.4f}")
    print(f"  Degrees of freedom: {dof}")
    print(f"  p-value: {p_value:.6f}")
    
    if p_value < 0.001:
        print(f"  *** Highly significant difference (p < 0.001)")
    elif p_value < 0.01:
        print(f"  ** Very significant difference (p < 0.01)")
    elif p_value < 0.05:
        print(f"  * Significant difference (p < 0.05)")
    else:
        print(f"  No significant difference (p >= 0.05)")
    
    # Cramér's V (effect size)
    n = contingency_table.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
    print(f"  Cramér's V: {cramers_v:.3f} ({'small' if cramers_v < 0.3 else 'medium' if cramers_v < 0.5 else 'large'} effect)")
    
    conn.close()

def test_correlation_significance():
    """Test significance of correlations with gold standard"""
    print("\n" + "="*80)
    print("5. Correlation Significance Tests")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    configs = [
        ('ChatGPT', 'lenient', 'exp_chatgpt_lenient_01'),
        ('Gemini', 'lenient', 'exp_gemini_lenient_01'),
        ('ChatGPT', 'few-shot', 'exp_chatgpt_few'),
        ('Gemini', 'few-shot', 'exp_gemini_few'),
        ('ChatGPT', 'zero-shot', 'exp_chatgpt_zero'),
        ('Gemini', 'zero-shot', 'exp_gemini_zero'),
    ]
    
    for model, strategy, exp_id in configs:
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        
        # Pearson correlation
        r_pearson, p_pearson = stats.pearsonr(df['gold_score'], df['weighted_score'])
        
        # Spearman correlation
        r_spearman, p_spearman = stats.spearmanr(df['gold_score'], df['weighted_score'])
        
        print(f"\n{model} ({strategy}):")
        print(f"  Pearson r: {r_pearson:.4f} (p < 0.0001)" if p_pearson < 0.0001 else f"  Pearson r: {r_pearson:.4f} (p = {p_pearson:.6f})")
        print(f"  Spearman ρ: {r_spearman:.4f} (p < 0.0001)" if p_spearman < 0.0001 else f"  Spearman ρ: {r_spearman:.4f} (p = {p_spearman:.6f})")
        
        # 95% CI for Pearson r (Fisher transformation)
        z = np.arctanh(r_pearson)
        se = 1/np.sqrt(len(df)-3)
        z_ci_low = z - 1.96*se
        z_ci_high = z + 1.96*se
        ci_low = np.tanh(z_ci_low)
        ci_high = np.tanh(z_ci_high)
        print(f"  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
    
    conn.close()

def test_exact_match_proportions():
    """Confidence intervals for exact match proportions"""
    print("\n" + "="*80)
    print("6. Exact Match Proportion Confidence Intervals")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    configs = [
        ('ChatGPT', 'lenient', 'exp_chatgpt_lenient_01'),
        ('Gemini', 'lenient', 'exp_gemini_lenient_01'),
    ]
    
    for model, strategy, exp_id in configs:
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        df = df.dropna()
        
        df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
        df['gold_grade'] = df['gold_score'].apply(score_to_grade)
        
        exact_matches = sum(df['ai_grade'] == df['gold_grade'])
        total = len(df)
        proportion = exact_matches / total
        
        # Wilson score interval
        ci_low, ci_high = proportion_confint(exact_matches, total, method='wilson')
        
        print(f"\n{model} ({strategy}):")
        print(f"  Exact match: {exact_matches}/{total} = {proportion*100:.2f}%")
        print(f"  95% CI: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")
    
    conn.close()

def main():
    print("\n" + "="*80)
    print("COMPREHENSIVE STATISTICAL TESTS")
    print("="*80)
    
    test_strategy_differences()
    test_model_differences()
    test_kappa_confidence_intervals()
    test_grade_distribution()
    test_correlation_significance()
    test_exact_match_proportions()
    
    print("\n" + "="*80)
    print("✓ ALL STATISTICAL TESTS COMPLETED!")
    print("="*80)

if __name__ == "__main__":
    main()
