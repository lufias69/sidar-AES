"""
RQ4: Error Analysis - Systematic Error Patterns

Analyzes error patterns in LLM grading:
- Error severity classification (critical, major, minor)
- Over-grading vs under-grading patterns
- Error distribution by grade level
- Systematic bias detection
- Per-rubric error analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
DATA_DIR = Path("results_experiment_final/data")
OUTPUT_DIR = Path("results_experiment_final/rq4_error_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("RQ4: ERROR ANALYSIS - SYSTEMATIC ERROR PATTERNS")
print("="*80 + "\n")

# Load data
print("Loading data...")
df_experiment = pd.read_csv(DATA_DIR / "experiment_data_complete.csv")
df_gold = pd.read_csv(DATA_DIR / "gold_standard.csv")

# Fix student_id format
df_gold['student_id'] = 'student_' + df_gold['student_id'].astype(str).str.zfill(2)
df_gold['question_number'] = df_gold['question_number'].astype(int)
df_experiment['student_id'] = df_experiment['student_id'].astype(str)
df_experiment['question_number'] = df_experiment['question_number'].astype(int)

# Merge
df = df_experiment.merge(
    df_gold[['student_id', 'question_number', 'gold_score']],
    on=['student_id', 'question_number'],
    how='inner'
)

print(f"  ✓ Merged dataset: {len(df)} records")

# ============================================================================
# Calculate Error Metrics
# ============================================================================
print("\nCalculating error metrics...")

# Error = LLM score - Gold score
df['error'] = df['weighted_score'] - df['gold_score']
df['abs_error'] = np.abs(df['error'])

# Round scores for classification
df['llm_grade'] = np.round(df['weighted_score']).astype(int)
df['gold_grade'] = np.round(df['gold_score']).astype(int)
df['grade_diff'] = df['llm_grade'] - df['gold_grade']

# Error severity categories
def classify_error_severity(abs_error):
    if abs_error < 0.5:
        return 'Negligible'
    elif abs_error < 1.0:
        return 'Minor'
    elif abs_error < 1.5:
        return 'Major'
    else:
        return 'Critical'

df['error_severity'] = df['abs_error'].apply(classify_error_severity)

# Direction: over-grading vs under-grading
def classify_direction(error):
    if error > 0.5:
        return 'Over-grading'
    elif error < -0.5:
        return 'Under-grading'
    else:
        return 'Accurate'

df['error_direction'] = df['error'].apply(classify_direction)

print(f"  ✓ Error metrics calculated")

# ============================================================================
# 1. Overall Error Summary by Model and Strategy
# ============================================================================
print("\n[1/5] Overall error summary...")

error_summary = []

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        
        data = df[(df['model'] == model) & (df['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        # Error statistics
        mae = data['abs_error'].mean()
        rmse = np.sqrt((data['error'] ** 2).mean())
        bias = data['error'].mean()
        
        # Error severity distribution
        severity_counts = data['error_severity'].value_counts()
        total = len(data)
        
        # Direction distribution
        direction_counts = data['error_direction'].value_counts()
        
        error_summary.append({
            'model': model,
            'strategy': strategy,
            'n_samples': int(total),
            'mae': round(mae, 4),
            'rmse': round(rmse, 4),
            'bias': round(bias, 4),
            'negligible_pct': round(severity_counts.get('Negligible', 0) / total * 100, 2),
            'minor_pct': round(severity_counts.get('Minor', 0) / total * 100, 2),
            'major_pct': round(severity_counts.get('Major', 0) / total * 100, 2),
            'critical_pct': round(severity_counts.get('Critical', 0) / total * 100, 2),
            'over_grading_pct': round(direction_counts.get('Over-grading', 0) / total * 100, 2),
            'accurate_pct': round(direction_counts.get('Accurate', 0) / total * 100, 2),
            'under_grading_pct': round(direction_counts.get('Under-grading', 0) / total * 100, 2)
        })
        
        print(f"  {model.upper()} {strategy}: MAE={mae:.3f}, Bias={bias:.3f} ({'over' if bias > 0 else 'under'})")

df_error_summary = pd.DataFrame(error_summary)
df_error_summary.to_csv(OUTPUT_DIR / "error_summary.csv", index=False)
print(f"\n  ✓ Saved error_summary.csv")

# ============================================================================
# 2. Error Distribution by True Grade Level
# ============================================================================
print("\n[2/5] Error distribution by grade level...")

grade_error_analysis = []

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        for grade in range(1, 6):
            
            data = df[
                (df['model'] == model) & 
                (df['strategy'] == strategy) &
                (df['gold_grade'] == grade)
            ]
            
            if len(data) == 0:
                continue
            
            grade_error_analysis.append({
                'model': model,
                'strategy': strategy,
                'true_grade': grade,
                'n_samples': int(len(data)),
                'mae': round(data['abs_error'].mean(), 4),
                'bias': round(data['error'].mean(), 4),
                'over_grading_pct': round((data['error'] > 0.5).sum() / len(data) * 100, 2),
                'under_grading_pct': round((data['error'] < -0.5).sum() / len(data) * 100, 2)
            })

df_grade_error = pd.DataFrame(grade_error_analysis)
df_grade_error.to_csv(OUTPUT_DIR / "error_by_grade_level.csv", index=False)
print(f"  ✓ Saved error_by_grade_level.csv")

# ============================================================================
# 3. Confusion Matrix Analysis
# ============================================================================
print("\n[3/5] Confusion matrix analysis...")

confusion_analysis = []

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        
        data = df[(df['model'] == model) & (df['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        # Build confusion matrix
        cm = np.zeros((5, 5), dtype=int)
        for _, row in data.iterrows():
            true_idx = int(row['gold_grade']) - 1
            pred_idx = int(row['llm_grade']) - 1
            if 0 <= true_idx < 5 and 0 <= pred_idx < 5:
                cm[true_idx, pred_idx] += 1
        
        # Save confusion matrix
        cm_df = pd.DataFrame(cm, 
                            index=[f'True_{i}' for i in range(1, 6)],
                            columns=[f'Pred_{i}' for i in range(1, 6)])
        cm_df.to_csv(OUTPUT_DIR / f"confusion_matrix_{model}_{strategy}.csv")
        
        # Analyze off-diagonal errors
        total = cm.sum()
        diagonal_sum = np.trace(cm)
        accuracy = diagonal_sum / total if total > 0 else 0
        
        # Adjacent errors (±1 grade)
        adjacent_mask = np.abs(np.arange(5)[:, None] - np.arange(5)[None, :]) == 1
        adjacent_errors = (cm * adjacent_mask).sum()
        
        # Major errors (≥2 grades off)
        major_mask = np.abs(np.arange(5)[:, None] - np.arange(5)[None, :]) >= 2
        major_errors = (cm * major_mask).sum()
        
        confusion_analysis.append({
            'model': model,
            'strategy': strategy,
            'accuracy': round(accuracy * 100, 2),
            'adjacent_errors_pct': round(adjacent_errors / total * 100, 2),
            'major_errors_pct': round(major_errors / total * 100, 2)
        })
        
        print(f"  {model.upper()} {strategy}: Accuracy={accuracy*100:.1f}%, Major errors={major_errors/total*100:.1f}%")

df_confusion = pd.DataFrame(confusion_analysis)
df_confusion.to_csv(OUTPUT_DIR / "confusion_analysis.csv", index=False)
print(f"\n  ✓ Saved confusion_analysis.csv and confusion matrices")

# ============================================================================
# 4. Systematic Bias Detection
# ============================================================================
print("\n[4/5] Detecting systematic biases...")

bias_analysis = []

for model in df['model'].unique():
    for strategy in df['strategy'].unique():
        
        data = df[(df['model'] == model) & (df['strategy'] == strategy)]
        
        if len(data) == 0:
            continue
        
        # Overall bias
        overall_bias = data['error'].mean()
        
        # Bias by question
        question_bias = data.groupby('question_number')['error'].mean().to_dict()
        
        # Bias by student
        student_bias = data.groupby('student_id')['error'].mean()
        
        # Consistency check: does bias vary significantly?
        from scipy import stats
        _, p_value_question = stats.f_oneway(*[
            data[data['question_number'] == q]['error'].values 
            for q in data['question_number'].unique() if len(data[data['question_number'] == q]) > 0
        ])
        
        bias_analysis.append({
            'model': model,
            'strategy': strategy,
            'overall_bias': round(overall_bias, 4),
            'bias_std_by_question': round(np.std(list(question_bias.values())), 4),
            'bias_std_by_student': round(student_bias.std(), 4),
            'question_effect_pvalue': round(p_value_question, 6),
            'systematic_question_bias': 'Yes' if p_value_question < 0.05 else 'No',
            'max_question_bias': round(max(question_bias.values(), key=abs), 4),
            'min_question_bias': round(min(question_bias.values(), key=abs), 4)
        })
        
        bias_direction = "over-grades" if overall_bias > 0 else "under-grades" if overall_bias < 0 else "neutral"
        print(f"  {model.upper()} {strategy}: {bias_direction} by {abs(overall_bias):.3f} points on average")

df_bias = pd.DataFrame(bias_analysis)
df_bias.to_csv(OUTPUT_DIR / "systematic_bias_analysis.csv", index=False)
print(f"\n  ✓ Saved systematic_bias_analysis.csv")

# ============================================================================
# 5. Critical Error Cases
# ============================================================================
print("\n[5/5] Identifying critical error cases...")

# Critical errors: |error| >= 1.5
critical_errors = df[df['error_severity'] == 'Critical'].copy()

if len(critical_errors) > 0:
    critical_summary = critical_errors.groupby(['model', 'strategy']).agg({
        'experiment_id': 'count',
        'error': ['mean', 'min', 'max']
    }).round(4)
    
    critical_summary.columns = ['_'.join(col).strip('_') for col in critical_summary.columns.values]
    critical_summary = critical_summary.reset_index()
    critical_summary.rename(columns={'experiment_id_count': 'n_critical_errors'}, inplace=True)
    
    critical_summary.to_csv(OUTPUT_DIR / "critical_errors_summary.csv", index=False)
    
    # Export sample critical errors
    critical_sample = critical_errors[['model', 'strategy', 'student_id', 'question_number', 
                                      'gold_score', 'weighted_score', 'error', 'error_direction']].head(50)
    critical_sample.to_csv(OUTPUT_DIR / "critical_errors_sample.csv", index=False)
    
    print(f"  ✓ Found {len(critical_errors)} critical errors")
    print(f"  ✓ Saved critical_errors_summary.csv and sample")
else:
    print(f"  ✓ No critical errors found")

# ============================================================================
# Summary JSON
# ============================================================================
summary = {
    'overall': {
        'total_graded': int(len(df)),
        'models': list(df['model'].unique()),
        'strategies': list(df['strategy'].unique())
    },
    'best_performer': {
        'lowest_mae': df_error_summary.loc[df_error_summary['mae'].idxmin()].to_dict(),
        'lowest_bias': df_error_summary.loc[df_error_summary['bias'].abs().idxmin()].to_dict()
    },
    'critical_errors': {
        'total_count': int(len(critical_errors)),
        'by_model': critical_errors.groupby('model').size().to_dict() if len(critical_errors) > 0 else {}
    }
}

with open(OUTPUT_DIR / "error_analysis_summary.json", 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\n  ✓ Saved error_analysis_summary.json")

# ============================================================================
# Display Summary
# ============================================================================
print("\n" + "="*80)
print("ERROR ANALYSIS SUMMARY")
print("="*80 + "\n")

print("Error Statistics by Model & Strategy:")
print(df_error_summary[['model', 'strategy', 'mae', 'rmse', 'bias']].to_string(index=False))

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nOutput files:")
print(f"  • error_summary.csv - Overall error metrics")
print(f"  • error_by_grade_level.csv - Errors by true grade")
print(f"  • confusion_analysis.csv - Confusion matrix analysis")
print(f"  • systematic_bias_analysis.csv - Bias detection")
print(f"  • critical_errors_summary.csv - Critical error analysis")
print(f"  • confusion_matrix_*.csv - Individual confusion matrices")
print(f"  • error_analysis_summary.json - Summary statistics")
print("="*80 + "\n")
