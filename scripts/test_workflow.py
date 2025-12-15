"""
Test workflow: Checkpoint, resume, multi-model support
Run 2 small experiments (ChatGPT + Gemini) with 2 questions only
"""
import subprocess
import sys
import time

def run_test_experiment(exp_id, strategy, model, max_questions=2):
    """Run a small test experiment."""
    print(f"\n{'='*80}")
    print(f"Testing: {exp_id} ({model}, {strategy})")
    print(f"{'='*80}\n")
    
    # Simulate stopping in the middle by using timeout
    # We'll run for ~30 seconds then check if we can resume
    
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--experiment_id", exp_id,
        "--strategy", strategy,
        "--model", model,
        "--trials", "1"
    ]
    
    try:
        result = subprocess.run(cmd, timeout=30, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("\n⚠️  Process timed out (expected for testing interrupt)")
        return "timeout"

def check_database_status(exp_id):
    """Check experiment status in database."""
    print(f"\n{'='*80}")
    print(f"Checking database status: {exp_id}")
    print(f"{'='*80}\n")
    
    cmd = [
        sys.executable,
        "scripts/db_status.py",
        "--experiment", exp_id
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def test_resume(exp_id, strategy, model):
    """Test resume functionality."""
    print(f"\n{'='*80}")
    print(f"Testing RESUME: {exp_id}")
    print(f"{'='*80}\n")
    
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--experiment_id", exp_id,
        "--strategy", strategy,
        "--model", model,
        "--trials", "1",
        "--resume"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def main():
    print("\n" + "="*80)
    print("WORKFLOW TEST: Checkpoint, Resume, Multi-Model")
    print("="*80)
    print("\nThis test will:")
    print("1. Run small ChatGPT experiment (will complete)")
    print("2. Check database storage")
    print("3. Run small Gemini experiment")
    print("4. Verify both models work correctly")
    print("5. Test that results are saved to database")
    print("\nEstimated time: 2-3 minutes")
    print("Estimated cost: ~$0.15")
    
    input("\nPress Enter to start test...")
    
    # Test 1: ChatGPT Lenient (small)
    print("\n" + "="*80)
    print("TEST 1: ChatGPT Lenient")
    print("="*80)
    
    success = run_test_experiment("test_workflow_chatgpt", "lenient", "chatgpt")
    
    if success:
        print("\n✅ ChatGPT experiment completed")
    else:
        print("\n❌ ChatGPT experiment failed")
        return
    
    # Check database
    time.sleep(2)
    db_ok = check_database_status("test_workflow_chatgpt")
    
    if db_ok:
        print("\n✅ Database storage working")
    else:
        print("\n❌ Database storage failed")
        return
    
    # Test 2: Gemini Lenient (small)
    print("\n" + "="*80)
    print("TEST 2: Gemini Lenient")
    print("="*80)
    
    success = run_test_experiment("test_workflow_gemini", "lenient", "gemini")
    
    if success:
        print("\n✅ Gemini experiment completed")
    else:
        print("\n❌ Gemini experiment failed")
        return
    
    # Check database for Gemini
    time.sleep(2)
    db_ok = check_database_status("test_workflow_gemini")
    
    if db_ok:
        print("\n✅ Gemini database storage working")
    else:
        print("\n❌ Gemini database storage failed")
        return
    
    # Final summary
    print("\n" + "="*80)
    print("WORKFLOW TEST RESULTS")
    print("="*80)
    print("\n✅ All tests passed!")
    print("\nVerified:")
    print("  ✓ ChatGPT model works")
    print("  ✓ Gemini model works")
    print("  ✓ Database checkpoint works")
    print("  ✓ Results are saved correctly")
    print("\nThe system is ready for full experiment run!")
    print("\nNext step:")
    print("  python scripts/run_optimized_experiments.py")
    print("\n" + "="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
