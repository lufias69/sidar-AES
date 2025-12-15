"""
Run additional trials for zero-shot and few-shot strategies to balance dataset.

This script runs 9 additional trials (02-10) for:
- ChatGPT zero-shot
- ChatGPT few-shot
- Gemini zero-shot
- Gemini few-shot

Total: 36 experiments (9 trials × 4 combinations)
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
    print(f"EXPERIMENT: {exp_id}")
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
                    # Mark as failed
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
                        status='failed',
                        error_message=result.get('error', 'Unknown error')
                    )
                    print(f"  [ERROR] Question {question['number']}: {result.get('error', 'Failed')}")
                    failed_tasks += 1
                
            except Exception as e:
                # Mark as failed
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
                    status='failed',
                    error_message=str(e)
                )
                print(f"  [ERROR] Question {question['number']}: {e}")
                failed_tasks += 1
        
        # Small delay between students
        time.sleep(1)
        
        # Progress update
        progress_pct = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        print(f"  [PROGRESS] {completed_tasks}/{total_tasks} tasks ({progress_pct:.1f}%)")
    
    # Final summary for this experiment
    print(f"\n{'─'*80}")
    print(f"EXPERIMENT {exp_id} SUMMARY:")
    print(f"  Completed tasks: {completed_tasks}/{total_tasks}")
    print(f"  Failed tasks: {failed_tasks}")
    print(f"  Skipped tasks: {skipped_tasks}")
    print(f"{'─'*80}")
    
    return exp_id


def main():
    """Main execution"""
    
    print("\n" + "="*80)
    print("RUNNING ADDITIONAL TRIALS FOR ZERO-SHOT AND FEW-SHOT")
    print("="*80)
    print("\nThis will run 36 experiments:")
    print("  - ChatGPT zero-shot: 9 trials (02-10)")
    print("  - ChatGPT few-shot: 9 trials (02-10)")
    print("  - Gemini zero-shot: 9 trials (02-10)")
    print("  - Gemini few-shot: 9 trials (02-10)")
    print("\nFeatures:")
    print("  [OK] Results saved to database (grading_results.db)")
    print("  [OK] Checkpoint/Resume support (can continue if interrupted)")
    print("  [OK] Progress tracking per task")
    print("\nEstimated time: 2-3 hours")
    print("="*80)
    print("\nStarting automatically...")
    
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
    print(f"[OK] Total tasks per trial: {len(df) * len(questions)}")
    
    # Define experiments to run
    experiments = []
    
    # ChatGPT zero-shot trials 02-10
    for trial in range(2, 11):
        experiments.append(('chatgpt', 'zero-shot', trial))
    
    # ChatGPT few-shot trials 02-10
    for trial in range(2, 11):
        experiments.append(('chatgpt', 'few-shot', trial))
    
    # Gemini zero-shot trials 02-10
    for trial in range(2, 11):
        experiments.append(('gemini', 'zero-shot', trial))
    
    # Gemini few-shot trials 02-10
    for trial in range(2, 11):
        experiments.append(('gemini', 'few-shot', trial))
    
    print(f"\n[OK] Total experiments to run: {len(experiments)}")
    
    # Initialize agents
    chatgpt_agent = ChatGPTAgent()
    gemini_agent = GeminiAgent()
    
    # Run experiments
    start_time = time.time()
    completed = 0
    failed = 0
    resumed = 0
    
    for idx, (model, strategy, trial) in enumerate(experiments, 1):
        print(f"\n{'='*80}")
        print(f"PROGRESS: {idx}/{len(experiments)}")
        print(f"{'='*80}")
        
        try:
            # Select appropriate agent
            if model == 'chatgpt':
                agent = chatgpt_agent
            else:  # gemini
                agent = gemini_agent
            
            exp_id = run_trial(model, strategy, trial, db, rubric, df, questions, agent)
            
            completed += 1
            
        except KeyboardInterrupt:
            print("\n\n[INTERRUPTED] Process interrupted by user.")
            print("[INFO] Progress saved to database.")
            print("[INFO] Run this script again to resume from checkpoint.")
            break
            
        except Exception as e:
            print(f"\n[ERROR] Failed to run {model} {strategy} trial {trial}: {e}")
            print(f"[INFO] Progress saved. You can resume by running this script again.")
            failed += 1
            continue
        
        # Status update
        elapsed = time.time() - start_time
        avg_time = elapsed / idx
        remaining = (len(experiments) - idx) * avg_time
        
        print(f"\n[STATUS] Completed: {completed}/{len(experiments)}")
        print(f"[STATUS] Failed: {failed}")
        print(f"[STATUS] Resumed: {resumed}")
        print(f"[STATUS] Elapsed: {elapsed/60:.1f} min")
        print(f"[STATUS] Estimated remaining: {remaining/60:.1f} min")
    
    # Final summary
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"\n  Total experiments: {len(experiments)}")
    print(f"  Completed: {completed}")
    print(f"  Resumed from checkpoint: {resumed}")
    print(f"  Failed: {failed}")
    print(f"  Total time: {total_time/60:.1f} minutes")
    
    if completed > 0:
        print(f"  Average per experiment: {total_time/completed:.1f} seconds")
    
    print("\n" + "="*80)
    print("[COMPLETE] ALL ADDITIONAL TRIALS COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("  1. python scripts/extract_analysis_data.py")
    print("  2. Re-run all RQ analyses (RQ1-RQ5)")
    print("  3. Generate comprehensive report")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
