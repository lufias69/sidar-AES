"""
Validity Analysis for Automated Essay Scoring Study
====================================================

This script calculates validity metrics comparing AI grades to expert grades:
- Pearson correlation coefficient (r)
- Mean Absolute Error (MAE)
- Exact match percentage
- Adjacent match percentage (within ±1 grade)

Usage:
    python validity_analysis.py

Requirements:
    - pandas
    - scipy
    - numpy

Input:
    - ../01_Data/gold_standard_anonymized.csv (expert grades)
    - AI grading results (you need to provide your own AI results)

Output:
    - Validity metrics printed to console
    - Optional: CSV file with detailed results

Author: AES Research Team
Date: December 2025
License: MIT
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from pathlib import Path


def load_expert_data(data_path='../01_Data/gold_standard_anonymized.csv'):
    """
    Load expert grading data from anonymized CSV.
    
    Parameters:
    -----------
    data_path : str
        Path to gold standard CSV file
        
    Returns:
    --------
    pd.DataFrame
        Expert grades with columns: task_id, student_id_anon, expert_score_total, expert_grade
    """
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} expert grades from {data_path}")
    print(f"Columns: {list(df.columns)}")
    return df


def calculate_pearson_r(expert_scores, ai_scores):
    """
    Calculate Pearson correlation coefficient.
    
    Parameters:
    -----------
    expert_scores : array-like
        Expert numeric scores (0-4)
    ai_scores : array-like
        AI numeric scores (0-4)
        
    Returns:
    --------
    tuple
        (correlation coefficient, p-value)
    """
    r, p_value = pearsonr(expert_scores, ai_scores)
    return r, p_value


def calculate_mae(expert_scores, ai_scores):
    """
    Calculate Mean Absolute Error.
    
    Parameters:
    -----------
    expert_scores : array-like
        Expert numeric scores
    ai_scores : array-like
        AI numeric scores
        
    Returns:
    --------
    float
        Mean absolute error
    """
    mae = np.mean(np.abs(np.array(expert_scores) - np.array(ai_scores)))
    return mae


def calculate_exact_match(expert_grades, ai_grades):
    """
    Calculate percentage of exact letter grade matches.
    
    Parameters:
    -----------
    expert_grades : array-like
        Expert letter grades (A/B/C/D)
    ai_grades : array-like
        AI letter grades (A/B/C/D)
        
    Returns:
    --------
    float
        Percentage of exact matches (0-100)
    """
    matches = np.sum(np.array(expert_grades) == np.array(ai_grades))
    percentage = (matches / len(expert_grades)) * 100
    return percentage


def calculate_adjacent_match(expert_grades, ai_grades):
    """
    Calculate percentage of adjacent matches (within ±1 letter grade).
    
    Parameters:
    -----------
    expert_grades : array-like
        Expert letter grades (A/B/C/D)
    ai_grades : array-like
        AI letter grades (A/B/C/D)
        
    Returns:
    --------
    float
        Percentage of exact + adjacent matches (0-100)
    """
    # Map grades to numbers for distance calculation
    grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1}
    
    expert_numeric = [grade_map.get(g, 0) for g in expert_grades]
    ai_numeric = [grade_map.get(g, 0) for g in ai_grades]
    
    # Count matches within 1 grade
    distances = np.abs(np.array(expert_numeric) - np.array(ai_numeric))
    adjacent_matches = np.sum(distances <= 1)
    percentage = (adjacent_matches / len(expert_grades)) * 100
    
    return percentage


def run_validity_analysis(expert_df, ai_df, model_name, strategy_name):
    """
    Run complete validity analysis for one model-strategy combination.
    
    Parameters:
    -----------
    expert_df : pd.DataFrame
        Expert grades with task_id, expert_score_total, expert_grade
    ai_df : pd.DataFrame
        AI grades with task_id, ai_score_total, ai_grade
    model_name : str
        Model name (e.g., 'ChatGPT', 'Gemini')
    strategy_name : str
        Strategy name (e.g., 'lenient', 'few-shot', 'zero-shot')
        
    Returns:
    --------
    dict
        Dictionary with all validity metrics
    """
    # Merge expert and AI grades by task_id
    merged = expert_df.merge(ai_df, on='task_id', how='inner')
    
    if len(merged) == 0:
        print("WARNING: No matching task_ids found between expert and AI data!")
        return None
    
    print(f"\nAnalyzing {model_name} - {strategy_name}")
    print(f"Matched {len(merged)} essays")
    
    # Calculate metrics
    r, p_value = calculate_pearson_r(merged['expert_score_total'], 
                                      merged['ai_score_total'])
    
    mae = calculate_mae(merged['expert_score_total'], 
                        merged['ai_score_total'])
    
    exact_match = calculate_exact_match(merged['expert_grade'], 
                                         merged['ai_grade'])
    
    adjacent_match = calculate_adjacent_match(merged['expert_grade'], 
                                               merged['ai_grade'])
    
    # Compile results
    results = {
        'model': model_name,
        'strategy': strategy_name,
        'n_essays': len(merged),
        'pearson_r': round(r, 3),
        'p_value': round(p_value, 4),
        'mae': round(mae, 3),
        'exact_match_pct': round(exact_match, 1),
        'adjacent_match_pct': round(adjacent_match, 1)
    }
    
    return results


def print_results(results):
    """Print validity results in formatted table."""
    print("\n" + "="*70)
    print(f"VALIDITY ANALYSIS RESULTS: {results['model']} - {results['strategy']}")
    print("="*70)
    print(f"Sample Size         : {results['n_essays']} essays")
    print(f"Pearson r           : {results['pearson_r']:.3f} (p={results['p_value']:.4f})")
    print(f"Mean Absolute Error : {results['mae']:.3f} points")
    print(f"Exact Match         : {results['exact_match_pct']:.1f}%")
    print(f"Adjacent Match      : {results['adjacent_match_pct']:.1f}% (±1 grade)")
    print("="*70)
    
    # Interpretation
    print("\nINTERPRETATION:")
    if results['pearson_r'] >= 0.90:
        print("  [EXCELLENT] correlation (r >= 0.90)")
    elif results['pearson_r'] >= 0.75:
        print("  [GOOD] correlation (0.75 <= r < 0.90)")
    elif results['pearson_r'] >= 0.50:
        print("  [MODERATE] correlation (0.50 <= r < 0.75)")
    else:
        print("  [WEAK] correlation (r < 0.50)")
    
    if results['mae'] <= 0.30:
        print("  [LOW] error (MAE <= 0.30)")
    elif results['mae'] <= 0.50:
        print("  [MODERATE] error (0.30 < MAE <= 0.50)")
    else:
        print("  [HIGH] error (MAE > 0.50)")
    
    if results['exact_match_pct'] >= 80:
        print("  [HIGH] agreement (exact match >= 80%)")
    elif results['exact_match_pct'] >= 60:
        print("  [MODERATE] agreement (60% <= exact match < 80%)")
    else:
        print("  [LOW] agreement (exact match < 60%)")


def main():
    """
    Main function to run validity analysis.
    
    This example uses the provided expert data and demonstrates how to 
    calculate validity metrics. You need to provide your own AI grading results.
    """
    print("="*70)
    print("AUTOMATED ESSAY SCORING - VALIDITY ANALYSIS")
    print("="*70)
    
    # Load expert data
    expert_df = load_expert_data()
    
    # Example: Create dummy AI data for demonstration
    # In practice, you would load actual AI grading results here
    print("\n" + "!"*70)
    print("NOTE: This is a DEMONSTRATION with dummy AI data")
    print("Replace this with your actual AI grading results!")
    print("!"*70)
    
    # Create example AI data (in practice, load from your AI results file)
    np.random.seed(42)
    ai_df = expert_df[['task_id']].copy()
    
    # Simulate AI scores with some noise (r ≈ 0.85)
    ai_df['ai_score_total'] = expert_df['expert_score_total'] + np.random.normal(0, 0.3, len(expert_df))
    ai_df['ai_score_total'] = ai_df['ai_score_total'].clip(0, 4)  # Keep in valid range
    
    # Convert to letter grades
    def score_to_grade(score):
        if score >= 3.50: return 'A'
        elif score >= 2.50: return 'B'
        elif score >= 1.50: return 'C'
        else: return 'D'
    
    ai_df['ai_grade'] = ai_df['ai_score_total'].apply(score_to_grade)
    
    # Run analysis
    results = run_validity_analysis(
        expert_df, 
        ai_df, 
        model_name='Example_AI',
        strategy_name='demonstration'
    )
    
    # Print results
    if results:
        print_results(results)
    
    print("\n" + "="*70)
    print("TO USE WITH YOUR OWN DATA:")
    print("="*70)
    print("1. Prepare AI results CSV with columns: task_id, ai_score_total, ai_grade")
    print("2. Load your AI data: ai_df = pd.read_csv('your_ai_results.csv')")
    print("3. Run analysis: results = run_validity_analysis(expert_df, ai_df, 'YourModel', 'YourStrategy')")
    print("4. Compare multiple conditions by running analysis for each model-strategy pair")
    print("="*70)


if __name__ == "__main__":
    main()
