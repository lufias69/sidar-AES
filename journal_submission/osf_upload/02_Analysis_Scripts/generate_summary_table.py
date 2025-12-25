"""
Generate Summary Tables for AES Study
======================================

This script creates formatted summary tables from the analysis results,
similar to those published in the manuscript.

Usage:
    python generate_summary_table.py

Requirements:
    - pandas
    - tabulate (optional, for pretty printing)

Input:
    - ../01_Data/reliability_metrics.csv
    - ../01_Data/performance_summary_by_condition.csv

Output:
    - Formatted tables printed to console
    - Optional: Export to CSV/Excel/LaTeX

Author: AES Research Team
Date: December 2025
License: MIT
"""

import pandas as pd
from pathlib import Path

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    print("NOTE: Install 'tabulate' for prettier tables: pip install tabulate")


def load_data():
    """Load all analysis results."""
    data_dir = Path('../01_Data')
    
    reliability = pd.read_csv(data_dir / 'reliability_metrics.csv')
    performance = pd.read_csv(data_dir / 'performance_summary_by_condition.csv')
    
    return reliability, performance


def create_comprehensive_table(reliability_df, performance_df):
    """
    Create comprehensive table combining reliability and performance metrics.
    
    This replicates Table 2 from the manuscript.
    """
    # Merge datasets
    merged = reliability_df.merge(
        performance_df, 
        on=['model', 'strategy'], 
        how='outer'
    )
    
    # Select and rename columns for clarity
    table = merged[[
        'model', 'strategy', 
        'pearson_r', 'icc_value', 'fleiss_kappa',
        'mae', 'accuracy', 
        'overall_bias',
        'adjacent_errors_pct', 'major_errors_pct'
    ]].copy()
    
    # Round values
    table['pearson_r'] = table['pearson_r'].round(3)
    table['icc_value'] = table['icc_value'].round(3)
    table['fleiss_kappa'] = table['fleiss_kappa'].round(3)
    table['mae'] = table['mae'].round(3)
    table['accuracy'] = table['accuracy'].round(1)
    table['overall_bias'] = table['overall_bias'].round(2)
    table['adjacent_errors_pct'] = table['adjacent_errors_pct'].round(1)
    table['major_errors_pct'] = table['major_errors_pct'].round(1)
    
    # Rename columns for display
    table.columns = [
        'Model', 'Strategy',
        'Pearson r', 'ICC', 'Kappa',
        'MAE', 'Accuracy (%)',
        'Bias',
        'Adjacent Errors (%)', 'Major Errors (%)'
    ]
    
    return table


def print_table(df, title="Summary Table"):
    """Print DataFrame as formatted table."""
    print("\n" + "="*100)
    print(title.center(100))
    print("="*100)
    
    if HAS_TABULATE:
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print(df.to_string(index=False))
    
    print("="*100)


def create_model_comparison_table(comprehensive_df):
    """Create table comparing models across strategies."""
    
    # Pivot to compare models
    comparison = comprehensive_df.pivot_table(
        index='Strategy',
        columns='Model',
        values=['Pearson r', 'ICC', 'Accuracy (%)'],
        aggfunc='first'
    )
    
    return comparison


def create_strategy_comparison_table(comprehensive_df):
    """Create table comparing strategies across models."""
    
    # Group by strategy and calculate means
    strategy_summary = comprehensive_df.groupby('Strategy').agg({
        'Pearson r': 'mean',
        'ICC': 'mean',
        'Kappa': 'mean',
        'Accuracy (%)': 'mean',
        'MAE': 'mean'
    }).round(3)
    
    return strategy_summary


def highlight_best_values(df, columns):
    """
    Identify best values in each column for highlighting.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Table to analyze
    columns : list
        Columns to find best values in
        
    Returns:
    --------
    dict
        Dictionary with column: (best_value, condition) pairs
    """
    best_values = {}
    
    for col in columns:
        if col in df.columns:
            # For bias and errors, lower is better
            if 'bias' in col.lower() or 'error' in col.lower() or 'mae' in col.lower():
                best_idx = df[col].abs().idxmin()
                best_values[col] = (df.loc[best_idx, col], 
                                   f"{df.loc[best_idx, 'Model']} {df.loc[best_idx, 'Strategy']}")
            else:
                # For r, ICC, kappa, accuracy - higher is better
                best_idx = df[col].idxmax()
                best_values[col] = (df.loc[best_idx, col], 
                                   f"{df.loc[best_idx, 'Model']} {df.loc[best_idx, 'Strategy']}")
    
    return best_values


def export_to_latex(df, filename='summary_table.tex'):
    """Export table to LaTeX format for manuscript."""
    latex_str = df.to_latex(index=False, float_format='%.3f')
    
    with open(filename, 'w') as f:
        f.write(latex_str)
    
    print(f"\nLaTeX table exported to {filename}")


def main():
    """Main function to generate summary tables."""
    print("="*100)
    print("AUTOMATED ESSAY SCORING - SUMMARY TABLES")
    print("="*100)
    
    # Load data
    print("\nLoading data...")
    reliability, performance = load_data()
    
    print(f"  Reliability metrics: {len(reliability)} conditions")
    print(f"  Performance metrics: {len(performance)} conditions")
    
    # Create comprehensive table
    print("\nGenerating comprehensive table...")
    comprehensive = create_comprehensive_table(reliability, performance)
    
    # Print main table
    print_table(comprehensive, "Table 1: Comprehensive Performance Metrics")
    
    # Highlight best performers
    print("\n" + "="*100)
    print("BEST PERFORMERS")
    print("="*100)
    
    best_values = highlight_best_values(comprehensive, [
        'Pearson r', 'ICC', 'Kappa', 'Accuracy (%)', 'MAE'
    ])
    
    for metric, (value, condition) in best_values.items():
        print(f"  {metric:20s}: {value:6.3f} - {condition}")
    
    # Model comparison
    print("\n")
    model_comp = create_model_comparison_table(comprehensive)
    print_table(model_comp, "Table 2: Model Comparison Across Strategies")
    
    # Strategy comparison
    print("\n")
    strategy_comp = create_strategy_comparison_table(comprehensive)
    print_table(strategy_comp, "Table 3: Strategy Performance Averages")
    
    # Key findings
    print("\n" + "="*100)
    print("KEY FINDINGS")
    print("="*100)
    
    # Find best combination for each metric
    print("\n1. VALIDITY (Pearson r):")
    best_validity = comprehensive.loc[comprehensive['Pearson r'].idxmax()]
    print(f"   Best: {best_validity['Model']} {best_validity['Strategy']}")
    print(f"   r = {best_validity['Pearson r']:.3f}, MAE = {best_validity['MAE']:.3f}")
    
    print("\n2. RELIABILITY (ICC):")
    best_reliability = comprehensive.loc[comprehensive['ICC'].idxmax()]
    print(f"   Best: {best_reliability['Model']} {best_reliability['Strategy']}")
    print(f"   ICC = {best_reliability['ICC']:.3f}, Kappa = {best_reliability['Kappa']:.3f}")
    
    print("\n3. ACCURACY:")
    best_accuracy = comprehensive.loc[comprehensive['Accuracy (%)'].idxmax()]
    print(f"   Best: {best_accuracy['Model']} {best_accuracy['Strategy']}")
    print(f"   Accuracy = {best_accuracy['Accuracy (%)']:.1f}%, Adjacent Errors = {best_accuracy['Adjacent Errors (%)']:.1f}%")
    
    print("\n4. BALANCED PERFORMANCE:")
    # Calculate composite score (normalized)
    comprehensive['composite'] = (
        comprehensive['Pearson r'] / comprehensive['Pearson r'].max() * 0.3 +
        comprehensive['ICC'] / comprehensive['ICC'].max() * 0.3 +
        comprehensive['Accuracy (%)'] / comprehensive['Accuracy (%)'].max() * 0.2 +
        (1 - comprehensive['MAE'] / comprehensive['MAE'].max()) * 0.2
    )
    best_overall = comprehensive.loc[comprehensive['composite'].idxmax()]
    print(f"   Best Overall: {best_overall['Model']} {best_overall['Strategy']}")
    print(f"   Composite Score = {best_overall['composite']:.3f}")
    
    # Export options
    print("\n" + "="*100)
    print("EXPORT OPTIONS")
    print("="*100)
    print("\nTo export tables:")
    print("  CSV:   comprehensive.to_csv('summary_table.csv', index=False)")
    print("  Excel: comprehensive.to_excel('summary_table.xlsx', index=False)")
    print("  LaTeX: export_to_latex(comprehensive, 'summary_table.tex')")
    print("="*100)


if __name__ == "__main__":
    main()
