"""
Test run untuk 1 trial saja (ChatGPT zero-shot trial 02).
Untuk memastikan sistem berjalan dengan baik sebelum menjalankan semua 36 eksperimen.
"""

import sys
import os
from pathlib import Path
import time
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import DatabaseManager
from src.core.prompt_builder import PromptBuilder
from src.core.rubric import RubricManager
from src.agents.chatgpt_agent import ChatGPTAgent
from src.agents.gemini_agent import GeminiAgent
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_student_data(excel_path):
    """Load student answers from Excel file."""
    print(f"[OK] Loading data from: {excel_path}")
    
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    df = pd.read_excel(excel_path)
    
    # Use 'Nama' for student name column
    if 'Nama' not in df.columns:
        raise ValueError(f"Column 'Nama' not found. Available columns: {df.columns.tolist()}")
    
    # Filter to selected students if file exists
    selected_file = project_root / "selected_students.txt"
    if selected_file.exists():
        with open(selected_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        
        selected_names = [line.split(',')[1] for line in lines if ',' in line]
        df = df[df['Nama'].isin(selected_names)].copy()
        print(f"[OK] Filtered to {len(df)} selected students")
    else:
        print(f"[OK] Using all {len(df)} students")
    
    return df


def extract_questions(df):
    """Extract question columns from dataframe."""
    # Get all columns that are questions (not Nama or NIM)
    question_cols = [col for col in df.columns if col not in ['Nama', 'NIM']]
    
    questions = []
    for i, col in enumerate(question_cols, 1):
        questions.append({
            'number': i,
            'text': col,  # Use column name as question text
            'column': col
        })
    
    print(f"[OK] Found {len(questions)} questions")
    return questions


def grade_task(agent, student_data, question_data, strategy_name, rubric):
    """Grade a single task and return results with metadata."""
    try:
        # Call agent's grade_essay method
        start_time = time.time()
        result = agent.grade_essay(
            student_id=student_data['id'],
            question_id=str(question_data['number']),
            question=question_data['text'],
            answer=student_data['answer'],
            rubric=rubric,
            trial=1
        )
        api_call_time = time.time() - start_time
        
        # Convert GradingResult to our format
        return {
            'success': True,
            'grades': result.scores,
            'weighted_score': result.weighted_score,
            'justification': json.dumps(result.scores, ensure_ascii=False),
            'overall_comment': result.overall_comment or '',
            'tokens': result.metadata.get('tokens', 0),
            'time': api_call_time,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'tokens': 0,
            'time': 0
        }


def run_trial(model_name, strategy, trial_num, db, rubric, df, questions, agent):
    """Run a single trial with checkpoint/resume support"""
    
    # Create experiment ID
    if strategy == 'zero-shot':
        exp_id = f"exp_{model_name}_zero_{trial_num:02d}"
    else:  # few-shot
        exp_id = f"exp_{model_name}_few_{trial_num:02d}"
    
    print(f"\n{'='*80}")
    print(f"TEST EXPERIMENT: {exp_id}")
    print(f"Model: {model_name.upper()}, Strategy: {strategy}, Trial: {trial_num}")
    print(f"{'='*80}")
    
    # Count progress
    total_tasks = len(df) * len(questions)
    completed_tasks = 0
    skipped_tasks = 0
    failed_tasks = 0
    
    # Process each student
    for idx, row in df.iterrows():
        student_name = row['Nama']
        student_id = f"student_{student_name.replace('Mahasiswa ', '').zfill(2)}"
        
        print(f"\n[{idx+1}/{len(df)}] Processing: {student_name}")
        
        # Process each question
        for question in questions:
            # Check if already completed
            if db.check_exists(exp_id, trial_num, student_id, question['number']):
                print(f"  [OK✓] Question {question['number']}: Already completed")
                skipped_tasks += 1
                completed_tasks += 1
                continue
            
            # Prepare student data
            student_data = {
                'id': student_id,
                'name': student_name,
                'answer': row[question['column']]
            }
            
            # Mark as pending/processing
            db.insert_or_update(
                experiment_id=exp_id,
                trial_number=trial_num,
                student_id=student_id,
                student_name=student_name,
                question_number=question['number'],
                question_text=question['text'],
                answer_text=student_data['answer'],
                model=model_name,
                strategy=strategy,
                status='processing'
            )
            
            # Grade using the agent
            try:
                result = grade_task(agent, student_data, question, strategy, rubric)
                
                if result['success']:
                    # Save successful result
                    db.insert_or_update(
                        experiment_id=exp_id,
                        trial_number=trial_num,
                        student_id=student_id,
                        student_name=student_name,
                        question_number=question['number'],
                        question_text=question['text'],
                        answer_text=student_data['answer'],
                        model=model_name,
                        strategy=strategy,
                        grades=result['grades'],
                        weighted_score=result['weighted_score'],
                        justification=result['justification'],
                        overall_comment=result['overall_comment'],
                        tokens_used=result['tokens'],
                        api_call_time=result['time'],
                        status='completed'
                    )
                    
                    print(f"  [OK] Question {question['number']}: Score {result['weighted_score']:.2f} ({result['tokens']} tokens)")
                    completed_tasks += 1
                    
                else:
                    # Save error
                    db.insert_or_update(
                        experiment_id=exp_id,
                        trial_number=trial_num,
                        student_id=student_id,
                        student_name=student_name,
                        question_number=question['number'],
                        question_text=question['text'],
                        answer_text=student_data['answer'],
                        model=model_name,
                        strategy=strategy,
                        error_message=result['error'],
                        status='failed'
                    )
                    print(f"  [ERROR] Question {question['number']}: {result['error']}")
                    failed_tasks += 1
                    
            except Exception as e:
                print(f"  [ERROR] Question {question['number']}: {str(e)}")
                failed_tasks += 1
                continue
    
    # Summary
    print(f"\n{'─'*80}")
    print(f"TRIAL SUMMARY: {exp_id}")
    print(f"{'─'*80}")
    print(f"  Total tasks: {total_tasks}")
    print(f"  Completed: {completed_tasks}")
    print(f"  Failed: {failed_tasks}")
    print(f"  Skipped (already done): {skipped_tasks}")
    print(f"{'─'*80}")
    
    return exp_id


def main():
    """Main execution"""
    
    print("\n" + "="*80)
    print("TEST: RUNNING 1 TRIAL")
    print("="*80)
    print("\nThis will run 1 experiment:")
    print("  - ChatGPT zero-shot: trial 02")
    print("\nFeatures:")
    print("  [OK] Results saved to database")
    print("  [OK] Checkpoint/Resume support")
    print("  [OK] Progress tracking per task")
    print("\nEstimated time: 3-5 minutes")
    print("="*80)
    
    # Initialize
    db_path = project_root / "results" / "grading_results.db"
    db = DatabaseManager(str(db_path))
    
    rubric_manager = RubricManager()
    rubric = rubric_manager.get_rubric("default")
    
    # Initialize PromptBuilder with rubric
    prompt_builder = PromptBuilder(rubric=rubric, language="indonesian")
    
    # Load data
    excel_path = project_root / "data" / "Jawaban" / "jawaban UTS  Capstone Project.xlsx"
    df = load_student_data(excel_path)
    
    # Extract questions
    questions = extract_questions(df)
    
    print(f"\n[OK] Loaded {len(df)} students, {len(questions)} questions each")
    print(f"[OK] Total tasks: {len(df) * len(questions)}")
    
    # Initialize agent (agent already handles strategy via rubric/prompts)
    chatgpt_agent = ChatGPTAgent()
    
    # Run test trial
    start_time = time.time()
    
    try:
        exp_id = run_trial('chatgpt', 'zero-shot', 2, db, rubric, df, questions, chatgpt_agent)
        
        total_time = time.time() - start_time
        
        print("\n" + "="*80)
        print("TEST COMPLETE!")
        print("="*80)
        print(f"\nExperiment: {exp_id}")
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"\nDatabase saved: results/grading_results.db")
        print("\nTo check results:")
        print(f"  python scripts/db_status.py --experiment {exp_id}")
        print("\n" + "="*80)
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Process interrupted by user.")
        print("[INFO] Progress saved to database.")
        print("[INFO] Run this script again to resume from checkpoint.")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
