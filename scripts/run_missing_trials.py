"""
Run missing trials to complete 10-trial sets for all strategies.

Missing experiments:
- Gemini zero-shot: trials 09-10 (2 more needed)
- Gemini few-shot: trials 02-10 (9 more needed)

Total: 11 experiments
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
            'justification': result.justification,
            'overall_comment': result.overall_comment,
            'tokens_used': getattr(result, 'tokens_used', 0),
            'api_call_time': api_call_time
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def run_trial(model: str, strategy: str, trial: int, db: DatabaseManager, 
              rubric: dict, df: pd.DataFrame, questions: list, agent):
    """Run a single trial experiment."""
    
    # Generate experiment ID
    if trial == 1:
        exp_id = f"exp_{model}_{strategy.replace('-shot', '')}"
    else:
        exp_id = f"exp_{model}_{strategy.replace('-shot', '')}_{trial:02d}"
    
    print(f"\n[START] Experiment: {exp_id}")
    print(f"[INFO] Model: {model}, Strategy: {strategy}, Trial: {trial}")
    
    # Check progress
    completed, total, percentage = db.get_progress(exp_id, trial)
    total_expected = len(df) * len(questions)
    
    if completed == total_expected and total_expected > 0:
        print(f"[SKIP] Experiment already completed: {completed}/{total_expected} tasks")
        return exp_id
    elif completed > 0:
        print(f"[RESUME] Found {completed}/{total_expected} completed tasks")
    
    # Set agent's prompt strategy
    agent.set_prompt_strategy(strategy)
    
    # Prepare tasks
    total_tasks = len(df) * len(questions)
    completed = 0
    failed = 0
    
    print(f"[INFO] Total tasks: {total_tasks}")
    
    for student_idx, (_, student_row) in enumerate(df.iterrows(), 1):
        student_id = f"{student_idx:02d}"
        student_name = student_row['Nama']
        
        print(f"\n[STUDENT] {student_idx}/{len(df)}: {student_name}")
        
        for question in questions:
            q_num = question['number']
            
            # Check if already completed
            if db.check_exists(exp_id, trial, student_id, q_num):
                print(f"  [Q{q_num}] ✓ Skip (already completed)")
                completed += 1
                continue
            
            # Get answer
            answer = student_row[question['column']]
            if pd.isna(answer) or str(answer).strip() == '':
                print(f"  [Q{q_num}] ⚠ Skip (no answer)")
                continue
            
            # Grade the task
            print(f"  [Q{q_num}] Grading...", end='', flush=True)
            
            student_data = {
                'id': student_id,
                'name': student_name,
                'answer': str(answer)
            }
            
            result = grade_task(agent, student_data, question, strategy, rubric)
            
            if result['success']:
                # Save to database
                db.insert_or_update(
                    experiment_id=exp_id,
                    trial_number=trial,
                    student_id=student_id,
                    student_name=student_name,
                    question_number=q_num,
                    question_text=question['text'],
                    answer_text=str(answer),
                    model=model,
                    strategy=strategy,
                    grades=result['grades'],
                    weighted_score=result['weighted_score'],
                    justification=result.get('justification', ''),
                    overall_comment=result.get('overall_comment', ''),
                    tokens_used=result.get('tokens_used', 0),
                    api_call_time=result.get('api_call_time', 0),
                    status='completed'
                )
                
                print(f" ✓ Score: {result['weighted_score']:.2f}")
                completed += 1
                
            else:
                # Save failed task
                db.insert_or_update(
                    experiment_id=exp_id,
                    trial_number=trial,
                    student_id=student_id,
                    student_name=student_name,
                    question_number=q_num,
                    question_text=question['text'],
                    answer_text=str(answer),
                    model=model,
                    strategy=strategy,
                    grades={},
                    weighted_score=0,
                    justification='',
                    overall_comment='',
                    tokens_used=0,
                    api_call_time=0,
                    status='failed',
                    error_message=result.get('error', 'Unknown error')
                )
                
                print(f" ✗ Failed: {result.get('error', 'Unknown error')}")
                failed += 1
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
    
    print(f"\n[COMPLETE] {exp_id}")
    print(f"  Completed: {completed}/{total_tasks}")
    print(f"  Failed: {failed}")
    
    return exp_id


def main():
    """Main function to run missing trials."""
    
    print("\n" + "="*80)
    print("RUNNING MISSING TRIALS")
    print("="*80)
    
    # Initialize database
    db = DatabaseManager()
    
    # Load rubric
    rubric_path = project_root / "config" / "rubrics.json"
    with open(rubric_path, 'r', encoding='utf-8') as f:
        rubrics = json.load(f)
    rubric = rubrics['default']
    
    # Initialize PromptBuilder with rubric
    prompt_builder = PromptBuilder(rubric=rubric, language="indonesian")
    
    # Load data
    excel_path = project_root / "data" / "Jawaban" / "jawaban UTS  Capstone Project.xlsx"
    df = load_student_data(excel_path)
    
    # Extract questions
    questions = extract_questions(df)
    
    print(f"\n[OK] Loaded {len(df)} students, {len(questions)} questions each")
    print(f"[OK] Total tasks per trial: {len(df) * len(questions)}")
    
    # Define missing experiments
    experiments = []
    
    # Gemini zero-shot trials 09-10 (2 more needed)
    for trial in range(9, 11):
        experiments.append(('gemini', 'zero-shot', trial))
    
    # Gemini few-shot trials 02-10 (9 more needed)
    for trial in range(2, 11):
        experiments.append(('gemini', 'few-shot', trial))
    
    print(f"\n[OK] Missing experiments to run: {len(experiments)}")
    print("\nExperiments:")
    for model, strategy, trial in experiments:
        print(f"  - {model} {strategy} trial {trial:02d}")
    
    # Initialize agent
    gemini_agent = GeminiAgent()
    
    # Run experiments
    start_time = time.time()
    completed = 0
    failed = 0
    
    for idx, (model, strategy, trial) in enumerate(experiments, 1):
        print(f"\n{'='*80}")
        print(f"PROGRESS: {idx}/{len(experiments)}")
        print(f"{'='*80}")
        
        try:
            exp_id = run_trial(model, strategy, trial, db, rubric, df, questions, gemini_agent)
            completed += 1
            
        except KeyboardInterrupt:
            print("\n\n[INTERRUPTED] Process interrupted by user.")
            print("[INFO] Progress saved to database.")
            print("[INFO] Run this script again to resume from checkpoint.")
            break
            
        except Exception as e:
            print(f"\n[ERROR] Failed to run {model} {strategy} trial {trial}: {e}")
            import traceback
            traceback.print_exc()
            print(f"[INFO] Progress saved. You can resume by running this script again.")
            failed += 1
            continue
        
        # Status update
        elapsed = time.time() - start_time
        avg_time = elapsed / idx
        remaining = (len(experiments) - idx) * avg_time
        
        print(f"\n[STATUS] Completed: {completed}/{len(experiments)}")
        print(f"[STATUS] Failed: {failed}")
        print(f"[STATUS] Elapsed: {elapsed/60:.1f} min")
        print(f"[STATUS] Estimated remaining: {remaining/60:.1f} min")
    
    # Final summary
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"\n  Total experiments: {len(experiments)}")
    print(f"  Completed: {completed}")
    print(f"  Failed: {failed}")
    print(f"  Total time: {total_time/60:.1f} minutes")
    
    if completed > 0:
        print(f"  Average per experiment: {total_time/completed:.1f} seconds")
    
    print("\n" + "="*80)
    print("[COMPLETE] MISSING TRIALS COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("  1. Verify all experiments have 10 trials")
    print("  2. Re-run reliability analysis (RQ2)")
    print("  3. Update final reports")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
