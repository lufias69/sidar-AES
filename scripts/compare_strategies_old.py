"""
Compare multiple experiment strategies against gold standard.
"""
import json
import sys
from pathlib import Path
from analyze_calibration import CalibrationAnalyzer

def compare_experiments(experiments: list, gold_dir: str = 'results/gold_standard'):
    """Compare multiple experiments and rank them."""
    
    print("\n" + "="*80)
    print("STRATEGY COMPARISON REPORT")
    print("="*80)
    
    results = []
    
    for exp_id in experiments:
        exp_dir = f"results/experiments/{exp_id}"
        if not Path(exp_dir).exists():
            print(f"\n⚠️  Experiment {exp_id} not found, skipping...")
            continue
        
        print(f"\nAnalyzing {exp_id}...")
        analyzer = CalibrationAnalyzer(gold_dir, exp_dir)
        analysis = analyzer.analyze_all(trial=1)
        
        if analysis['overall']['total_students'] == 0:
            print(f"  No data found for {exp_id}")
            continue
        
        overall = analysis['overall']
        results.append({
            'experiment_id': exp_id,
            'avg_score_diff': overall['avg_score_diff'],
            'avg_score_diff_abs': abs(overall['avg_score_diff']),
            'criteria_stats': overall['criteria_stats'],
            'students': analysis['overall']['total_students']
        })
    
    if not results:
        print("\nNo valid experiments found!")
        return
    
    # Rank by absolute difference (closest to gold standard)
    results.sort(key=lambda x: x['avg_score_diff_abs'])
    
    print("\n" + "="*80)
    print("RANKING (Best to Worst Alignment)")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        exp_id = result['experiment_id']
        diff = result['avg_score_diff']
        abs_diff = result['avg_score_diff_abs']
        
        if diff > 0:
            bias = "TOO HARSH"
            emoji = "🔴"
        elif diff < 0:
            bias = "TOO LENIENT"
            emoji = "🔵"
        else:
            bias = "PERFECT"
            emoji = "🟢"
        
        print(f"\n{i}. {exp_id.upper()}")
        print(f"   {emoji} Avg Difference: {diff:.3f} ({bias})")
        print(f"   Absolute Error: {abs_diff:.3f}")
        print(f"   Students: {result['students']}")
        
        # Show criteria breakdown
        print(f"   Criteria breakdown:")
        for criterion, stats in result['criteria_stats'].items():
            avg_diff = stats['avg_diff']
            exact_match = stats['exact_match']
            total = stats['total']
            exact_pct = exact_match / total * 100 if total > 0 else 0
            
            if avg_diff > 0.3:
                status = "❌ Too harsh"
            elif avg_diff < -0.3:
                status = "❌ Too lenient"
            else:
                status = "✅ Good"
            
            print(f"     - {criterion}: {avg_diff:+.2f} ({exact_pct:.0f}% exact) {status}")
    
    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    best = results[0]
    best_id = best['experiment_id']
    best_diff = best['avg_score_diff']
    
    if best['avg_score_diff_abs'] < 1.0:
        print(f"\n✅ WINNER: {best_id}")
        print(f"   Excellent alignment! Use this strategy for full experiments.")
        if best_diff > 0:
            print(f"   Note: Still slightly harsh ({best_diff:.2f}), but acceptable.")
        elif best_diff < 0:
            print(f"   Note: Still slightly lenient ({best_diff:.2f}), but acceptable.")
    elif best['avg_score_diff_abs'] < 2.0:
        print(f"\n⚠️  BEST OPTION: {best_id}")
        print(f"   Moderate alignment. Better than baseline but room for improvement.")
        if best_diff > 0:
            print(f"   Still too harsh by {best_diff:.2f} points. Consider:")
            print(f"   - Increase leniency in rubric descriptions")
            print(f"   - Add more few-shot examples of generous grading")
        else:
            print(f"   Still too lenient by {abs(best_diff):.2f} points. Consider:")
            print(f"   - Tighten rubric standards")
            print(f"   - Use stricter prompting")
    else:
        print(f"\n❌ ALL STRATEGIES MISALIGNED")
        print(f"   Best option ({best_id}) still off by {best['avg_score_diff_abs']:.2f} points")
        print(f"   Action required:")
        print(f"   1. Review and revise rubric descriptions")
        print(f"   2. Adjust few-shot examples to match gold standard")
        print(f"   3. Consider hybrid strategies")
    
    # Compare specific improvements
    if len(results) > 1:
        print(f"\n" + "-"*80)
        print("IMPROVEMENTS vs BASELINE")
        print("-"*80)
        
        # Assume first experiment in list is baseline
        baseline_name = experiments[0]
        baseline = next((r for r in results if r['experiment_id'] == baseline_name), None)
        
        if baseline:
            for result in results[1:]:
                exp_id = result['experiment_id']
                improvement = baseline['avg_score_diff_abs'] - result['avg_score_diff_abs']
                improvement_pct = (improvement / baseline['avg_score_diff_abs']) * 100
                
                if improvement > 0:
                    print(f"\n✅ {exp_id}: Improved by {improvement:.2f} points ({improvement_pct:.1f}%)")
                elif improvement < 0:
                    print(f"\n❌ {exp_id}: Worse by {abs(improvement):.2f} points ({abs(improvement_pct):.1f}%)")
                else:
                    print(f"\n➖ {exp_id}: No change")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare multiple experiment strategies')
    parser.add_argument('experiments', nargs='+',
                        help='Experiment IDs to compare (e.g., test_01 test_lenient test_fewshot)')
    parser.add_argument('--gold-dir', default='results/gold_standard',
                        help='Directory containing gold standard files')
    
    args = parser.parse_args()
    
    compare_experiments(args.experiments, args.gold_dir)


if __name__ == "__main__":
    main()
