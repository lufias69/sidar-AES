"""
Run all 10 experiments with checkpoint/resume support.

This script runs a predefined set of experiments to compare different
prompting strategies and AI models.

Experiments:
  exp_01: Zero-shot + ChatGPT
  exp_02: Zero-shot + Gemini
  exp_03: Few-shot + ChatGPT
  exp_04: Few-shot + Gemini
  exp_05: Chain-of-Thought + ChatGPT
  exp_06: Chain-of-Thought + Gemini
  exp_07: Detailed Rubric + ChatGPT
  exp_08: Detailed Rubric + Gemini
  exp_09: Strict Mode + ChatGPT
  exp_10: Lenient Mode + ChatGPT

Usage:
    python scripts/run_all_experiments.py                # Run all 10 experiments
    python scripts/run_all_experiments.py --start 3      # Start from experiment 3
    python scripts/run_all_experiments.py --only 1 5 9   # Run only experiments 1, 5, 9
"""

import sys
import argparse
from pathlib import Path
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.run_experiment import run_experiment
from src.database.db_manager import DatabaseManager


# Define all experiments
EXPERIMENTS = [
    {
        'id': 'exp_01',
        'name': 'Zero-shot + ChatGPT',
        'strategy': 'zero-shot',
        'model': 'chatgpt',
        'trials': 4
    },
    {
        'id': 'exp_02',
        'name': 'Zero-shot + Gemini',
        'strategy': 'zero-shot',
        'model': 'gemini',
        'trials': 4
    },
    {
        'id': 'exp_03',
        'name': 'Few-shot + ChatGPT',
        'strategy': 'few-shot',
        'model': 'chatgpt',
        'trials': 4
    },
    {
        'id': 'exp_04',
        'name': 'Few-shot + Gemini',
        'strategy': 'few-shot',
        'model': 'gemini',
        'trials': 4
    },
    {
        'id': 'exp_05',
        'name': 'Chain-of-Thought + ChatGPT',
        'strategy': 'cot',
        'model': 'chatgpt',
        'trials': 4
    },
    {
        'id': 'exp_06',
        'name': 'Chain-of-Thought + Gemini',
        'strategy': 'cot',
        'model': 'gemini',
        'trials': 4
    },
    {
        'id': 'exp_07',
        'name': 'Detailed Rubric + ChatGPT',
        'strategy': 'detailed-rubric',
        'model': 'chatgpt',
        'trials': 4
    },
    {
        'id': 'exp_08',
        'name': 'Detailed Rubric + Gemini',
        'strategy': 'detailed-rubric',
        'model': 'gemini',
        'trials': 4
    },
    {
        'id': 'exp_09',
        'name': 'Strict Mode + ChatGPT',
        'strategy': 'strict',
        'model': 'chatgpt',
        'trials': 4
    },
    {
        'id': 'exp_10',
        'name': 'Lenient Mode + ChatGPT',
        'strategy': 'lenient',
        'model': 'chatgpt',
        'trials': 4
    },
]


def show_experiment_plan(experiments, language='indonesian'):
    """Display the experiment plan."""
    print("=" * 80)
    print("EXPERIMENT PLAN")
    print("=" * 80)
    print()
    print(f"Total experiments: {len(experiments)}")
    print(f"Per experiment: 10 students × 7 questions × 4 trials = 280 grading tasks")
    print(f"Total grading tasks: {len(experiments) × 280} = {len(experiments) * 280}")
    print()
    
    # Estimate cost and time
    chatgpt_experiments = sum(1 for e in experiments if e['model'] == 'chatgpt')
    gemini_experiments = sum(1 for e in experiments if e['model'] == 'gemini')
    
    est_cost_chatgpt = chatgpt_experiments * 280 * 0.03  # ~$0.03 per task
    est_cost_gemini = gemini_experiments * 280 * 0.005   # ~$0.005 per task
    total_cost = est_cost_chatgpt + est_cost_gemini
    
    est_time_hours = len(experiments) * 280 * 2 / 3600  # ~2s per task
    
    print(f"Estimated cost:")
    print(f"  ChatGPT ({chatgpt_experiments} experiments): ${est_cost_chatgpt:.2f}")
    print(f"  Gemini ({gemini_experiments} experiments): ${est_cost_gemini:.2f}")
    print(f"  Total: ${total_cost:.2f}")
    print()
    print(f"Estimated time: ~{est_time_hours:.1f} hours")
    print()
    
    print("Experiments to run:")
    for i, exp in enumerate(experiments, 1):
        print(f"  {i:2d}. {exp['id']}: {exp['name']}")
    print()


def run_all_experiments(
    start_from: int = 1,
    only: list = None,
    language: str = 'indonesian',
    resume: bool = True
):
    """
    Run all experiments in sequence.
    
    Args:
        start_from: Start from this experiment number (1-indexed)
        only: List of experiment numbers to run (1-indexed), or None for all
        language: Language for justifications
        resume: Whether to resume from checkpoints
    """
    # Filter experiments
    if only:
        experiments = [EXPERIMENTS[i-1] for i in only if 1 <= i <= len(EXPERIMENTS)]
        print(f"Running selected experiments: {only}")
    else:
        experiments = EXPERIMENTS[start_from-1:]
        if start_from > 1:
            print(f"Starting from experiment {start_from}")
    
    show_experiment_plan(experiments, language)
    
    # Confirm
    response = input("Proceed with experiments? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled by user")
        return
    
    print()
    print("=" * 80)
    print("STARTING EXPERIMENTS")
    print("=" * 80)
    print()
    
    start_time = time.time()
    completed = []
    failed = []
    
    for i, exp in enumerate(experiments, 1):
        print(f"\n{'='*80}")
        print(f"EXPERIMENT {i}/{len(experiments)}: {exp['name']}")
        print(f"{'='*80}\n")
        
        exp_start_time = time.time()
        
        try:
            run_experiment(
                experiment_id=exp['id'],
                strategy=exp['strategy'],
                model=exp['model'],
                trials=exp['trials'],
                language=language,
                resume=resume
            )
            
            exp_duration = time.time() - exp_start_time
            completed.append({
                'experiment': exp['name'],
                'duration': exp_duration
            })
            
            print(f"\n✓ {exp['name']} completed in {exp_duration/60:.1f} minutes")
            
        except Exception as e:
            exp_duration = time.time() - exp_start_time
            failed.append({
                'experiment': exp['name'],
                'error': str(e),
                'duration': exp_duration
            })
            
            print(f"\n❌ {exp['name']} failed after {exp_duration/60:.1f} minutes")
            print(f"Error: {e}")
            print("\nContinuing with next experiment...")
        
        # Short break between experiments
        if i < len(experiments):
            print("\nWaiting 5 seconds before next experiment...")
            time.sleep(5)
    
    # Final summary
    total_duration = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 80)
    print()
    print(f"Total time: {total_duration/3600:.2f} hours")
    print(f"Completed: {len(completed)}/{len(experiments)}")
    print(f"Failed: {len(failed)}/{len(experiments)}")
    print()
    
    if completed:
        print("✅ Completed experiments:")
        for exp in completed:
            print(f"  - {exp['experiment']} ({exp['duration']/60:.1f} min)")
        print()
    
    if failed:
        print("❌ Failed experiments:")
        for exp in failed:
            print(f"  - {exp['experiment']}: {exp['error']}")
        print()
        print("You can retry failed experiments individually using:")
        print("  python scripts/run_experiment.py --experiment_id <exp_id> --strategy <strategy> --model <model> --resume")
        print()
    
    # Show database summary
    db = DatabaseManager()
    print("Database summary:")
    for exp in experiments:
        stats = db.get_statistics(exp['id'])
        if stats['total_tasks'] > 0:
            print(f"  {exp['id']}: {stats['completed']}/{stats['total_tasks']} ({stats['progress_percentage']:.1f}%)")
    
    print()
    print("Next steps:")
    print("  1. Check database status: python scripts/db_status.py")
    print("  2. Export to JSON: python scripts/export_to_json.py --experiment <exp_id>")
    print("  3. Run analysis: python scripts/evaluate_experiments.py")


def main():
    parser = argparse.ArgumentParser(
        description="Run all experiments with checkpoint/resume support"
    )
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='Start from this experiment number (1-10)'
    )
    parser.add_argument(
        '--only',
        type=int,
        nargs='+',
        help='Run only these experiment numbers (e.g., --only 1 3 5)'
    )
    parser.add_argument(
        '--language',
        type=str,
        choices=['indonesian', 'english'],
        default='indonesian',
        help='Language for justifications (default: indonesian)'
    )
    parser.add_argument(
        '--no-resume',
        action='store_true',
        help='Do not resume from checkpoints (start fresh)'
    )
    
    args = parser.parse_args()
    
    run_all_experiments(
        start_from=args.start,
        only=args.only,
        language=args.language,
        resume=not args.no_resume
    )


if __name__ == "__main__":
    main()
