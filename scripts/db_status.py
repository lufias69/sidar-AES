"""
Monitor database status and progress for experiments.

Usage:
    python scripts/db_status.py                           # Show all experiments
    python scripts/db_status.py --experiment exp_01       # Show specific experiment
    python scripts/db_status.py --experiment exp_01 --failed  # Show failed tasks
    python scripts/db_status.py --experiment exp_01 --reset-failed  # Reset failed tasks to pending
"""

import sys
import argparse
from pathlib import Path
from tabulate import tabulate

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db_manager import DatabaseManager


def show_all_experiments(db: DatabaseManager):
    """Show summary of all experiments."""
    import sqlite3
    
    conn = db._get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT experiment_id
        FROM grading_results
        ORDER BY experiment_id
    """)
    
    experiments = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not experiments:
        print("No experiments found in database.")
        return
    
    print("=" * 80)
    print("ALL EXPERIMENTS")
    print("=" * 80)
    print()
    
    table_data = []
    for exp_id in experiments:
        stats = db.get_statistics(exp_id)
        table_data.append([
            exp_id,
            stats['completed'],
            stats['total_tasks'],
            f"{stats['progress_percentage']:.1f}%",
            stats['failed'],
            stats['pending'],
            f"{stats['total_tokens_used']:,}"
        ])
    
    headers = ['Experiment', 'Completed', 'Total', 'Progress', 'Failed', 'Pending', 'Tokens']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    print()


def show_experiment_details(db: DatabaseManager, experiment_id: str):
    """Show detailed statistics for an experiment."""
    stats = db.get_statistics(experiment_id)
    
    if stats['total_tasks'] == 0:
        print(f"Experiment '{experiment_id}' not found.")
        return
    
    print("=" * 80)
    print(f"EXPERIMENT: {experiment_id}")
    print("=" * 80)
    print()
    
    # Overall stats
    print("Overall Progress:")
    print(f"  Total tasks:     {stats['total_tasks']}")
    print(f"  Completed:       {stats['completed']} ({stats['progress_percentage']:.1f}%)")
    print(f"  Failed:          {stats['failed']}")
    print(f"  Processing:      {stats['processing']}")
    print(f"  Pending:         {stats['pending']}")
    print()
    
    # Performance stats
    print("Performance:")
    print(f"  Avg tokens/task: {stats['avg_tokens_per_task']:.0f}")
    print(f"  Total tokens:    {stats['total_tokens_used']:,}")
    print(f"  Avg time/task:   {stats['avg_time_per_task']:.2f}s")
    print()
    
    # Per trial stats
    if stats['trials']:
        print("Progress by Trial:")
        trial_data = []
        for trial_info in stats['trials']:
            trial_data.append([
                f"Trial {trial_info['trial']}",
                trial_info['completed'],
                trial_info['total'],
                f"{trial_info['percentage']:.1f}%"
            ])
        
        headers = ['Trial', 'Completed', 'Total', 'Progress']
        print(tabulate(trial_data, headers=headers, tablefmt='grid'))
        print()


def show_failed_tasks(db: DatabaseManager, experiment_id: str):
    """Show all failed tasks with error messages."""
    failed = db.get_failed_tasks(experiment_id)
    
    if not failed:
        print(f"No failed tasks for experiment '{experiment_id}'")
        return
    
    print("=" * 80)
    print(f"FAILED TASKS: {experiment_id}")
    print("=" * 80)
    print()
    
    for task in failed:
        print(f"Trial {task['trial_number']} | {task['student_id']} | Q{task['question_number']}")
        print(f"  Student: {task['student_name']}")
        print(f"  Error: {task['error_message']}")
        print(f"  Timestamp: {task['timestamp']}")
        print()


def reset_failed_tasks(db: DatabaseManager, experiment_id: str):
    """Reset failed tasks to pending for retry."""
    count = db.reset_failed_tasks(experiment_id)
    
    if count > 0:
        print(f"✓ Reset {count} failed tasks to pending status")
        print(f"  Run experiment with --resume to retry")
    else:
        print(f"No failed tasks found for experiment '{experiment_id}'")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor database status and experiment progress"
    )
    parser.add_argument(
        '--experiment',
        type=str,
        help='Specific experiment ID to show details'
    )
    parser.add_argument(
        '--failed',
        action='store_true',
        help='Show failed tasks with error messages'
    )
    parser.add_argument(
        '--reset-failed',
        action='store_true',
        help='Reset failed tasks to pending for retry'
    )
    
    args = parser.parse_args()
    
    db = DatabaseManager()
    
    if args.experiment:
        if args.reset_failed:
            reset_failed_tasks(db, args.experiment)
        elif args.failed:
            show_failed_tasks(db, args.experiment)
        else:
            show_experiment_details(db, args.experiment)
    else:
        show_all_experiments(db)


if __name__ == "__main__":
    main()
