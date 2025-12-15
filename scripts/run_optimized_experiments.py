"""
Run optimized experiment set: 10 lenient + 1 zero-shot + 1 few-shot
Total: 840 tasks, ~$8.74, ~1.6 hours
"""
import subprocess
import sys
import time
from datetime import datetime

# Experiment configuration
EXPERIMENTS = [
    # ChatGPT experiments
    # 10 trials dengan lenient strategy (fokus utama)
    *[{"id": f"exp_chatgpt_lenient_{i:02d}", "strategy": "lenient", "model": "chatgpt", "trials": 1} 
      for i in range(1, 11)],
    
    # 1 trial zero-shot (baseline comparison)
    {"id": "exp_chatgpt_zero", "strategy": "zero-shot", "model": "chatgpt", "trials": 1},
    
    # 1 trial few-shot (alternative comparison)
    {"id": "exp_chatgpt_few", "strategy": "few-shot", "model": "chatgpt", "trials": 1},
    
    # Gemini experiments (for model comparison)
    # 10 trials dengan lenient strategy
    *[{"id": f"exp_gemini_lenient_{i:02d}", "strategy": "lenient", "model": "gemini", "trials": 1} 
      for i in range(1, 11)],
    
    # 1 trial zero-shot
    {"id": "exp_gemini_zero", "strategy": "zero-shot", "model": "gemini", "trials": 1},
    
    # 1 trial few-shot
    {"id": "exp_gemini_few", "strategy": "few-shot", "model": "gemini", "trials": 1},
]

def run_experiment(exp_config):
    """Run a single experiment."""
    exp_id = exp_config['id']
    strategy = exp_config['strategy']
    model = exp_config['model']
    trials = exp_config['trials']
    
    print(f"\n{'='*80}")
    print(f"Starting: {exp_id}")
    print(f"Strategy: {strategy}, Model: {model}, Trials: {trials}")
    print(f"{'='*80}\n")
    
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--experiment_id", exp_id,
        "--strategy", strategy,
        "--model", model,
        "--trials", str(trials)
    ]
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,
            text=True
        )
        
        elapsed = time.time() - start_time
        print(f"\n✅ {exp_id} completed in {elapsed/60:.1f} minutes")
        return True, elapsed
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {exp_id} failed with error code {e.returncode}")
        return False, 0
    except KeyboardInterrupt:
        print(f"\n⚠️  Interrupted by user")
        raise

def main():
    print("\n" + "="*80)
    print("OPTIMIZED EXPERIMENT RUN - CHATGPT + GEMINI")
    print("="*80)
    print(f"\nTotal experiments: {len(EXPERIMENTS)}")
    print(f"Total tasks: {len(EXPERIMENTS) * 70}")
    print(f"Estimated cost: ~$9.09 (ChatGPT: $6.99, Gemini: $2.10)")
    print(f"Estimated time: ~3.2 hours")
    print(f"\nConfiguration:")
    print(f"  ChatGPT:")
    print(f"    - 10 Lenient trials")
    print(f"    - 1 Zero-shot baseline")
    print(f"    - 1 Few-shot baseline")
    print(f"  Gemini:")
    print(f"    - 10 Lenient trials")
    print(f"    - 1 Zero-shot baseline")
    print(f"    - 1 Few-shot baseline")
    print(f"\nStart time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Confirmation
    response = input("\nProceed with execution? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Execution cancelled.")
        return
    
    total_start = time.time()
    completed = 0
    failed = 0
    total_time = 0
    
    for i, exp in enumerate(EXPERIMENTS, 1):
        print(f"\n{'='*80}")
        print(f"Progress: {i}/{len(EXPERIMENTS)} experiments")
        print(f"{'='*80}")
        
        success, elapsed = run_experiment(exp)
        
        if success:
            completed += 1
            total_time += elapsed
        else:
            failed += 1
            
        # Progress summary
        remaining = len(EXPERIMENTS) - i
        if completed > 0:
            avg_time = total_time / completed
            est_remaining = (avg_time * remaining) / 60
            print(f"\nProgress: {completed} completed, {failed} failed, {remaining} remaining")
            print(f"Estimated time remaining: {est_remaining:.1f} minutes")
    
    # Final summary
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*80)
    print("EXECUTION COMPLETE")
    print("="*80)
    print(f"\nCompleted: {completed}/{len(EXPERIMENTS)}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_elapsed/3600:.2f} hours")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed > 0:
        print(f"\n⚠️  {failed} experiments failed. Check logs for details.")
    else:
        print(f"\n✅ All experiments completed successfully!")
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. View progress:")
    print("   python scripts/db_status.py")
    
    print("\n2. Compare lenient trials (consistency analysis):")
    print("   # ChatGPT consistency")
    print("   python scripts/analyze_consistency.py --pattern \"exp_chatgpt_lenient_*\"")
    print("   # Gemini consistency")
    print("   python scripts/analyze_consistency.py --pattern \"exp_gemini_lenient_*\"")
    
    print("\n3. Compare strategies (lenient vs baselines):")
    print("   # ChatGPT strategies")
    print("   python scripts/compare_strategies.py exp_chatgpt_lenient_01 exp_chatgpt_zero exp_chatgpt_few")
    print("   # Gemini strategies")
    print("   python scripts/compare_strategies.py exp_gemini_lenient_01 exp_gemini_zero exp_gemini_few")
    
    print("\n4. Compare models (ChatGPT vs Gemini):")
    print("   python scripts/compare_strategies.py exp_chatgpt_lenient_01 exp_gemini_lenient_01")
    
    print("\n5. Full calibration analysis:")
    print("   python scripts/analyze_calibration.py --experiment exp_chatgpt_lenient_01")
    print("   python scripts/analyze_calibration.py --experiment exp_gemini_lenient_01")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        print("Progress is saved in database. You can resume anytime.")
        sys.exit(1)
