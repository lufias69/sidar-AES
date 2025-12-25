"""
Generate Summary Tables for OSF Upload
=======================================

This script creates formatted summary tables from analysis results
and exports them to the tables/ folder.

Author: AES Research Team
Date: December 2025
"""

import pandas as pd
from pathlib import Path

# Paths
DATA_DIR = Path('../01_Data')
OUTPUT_DIR = Path('../03_Results/tables')

def create_comprehensive_performance_table():
    """Create Table 1: Comprehensive Performance Metrics"""
    
    # Load data
    reliability = pd.read_csv(DATA_DIR / 'reliability_metrics.csv')
    performance = pd.read_csv(DATA_DIR / 'performance_summary_by_condition.csv')
    
    # Merge
    comprehensive = reliability.merge(performance, on=['model', 'strategy'], how='outer')
    
    # Select key columns
    table = comprehensive[[
        'model', 'strategy',
        'pearson_r', 'icc_value', 'fleiss_kappa',
        'mae', 'accuracy',
        'adjacent_errors_pct', 'major_errors_pct',
        'overall_bias'
    ]].copy()
    
    # Round values
    table['pearson_r'] = table['pearson_r'].round(3)
    table['icc_value'] = table['icc_value'].round(3)
    table['fleiss_kappa'] = table['fleiss_kappa'].round(3)
    table['mae'] = table['mae'].round(3)
    table['accuracy'] = table['accuracy'].round(1)
    table['adjacent_errors_pct'] = table['adjacent_errors_pct'].round(1)
    table['major_errors_pct'] = table['major_errors_pct'].round(1)
    table['overall_bias'] = table['overall_bias'].round(2)
    
    # Rename for clarity
    table.columns = [
        'Model', 'Strategy', 'Pearson_r', 'ICC', 'Fleiss_Kappa',
        'MAE', 'Accuracy_pct', 'Adjacent_Errors_pct', 
        'Major_Errors_pct', 'Overall_Bias'
    ]
    
    # Sort
    table = table.sort_values(['Model', 'Strategy'])
    
    # Export
    output_file = OUTPUT_DIR / 'table1_comprehensive_performance.csv'
    table.to_csv(output_file, index=False)
    print(f"✓ Created: {output_file.name}")
    
    return table


def create_reliability_details_table():
    """Create Table 2: Detailed Reliability Metrics"""
    
    reliability = pd.read_csv(DATA_DIR / 'reliability_metrics.csv')
    
    # Select columns
    table = reliability[[
        'model', 'strategy',
        'pearson_r', 'pearson_p',
        'icc_value', 'icc_ci_lower', 'icc_ci_upper',
        'fleiss_kappa',
        'coefficient_variation',
        'n_trials'
    ]].copy()
    
    # Round (pearson_p is string "<0.001", keep as-is)
    table['pearson_r'] = table['pearson_r'].round(3)
    # table['pearson_p'] already formatted as string
    table['icc_value'] = table['icc_value'].round(3)
    table['icc_ci_lower'] = table['icc_ci_lower'].round(3)
    table['icc_ci_upper'] = table['icc_ci_upper'].round(3)
    table['fleiss_kappa'] = table['fleiss_kappa'].round(3)
    table['coefficient_variation'] = table['coefficient_variation'].round(1)
    
    # Rename
    table.columns = [
        'Model', 'Strategy', 'Pearson_r', 'Pearson_p',
        'ICC', 'ICC_CI_Lower', 'ICC_CI_Upper',
        'Fleiss_Kappa', 'CV_percent', 'N_Trials'
    ]
    
    # Export
    output_file = OUTPUT_DIR / 'table2_reliability_details.csv'
    table.to_csv(output_file, index=False)
    print(f"✓ Created: {output_file.name}")
    
    return table


def create_validity_comparison_table():
    """Create Table 3: Validity Metrics Comparison"""
    
    reliability = pd.read_csv(DATA_DIR / 'reliability_metrics.csv')
    
    # Select validity-related columns
    table = reliability[[
        'model', 'strategy',
        'pearson_r',
        'mae',
        'exact_match_pct'
    ]].copy()
    
    # Round
    table['pearson_r'] = table['pearson_r'].round(3)
    table['mae'] = table['mae'].round(3)
    table['exact_match_pct'] = table['exact_match_pct'].round(1)
    
    # Calculate adjacent match (100% - major errors)
    # Assuming adjacent = exact + 1-off errors
    # For simplicity, we'll add a calculated column
    
    # Rename
    table.columns = [
        'Model', 'Strategy', 'Pearson_r', 'MAE', 'Exact_Match_pct'
    ]
    
    # Pivot for comparison
    pivot = table.pivot_table(
        index='Strategy',
        columns='Model',
        values=['Pearson_r', 'MAE', 'Exact_Match_pct']
    )
    
    # Export both versions
    output_file1 = OUTPUT_DIR / 'table3_validity_comparison.csv'
    table.to_csv(output_file1, index=False)
    print(f"✓ Created: {output_file1.name}")
    
    output_file2 = OUTPUT_DIR / 'table3_validity_comparison_pivot.csv'
    pivot.to_csv(output_file2)
    print(f"✓ Created: {output_file2.name}")
    
    return table


def create_error_patterns_summary():
    """Create Table 4: Error Patterns Summary"""
    
    performance = pd.read_csv(DATA_DIR / 'performance_summary_by_condition.csv')
    
    # Select error-related columns
    table = performance[[
        'model', 'strategy',
        'accuracy',
        'adjacent_errors_pct',
        'major_errors_pct',
        'overall_bias'
    ]].copy()
    
    # Round
    table['accuracy'] = table['accuracy'].round(1)
    table['adjacent_errors_pct'] = table['adjacent_errors_pct'].round(1)
    table['major_errors_pct'] = table['major_errors_pct'].round(1)
    table['overall_bias'] = table['overall_bias'].round(2)
    
    # Add interpretation
    table['Bias_Direction'] = table['overall_bias'].apply(
        lambda x: 'Overgrading' if x > 0.1 else ('Undergrading' if x < -0.1 else 'Minimal')
    )
    
    # Rename
    table.columns = [
        'Model', 'Strategy', 'Accuracy_pct',
        'Adjacent_Errors_pct', 'Major_Errors_pct',
        'Overall_Bias', 'Bias_Direction'
    ]
    
    # Export
    output_file = OUTPUT_DIR / 'table4_error_patterns_summary.csv'
    table.to_csv(output_file, index=False)
    print(f"✓ Created: {output_file.name}")
    
    return table


def main():
    """Generate all summary tables"""
    
    print("="*70)
    print("GENERATING SUMMARY TABLES FOR OSF")
    print("="*70)
    
    # Create output directory if doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n1. Creating comprehensive performance table...")
    create_comprehensive_performance_table()
    
    print("\n2. Creating reliability details table...")
    create_reliability_details_table()
    
    print("\n3. Creating validity comparison table...")
    create_validity_comparison_table()
    
    print("\n4. Creating error patterns summary...")
    create_error_patterns_summary()
    
    print("\n" + "="*70)
    print("ALL TABLES GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"\nLocation: {OUTPUT_DIR}")
    print("\nFiles created:")
    for file in sorted(OUTPUT_DIR.glob('table*.csv')):
        size_kb = file.stat().st_size / 1024
        print(f"  ✓ {file.name} ({size_kb:.2f} KB)")
    
    print("\nNOTE: Confusion matrix tables already copied separately")
    print("="*70)


if __name__ == "__main__":
    main()
