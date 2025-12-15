"""
Test Evaluation Metrics

Quick test to verify all evaluation metrics work correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation.agreement import AgreementMetrics
from src.evaluation.consistency import ConsistencyMetrics
from src.evaluation.accuracy import AccuracyMetrics
from src.evaluation.visualizer import MetricsVisualizer
import numpy as np
import matplotlib.pyplot as plt

def test_agreement_metrics():
    """Test agreement metrics calculation."""
    print("\n" + "="*60)
    print("TESTING AGREEMENT METRICS (Fleiss' Kappa)")
    print("="*60)
    
    # Simulate ratings
    chatgpt = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    gemini = ['A', 'B', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A']
    lecturer = ['A', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    
    calculator = AgreementMetrics()
    results = calculator.calculate_all_agreements(chatgpt, gemini, lecturer, "Test Criterion")
    
    print(f"\n✅ Fleiss' Kappa: {results['fleiss_kappa']['kappa']:.3f}")
    print(f"   Interpretation: {results['fleiss_kappa']['interpretation']}")
    
    print(f"\n✅ Cohen's Kappa (pairwise):")
    print(f"   ChatGPT vs Lecturer: {results['cohen_kappa_pairwise']['chatgpt_vs_lecturer']['kappa']:.3f}")
    print(f"   Gemini vs Lecturer: {results['cohen_kappa_pairwise']['gemini_vs_lecturer']['kappa']:.3f}")
    print(f"   ChatGPT vs Gemini: {results['cohen_kappa_pairwise']['chatgpt_vs_gemini']['kappa']:.3f}")
    
    return True

def test_consistency_metrics():
    """Test consistency metrics calculation."""
    print("\n" + "="*60)
    print("TESTING CONSISTENCY METRICS (ICC, SD, CV)")
    print("="*60)
    
    # Simulate 4 trials
    trial1 = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    trial2 = ['A', 'B', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A']
    trial3 = ['A', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    trial4 = ['A', 'B', 'B', 'B', 'C', 'B', 'A', 'B', 'C', 'A']
    
    trials = [trial1, trial2, trial3, trial4]
    
    calculator = ConsistencyMetrics()
    results = calculator.calculate_all_consistency(trials, "ChatGPT", "Test Criterion")
    
    print(f"\n✅ Standard Deviation:")
    print(f"   Mean SD: {results['standard_deviation']['mean_sd']:.3f}")
    
    print(f"\n✅ Coefficient of Variation:")
    print(f"   Mean CV: {results['coefficient_of_variation']['mean_cv']:.2f}%")
    print(f"   {results['coefficient_of_variation']['interpretation']}")
    
    print(f"\n✅ Intraclass Correlation:")
    print(f"   ICC: {results['intraclass_correlation']['icc']:.3f}")
    print(f"   95% CI: [{results['intraclass_correlation']['ci_95_lower']:.3f}, {results['intraclass_correlation']['ci_95_upper']:.3f}]")
    print(f"   {results['intraclass_correlation']['interpretation']}")
    
    print(f"\n✅ Agreement:")
    print(f"   Perfect agreement: {results['agreement']['perfect_agreement_pct']:.1f}%")
    
    return True

def test_accuracy_metrics():
    """Test accuracy metrics calculation."""
    print("\n" + "="*60)
    print("TESTING ACCURACY METRICS (MAE, RMSE, F1)")
    print("="*60)
    
    predictions = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    ground_truth = ['A', 'B', 'C', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    
    calculator = AccuracyMetrics()
    results = calculator.calculate_all_accuracy(predictions, ground_truth, "ChatGPT", "Test Criterion")
    
    print(f"\n✅ Mean Absolute Error:")
    print(f"   MAE: {results['mae']['mae']:.3f}")
    print(f"   {results['mae']['interpretation']}")
    print(f"   Exact matches: {results['mae']['exact_match_pct']:.1f}%")
    
    print(f"\n✅ Root Mean Square Error:")
    print(f"   RMSE: {results['rmse']['rmse']:.3f}")
    print(f"   {results['rmse']['interpretation']}")
    
    print(f"\n✅ Precision/Recall/F1:")
    print(f"   Precision: {results['precision_recall_f1']['precision']:.3f}")
    print(f"   Recall: {results['precision_recall_f1']['recall']:.3f}")
    print(f"   F1-Score: {results['precision_recall_f1']['f1_score']:.3f}")
    print(f"   {results['precision_recall_f1']['interpretation']}")
    
    print(f"\n✅ Confusion Matrix:")
    print(f"   Overall accuracy: {results['confusion_matrix']['overall_accuracy']:.3f}")
    
    return True

def test_visualizations():
    """Test visualization generation."""
    print("\n" + "="*60)
    print("TESTING VISUALIZATIONS")
    print("="*60)
    
    try:
        visualizer = MetricsVisualizer()
        
        # Test consistency box plot
        consistency_data = {
            'ChatGPT': {
                'standard_deviation': {'sd_per_essay': np.random.normal(0.3, 0.1, 10).tolist()},
                'coefficient_of_variation': {'cv_per_essay': np.random.normal(15, 5, 10).tolist()},
                'intraclass_correlation': {'icc': 0.85, 'ci_95_lower': 0.78, 'ci_95_upper': 0.92}
            },
            'Gemini': {
                'standard_deviation': {'sd_per_essay': np.random.normal(0.4, 0.12, 10).tolist()},
                'coefficient_of_variation': {'cv_per_essay': np.random.normal(18, 6, 10).tolist()},
                'intraclass_correlation': {'icc': 0.78, 'ci_95_lower': 0.70, 'ci_95_upper': 0.86}
            }
        }
        
        fig = visualizer.plot_consistency_boxplot(consistency_data, "Test Criterion")
        plt.close(fig)
        
        print("\n✅ Consistency box plot created successfully")
        
        # Test confusion matrix
        cm = np.array([[20, 3, 1, 0], [2, 15, 3, 0], [0, 2, 8, 2], [0, 0, 1, 3]])
        labels = ['A', 'B', 'C', 'D/E']
        fig2 = visualizer.plot_confusion_matrix(cm, labels, "ChatGPT", "Test")
        plt.close(fig2)
        
        print("✅ Confusion matrix created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EVALUATION METRICS TEST SUITE")
    print("="*60)
    
    tests = [
        ("Agreement Metrics", test_agreement_metrics),
        ("Consistency Metrics", test_consistency_metrics),
        ("Accuracy Metrics", test_accuracy_metrics),
        ("Visualizations", test_visualizations)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ {test_name} FAILED: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
