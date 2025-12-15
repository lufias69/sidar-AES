"""
RQ5: Error Analysis - Identify patterns and challenging tasks

This script analyzes:
1. Challenging tasks (high error across all strategies)
2. Grade-specific performance patterns
3. Systematic error types (overgrading vs undergrading)
4. Question-level difficulty analysis
5. Student-level performance variation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
BASELINE_FILE = ANALYSIS_DIR / "baseline" / "gold_standard_70_tasks.csv"
EXPERIMENTS_DIR = ANALYSIS_DIR / "experiments"
METRICS_DIR = ANALYSIS_DIR / "metrics"
TABLES_DIR = ANALYSIS_DIR / "tables"
FIGURES_DIR = ANALYSIS_DIR / "figures" / "error_analysis"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def score_to_grade(score):
    """Convert numerical score to letter grade"""
    if score >= 3.6: return 'A'
    elif score >= 3.0: return 'B'
    elif score >= 2.0: return 'C'
    elif score >= 1.0: return 'D'
    else: return 'E'

def load_baseline():
    """Load expert gold standard grades"""
    print("\n" + "="*70)
    print("LOADING BASELINE GOLD STANDARD")
    print("="*70)
    
    df = pd.read_csv(BASELINE_FILE)
    df_unique = df.drop_duplicates(subset=['student_name', 'question_number'])
    
    print(f"✅ Loaded {len(df_unique)} unique tasks")
    
    return df_unique

def load_predictions(model, strategy):
    """Load AI predictions for a specific model-strategy combination"""
    
    if strategy == 'lenient':
        exp_name = f"exp_exp_{model}_lenient_01_{model}_lenient"
    elif strategy == 'zero-shot':
        exp_name = f"exp_exp_{model}_zero_{model}_zero-shot"
    elif strategy == 'few-shot':
        exp_name = f"exp_exp_{model}_few_{model}_few-shot"
    
    exp_dir = EXPERIMENTS_DIR / exp_name
    pred_file = exp_dir / "predictions.csv"
    
    if not pred_file.exists():
        print(f"  ⚠️  File not found: {pred_file}")
        return None
    
    df = pd.read_csv(pred_file)
    return df

def analyze_task_difficulty(baseline_df):
    """Analyze which tasks are most challenging across all strategies"""
    
    print("\n" + "="*70)
    print("ANALYZING TASK DIFFICULTY")
    print("="*70)
    
    # Load all predictions
    strategies = ['lenient', 'zero-shot', 'few-shot']
    models = ['chatgpt', 'gemini']
    
    all_errors = []
    
    for model in models:
        for strategy in strategies:
            pred_df = load_predictions(model, strategy)
            if pred_df is None:
                continue
            
            # Merge with baseline
            merged = baseline_df.merge(
                pred_df[['student_name', 'question_number', 'weighted_score', 'grade']],
                on=['student_name', 'question_number'],
                suffixes=('_expert', '_ai')
            )
            
            # Calculate absolute error
            merged['abs_error'] = abs(merged['weighted_score_expert'] - merged['weighted_score_ai'])
            merged['grade_diff'] = (merged['weighted_score_ai'] - merged['weighted_score_expert'])
            merged['model'] = model
            merged['strategy'] = strategy
            
            all_errors.append(merged)
    
    # Combine all errors
    error_df = pd.concat(all_errors, ignore_index=True)
    
    # Calculate average error per task
    task_errors = error_df.groupby(['student_name', 'question_number']).agg({
        'abs_error': ['mean', 'std', 'min', 'max'],
        'grade_diff': 'mean',
        'weighted_score_expert': 'first',
        'grade_expert': 'first',
        'question_text': 'first',
        'answer': 'first'
    }).reset_index()
    
    task_errors.columns = ['student_name', 'question_number', 'mean_abs_error', 
                          'std_abs_error', 'min_abs_error', 'max_abs_error',
                          'mean_grade_diff', 'expert_score', 'expert_grade',
                          'question_text', 'answer']
    
    # Sort by mean absolute error
    task_errors = task_errors.sort_values('mean_abs_error', ascending=False)
    
    print(f"\n  Total tasks analyzed: {len(task_errors)}")
    print(f"  Average error across all tasks: {task_errors['mean_abs_error'].mean():.3f}")
    print(f"  Error range: [{task_errors['mean_abs_error'].min():.3f}, {task_errors['mean_abs_error'].max():.3f}]")
    
    return task_errors, error_df

def identify_challenging_tasks(task_errors, top_n=10):
    """Identify most challenging tasks"""
    
    print("\n" + "="*70)
    print(f"TOP {top_n} MOST CHALLENGING TASKS")
    print("="*70)
    
    challenging = task_errors.head(top_n)
    
    for idx, row in challenging.iterrows():
        print(f"\n  RANK {challenging.index.get_loc(idx) + 1}:")
        print(f"    Student: {row['student_name']}, Question: {row['question_number']}")
        print(f"    Expert Grade: {row['expert_grade']} (Score: {row['expert_score']:.2f})")
        print(f"    Mean Absolute Error: {row['mean_abs_error']:.3f}")
        print(f"    Error Range: [{row['min_abs_error']:.3f}, {row['max_abs_error']:.3f}]")
        print(f"    Mean Grade Difference: {row['mean_grade_diff']:+.3f}")
        print(f"    Question: {row['question_text'][:80]}...")
    
    return challenging

def analyze_grade_specific_performance(error_df):
    """Analyze performance for each grade level"""
    
    print("\n" + "="*70)
    print("GRADE-SPECIFIC PERFORMANCE ANALYSIS")
    print("="*70)
    
    grade_stats = error_df.groupby('grade_expert').agg({
        'abs_error': ['mean', 'std', 'count'],
        'grade_diff': ['mean', 'std']
    }).reset_index()
    
    grade_stats.columns = ['grade', 'mean_abs_error', 'std_abs_error', 'n_samples',
                          'mean_grade_diff', 'std_grade_diff']
    
    # Sort by grade
    grade_order = ['A', 'B', 'C', 'D', 'E']
    grade_stats['grade'] = pd.Categorical(grade_stats['grade'], categories=grade_order, ordered=True)
    grade_stats = grade_stats.sort_values('grade')
    
    print("\n  Performance by Grade:")
    for _, row in grade_stats.iterrows():
        bias_direction = "overgrade" if row['mean_grade_diff'] > 0 else "undergrade"
        print(f"\n    Grade {row['grade']}:")
        print(f"      Samples: {row['n_samples']}")
        print(f"      Mean Absolute Error: {row['mean_abs_error']:.3f} ± {row['std_abs_error']:.3f}")
        print(f"      Mean Bias: {row['mean_grade_diff']:+.3f} ({bias_direction})")
    
    return grade_stats

def analyze_question_difficulty(error_df):
    """Analyze performance by question number"""
    
    print("\n" + "="*70)
    print("QUESTION-LEVEL DIFFICULTY ANALYSIS")
    print("="*70)
    
    question_stats = error_df.groupby('question_number').agg({
        'abs_error': ['mean', 'std', 'count'],
        'grade_diff': ['mean', 'std'],
        'weighted_score_expert': 'mean'
    }).reset_index()
    
    question_stats.columns = ['question_number', 'mean_abs_error', 'std_abs_error', 
                             'n_samples', 'mean_grade_diff', 'std_grade_diff', 
                             'avg_expert_score']
    
    question_stats = question_stats.sort_values('mean_abs_error', ascending=False)
    
    print("\n  Questions ranked by difficulty (mean error):")
    for idx, row in question_stats.iterrows():
        print(f"\n    Question {row['question_number']}:")
        print(f"      Samples: {row['n_samples']}")
        print(f"      Avg Expert Score: {row['avg_expert_score']:.2f}")
        print(f"      Mean Absolute Error: {row['mean_abs_error']:.3f}")
        print(f"      Mean Bias: {row['mean_grade_diff']:+.3f}")
    
    return question_stats

def analyze_systematic_errors(error_df):
    """Analyze systematic error patterns"""
    
    print("\n" + "="*70)
    print("SYSTEMATIC ERROR ANALYSIS")
    print("="*70)
    
    # Overall bias
    print("\n  OVERALL BIAS:")
    for model in error_df['model'].unique():
        for strategy in error_df['strategy'].unique():
            subset = error_df[(error_df['model'] == model) & (error_df['strategy'] == strategy)]
            if len(subset) == 0:
                continue
            
            mean_bias = subset['grade_diff'].mean()
            bias_type = "overgrading" if mean_bias > 0 else "undergrading"
            
            overgrade_pct = (subset['grade_diff'] > 0).sum() / len(subset) * 100
            undergrade_pct = (subset['grade_diff'] < 0).sum() / len(subset) * 100
            exact_pct = (subset['grade_diff'] == 0).sum() / len(subset) * 100
            
            print(f"\n    {model.upper()} - {strategy}:")
            print(f"      Mean Bias: {mean_bias:+.3f} ({bias_type})")
            print(f"      Overgrading: {overgrade_pct:.1f}%")
            print(f"      Undergrading: {undergrade_pct:.1f}%")
            print(f"      Exact: {exact_pct:.1f}%")
    
    # Confusion patterns
    print("\n  CONFUSION PATTERNS (Most common misclassifications):")
    for model in ['chatgpt', 'gemini']:
        for strategy in ['lenient', 'zero-shot', 'few-shot']:
            subset = error_df[(error_df['model'] == model) & (error_df['strategy'] == strategy)]
            if len(subset) == 0:
                continue
            
            # Count grade transitions
            confusion = subset[subset['grade_expert'] != subset['grade_ai']].groupby(
                ['grade_expert', 'grade_ai']
            ).size().sort_values(ascending=False)
            
            if len(confusion) > 0:
                print(f"\n    {model.upper()} - {strategy} (top 3):")
                for (expert_g, ai_g), count in confusion.head(3).items():
                    pct = count / len(subset) * 100
                    print(f"      {expert_g} → {ai_g}: {count} times ({pct:.1f}%)")

def create_visualizations(task_errors, grade_stats, question_stats, error_df):
    """Create comprehensive error analysis visualizations"""
    
    print("\n" + "="*70)
    print("CREATING ERROR ANALYSIS VISUALIZATIONS")
    print("="*70)
    
    # 1. Task difficulty distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(range(len(task_errors)), task_errors['mean_abs_error'].values, 
           color='steelblue', alpha=0.7, edgecolor='black')
    ax.axhline(task_errors['mean_abs_error'].mean(), color='red', 
               linestyle='--', linewidth=2, label='Overall Mean')
    
    ax.set_xlabel('Task Rank (by difficulty)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Absolute Error', fontsize=12, fontweight='bold')
    ax.set_title('Task Difficulty Distribution\n(Averaged across all models and strategies)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_17_task_difficulty_distribution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()
    
    # 2. Grade-specific error patterns
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 2a. Mean absolute error by grade
    ax = axes[0]
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']
    bars = ax.bar(grade_stats['grade'], grade_stats['mean_abs_error'], 
                  yerr=grade_stats['std_abs_error'], capsize=10,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    ax.set_xlabel('Expert Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Absolute Error', fontsize=12, fontweight='bold')
    ax.set_title('Error by Grade Level', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 2b. Bias direction by grade
    ax = axes[1]
    bars = ax.bar(grade_stats['grade'], grade_stats['mean_grade_diff'],
                  color=['red' if x > 0 else 'blue' for x in grade_stats['mean_grade_diff']],
                  alpha=0.7, edgecolor='black', linewidth=2)
    
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Expert Grade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Grade Difference (AI - Expert)', fontsize=12, fontweight='bold')
    ax.set_title('Bias Direction by Grade\n(Red=Overgrade, Blue=Undergrade)', 
                fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        va = 'bottom' if height > 0 else 'top'
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:+.3f}',
               ha='center', va=va, fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_18_grade_specific_errors.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()
    
    # 3. Question difficulty comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = question_stats['question_number'].values
    y1 = question_stats['mean_abs_error'].values
    y2 = question_stats['avg_expert_score'].values
    
    ax2 = ax.twinx()
    
    bars = ax.bar(x, y1, alpha=0.7, color='coral', edgecolor='black', linewidth=2, label='Mean Error')
    line = ax2.plot(x, y2, 'o-', color='navy', linewidth=3, markersize=10, label='Avg Expert Score')
    
    ax.set_xlabel('Question Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Absolute Error', fontsize=12, fontweight='bold', color='coral')
    ax2.set_ylabel('Average Expert Score', fontsize=12, fontweight='bold', color='navy')
    ax.set_title('Question Difficulty Analysis', fontsize=14, fontweight='bold')
    ax.tick_params(axis='y', labelcolor='coral')
    ax2.tick_params(axis='y', labelcolor='navy')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}',
               ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    output_file = FIGURES_DIR / "figure_19_question_difficulty.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()
    
    # 4. Error distribution by model and strategy
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    strategies = ['lenient', 'zero-shot', 'few-shot']
    models = ['chatgpt', 'gemini']
    
    for i, model in enumerate(models):
        for j, strategy in enumerate(strategies):
            ax = axes[i, j]
            
            subset = error_df[(error_df['model'] == model) & (error_df['strategy'] == strategy)]
            
            if len(subset) > 0:
                # Violin plot of grade differences
                parts = ax.violinplot([subset['grade_diff'].values], positions=[0], 
                                     widths=0.7, showmeans=True, showmedians=True)
                
                # Color based on bias direction
                mean_bias = subset['grade_diff'].mean()
                color = 'red' if mean_bias > 0 else 'blue'
                for pc in parts['bodies']:
                    pc.set_facecolor(color)
                    pc.set_alpha(0.5)
                
                ax.axhline(0, color='black', linestyle='--', linewidth=1)
                ax.set_ylabel('Grade Difference (AI - Expert)', fontsize=10, fontweight='bold')
                ax.set_title(f'{model.upper()} - {strategy}\nBias: {mean_bias:+.3f}', 
                           fontsize=11, fontweight='bold')
                ax.set_xticks([])
                ax.grid(axis='y', alpha=0.3)
            else:
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center', 
                       transform=ax.transAxes, fontsize=12)
                ax.set_xticks([])
                ax.set_yticks([])
    
    plt.suptitle('Error Distribution by Model and Strategy', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    output_file = FIGURES_DIR / "figure_20_error_distributions.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_file.name}")
    plt.close()

def main():
    """Main execution"""
    
    print("\n" + "="*70)
    print("RQ5: ERROR ANALYSIS")
    print("="*70)
    
    # Load baseline
    baseline_df = load_baseline()
    
    # Analyze task difficulty
    task_errors, error_df = analyze_task_difficulty(baseline_df)
    
    # Identify challenging tasks
    challenging_tasks = identify_challenging_tasks(task_errors, top_n=10)
    
    # Save challenging tasks
    output_file = TABLES_DIR / "table_11_challenging_tasks.csv"
    challenging_tasks[['student_name', 'question_number', 'expert_grade', 'expert_score',
                      'mean_abs_error', 'std_abs_error', 'mean_grade_diff', 
                      'question_text']].to_csv(output_file, index=False)
    print(f"\n✅ Saved: {output_file.name}")
    
    # Save all task errors
    output_file = TABLES_DIR / "table_12_all_task_errors.csv"
    task_errors[['student_name', 'question_number', 'expert_grade', 'expert_score',
                'mean_abs_error', 'std_abs_error', 'mean_grade_diff']].to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file.name}")
    
    # Grade-specific analysis
    grade_stats = analyze_grade_specific_performance(error_df)
    output_file = TABLES_DIR / "table_13_grade_specific_performance.csv"
    grade_stats.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file.name}")
    
    # Question-level analysis
    question_stats = analyze_question_difficulty(error_df)
    output_file = TABLES_DIR / "table_14_question_difficulty.csv"
    question_stats.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file.name}")
    
    # Systematic errors
    analyze_systematic_errors(error_df)
    
    # Create visualizations
    create_visualizations(task_errors, grade_stats, question_stats, error_df)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    print(f"\n  📊 Key Findings:")
    print(f"     - Total tasks analyzed: {len(task_errors)}")
    print(f"     - Average error: {task_errors['mean_abs_error'].mean():.3f}")
    print(f"     - Most challenging task error: {task_errors['mean_abs_error'].max():.3f}")
    print(f"     - Least challenging task error: {task_errors['mean_abs_error'].min():.3f}")
    
    print(f"\n  🎯 Challenging Tasks:")
    print(f"     - Top 10% tasks have mean error > {task_errors['mean_abs_error'].quantile(0.9):.3f}")
    print(f"     - Bottom 10% tasks have mean error < {task_errors['mean_abs_error'].quantile(0.1):.3f}")
    
    print("\n" + "="*70)
    print("✅ RQ5 ERROR ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\n📊 Generated:")
    print(f"   - 4 figures (task difficulty, grade errors, question difficulty, distributions)")
    print(f"   - 4 tables (challenging tasks, all errors, grade stats, question stats)")

if __name__ == "__main__":
    main()
