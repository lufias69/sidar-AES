"""
Run a single experiment with checkpoint/resume support using SQLite database.

This script runs one experiment configuration with multiple trials,
storing results in database for crash recovery and progress tracking.
"""

import sys
import os
from pathlib import Path
import argparse
import pandas as pd
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import DatabaseManager
from src.core.prompt_builder import PromptBuilder
from src.core.rubric import RubricManager
from src.agents.chatgpt_agent import ChatGPTAgent
from src.agents.gemini_agent import GeminiAgent


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
    selected_file = "selected_students.txt"
    if os.path.exists(selected_file):
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


def create_grader(model_name, strategy_name, rubric):
    """Create appropriate grader instance."""
    if model_name == 'chatgpt':
        return ChatGPTAgent(
            rubric=rubric,
            strategy=strategy_name
        )
    elif model_name == 'gemini':
        return GeminiAgent(
            rubric=rubric,
            strategy=strategy_name
        )
    else:
        raise ValueError(f"Unknown model: {model_name}")


def grade_task(grader, prompt_builder, student, question, strategy_name, rubric):
    """Grade a single task and return results with metadata."""
    try:
        # Call agent's grade_essay method
        start_time = time.time()
        result = grader.grade_essay(
            student_id=student['id'],
            question_id=str(question['number']),
            question=question['text'],
            answer=student['answer'],
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


def run_experiment(experiment_id, strategy, model, trials, excel_path, db_path):
    """
    Run experiment with checkpoint/resume support.
    
    Args:
        experiment_id: Unique identifier for this experiment
        strategy: Prompting strategy to use
        model: Model to use ('chatgpt' or 'gemini')
        trials: Number of independent trials
        excel_path: Path to student data Excel file
        db_path: Path to SQLite database
    """
    print(f"\n{'='*60}")
    print(f"Experiment: {experiment_id}")
    print(f"Strategy: {strategy}")
    print(f"Model: {model}")
    print(f"Trials: {trials}")
    print(f"{'='*60}\n")
    
    # Initialize components
    db_manager = DatabaseManager(db_path)
    rubric_manager = RubricManager()
    rubric = rubric_manager.get_rubric("default")  # Get actual Rubric object
    prompt_builder = PromptBuilder(rubric)
    
    # Load data
    df = load_student_data(excel_path)
    questions = extract_questions(df)
    
    # Create grader
    grader = create_grader(model, strategy, rubric)
    
    # Calculate total tasks
    total_tasks = len(df) * len(questions) * trials
    completed_tasks = 0
    
    print(f"\n[OK] Total tasks to process: {total_tasks}")
    print(f"    - Students: {len(df)}")
    print(f"    - Questions: {len(questions)}")
    print(f"    - Trials: {trials}")
    
    # Process each trial
    for trial in range(1, trials + 1):
        print(f"\n{'='*60}")
        print(f"TRIAL {trial}/{trials}")
        print(f"{'='*60}")
        
        trial_start = time.time()
        trial_completed = 0
        trial_skipped = 0
        
        # Process each student
        for idx, row in df.iterrows():
            # Use row name (Mahasiswa X) as student_id since NIM column doesn't exist
            student_name = row['Nama']
            student_id = f"student_{student_name.replace('Mahasiswa ', '').zfill(2)}"
            
            # Process each question
            for question in questions:
                # Check if already completed
                if db_manager.check_exists(
                    experiment_id, trial, student_id, question['number']
                ):
                    trial_skipped += 1
                    completed_tasks += 1
                    continue
                
                # Prepare student data
                student_data = {
                    'id': student_id,
                    'name': student_name,
                    'answer': row[question['column']]
                }
                
                # Insert pending task
                db_manager.insert_or_update(
                    experiment_id=experiment_id,
                    trial_number=trial,
                    student_id=student_id,
                    student_name=student_name,
                    question_number=question['number'],
                    question_text=question['text'],
                    answer_text=student_data['answer'],
                    model=model,
                    strategy=strategy,
                    status='pending'
                )
                
                # Mark as processing
                db_manager.insert_or_update(
                    experiment_id=experiment_id,
                    trial_number=trial,
                    student_id=student_id,
                    student_name=student_name,
                    question_number=question['number'],
                    question_text=question['text'],
                    answer_text=student_data['answer'],
                    model=model,
                    strategy=strategy,
                    status='processing'
                )
                
                # Grade the task
                result = grade_task(
                    grader, prompt_builder, student_data, question, strategy, rubric
                )
                
                # Update database
                if result['success']:
                    db_manager.insert_or_update(
                        experiment_id=experiment_id,
                        trial_number=trial,
                        student_id=student_id,
                        student_name=student_name,
                        question_number=question['number'],
                        question_text=question['text'],
                        answer_text=student_data['answer'],
                        model=model,
                        strategy=strategy,
                        grades=result['grades'],
                        weighted_score=result['weighted_score'],
                        justification=result['justification'],
                        overall_comment=result['overall_comment'],
                        tokens_used=result['tokens'],
                        api_call_time=result['time'],
                        status='completed'
                    )
                    trial_completed += 1
                    completed_tasks += 1
                    
                    # Progress indicator
                    progress = (completed_tasks / total_tasks) * 100
                    print(f"[{progress:5.1f}%] Trial {trial}, Student {student_name}, Q{question['number']}: {result['weighted_score']:.1f} ({result['tokens']} tokens, {result['time']:.1f}s)")
                else:
                    db_manager.insert_or_update(
                        experiment_id=experiment_id,
                        trial_number=trial,
                        student_id=student_id,
                        student_name=student_name,
                        question_number=question['number'],
                        question_text=question['text'],
                        answer_text=student_data['answer'],
                        model=model,
                        strategy=strategy,
                        status='failed',
                        error_message=result['error']
                    )
                    print(f"[ERROR] Trial {trial}, Student {student_name}, Q{question['number']}: {result['error']}")
        
        # Trial summary
        trial_time = time.time() - trial_start
        print(f"\n[OK] Trial {trial} completed:")
        print(f"    - New tasks: {trial_completed}")
        print(f"    - Skipped (already done): {trial_skipped}")
        print(f"    - Time: {trial_time:.1f}s ({trial_time/60:.1f} min)")
    
    # Experiment summary
    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETED: {experiment_id}")
    print(f"{'='*60}")
    print(f"Total tasks processed: {completed_tasks}/{total_tasks}")
    
    # Export to JSON for each trial
    from pathlib import Path
    export_dir = Path(f"results/{experiment_id}")
    for trial_num in range(1, trials + 1):
        db_manager.export_to_json(experiment_id, trial_num, export_dir)
    print(f"[OK] Results exported to: {export_dir}")


def main():
    parser = argparse.ArgumentParser(description='Run grading experiment with checkpoint support')
    parser.add_argument('--experiment_id', required=True, help='Unique experiment identifier')
    parser.add_argument('--strategy', required=True, 
                       choices=['zero-shot', 'few-shot', 'cot', 'lenient', 'detailed-rubric', 'strict'],
                       help='Prompting strategy')
    parser.add_argument('--model', required=True, 
                       choices=['chatgpt', 'gemini'],
                       help='Model to use')
    parser.add_argument('--trials', type=int, default=1,
                       help='Number of independent trials (default: 1)')
    parser.add_argument('--excel', default='data/Jawaban/jawaban UTS  Capstone Project.xlsx',
                       help='Path to Excel file with student data')
    parser.add_argument('--db', default='results/grading_results.db',
                       help='Path to SQLite database')
    
    args = parser.parse_args()
    
    # Create results directory if needed
    os.makedirs('results', exist_ok=True)
    
    # Run experiment
    run_experiment(
        experiment_id=args.experiment_id,
        strategy=args.strategy,
        model=args.model,
        trials=args.trials,
        excel_path=args.excel,
        db_path=args.db
    )


if __name__ == '__main__':
    main()
