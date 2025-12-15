"""
Export experiment results from database to JSON files.

This converts SQLite database results to JSON format for compatibility
with existing analysis scripts and for manual review.

Usage:
    python scripts/export_to_json.py --experiment exp_01
    python scripts/export_to_json.py --experiment exp_01 --trial 1
    python scripts/export_to_json.py --experiment exp_01 --output results/custom_dir
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db_manager import DatabaseManager


def export_experiment(
    experiment_id: str,
    trial_number: int = None,
    output_dir: str = None
):
    """
    Export experiment results to JSON files.
    
    Args:
        experiment_id: Experiment identifier
        trial_number: Optional specific trial to export (exports all if None)
        output_dir: Custom output directory (auto-generated if None)
    """
    db = DatabaseManager()
    
    # Get experiment stats
    stats = db.get_statistics(experiment_id)
    
    if stats['total_tasks'] == 0:
        print(f"❌ Experiment '{experiment_id}' not found in database")
        return
    
    print("=" * 80)
    print(f"EXPORTING EXPERIMENT: {experiment_id}")
    print("=" * 80)
    print(f"Total tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed']} ({stats['progress_percentage']:.1f}%)")
    print()
    
    if stats['completed'] == 0:
        print("❌ No completed tasks to export")
        return
    
    # Determine trials to export
    if trial_number:
        trials = [trial_number]
        print(f"Exporting trial {trial_number}...")
    else:
        trials = [t['trial'] for t in stats['trials']]
        print(f"Exporting all trials: {len(trials)} trials...")
    
    print()
    
    # Export each trial
    for trial in trials:
        if output_dir:
            output_path = Path(output_dir) / f"trial_{trial}"
        else:
            output_path = Path(f"results/experiments/{experiment_id}/trial_{trial}")
        
        # Check if trial has any completed tasks
        completed, total, percentage = db.get_progress(experiment_id, trial)
        
        if completed == 0:
            print(f"  Trial {trial}: No completed tasks to export")
            continue
        
        # Export
        db.export_to_json(experiment_id, trial, output_path)
        print(f"  Trial {trial}: Exported {completed} results to {output_path}")
    
    print()
    print("✅ Export complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Export experiment results from database to JSON files"
    )
    parser.add_argument(
        '--experiment',
        type=str,
        required=True,
        help='Experiment ID to export'
    )
    parser.add_argument(
        '--trial',
        type=int,
        help='Specific trial number to export (optional, exports all if not specified)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Custom output directory (optional, auto-generated if not specified)'
    )
    
    args = parser.parse_args()
    
    export_experiment(
        experiment_id=args.experiment,
        trial_number=args.trial,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()
