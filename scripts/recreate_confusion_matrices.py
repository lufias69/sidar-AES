"""
Recreate confusion matrices with ALL grades (A, B, C, D, E) displayed
Even if some grades don't appear in the data
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUTPUT_DIR = Path('results/figures')
OUTPUT_DIR.mkdir(exist_ok=True)

def score_to_grade(score):
    """Convert weighted score to letter grade"""
    if pd.isna(score):
        return None
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
    """Load gold standard from JSON files with correct student name mapping
    
    Note: Gold standard uses array index (0-6) as question number (1-7)
    NOT the question number extracted from the text!
    """
    import json
    gold_dir = Path('results/gold_standard')
    name_to_scores = {}
    
    for file in gold_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            student_name = data['student_name']  # e.g., "Mahasiswa 1"
            
            name_to_scores[student_name] = {}
            # Use array index + 1 as question number (1-7)
            for idx, q in enumerate(data['questions'], start=1):
                name_to_scores[student_name][idx] = q['weighted_score']
    
    return name_to_scores

def create_confusion_matrix_with_all_grades():
    """Create confusion matrices ensuring ALL grades A-E are displayed"""
    print("="*80)
    print("CREATING CONFUSION MATRICES WITH ALL GRADES (A, B, C, D, E)")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    # All possible grades
    ALL_GRADES = ['A', 'B', 'C', 'D', 'E']
    
    # Configurations to process
    configs = [
        ('chatgpt', 'lenient', 'exp_chatgpt_lenient_01'),
        ('gemini', 'lenient', 'exp_gemini_lenient_01'),
        ('chatgpt', 'zero-shot', 'exp_chatgpt_zero'),
        ('gemini', 'zero-shot', 'exp_gemini_zero'),
    ]
    
    for model, strategy, exp_id in configs:
        print(f"\nProcessing {model.upper()} ({strategy})...")
        
        # Query data with student_name
        df = pd.read_sql_query(f"""
            SELECT student_id, student_name, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        # Add gold standard using student_name
        df['gold_score'] = df.apply(
            lambda row: gold_data.get(row['student_name'], {}).get(row['question_number']),
            axis=1
        )
        
        # Convert to grades
        df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
        df['gold_grade'] = df['gold_score'].apply(score_to_grade)
        
        # Drop nulls
        df = df.dropna()
        
        print(f"  Total samples: {len(df)}")
        print(f"  Gold grades: {sorted(df['gold_grade'].unique())}")
        print(f"  AI grades: {sorted(df['ai_grade'].unique())}")
        
        # Create confusion matrix with explicit categories
        cm = pd.crosstab(
            df['gold_grade'], 
            df['ai_grade'],
            rownames=['Gold Standard Grade'],
            colnames=['AI Predicted Grade'],
            dropna=False
        )
        
        # Reindex to ensure ALL grades are present (fill missing with 0)
        cm = cm.reindex(index=ALL_GRADES, columns=ALL_GRADES, fill_value=0)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   cbar_kws={'label': 'Count'},
                   linewidths=0.5, linecolor='gray',
                   vmin=0, vmax=cm.max().max())
        
        # Title and labels
        title = f'Confusion Matrix: {model.upper()} ({strategy})\nGold Standard vs AI Grades'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('AI Predicted Grade', fontsize=12, fontweight='bold')
        ax.set_ylabel('Gold Standard Grade', fontsize=12, fontweight='bold')
        
        # Add note about empty cells
        note = "Note: Empty or zero cells indicate grade combinations not present in data"
        fig.text(0.5, 0.02, note, ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout()
        
        # Save
        filename = f'confusion_matrix_{model}_{strategy.replace("-", "")}.png'
        plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✅ Saved: {filename}")
        
        # Print statistics
        total = cm.sum().sum()
        diagonal = np.diag(cm).sum()
        accuracy = diagonal / total if total > 0 else 0
        print(f"  Accuracy: {accuracy:.1%} ({diagonal}/{total})")
        
        # Show which grades are missing
        gold_missing = [g for g in ALL_GRADES if cm.loc[g].sum() == 0]
        ai_missing = [g for g in ALL_GRADES if cm[g].sum() == 0]
        
        if gold_missing:
            print(f"  ⚠️  Gold standard missing: {', '.join(gold_missing)}")
        if ai_missing:
            print(f"  ⚠️  AI predictions missing: {', '.join(ai_missing)}")
    
    conn.close()
    
    print("\n" + "="*80)
    print("✅ ALL CONFUSION MATRICES CREATED SUCCESSFULLY")
    print("="*80)
    print(f"\nSaved to: {OUTPUT_DIR}")
    print("\nAll grades (A, B, C, D, E) are now displayed in the matrices.")
    print("Zero values indicate grade combinations that didn't occur in the data.")

if __name__ == '__main__':
    create_confusion_matrix_with_all_grades()
