"""
Extract and prepare data from database for comprehensive analysis.

Outputs:
1. experiment_data_complete.csv - All experiment data
2. per_item_scores.csv - Scores per (student, question, trial) for consistency analysis
3. gold_standard.csv - Gold standard reference scores
4. experiment_summary.json - Metadata about experiments
"""

import sqlite3
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

# Paths
DB_PATH = "results/grading_results.db"
OUTPUT_DIR = Path("results_experiment_final/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*80)
print("EXTRACTING DATA FROM DATABASE")
print("="*80 + "\n")

# Connect to database
conn = sqlite3.connect(DB_PATH)

# 1. Extract ALL experiment data
print("[1/4] Extracting all experiment data...")
query_all = """
    SELECT 
        experiment_id,
        trial_number,
        student_id,
        student_name,
        question_number,
        question_text,
        answer_text,
        model,
        strategy,
        grades,
        weighted_score,
        justification,
        overall_comment,
        tokens_used,
        api_call_time,
        timestamp,
        status
    FROM grading_results
    WHERE status = 'completed'
    ORDER BY experiment_id, trial_number, student_id, question_number
"""

df_all = pd.read_sql_query(query_all, conn)
print(f"   ✓ Loaded {len(df_all)} completed gradings")

# Save complete data
output_file = OUTPUT_DIR / "experiment_data_complete.csv"
df_all.to_csv(output_file, index=False, encoding='utf-8')
print(f"   ✓ Saved to: {output_file}")

# 2. Extract per-item scores (for consistency analysis)
print("\n[2/4] Extracting per-item scores...")

# Get experiment patterns for 10-trial experiments
experiment_patterns = {
    'chatgpt_zero': [f'exp_chatgpt_zero{"" if i==1 else f"_{i:02d}"}' for i in range(1, 12)],
    'chatgpt_few': [f'exp_chatgpt_few{"" if i==1 else f"_{i:02d}"}' for i in range(1, 12)],
    'chatgpt_lenient': [f'exp_chatgpt_lenient_{i:02d}' for i in range(1, 13)],
    'gemini_zero': [f'exp_gemini_zero{"" if i==1 else f"_{i:02d}"}' for i in range(1, 11)],
    'gemini_few': [f'exp_gemini_few{"" if i==1 else f"_{i:02d}"}' for i in range(1, 11)],
    'gemini_lenient': [f'exp_gemini_lenient_{i:02d}' for i in range(1, 14)],
}

per_item_data = []

for strategy_name, exp_ids in experiment_patterns.items():
    model = strategy_name.split('_')[0]
    strategy = strategy_name.split('_', 1)[1]
    
    for trial_idx, exp_id in enumerate(exp_ids, start=1):
        query = f"""
            SELECT 
                student_id,
                student_name,
                question_number,
                question_text,
                weighted_score
            FROM grading_results
            WHERE experiment_id = ? AND status = 'completed'
        """
        
        df_trial = pd.read_sql_query(query, conn, params=(exp_id,))
        
        for _, row in df_trial.iterrows():
            per_item_data.append({
                'model': model,
                'strategy': strategy,
                'trial_number': trial_idx,
                'student_id': row['student_id'],
                'student_name': row['student_name'],
                'question_number': row['question_number'],
                'question_text': row['question_text'],
                'score': row['weighted_score']
            })

df_per_item = pd.DataFrame(per_item_data)
print(f"   ✓ Loaded {len(df_per_item)} per-item scores")

output_file = OUTPUT_DIR / "per_item_scores.csv"
df_per_item.to_csv(output_file, index=False, encoding='utf-8')
print(f"   ✓ Saved to: {output_file}")

# 3. Load gold standard
print("\n[3/4] Loading gold standard...")

# Use baseline as gold standard
baseline_path = Path("results/baseline_batch")
if baseline_path.exists():
    gold_data = []
    
    for json_file in sorted(baseline_path.glob("student_*.json")):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract student info from filename or data
        student_name = data.get('student_name', '')
        student_index = data.get('student_index', 0)
        student_id = f"{student_index:02d}"
        
        for i, question_data in enumerate(data['questions'], start=1):
            # Use ChatGPT baseline as gold standard
            if 'chatgpt' in question_data:
                gold_data.append({
                    'student_id': student_id,
                    'student_name': student_name,
                    'question_number': i,
                    'question_text': question_data.get('question', ''),
                    'gold_score': question_data['chatgpt']['weighted_score'],
                    'gold_grades': json.dumps(question_data['chatgpt']['scores'])
                })
    
    df_gold = pd.DataFrame(gold_data)
    print(f"   ✓ Created {len(df_gold)} gold standard entries from baseline")
    
    output_file = OUTPUT_DIR / "gold_standard.csv"
    df_gold.to_csv(output_file, index=False, encoding='utf-8')
    print(f"   ✓ Saved to: {output_file}")
else:
    print("   ⚠ Baseline not found, gold standard will be missing")

# 4. Create experiment summary
print("\n[4/4] Creating experiment summary...")

summary = {
    'total_experiments': df_all['experiment_id'].nunique(),
    'total_gradings': len(df_all),
    'models': df_all['model'].unique().tolist(),
    'strategies': df_all['strategy'].unique().tolist(),
    'experiments_by_model_strategy': {},
    'students': {
        'total': df_all['student_id'].nunique(),
        'ids': sorted(df_all['student_id'].unique().tolist())
    },
    'questions': {
        'total': df_all['question_number'].nunique(),
        'numbers': sorted(df_all['question_number'].unique().tolist())
    },
    'date_range': {
        'first': df_all['timestamp'].min(),
        'last': df_all['timestamp'].max()
    }
}

# Count experiments per model-strategy
for model in df_all['model'].unique():
    for strategy in df_all['strategy'].unique():
        mask = (df_all['model'] == model) & (df_all['strategy'] == strategy)
        exp_count = df_all[mask]['experiment_id'].nunique()
        if exp_count > 0:
            key = f"{model}_{strategy}"
            summary['experiments_by_model_strategy'][key] = {
                'experiments': int(exp_count),
                'gradings': int(mask.sum())
            }

output_file = OUTPUT_DIR / "experiment_summary.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False, default=int)

print(f"   ✓ Saved to: {output_file}")

# Print summary
print("\n" + "="*80)
print("EXTRACTION COMPLETE")
print("="*80)
print(f"\nTotal Experiments: {summary['total_experiments']}")
print(f"Total Gradings: {summary['total_gradings']}")
print(f"Models: {', '.join(summary['models'])}")
print(f"Strategies: {', '.join(summary['strategies'])}")
print(f"\nStudents: {summary['students']['total']}")
print(f"Questions: {summary['questions']['total']}")

print("\n" + "="*80)
print("OUTPUT FILES:")
print("="*80)
print(f"1. {OUTPUT_DIR}/experiment_data_complete.csv")
print(f"2. {OUTPUT_DIR}/per_item_scores.csv")
print(f"3. {OUTPUT_DIR}/gold_standard.csv")
print(f"4. {OUTPUT_DIR}/experiment_summary.json")
print("="*80 + "\n")

conn.close()
