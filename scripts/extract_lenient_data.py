"""
Extract lenient strategy data from database for focused analysis.

This script filters data to include only:
- Strategy: lenient
- Models: ChatGPT and Gemini
- Trials: 10 trials each
- Expected: 1,538 total tasks (770 ChatGPT + 768 Gemini)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import DatabaseManager


def load_expert_grades(gold_standard_dir):
    """Load expert grades from gold standard JSON files."""
    print("\n[1/4] Loading expert grades...")
    
    import json
    gold_standard_dir = Path(gold_standard_dir)
    
    expert_data = []
    json_files = list(gold_standard_dir.glob("*.json"))
    
    print(f"  Found {len(json_files)} gold standard files")
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        student_name = data['student_name']
        student_id = f"student_{student_name.replace('Mahasiswa ', '').zfill(2)}"
        
        for idx, q_data in enumerate(data['questions'], 1):
            # Calculate letter grade from weighted_score
            score = q_data['weighted_score']
            if score >= 3.5:
                grade = 'A'
            elif score >= 2.5:
                grade = 'B'
            elif score >= 1.5:
                grade = 'C'
            elif score >= 0.5:
                grade = 'D'
            else:
                grade = 'E'
            
            expert_data.append({
                'student_id': student_id,
                'student_name': student_name,
                'question_number': idx,
                'expert_grade': grade,
                'expert_score': score
            })
    
    expert_df = pd.DataFrame(expert_data)
    print(f"  Extracted {len(expert_df)} expert grades")
    print(f"  Questions: {sorted(expert_df['question_number'].unique())}")
    print(f"  Students: {len(expert_df['student_id'].unique())}")
    print(f"  Grade distribution: {expert_df['expert_grade'].value_counts().to_dict()}")
    
    return expert_df


def extract_lenient_data(db_path, output_dir):
    """Extract lenient strategy data from database."""
    print("\n[2/4] Extracting lenient data from database...")
    
    db = DatabaseManager(str(db_path))
    conn = db._get_connection()
    
    # Query for lenient strategy only
    query = """
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
        status
    FROM grading_results
    WHERE strategy = 'lenient'
        AND status = 'completed'
    ORDER BY experiment_id, trial_number, student_id, question_number
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"  Retrieved {len(df)} records")
    print(f"  Models: {df['model'].unique()}")
    print(f"  Trials: {sorted(df['trial_number'].unique())}")
    print(f"  Students: {len(df['student_id'].unique())}")
    print(f"  Questions: {sorted(df['question_number'].unique())}")
    
    # Parse grades JSON
    print("\n  Parsing grade data...")
    import json
    
    def parse_grades(grades_str):
        try:
            grades = json.loads(grades_str)
            return grades.get('overall', 'N/A')
        except:
            return 'N/A'
    
    df['aes_grade'] = df['grades'].apply(parse_grades)
    
    # Distribution summary
    print("\n  Data distribution:")
    for model in df['model'].unique():
        model_df = df[df['model'] == model]
        print(f"    {model.upper()}: {len(model_df)} tasks across {len(model_df['trial_number'].unique())} trials")
    
    return df


def merge_with_expert(aes_df, expert_df):
    """Merge AES grades with expert grades."""
    print("\n[3/4] Merging with expert grades...")
    
    # Merge on student_id and question_number
    merged = aes_df.merge(
        expert_df[['student_id', 'question_number', 'expert_grade', 'expert_score']],
        on=['student_id', 'question_number'],
        how='left'
    )
    
    print(f"  Merged dataset: {len(merged)} records")
    
    # Check for missing expert grades
    missing = merged['expert_grade'].isna().sum()
    if missing > 0:
        print(f"  WARNING: {missing} records without expert grades")
    else:
        print(f"  All records have expert grades!")
    
    # Data quality check
    print("\n  Data quality check:")
    print(f"    Complete records: {len(merged[merged['expert_grade'].notna()])}")
    print(f"    AES grades: {merged['aes_grade'].value_counts().to_dict()}")
    print(f"    Expert grades: {merged['expert_grade'].value_counts().to_dict()}")
    
    return merged


def save_datasets(merged_df, output_dir):
    """Save extracted datasets."""
    print("\n[4/4] Saving datasets...")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Full dataset
    full_path = output_dir / "lenient_full_data.csv"
    merged_df.to_csv(full_path, index=False)
    print(f"  ✓ Saved full dataset: {full_path}")
    print(f"    {len(merged_df)} records")
    
    # 2. ChatGPT only
    chatgpt_df = merged_df[merged_df['model'] == 'chatgpt'].copy()
    chatgpt_path = output_dir / "lenient_chatgpt.csv"
    chatgpt_df.to_csv(chatgpt_path, index=False)
    print(f"  ✓ Saved ChatGPT dataset: {chatgpt_path}")
    print(f"    {len(chatgpt_df)} records across {len(chatgpt_df['trial_number'].unique())} trials")
    
    # 3. Gemini only
    gemini_df = merged_df[merged_df['model'] == 'gemini'].copy()
    gemini_path = output_dir / "lenient_gemini.csv"
    gemini_df.to_csv(gemini_path, index=False)
    print(f"  ✓ Saved Gemini dataset: {gemini_path}")
    print(f"    {len(gemini_df)} records across {len(gemini_df['trial_number'].unique())} trials")
    
    # 4. Summary statistics
    summary_path = output_dir / "lenient_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("LENIENT STRATEGY DATA EXTRACTION SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("OVERALL STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Records: {len(merged_df)}\n")
        f.write(f"Students: {len(merged_df['student_id'].unique())}\n")
        f.write(f"Questions: {len(merged_df['question_number'].unique())}\n")
        f.write(f"Trials: {len(merged_df['trial_number'].unique())}\n")
        f.write(f"Models: {', '.join(merged_df['model'].unique())}\n\n")
        
        f.write("MODEL BREAKDOWN\n")
        f.write("-"*80 + "\n")
        for model in merged_df['model'].unique():
            model_df = merged_df[merged_df['model'] == model]
            f.write(f"\n{model.upper()}:\n")
            f.write(f"  Records: {len(model_df)}\n")
            f.write(f"  Trials: {sorted(model_df['trial_number'].unique())}\n")
            f.write(f"  Students: {len(model_df['student_id'].unique())}\n")
            f.write(f"  Questions: {sorted(model_df['question_number'].unique())}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("GRADE DISTRIBUTION\n")
        f.write("="*80 + "\n\n")
        
        f.write("AES Grades:\n")
        aes_counts = merged_df['aes_grade'].value_counts().sort_index()
        for grade, count in aes_counts.items():
            pct = (count / len(merged_df)) * 100
            f.write(f"  {grade}: {count} ({pct:.1f}%)\n")
        
        f.write("\nExpert Grades:\n")
        expert_counts = merged_df['expert_grade'].value_counts().sort_index()
        for grade, count in expert_counts.items():
            pct = (count / len(merged_df)) * 100
            f.write(f"  {grade}: {count} ({pct:.1f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("QUALITY METRICS\n")
        f.write("="*80 + "\n\n")
        
        # Agreement preview
        agreement = (merged_df['aes_grade'] == merged_df['expert_grade']).sum()
        agreement_pct = (agreement / len(merged_df)) * 100
        f.write(f"Exact Agreement: {agreement}/{len(merged_df)} ({agreement_pct:.1f}%)\n")
        
        # Missing data
        missing_expert = merged_df['expert_grade'].isna().sum()
        missing_aes = (merged_df['aes_grade'] == 'N/A').sum()
        f.write(f"Missing Expert Grades: {missing_expert}\n")
        f.write(f"Missing AES Grades: {missing_aes}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("DATA FILES GENERATED\n")
        f.write("="*80 + "\n\n")
        f.write(f"1. {full_path.name} - Full dataset ({len(merged_df)} records)\n")
        f.write(f"2. {chatgpt_path.name} - ChatGPT only ({len(chatgpt_df)} records)\n")
        f.write(f"3. {gemini_path.name} - Gemini only ({len(gemini_df)} records)\n")
        f.write(f"4. {summary_path.name} - This summary file\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved summary: {summary_path}")
    
    return {
        'full': full_path,
        'chatgpt': chatgpt_path,
        'gemini': gemini_path,
        'summary': summary_path
    }


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("EXTRACTING LENIENT STRATEGY DATA FOR FOCUSED ANALYSIS")
    print("="*80)
    
    # Paths
    db_path = project_root / "results" / "grading_results.db"
    gold_standard_dir = project_root / "results" / "gold_standard"
    output_dir = project_root / "results" / "lenient_analysis"
    
    print(f"\nDatabase: {db_path}")
    print(f"Gold standard: {gold_standard_dir}")
    print(f"Output directory: {output_dir}")
    
    # Load expert grades
    expert_df = load_expert_grades(gold_standard_dir)
    
    # Extract lenient data
    aes_df = extract_lenient_data(db_path, output_dir)
    
    # Merge
    merged_df = merge_with_expert(aes_df, expert_df)
    
    # Save
    files = save_datasets(merged_df, output_dir)
    
    # Final summary
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("="*80)
    print(f"\nTotal records extracted: {len(merged_df)}")
    print(f"ChatGPT: {len(merged_df[merged_df['model'] == 'chatgpt'])}")
    print(f"Gemini: {len(merged_df[merged_df['model'] == 'gemini'])}")
    print(f"\nFiles saved to: {output_dir}")
    print("\nNext step: Run RQ1 analysis (rq1_reliability_lenient.py)")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
