"""
Run ChatGPT-only experiments (12 experiments)
Pragmatic approach: Run validated ChatGPT first, Gemini can follow later
"""

import subprocess
import sys
import time
from pathlib import Path

# Experiment configurations
EXPERIMENTS = [
    # 10 lenient trials (main experiments)
    {"id": "exp_chatgpt_lenient_01", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_02", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_03", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_04", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_05", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_06", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_07", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_08", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_09", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_lenient_10", "strategy": "lenient", "model": "chatgpt", "trials": 1},
    
    # Baseline comparisons
    {"id": "exp_chatgpt_zero", "strategy": "zero-shot", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_few", "strategy": "few-shot", "model": "chatgpt", "trials": 1},
]

def run_experiment(exp_config):
    """Run a single experiment"""
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--experiment_id", exp_config["id"],
        "--strategy", exp_config["strategy"],
        "--model", exp_config["model"],
        "--trials", str(exp_config["trials"])
    ]
    
    print(f"\n{'='*70}")
    print(f"Running: {exp_config['id']}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=False)
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"\n[OK] {exp_config['id']} completed in {elapsed:.1f}s ({elapsed/60:.1f} min)")
        return True
    else:
        print(f"\n[ERROR] {exp_config['id']} failed with code {result.returncode}")
        return False

def main():
    print(f"\n{'='*70}")
    print("ChatGPT-Only Experiments Runner")
    print(f"{'='*70}")
    print(f"Total experiments: {len(EXPERIMENTS)}")
    print(f"Total tasks: {len(EXPERIMENTS) * 70} (10 students × 7 questions)")
    print(f"Estimated cost: $6.99")
    print(f"Estimated time: ~2.5 hours")
    print(f"{'='*70}\n")
    
    input("Press ENTER to start (or Ctrl+C to cancel)...")
    
    start_time = time.time()
    successful = 0
    failed = 0
    
    for i, exp in enumerate(EXPERIMENTS, 1):
        print(f"\n\n### EXPERIMENT {i}/{len(EXPERIMENTS)} ###")
        
        if run_experiment(exp):
            successful += 1
        else:
            failed += 1
            response = input(f"\nExperiment failed. Continue? (y/n): ")
            if response.lower() != 'y':
                break
    
    # Summary
    total_time = time.time() - start_time
    print(f"\n\n{'='*70}")
    print("BATCH COMPLETED")
    print(f"{'='*70}")
    print(f"Successful: {successful}/{len(EXPERIMENTS)}")
    print(f"Failed: {failed}/{len(EXPERIMENTS)}")
    print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
