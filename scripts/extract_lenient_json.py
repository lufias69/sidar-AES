"""
Extract lenient strategy data from JSON experiment files.

Reads all 10 trials × 2 models = 20 experiment folders and consolidates into analysis dataset.
"""

import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_expert_grades(gold_standard_dir):
    """Load expert grades from gold standard JSON files."""
    print("\n[1/3] Loading expert grades...")
    
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
    print(f"  Extracted {len(expert_df)} expert grades from {len(json_files)} students")
    print(f"  Grade distribution: {expert_df['expert_grade'].value_counts().to_dict()}")
    
    return expert_df


def extract_lenient_from_json(results_dir):
    """Extract lenient strategy data from JSON experiment folders."""
    print("\n[2/3] Extracting lenient data from JSON files...")
    
    results_dir = Path(results_dir)
    all_data = []
    
    # Find all lenient experiment folders
    lenient_folders = list(results_dir.glob("exp_*_lenient_*"))
    lenient_folders.sort()
    
    print(f"  Found {len(lenient_folders)} lenient experiment folders")
    
    for folder in lenient_folders:
        # Parse folder name: exp_{model}_lenient_{trial:02d}
        folder_name = folder.name
        parts = folder_name.split('_')
        model = parts[1]  # chatgpt or gemini
        trial = int(parts[3])  # trial number
        
        # Read all JSON files in folder
        json_files = list(folder.glob("*.json"))
        
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"    WARNING: Failed to parse {json_file}")
                    continue
            
            student_name = data.get('student_name', '')
            student_id = data.get('student_id', '')  # Use existing student_id from JSON
            
            # Extract each question's grading
            for q_data in data.get('questions', []):
                q_num = q_data.get('question_id', 0)  # Changed from question_number to question_id
                
                # Get grades - structure is different
                grades = q_data.get('grades', {})
                weighted_score = q_data.get('weighted_score', 0.0)
                
                # Calculate overall grade from weighted_score
                if weighted_score >= 3.5:
                    overall_grade = 'A'
                elif weighted_score >= 2.5:
                    overall_grade = 'B'
                elif weighted_score >= 1.5:
                    overall_grade = 'C'
                elif weighted_score >= 0.5:
                    overall_grade = 'D'
                else:
                    overall_grade = 'E'
                
                all_data.append({
                    'experiment_id': folder_name,
                    'trial_number': trial,
                    'model': model,
                    'strategy': 'lenient',
                    'student_id': student_id,
                    'student_name': student_name,
                    'question_number': q_num,
                    'question_text': q_data.get('question', ''),
                    'answer_text': q_data.get('answer', ''),
                    'aes_grade': overall_grade,
                    'weighted_score': weighted_score,
                    'grades_detail': json.dumps(grades, ensure_ascii=False),
                    'justification': q_data.get('justification', ''),
                    'overall_comment': q_data.get('overall_comment', ''),
                    'tokens_used': q_data.get('metadata', {}).get('tokens', 0),
                    'api_call_time': q_data.get('metadata', {}).get('call_time', 0.0)
                })
    
    df = pd.DataFrame(all_data)
    
    if len(df) == 0:
        print("  ERROR: No data extracted!")
        return df
    
    print(f"  Extracted {len(df)} grading records")
    print(f"\n  Data distribution:")
    for model in sorted(df['model'].unique()):
        model_df = df[df['model'] == model]
        trials = sorted(model_df['trial_number'].unique())
        print(f"    {model.upper()}: {len(model_df)} records across trials {min(trials)}-{max(trials)}")
    
    print(f"\n  Students: {len(df['student_id'].unique())}")
    print(f"  Questions: {sorted(df['question_number'].unique())}")
    print(f"  AES grade distribution: {df['aes_grade'].value_counts().to_dict()}")
    
    return df


def merge_and_save(aes_df, expert_df, output_dir):
    """Merge AES with expert grades and save datasets."""
    print("\n[3/3] Merging with expert grades and saving...")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Merge
    merged = aes_df.merge(
        expert_df[['student_id', 'question_number', 'expert_grade', 'expert_score']],
        on=['student_id', 'question_number'],
        how='left'
    )
    
    print(f"  Merged dataset: {len(merged)} records")
    
    # Check missing
    missing = merged['expert_grade'].isna().sum()
    if missing > 0:
        print(f"  WARNING: {missing} records without expert grades")
        # Show which students are missing
        missing_students = merged[merged['expert_grade'].isna()]['student_id'].unique()
        print(f"  Missing students: {list(missing_students)}")
    else:
        print(f"  ✓ All records have expert grades!")
    
    # Save datasets
    print("\n  Saving files...")
    
    # 1. Full dataset
    full_path = output_dir / "lenient_full_data.csv"
    merged.to_csv(full_path, index=False, encoding='utf-8')
    print(f"    ✓ Full dataset: {len(merged)} records")
    
    # 2. ChatGPT only
    chatgpt_df = merged[merged['model'] == 'chatgpt'].copy()
    chatgpt_path = output_dir / "lenient_chatgpt.csv"
    chatgpt_df.to_csv(chatgpt_path, index=False, encoding='utf-8')
    print(f"    ✓ ChatGPT: {len(chatgpt_df)} records, {len(chatgpt_df['trial_number'].unique())} trials")
    
    # 3. Gemini only
    gemini_df = merged[merged['model'] == 'gemini'].copy()
    gemini_path = output_dir / "lenient_gemini.csv"
    gemini_df.to_csv(gemini_path, index=False, encoding='utf-8')
    print(f"    ✓ Gemini: {len(gemini_df)} records, {len(gemini_df['trial_number'].unique())} trials")
    
    # 4. Summary report
    summary_path = output_dir / "data_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("LENIENT STRATEGY DATA EXTRACTION SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source: JSON files from exp_*_lenient_* folders\n\n")
        
        f.write("OVERALL STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Records: {len(merged)}\n")
        f.write(f"Students: {len(merged['student_id'].unique())}\n")
        f.write(f"Questions per student: {len(merged['question_number'].unique())}\n")
        f.write(f"Trials: {len(merged['trial_number'].unique())}\n")
        f.write(f"Models: {', '.join(sorted(merged['model'].unique()))}\n\n")
        
        for model in sorted(merged['model'].unique()):
            model_df = merged[merged['model'] == model]
            f.write(f"{model.upper()}:\n")
            f.write(f"  Records: {len(model_df)}\n")
            f.write(f"  Trials: {sorted(model_df['trial_number'].unique())}\n")
            f.write(f"  Students: {len(model_df['student_id'].unique())}\n\n")
        
        f.write("GRADE DISTRIBUTION\n")
        f.write("-"*80 + "\n\n")
        
        f.write("AES Grades (All):\n")
        for grade, count in sorted(merged['aes_grade'].value_counts().items()):
            pct = (count / len(merged)) * 100
            f.write(f"  {grade}: {count} ({pct:.1f}%)\n")
        
        f.write("\nExpert Grades:\n")
        for grade, count in sorted(merged['expert_grade'].value_counts().items()):
            pct = (count / len(merged[merged['expert_grade'].notna()])) * 100
            f.write(f"  {grade}: {count} ({pct:.1f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("AGREEMENT PREVIEW\n")
        f.write("="*80 + "\n\n")
        
        valid = merged[merged['expert_grade'].notna()].copy()
        if len(valid) > 0:
            agreement = (valid['aes_grade'] == valid['expert_grade']).sum()
            agreement_pct = (agreement / len(valid)) * 100
            f.write(f"Exact Agreement: {agreement}/{len(valid)} ({agreement_pct:.1f}%)\n")
            
            # Per model
            for model in sorted(merged['model'].unique()):
                model_valid = valid[valid['model'] == model]
                if len(model_valid) > 0:
                    model_agree = (model_valid['aes_grade'] == model_valid['expert_grade']).sum()
                    model_pct = (model_agree / len(model_valid)) * 100
                    f.write(f"  {model.upper()}: {model_agree}/{len(model_valid)} ({model_pct:.1f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("DATA QUALITY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Complete records (with expert): {len(valid)}\n")
        f.write(f"Missing expert grades: {missing}\n")
        f.write(f"Missing AES grades: {(merged['aes_grade'] == 'N/A').sum()}\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"    ✓ Summary: {summary_path.name}")
    
    return {
        'full': full_path,
        'chatgpt': chatgpt_path,
        'gemini': gemini_path,
        'summary': summary_path
    }


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("EXTRACTING LENIENT STRATEGY DATA FROM JSON FILES")
    print("="*80)
    
    # Paths
    results_dir = project_root / "results"
    gold_standard_dir = results_dir / "gold_standard"
    output_dir = results_dir / "lenient_analysis"
    
    print(f"\nExperiment folders: {results_dir}")
    print(f"Gold standard: {gold_standard_dir}")
    print(f"Output: {output_dir}")
    
    # Load expert grades
    expert_df = load_expert_grades(gold_standard_dir)
    
    # Extract from JSON
    aes_df = extract_lenient_from_json(results_dir)
    
    if len(aes_df) == 0:
        print("\nERROR: No data extracted! Exiting.")
        return
    
    # Merge and save
    files = merge_and_save(aes_df, expert_df, output_dir)
    
    # Final summary
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("="*80)
    print(f"\nTotal records: {len(aes_df)}")
    
    chatgpt_count = len(aes_df[aes_df['model'] == 'chatgpt'])
    gemini_count = len(aes_df[aes_df['model'] == 'gemini'])
    print(f"ChatGPT: {chatgpt_count} records")
    print(f"Gemini: {gemini_count} records")
    
    print(f"\nFiles saved to: {output_dir}")
    print(f"  - {files['full'].name}")
    print(f"  - {files['chatgpt'].name}")
    print(f"  - {files['gemini'].name}")
    print(f"  - {files['summary'].name}")
    
    print("\nNext step: RQ1 Analysis - Reliability vs Expert")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
