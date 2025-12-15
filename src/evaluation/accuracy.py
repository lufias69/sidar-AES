"""
Accuracy Metrics Module

Measures accuracy of AI agents compared to ground truth (Lecturer scores):
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Precision, Recall, F1-Score
- Confusion Matrix
- Classification Report
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
    cohen_kappa_score
)


class AccuracyMetrics:
    """
    Calculate accuracy metrics comparing AI predictions to ground truth.
    
    Use case: Compare ChatGPT/Gemini scores against Lecturer scores.
    """
    
    def __init__(self):
        """Initialize accuracy metrics calculator."""
        self.grade_to_numeric = {'A': 4, 'B': 3, 'C': 2, 'D/E': 1, 'D': 1, 'E': 1}
        self.numeric_to_grade = {4: 'A', 3: 'B', 2: 'C', 1: 'D/E'}
        self.grade_categories = ['A', 'B', 'C', 'D/E']
    
    def convert_grades_to_numeric(self, grades: List[str]) -> np.ndarray:
        """Convert letter grades to numeric values."""
        return np.array([self.grade_to_numeric.get(g, np.nan) for g in grades])
    
    def mae(
        self,
        predictions: List[str],
        ground_truth: List[str]
    ) -> Dict[str, float]:
        """
        Calculate Mean Absolute Error.
        
        MAE measures average absolute difference between predictions and truth.
        Lower is better (0 = perfect).
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades (ground truth)
        
        Returns:
            Dictionary with MAE and interpretation
        """
        pred_numeric = self.convert_grades_to_numeric(predictions)
        truth_numeric = self.convert_grades_to_numeric(ground_truth)
        
        # Remove NaN values
        valid_mask = ~(np.isnan(pred_numeric) | np.isnan(truth_numeric))
        pred_numeric = pred_numeric[valid_mask]
        truth_numeric = truth_numeric[valid_mask]
        
        mae_value = mean_absolute_error(truth_numeric, pred_numeric)
        
        # Calculate percentage of exact matches
        exact_matches = np.sum(pred_numeric == truth_numeric)
        exact_match_pct = (exact_matches / len(pred_numeric)) * 100
        
        # Calculate percentage within 1 grade
        within_1_grade = np.sum(np.abs(pred_numeric - truth_numeric) <= 1)
        within_1_pct = (within_1_grade / len(pred_numeric)) * 100
        
        return {
            'mae': float(mae_value),
            'interpretation': self._interpret_mae(mae_value),
            'exact_matches': int(exact_matches),
            'exact_match_pct': float(exact_match_pct),
            'within_1_grade': int(within_1_grade),
            'within_1_grade_pct': float(within_1_pct),
            'n': int(len(pred_numeric))
        }
    
    def rmse(
        self,
        predictions: List[str],
        ground_truth: List[str]
    ) -> Dict[str, float]:
        """
        Calculate Root Mean Square Error.
        
        RMSE penalizes larger errors more than MAE.
        Lower is better (0 = perfect).
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
        
        Returns:
            Dictionary with RMSE and interpretation
        """
        pred_numeric = self.convert_grades_to_numeric(predictions)
        truth_numeric = self.convert_grades_to_numeric(ground_truth)
        
        valid_mask = ~(np.isnan(pred_numeric) | np.isnan(truth_numeric))
        pred_numeric = pred_numeric[valid_mask]
        truth_numeric = truth_numeric[valid_mask]
        
        mse = mean_squared_error(truth_numeric, pred_numeric)
        rmse_value = np.sqrt(mse)
        
        return {
            'rmse': float(rmse_value),
            'mse': float(mse),
            'interpretation': self._interpret_rmse(rmse_value),
            'n': int(len(pred_numeric))
        }
    
    def precision_recall_f1(
        self,
        predictions: List[str],
        ground_truth: List[str],
        average: str = 'weighted'
    ) -> Dict[str, any]:
        """
        Calculate Precision, Recall, and F1-Score.
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
            average: Averaging method ('micro', 'macro', 'weighted', or None)
        
        Returns:
            Dictionary with precision, recall, F1, and per-class metrics
        """
        # Ensure all categories are represented
        pred_array = np.array(predictions)
        truth_array = np.array(ground_truth)
        
        # Calculate metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            truth_array,
            pred_array,
            labels=self.grade_categories,
            average=average,
            zero_division=0
        )
        
        # Per-class metrics (if not averaged)
        if average is None or average == 'weighted':
            per_class_precision, per_class_recall, per_class_f1, per_class_support = \
                precision_recall_fscore_support(
                    truth_array,
                    pred_array,
                    labels=self.grade_categories,
                    average=None,
                    zero_division=0
                )
            
            per_class_metrics = {
                grade: {
                    'precision': float(p),
                    'recall': float(r),
                    'f1': float(f),
                    'support': int(s)
                }
                for grade, p, r, f, s in zip(
                    self.grade_categories,
                    per_class_precision,
                    per_class_recall,
                    per_class_f1,
                    per_class_support
                )
            }
        else:
            per_class_metrics = None
        
        result = {
            'average_method': average,
            'n': len(predictions)
        }
        
        if average:
            result['precision'] = float(precision)
            result['recall'] = float(recall)
            result['f1_score'] = float(f1)
            result['interpretation'] = self._interpret_f1(f1)
        
        if per_class_metrics:
            result['per_class'] = per_class_metrics
        
        return result
    
    def confusion_matrix_analysis(
        self,
        predictions: List[str],
        ground_truth: List[str]
    ) -> Dict[str, any]:
        """
        Generate confusion matrix and analysis.
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
        
        Returns:
            Dictionary with confusion matrix and analysis
        """
        pred_array = np.array(predictions)
        truth_array = np.array(ground_truth)
        
        # Confusion matrix
        cm = confusion_matrix(
            truth_array,
            pred_array,
            labels=self.grade_categories
        )
        
        # Normalize confusion matrix (row-wise: true label perspective)
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm_normalized = np.nan_to_num(cm_normalized)  # Replace NaN with 0
        
        # Calculate accuracy per class
        accuracy_per_class = {
            grade: float(cm[i, i] / cm[i, :].sum()) if cm[i, :].sum() > 0 else 0.0
            for i, grade in enumerate(self.grade_categories)
        }
        
        # Overall accuracy
        overall_accuracy = np.trace(cm) / np.sum(cm)
        
        # Find most common misclassifications
        misclassifications = []
        for i, true_grade in enumerate(self.grade_categories):
            for j, pred_grade in enumerate(self.grade_categories):
                if i != j and cm[i, j] > 0:
                    misclassifications.append({
                        'true_grade': true_grade,
                        'predicted_grade': pred_grade,
                        'count': int(cm[i, j]),
                        'percentage': float(cm[i, j] / cm[i, :].sum() * 100)
                    })
        
        # Sort by count
        misclassifications.sort(key=lambda x: x['count'], reverse=True)
        
        return {
            'confusion_matrix': cm.tolist(),
            'confusion_matrix_normalized': cm_normalized.tolist(),
            'labels': self.grade_categories,
            'overall_accuracy': float(overall_accuracy),
            'accuracy_per_class': accuracy_per_class,
            'misclassifications': misclassifications[:5],  # Top 5
            'total_predictions': int(np.sum(cm))
        }
    
    def classification_report_dict(
        self,
        predictions: List[str],
        ground_truth: List[str]
    ) -> Dict[str, any]:
        """
        Generate sklearn classification report as dictionary.
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
        
        Returns:
            Dictionary with complete classification report
        """
        pred_array = np.array(predictions)
        truth_array = np.array(ground_truth)
        
        report = classification_report(
            truth_array,
            pred_array,
            labels=self.grade_categories,
            output_dict=True,
            zero_division=0
        )
        
        return report
    
    def grade_distribution_comparison(
        self,
        predictions: List[str],
        ground_truth: List[str]
    ) -> Dict[str, any]:
        """
        Compare grade distributions between predictions and ground truth.
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
        
        Returns:
            Dictionary with distribution statistics
        """
        pred_counts = pd.Series(predictions).value_counts()
        truth_counts = pd.Series(ground_truth).value_counts()
        
        # Ensure all categories present
        for grade in self.grade_categories:
            if grade not in pred_counts:
                pred_counts[grade] = 0
            if grade not in truth_counts:
                truth_counts[grade] = 0
        
        pred_counts = pred_counts.sort_index()
        truth_counts = truth_counts.sort_index()
        
        # Calculate distribution differences
        distribution_diff = {
            grade: {
                'predicted_count': int(pred_counts.get(grade, 0)),
                'ground_truth_count': int(truth_counts.get(grade, 0)),
                'difference': int(pred_counts.get(grade, 0) - truth_counts.get(grade, 0)),
                'predicted_pct': float(pred_counts.get(grade, 0) / len(predictions) * 100),
                'ground_truth_pct': float(truth_counts.get(grade, 0) / len(ground_truth) * 100)
            }
            for grade in self.grade_categories
        }
        
        # Chi-square test for distribution similarity
        from scipy.stats import chisquare
        chi2_stat, p_value = chisquare(
            [pred_counts.get(g, 0) for g in self.grade_categories],
            [truth_counts.get(g, 0) for g in self.grade_categories]
        )
        
        return {
            'distributions': distribution_diff,
            'chi_square_statistic': float(chi2_stat),
            'p_value': float(p_value),
            'distributions_similar': p_value > 0.05,
            'n_predictions': len(predictions),
            'n_ground_truth': len(ground_truth)
        }
    
    def _interpret_mae(self, mae: float) -> str:
        """Interpret MAE value."""
        if mae < 0.25:
            return "Excellent accuracy (MAE < 0.25 grades)"
        elif mae < 0.5:
            return "Good accuracy (0.25 ≤ MAE < 0.5 grades)"
        elif mae < 1.0:
            return "Moderate accuracy (0.5 ≤ MAE < 1 grade)"
        else:
            return "Poor accuracy (MAE ≥ 1 grade)"
    
    def _interpret_rmse(self, rmse: float) -> str:
        """Interpret RMSE value."""
        if rmse < 0.3:
            return "Excellent accuracy (RMSE < 0.3)"
        elif rmse < 0.6:
            return "Good accuracy (0.3 ≤ RMSE < 0.6)"
        elif rmse < 1.0:
            return "Moderate accuracy (0.6 ≤ RMSE < 1.0)"
        else:
            return "Poor accuracy (RMSE ≥ 1.0)"
    
    def _interpret_f1(self, f1: float) -> str:
        """Interpret F1-Score."""
        if f1 >= 0.9:
            return "Excellent classification (F1 ≥ 0.9)"
        elif f1 >= 0.8:
            return "Good classification (0.8 ≤ F1 < 0.9)"
        elif f1 >= 0.6:
            return "Moderate classification (0.6 ≤ F1 < 0.8)"
        else:
            return "Poor classification (F1 < 0.6)"
    
    def calculate_all_accuracy(
        self,
        predictions: List[str],
        ground_truth: List[str],
        agent_name: str = "Agent",
        criterion_name: str = "Overall"
    ) -> Dict[str, any]:
        """
        Calculate all accuracy metrics for an agent.
        
        This is the main function for comparing AI predictions to ground truth.
        
        Args:
            predictions: AI-predicted grades
            ground_truth: Lecturer grades
            agent_name: Name of the agent (e.g., "ChatGPT", "Gemini")
            criterion_name: Name of the criterion being evaluated
        
        Returns:
            Comprehensive dictionary with all accuracy metrics
        """
        mae_result = self.mae(predictions, ground_truth)
        rmse_result = self.rmse(predictions, ground_truth)
        prf_result = self.precision_recall_f1(predictions, ground_truth, average='weighted')
        cm_result = self.confusion_matrix_analysis(predictions, ground_truth)
        dist_result = self.grade_distribution_comparison(predictions, ground_truth)
        
        return {
            'agent': agent_name,
            'criterion': criterion_name,
            'n': len(predictions),
            'mae': mae_result,
            'rmse': rmse_result,
            'precision_recall_f1': prf_result,
            'confusion_matrix': cm_result,
            'distribution_comparison': dist_result,
            'overall_assessment': self._overall_accuracy_assessment(mae_result, prf_result, cm_result)
        }
    
    def _overall_accuracy_assessment(
        self,
        mae: Dict,
        prf: Dict,
        cm: Dict
    ) -> str:
        """Generate overall accuracy assessment."""
        mae_val = mae['mae']
        f1_val = prf.get('f1_score', 0)
        accuracy = cm['overall_accuracy']
        exact_match_pct = mae['exact_match_pct']
        
        if mae_val < 0.3 and f1_val >= 0.85 and exact_match_pct >= 70:
            return "Excellent: Agent predictions highly accurate and reliable"
        elif mae_val < 0.5 and f1_val >= 0.75 and exact_match_pct >= 60:
            return "Good: Agent predictions are accurate and mostly reliable"
        elif mae_val < 1.0 and f1_val >= 0.60:
            return "Moderate: Agent predictions acceptable but need improvement"
        else:
            return "Poor: Agent predictions show significant deviation from ground truth"


if __name__ == "__main__":
    # Example usage
    print("=== Accuracy Metrics Example ===\n")
    
    # Simulate predictions vs ground truth
    predictions = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    ground_truth = ['A', 'B', 'C', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    
    calculator = AccuracyMetrics()
    results = calculator.calculate_all_accuracy(predictions, ground_truth, "ChatGPT", "Pemahaman Konten")
    
    print(f"Agent: {results['agent']}")
    print(f"Criterion: {results['criterion']}")
    print(f"Total predictions: {results['n']}")
    
    print(f"\nMean Absolute Error:")
    print(f"  MAE: {results['mae']['mae']:.3f}")
    print(f"  {results['mae']['interpretation']}")
    print(f"  Exact matches: {results['mae']['exact_match_pct']:.1f}%")
    print(f"  Within 1 grade: {results['mae']['within_1_grade_pct']:.1f}%")
    
    print(f"\nRoot Mean Square Error:")
    print(f"  RMSE: {results['rmse']['rmse']:.3f}")
    print(f"  {results['rmse']['interpretation']}")
    
    print(f"\nPrecision/Recall/F1:")
    print(f"  Precision: {results['precision_recall_f1']['precision']:.3f}")
    print(f"  Recall: {results['precision_recall_f1']['recall']:.3f}")
    print(f"  F1-Score: {results['precision_recall_f1']['f1_score']:.3f}")
    print(f"  {results['precision_recall_f1']['interpretation']}")
    
    print(f"\nConfusion Matrix Analysis:")
    print(f"  Overall accuracy: {results['confusion_matrix']['overall_accuracy']:.3f}")
    print(f"  Top misclassifications:")
    for mis in results['confusion_matrix']['misclassifications'][:3]:
        print(f"    {mis['true_grade']} → {mis['predicted_grade']}: {mis['count']} ({mis['percentage']:.1f}%)")
    
    print(f"\nOverall: {results['overall_assessment']}")
