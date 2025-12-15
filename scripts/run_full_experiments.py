"""
Run Full Experiments - ChatGPT + Gemini
24 experiments total untuk inter-rater reliability dan model comparison

Rencana:
- 10 trials lenient ChatGPT (untuk consistency analysis)
- 2 baseline ChatGPT (zero-shot, few-shot untuk comparison)
- 10 trials lenient Gemini (untuk consistency analysis)
- 2 baseline Gemini (zero-shot, few-shot untuk comparison)

Total: 24 experiments × 70 tasks = 1,680 tasks
Cost: ~$7.20 (ChatGPT $6.99 + Gemini $0.21)
Time: ~3-3.5 hours
"""

import subprocess
import sys
import time
import sqlite3
from pathlib import Path

# ============================================================================
# EXPERIMENT CONFIGURATIONS
# ============================================================================

EXPERIMENTS = [
    # ========== CHATGPT EXPERIMENTS (12 total) ==========
    
    # 10 lenient trials untuk inter-rater reliability
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
    
    # 2 baseline untuk strategy comparison
    {"id": "exp_chatgpt_zero", "strategy": "zero-shot", "model": "chatgpt", "trials": 1},
    {"id": "exp_chatgpt_few", "strategy": "few-shot", "model": "chatgpt", "trials": 1},
    
    # ========== GEMINI EXPERIMENTS (12 total) ==========
    
    # 10 lenient trials untuk inter-rater reliability
    {"id": "exp_gemini_lenient_01", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_02", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_03", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_04", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_05", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_06", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_07", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_08", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_09", "strategy": "lenient", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_lenient_10", "strategy": "lenient", "model": "gemini", "trials": 1},
    
    # 2 baseline untuk strategy comparison
    {"id": "exp_gemini_zero", "strategy": "zero-shot", "model": "gemini", "trials": 1},
    {"id": "exp_gemini_few", "strategy": "few-shot", "model": "gemini", "trials": 1},
]


def is_experiment_complete(experiment_id):
    """Check if an experiment is already 100% complete in the database"""
    try:
        conn = sqlite3.connect('results/grading_results.db')
        cur = conn.cursor()
        
        # Count completed and failed tasks
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
            FROM grading_results 
            WHERE experiment_id = ?
        """, (experiment_id,))
        
        row = cur.fetchone()
        conn.close()
        
        if row and row[0] > 0:  # Has tasks
            total, completed, failed = row
            # Consider complete if we have 70 completed tasks (or 60+ if some failed)
            if completed >= 70:
                return True, completed, failed
            elif completed >= 60 and total >= 70:  # Partial but substantial
                return "partial", completed, failed
        
        return False, 0, 0
        
    except Exception as e:
        return False, 0, 0


def run_experiment(exp_config):
    """Run a single experiment"""
    # Check if already complete
    status, completed, failed = is_experiment_complete(exp_config["id"])
    
    if status == True:
        print(f"\n[SKIP] {exp_config['id']} already complete ({completed} tasks)")
        return "skipped"
    elif status == "partial":
        print(f"\n[PARTIAL] {exp_config['id']} has {completed} completed, {failed} failed - skipping")
        return "skipped"
    
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--experiment_id", exp_config["id"],
        "--strategy", exp_config["strategy"],
        "--model", exp_config["model"],
        "--trials", str(exp_config["trials"])
    ]
    
    model_name = "ChatGPT" if exp_config["model"] == "chatgpt" else "Gemini"
    print(f"\n{'='*70}")
    print(f"Running: {exp_config['id']}")
    print(f"Model: {model_name} | Strategy: {exp_config['strategy']}")
    print(f"{'='*70}\n")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=False)
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"\n[SUCCESS] {exp_config['id']} completed in {elapsed:.1f}s ({elapsed/60:.1f} min)")
        return True
    else:
        print(f"\n[FAILED] {exp_config['id']} failed with code {result.returncode}")
        return False


def main():
    print(f"\n{'='*70}")
    print("FULL EXPERIMENTS RUNNER - ChatGPT + Gemini")
    print(f"{'='*70}")
    print(f"\nEXPERIMENT PLAN:")
    print(f"  ChatGPT:")
    print(f"    - 10 lenient trials (consistency analysis)")
    print(f"    - 2 baseline (zero-shot, few-shot)")
    print(f"  Gemini:")
    print(f"    - 10 lenient trials (consistency analysis)")
    print(f"    - 2 baseline (zero-shot, few-shot)")
    print(f"\nTOTALS:")
    print(f"  Experiments: {len(EXPERIMENTS)}")
    print(f"  Tasks: {len(EXPERIMENTS) * 70} (10 students × 7 questions × 24 experiments)")
    print(f"  Estimated cost: $7.20")
    print(f"  Estimated time: ~3-3.5 hours")
    print(f"\nANALYSIS YANG BISA DILAKUKAN:")
    print(f"  1. Inter-rater reliability (10 lenient trials per model)")
    print(f"  2. Strategy comparison (lenient vs zero-shot vs few-shot)")
    print(f"  3. Model comparison (ChatGPT vs Gemini)")
    print(f"  4. Alignment with gold standard (dosen grades)")
    print(f"{'='*70}\n")
    
    input("Press ENTER to start (or Ctrl+C to cancel)...")
    
    overall_start = time.time()
    successful = 0
    failed = 0
    skipped = 0
    
    # Group experiments by model for better organization
    chatgpt_exps = [e for e in EXPERIMENTS if e["model"] == "chatgpt"]
    gemini_exps = [e for e in EXPERIMENTS if e["model"] == "gemini"]
    
    # Run ChatGPT experiments first
    print(f"\n{'#'*70}")
    print(f"# PHASE 1: ChatGPT Experiments ({len(chatgpt_exps)} total)")
    print(f"{'#'*70}\n")
    
    for i, exp in enumerate(chatgpt_exps, 1):
        print(f"\n### ChatGPT Experiment {i}/{len(chatgpt_exps)} ###")
        
        result = run_experiment(exp)
        if result == "skipped":
            skipped += 1
        elif result:
            successful += 1
        else:
            failed += 1
            response = input(f"\nExperiment failed. Continue? (y/n): ")
            if response.lower() != 'y':
                print("\nStopped by user.")
                break
    
    # Run Gemini experiments
    print(f"\n{'#'*70}")
    print(f"# PHASE 2: Gemini Experiments ({len(gemini_exps)} total)")
    print(f"{'#'*70}\n")
    
    for i, exp in enumerate(gemini_exps, 1):
        print(f"\n### Gemini Experiment {i}/{len(gemini_exps)} ###")
        
        result = run_experiment(exp)
        if result == "skipped":
            skipped += 1
        elif result:
            successful += 1
        else:
            failed += 1
            response = input(f"\nExperiment failed. Continue? (y/n): ")
            if response.lower() != 'y':
                print("\nStopped by user.")
                break
    
    # Final summary
    total_time = time.time() - overall_start
    print(f"\n\n{'='*70}")
    print("BATCH COMPLETED")
    print(f"{'='*70}")
    print(f"Successful: {successful}/{len(EXPERIMENTS)}")
    print(f"Skipped (already complete): {skipped}/{len(EXPERIMENTS)}")
    print(f"Failed: {failed}/{len(EXPERIMENTS)}")
    print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"{'='*70}\n")
    
    # Next steps
    if successful > 0:
        print("NEXT STEPS:")
        print("1. Check results: python scripts/db_status.py")
        print("2. Consistency analysis: python scripts/analyze_consistency.py --pattern 'exp_chatgpt_lenient_*'")
        print("3. Strategy comparison: python scripts/compare_strategies.py exp_chatgpt_lenient_01 exp_chatgpt_zero exp_chatgpt_few")
        print("4. Model comparison: python scripts/compare_strategies.py exp_chatgpt_lenient_01 exp_gemini_lenient_01")
        print()


if __name__ == "__main__":
    main()
