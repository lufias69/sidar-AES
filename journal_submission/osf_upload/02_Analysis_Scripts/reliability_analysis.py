"""
Reliability Analysis for Automated Essay Scoring Study
=======================================================

This script calculates reliability metrics for repeated AI grading:
- Intraclass Correlation Coefficient (ICC 2,1)
- Fleiss' Kappa for multi-rater agreement
- Coefficient of Variation (CV)
- Standard deviation across trials

Usage:
    python reliability_analysis.py

Requirements:
    - pandas
    - numpy
    - pingouin (for ICC calculation)
    - statsmodels (for Fleiss' kappa)

Input:
    - Trial-by-trial AI grading results (you need to provide)

Output:
    - Reliability metrics printed to console
    - Comparison to published values

Author: AES Research Team
Date: December 2025
License: MIT
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Optional imports (install if needed)
try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False
    print("WARNING: pingouin not installed. ICC calculation will be skipped.")
    print("Install with: pip install pingouin")

try:
    from statsmodels.stats.inter_rater import fleiss_kappa
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("WARNING: statsmodels not installed. Fleiss' kappa calculation will be skipped.")
    print("Install with: pip install statsmodels")


def calculate_icc(data_df, targets='student_id', raters='trial', ratings='score'):
    """
    Calculate Intraclass Correlation Coefficient (ICC 2,1).
    
    ICC(2,1) assesses consistency across trials (raters) for each student (target).
    
    Parameters:
    -----------
    data_df : pd.DataFrame
        Long-format data with columns for targets, raters, and ratings
    targets : str
        Column name for subjects (e.g., 'student_id')
    raters : str
        Column name for trials/raters (e.g., 'trial')
    ratings : str
        Column name for scores (e.g., 'score')
        
    Returns:
    --------
    dict
        ICC value, confidence interval, and interpretation
    """
    if not HAS_PINGOUIN:
        return {
            'icc_value': None,
            'ci_lower': None,
            'ci_upper': None,
            'error': 'pingouin not installed'
        }
    
    try:
        # Calculate ICC using pingouin
        icc_results = pg.intraclass_corr(
            data=data_df,
            targets=targets,
            raters=raters,
            ratings=ratings
        )
        
        # Extract ICC(2,1) - Two-way random effects, single rater
        icc_2_1 = icc_results[icc_results['Type'] == 'ICC2'].iloc[0]
        
        results = {
            'icc_value': round(icc_2_1['ICC'], 3),
            'ci_lower': round(icc_2_1['CI95%'][0], 3),
            'ci_upper': round(icc_2_1['CI95%'][1], 3),
            'n_targets': data_df[targets].nunique(),
            'n_raters': data_df[raters].nunique()
        }
        
        return results
        
    except Exception as e:
        return {
            'icc_value': None,
            'ci_lower': None,
            'ci_upper': None,
            'error': str(e)
        }


def calculate_fleiss_kappa(data_wide):
    """
    Calculate Fleiss' Kappa for multi-rater agreement.
    
    Parameters:
    -----------
    data_wide : pd.DataFrame
        Wide-format data where rows are subjects and columns are raters/trials
        Each cell contains a categorical rating (e.g., 'A', 'B', 'C', 'D')
        
    Returns:
    --------
    float
        Fleiss' kappa value (0-1, higher = better agreement)
    """
    if not HAS_STATSMODELS:
        return None
    
    try:
        # Convert letter grades to category counts
        # Format needed: [n_subjects, n_categories] with counts per category
        categories = ['A', 'B', 'C', 'D']
        n_subjects = len(data_wide)
        n_raters = len(data_wide.columns)
        
        # Create frequency table
        freq_table = np.zeros((n_subjects, len(categories)))
        
        for i, row in data_wide.iterrows():
            for grade in row:
                if grade in categories:
                    cat_idx = categories.index(grade)
                    freq_table[i, cat_idx] += 1
        
        # Calculate Fleiss' kappa
        kappa = fleiss_kappa(freq_table)
        
        return round(kappa, 3)
        
    except Exception as e:
        print(f"Error calculating Fleiss' kappa: {e}")
        return None


def calculate_coefficient_of_variation(data_df, groupby='student_id', value_col='score'):
    """
    Calculate Coefficient of Variation (CV) across trials.
    
    CV = (standard deviation / mean) × 100%
    
    Parameters:
    -----------
    data_df : pd.DataFrame
        Data with multiple trials per student
    groupby : str
        Column to group by (e.g., 'student_id')
    value_col : str
        Column with numeric scores
        
    Returns:
    --------
    float
        Mean CV across all subjects (percentage)
    """
    # Calculate CV for each subject
    cv_by_subject = data_df.groupby(groupby)[value_col].apply(
        lambda x: (x.std() / x.mean()) * 100 if x.mean() != 0 else 0
    )
    
    # Return mean CV
    mean_cv = cv_by_subject.mean()
    
    return round(mean_cv, 1)


def calculate_consistency_metrics(data_df, groupby='student_id', value_col='score'):
    """
    Calculate additional consistency metrics.
    
    Parameters:
    -----------
    data_df : pd.DataFrame
        Data with multiple trials per student
    groupby : str
        Column to group by
    value_col : str
        Column with numeric scores
        
    Returns:
    --------
    dict
        Dictionary with SD, range, and variability metrics
    """
    grouped = data_df.groupby(groupby)[value_col]
    
    metrics = {
        'mean_sd': round(grouped.std().mean(), 3),
        'mean_range': round((grouped.max() - grouped.min()).mean(), 3),
        'max_sd': round(grouped.std().max(), 3),
        'min_sd': round(grouped.std().min(), 3)
    }
    
    return metrics


def print_reliability_results(model_name, strategy_name, icc_results, kappa, cv, consistency):
    """Print reliability results in formatted table."""
    print("\n" + "="*70)
    print(f"RELIABILITY ANALYSIS RESULTS: {model_name} - {strategy_name}")
    print("="*70)
    
    # ICC Results
    if icc_results and icc_results['icc_value'] is not None:
        print(f"\nIntraclass Correlation Coefficient (ICC 2,1):")
        print(f"  Value           : {icc_results['icc_value']:.3f}")
        print(f"  95% CI          : [{icc_results['ci_lower']:.3f}, {icc_results['ci_upper']:.3f}]")
        print(f"  Sample          : {icc_results['n_targets']} students × {icc_results['n_raters']} trials")
        
        # Interpretation (Koo & Li, 2016)
        if icc_results['icc_value'] >= 0.90:
            print("  Interpretation  : [EXCELLENT] reliability (ICC >= 0.90)")
        elif icc_results['icc_value'] >= 0.75:
            print("  Interpretation  : [GOOD] reliability (0.75 <= ICC < 0.90)")
        elif icc_results['icc_value'] >= 0.50:
            print("  Interpretation  : [MODERATE] reliability (0.50 <= ICC < 0.75)")
        else:
            print("  Interpretation  : [POOR] reliability (ICC < 0.50)")
    else:
        print(f"\nICC: Not calculated (requires pingouin)")
    
    # Fleiss' Kappa
    if kappa is not None:
        print(f"\nFleiss' Kappa (Multi-rater Agreement):")
        print(f"  Value           : {kappa:.3f}")
        
        # Interpretation (Landis & Koch, 1977)
        if kappa >= 0.81:
            print("  Interpretation  : [EXCELLENT] agreement (kappa >= 0.81)")
        elif kappa >= 0.61:
            print("  Interpretation  : [SUBSTANTIAL] agreement (0.61 <= kappa < 0.81)")
        elif kappa >= 0.41:
            print("  Interpretation  : [MODERATE] agreement (0.41 <= kappa < 0.61)")
        elif kappa >= 0.21:
            print("  Interpretation  : [FAIR] agreement (0.21 <= kappa < 0.41)")
        else:
            print("  Interpretation  : [SLIGHT] agreement (kappa < 0.21)")
    else:
        print(f"\nFleiss' Kappa: Not calculated (requires statsmodels)")
    
    # Coefficient of Variation
    if cv is not None:
        print(f"\nCoefficient of Variation (CV):")
        print(f"  Value           : {cv:.1f}%")
        
        if cv <= 10:
            print("  Interpretation  : [EXCELLENT] consistency (CV <= 10%)")
        elif cv <= 20:
            print("  Interpretation  : [GOOD] consistency (10% < CV <= 20%)")
        elif cv <= 30:
            print("  Interpretation  : [MODERATE] consistency (20% < CV <= 30%)")
        else:
            print("  Interpretation  : [POOR] consistency (CV > 30%)")
    
    # Additional metrics
    if consistency:
        print(f"\nConsistency Metrics:")
        print(f"  Mean SD         : {consistency['mean_sd']:.3f} points")
        print(f"  Mean Range      : {consistency['mean_range']:.3f} points")
        print(f"  Max SD          : {consistency['max_sd']:.3f} points")
        print(f"  Min SD          : {consistency['min_sd']:.3f} points")
    
    print("="*70)


def load_published_benchmarks():
    """
    Load published reliability metrics from the study for comparison.
    
    Returns:
    --------
    pd.DataFrame
        Published reliability metrics from ../01_Data/reliability_metrics.csv
    """
    try:
        benchmarks = pd.read_csv('../01_Data/reliability_metrics.csv')
        return benchmarks
    except FileNotFoundError:
        return None


def main():
    """
    Main function to run reliability analysis.
    
    This demonstrates how to calculate reliability metrics.
    You need to provide your own trial-by-trial grading data.
    """
    print("="*70)
    print("AUTOMATED ESSAY SCORING - RELIABILITY ANALYSIS")
    print("="*70)
    
    # Example: Create dummy data for demonstration
    print("\n" + "!"*70)
    print("NOTE: This is a DEMONSTRATION with dummy data")
    print("Replace this with your actual trial-by-trial AI grading results!")
    print("!"*70)
    
    # Create example data: 10 students × 10 trials
    np.random.seed(42)
    n_students = 10
    n_trials = 10
    
    data = []
    for student in range(n_students):
        # Each student has a "true" score with some trial-to-trial variation
        true_score = np.random.uniform(1.5, 3.8)
        
        for trial in range(n_trials):
            # Add noise to simulate trial variability (SD ≈ 0.2)
            score = true_score + np.random.normal(0, 0.2)
            score = np.clip(score, 0, 4)
            
            # Convert to letter grade
            if score >= 3.50: grade = 'A'
            elif score >= 2.50: grade = 'B'
            elif score >= 1.50: grade = 'C'
            else: grade = 'D'
            
            data.append({
                'student_id': f'S{student:03d}',
                'trial': f'T{trial+1}',
                'score': round(score, 2),
                'grade': grade
            })
    
    df = pd.DataFrame(data)
    
    print(f"\nGenerated example data: {len(df)} observations")
    print(f"  Students: {df['student_id'].nunique()}")
    print(f"  Trials: {df['trial'].nunique()}")
    
    # Calculate ICC
    print("\nCalculating ICC...")
    icc_results = calculate_icc(df, targets='student_id', raters='trial', ratings='score')
    
    # Calculate Fleiss' Kappa (need wide format)
    print("Calculating Fleiss' Kappa...")
    df_wide = df.pivot(index='student_id', columns='trial', values='grade')
    kappa = calculate_fleiss_kappa(df_wide)
    
    # Calculate CV
    print("Calculating Coefficient of Variation...")
    cv = calculate_coefficient_of_variation(df, groupby='student_id', value_col='score')
    
    # Calculate consistency metrics
    print("Calculating consistency metrics...")
    consistency = calculate_consistency_metrics(df, groupby='student_id', value_col='score')
    
    # Print results
    print_reliability_results(
        model_name='Example_AI',
        strategy_name='demonstration',
        icc_results=icc_results,
        kappa=kappa,
        cv=cv,
        consistency=consistency
    )
    
    # Compare to published benchmarks
    benchmarks = load_published_benchmarks()
    if benchmarks is not None:
        print("\n" + "="*70)
        print("PUBLISHED BENCHMARKS FROM STUDY")
        print("="*70)
        print("\nComparison with actual study results:")
        print(benchmarks[['model', 'strategy', 'icc_value', 'fleiss_kappa', 
                          'coefficient_variation', 'pearson_r']].to_string(index=False))
        print("\nBest performers:")
        best_icc = benchmarks.loc[benchmarks['icc_value'].idxmax()]
        print(f"  Highest ICC: {best_icc['model']} {best_icc['strategy']} (ICC={best_icc['icc_value']:.3f})")
        best_kappa = benchmarks.loc[benchmarks['fleiss_kappa'].idxmax()]
        print(f"  Highest Kappa: {best_kappa['model']} {best_kappa['strategy']} (κ={best_kappa['fleiss_kappa']:.3f})")
    
    print("\n" + "="*70)
    print("TO USE WITH YOUR OWN DATA:")
    print("="*70)
    print("1. Prepare trial-by-trial CSV with columns: student_id, trial, score, grade")
    print("2. Load your data: df = pd.read_csv('your_trials.csv')")
    print("3. Calculate ICC: icc = calculate_icc(df, 'student_id', 'trial', 'score')")
    print("4. Calculate Kappa: df_wide = df.pivot(...); kappa = calculate_fleiss_kappa(df_wide)")
    print("5. Run analysis for each model-strategy combination")
    print("="*70)


if __name__ == "__main__":
    main()
