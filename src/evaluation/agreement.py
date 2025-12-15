"""
Agreement Metrics Module

Implements inter-rater agreement metrics:
- Fleiss' Kappa: Multi-rater agreement (PRIMARY METRIC)
- Cohen's Kappa: Pairwise agreement
- Krippendorff's Alpha: Alternative agreement metric
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from scipy.stats import chi2_contingency
from itertools import combinations


class AgreementMetrics:
    """
    Calculate inter-rater agreement metrics for essay scoring.
    
    Primary use: Measure agreement between ChatGPT, Gemini, and Lecturer
    """
    
    def __init__(self):
        """Initialize agreement metrics calculator."""
        self.grade_categories = ['A', 'B', 'C', 'D/E']
    
    def fleiss_kappa(
        self,
        ratings: np.ndarray,
        categories: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Calculate Fleiss' Kappa for multiple raters.
        
        Fleiss' Kappa measures agreement among multiple raters when each item
        is rated by the same number of raters. Perfect for comparing:
        ChatGPT (4 trials) vs Gemini (4 trials) vs Lecturer (1 score)
        
        Args:
            ratings: Array of shape (n_items, n_raters) containing categorical ratings
                    Example: [[A, A, B], [B, B, B], [C, A, A], ...]
            categories: List of possible categories (default: ['A', 'B', 'C', 'D/E'])
        
        Returns:
            Dictionary with:
                - kappa: Fleiss' Kappa value
                - interpretation: Text interpretation
                - p_observed: Observed agreement proportion
                - p_expected: Expected agreement by chance
                - n_items: Number of items rated
                - n_raters: Number of raters
        
        Interpretation:
            < 0.00: Poor agreement
            0.00 - 0.20: Slight agreement
            0.21 - 0.40: Fair agreement
            0.41 - 0.60: Moderate agreement
            0.61 - 0.80: Substantial agreement
            0.81 - 1.00: Almost perfect agreement
        """
        if categories is None:
            categories = self.grade_categories
        
        # Convert to numpy array if not already
        ratings = np.array(ratings)
        n_items, n_raters = ratings.shape
        
        # Create frequency matrix: n_items x n_categories
        n_categories = len(categories)
        freq_matrix = np.zeros((n_items, n_categories))
        
        for i, item_ratings in enumerate(ratings):
            for rating in item_ratings:
                if rating in categories:
                    cat_idx = categories.index(rating)
                    freq_matrix[i, cat_idx] += 1
        
        # Calculate P_i (proportion of rater pairs agreeing for each item)
        P_i = np.sum(freq_matrix * (freq_matrix - 1), axis=1) / (n_raters * (n_raters - 1))
        
        # Calculate P_bar (mean proportion of agreement)
        P_bar = np.mean(P_i)
        
        # Calculate p_j (proportion of all assignments to category j)
        p_j = np.sum(freq_matrix, axis=0) / (n_items * n_raters)
        
        # Calculate P_bar_e (expected agreement by chance)
        P_bar_e = np.sum(p_j ** 2)
        
        # Calculate Fleiss' Kappa
        if P_bar_e == 1.0:
            kappa = 1.0  # Perfect agreement
        else:
            kappa = (P_bar - P_bar_e) / (1 - P_bar_e)
        
        # Interpret kappa
        interpretation = self._interpret_kappa(kappa)
        
        return {
            'kappa': float(kappa),
            'interpretation': interpretation,
            'p_observed': float(P_bar),
            'p_expected': float(P_bar_e),
            'n_items': int(n_items),
            'n_raters': int(n_raters),
            'category_proportions': {cat: float(p) for cat, p in zip(categories, p_j)}
        }
    
    def cohen_kappa(
        self,
        rater1: np.ndarray,
        rater2: np.ndarray,
        categories: Optional[List[str]] = None,
        weights: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate Cohen's Kappa for two raters.
        
        Use for pairwise comparisons:
        - ChatGPT vs Lecturer
        - Gemini vs Lecturer
        - ChatGPT vs Gemini
        
        Args:
            rater1: Array of ratings from first rater
            rater2: Array of ratings from second rater
            categories: List of possible categories
            weights: Weighting scheme ('linear', 'quadratic', or None)
        
        Returns:
            Dictionary with kappa, standard error, and confidence interval
        """
        if categories is None:
            categories = self.grade_categories
        
        rater1 = np.array(rater1)
        rater2 = np.array(rater2)
        
        n = len(rater1)
        n_categories = len(categories)
        
        # Create confusion matrix
        confusion = np.zeros((n_categories, n_categories))
        for r1, r2 in zip(rater1, rater2):
            if r1 in categories and r2 in categories:
                i = categories.index(r1)
                j = categories.index(r2)
                confusion[i, j] += 1
        
        # Create weight matrix
        if weights == 'linear':
            weight_matrix = 1 - np.abs(np.arange(n_categories)[:, None] - np.arange(n_categories)) / (n_categories - 1)
        elif weights == 'quadratic':
            weight_matrix = 1 - ((np.arange(n_categories)[:, None] - np.arange(n_categories)) / (n_categories - 1)) ** 2
        else:
            # Identity matrix for unweighted kappa
            weight_matrix = np.eye(n_categories)
        
        # Normalize confusion matrix
        confusion_norm = confusion / n
        
        # Calculate observed agreement
        p_observed = np.sum(weight_matrix * confusion_norm)
        
        # Calculate expected agreement
        row_sums = np.sum(confusion_norm, axis=1)
        col_sums = np.sum(confusion_norm, axis=0)
        expected = np.outer(row_sums, col_sums)
        p_expected = np.sum(weight_matrix * expected)
        
        # Calculate Cohen's Kappa
        if p_expected == 1.0:
            kappa = 1.0
        else:
            kappa = (p_observed - p_expected) / (1 - p_expected)
        
        # Calculate standard error (for unweighted kappa)
        if weights is None:
            se = self._cohen_kappa_se(confusion_norm, p_observed, p_expected)
        else:
            se = None  # SE calculation complex for weighted kappa
        
        # 95% confidence interval
        ci_lower = kappa - 1.96 * se if se else None
        ci_upper = kappa + 1.96 * se if se else None
        
        interpretation = self._interpret_kappa(kappa)
        
        result = {
            'kappa': float(kappa),
            'interpretation': interpretation,
            'p_observed': float(p_observed),
            'p_expected': float(p_expected),
            'n': int(n),
            'confusion_matrix': confusion.tolist()
        }
        
        if se:
            result['standard_error'] = float(se)
            result['ci_95_lower'] = float(ci_lower)
            result['ci_95_upper'] = float(ci_upper)
        
        return result
    
    def _cohen_kappa_se(
        self,
        confusion_norm: np.ndarray,
        p_o: float,
        p_e: float
    ) -> float:
        """Calculate standard error for Cohen's Kappa."""
        n_categories = confusion_norm.shape[0]
        
        # Marginal probabilities
        row_sums = np.sum(confusion_norm, axis=1)
        col_sums = np.sum(confusion_norm, axis=0)
        
        # Variance components
        var_term1 = p_o * (1 - p_o)
        var_term2 = 2 * (1 - p_o) * (2 * p_o * p_e - np.sum(row_sums * col_sums * (row_sums + col_sums)))
        var_term3 = (1 - p_o) ** 2 * (np.sum((row_sums + col_sums) ** 2) - 4 * p_e ** 2)
        
        variance = (var_term1 + var_term2 + var_term3) / ((1 - p_e) ** 2)
        
        # Standard error
        n = np.sum(confusion_norm) if np.sum(confusion_norm) > 0 else 1
        se = np.sqrt(variance / n)
        
        return se
    
    def krippendorff_alpha(
        self,
        ratings: np.ndarray,
        level: str = 'nominal'
    ) -> Dict[str, float]:
        """
        Calculate Krippendorff's Alpha for multiple raters.
        
        More robust than Fleiss' Kappa for missing data and different numbers
        of raters per item.
        
        Args:
            ratings: Array of shape (n_raters, n_items) with possible NaN for missing
            level: Measurement level ('nominal', 'ordinal', 'interval', 'ratio')
        
        Returns:
            Dictionary with alpha value and interpretation
        """
        ratings = np.array(ratings, dtype=float)
        n_raters, n_items = ratings.shape
        
        # Convert grades to numeric if needed
        if level in ['ordinal', 'interval', 'ratio']:
            # Map grades to numeric values: A=4, B=3, C=2, D/E=1
            grade_map = {'A': 4, 'B': 3, 'C': 2, 'D/E': 1, 'D': 1, 'E': 1}
            ratings_numeric = np.array([[grade_map.get(r, np.nan) for r in row] for row in ratings])
        else:
            ratings_numeric = ratings
        
        # Calculate coincidence matrix
        values = np.unique(ratings_numeric[~np.isnan(ratings_numeric)])
        n_values = len(values)
        coincidence = np.zeros((n_values, n_values))
        
        for item in range(n_items):
            item_ratings = ratings_numeric[:, item]
            valid_ratings = item_ratings[~np.isnan(item_ratings)]
            n_valid = len(valid_ratings)
            
            if n_valid < 2:
                continue
            
            for i, val1 in enumerate(values):
                for j, val2 in enumerate(values):
                    count1 = np.sum(valid_ratings == val1)
                    count2 = np.sum(valid_ratings == val2)
                    
                    if i == j:
                        coincidence[i, j] += count1 * (count1 - 1) / (n_valid - 1) if n_valid > 1 else 0
                    else:
                        coincidence[i, j] += count1 * count2 / (n_valid - 1) if n_valid > 1 else 0
        
        # Calculate disagreement
        if level == 'nominal':
            delta = 1 - np.eye(n_values)
        elif level == 'ordinal':
            # Ordinal distance
            delta = np.abs(np.arange(n_values)[:, None] - np.arange(n_values))
        else:  # interval or ratio
            # Squared difference
            delta = (values[:, None] - values) ** 2
        
        # Observed disagreement
        n_c = np.sum(coincidence)
        d_o = np.sum(coincidence * delta) / n_c if n_c > 0 else 0
        
        # Expected disagreement
        n_k = np.sum(coincidence, axis=1)
        d_e = np.sum(np.outer(n_k, n_k) * delta) / (n_c ** 2) if n_c > 0 else 0
        
        # Krippendorff's Alpha
        if d_e == 0:
            alpha = 1.0
        else:
            alpha = 1 - (d_o / d_e)
        
        interpretation = self._interpret_kappa(alpha)  # Same interpretation scale
        
        return {
            'alpha': float(alpha),
            'interpretation': interpretation,
            'd_observed': float(d_o),
            'd_expected': float(d_e),
            'level': level
        }
    
    def pairwise_agreement_matrix(
        self,
        raters_dict: Dict[str, np.ndarray]
    ) -> pd.DataFrame:
        """
        Calculate Cohen's Kappa for all pairs of raters.
        
        Args:
            raters_dict: Dictionary mapping rater names to their ratings
                        Example: {'ChatGPT': [...], 'Gemini': [...], 'Lecturer': [...]}
        
        Returns:
            DataFrame with pairwise kappa values
        """
        rater_names = list(raters_dict.keys())
        n_raters = len(rater_names)
        
        kappa_matrix = np.zeros((n_raters, n_raters))
        
        for i, rater1 in enumerate(rater_names):
            for j, rater2 in enumerate(rater_names):
                if i == j:
                    kappa_matrix[i, j] = 1.0  # Perfect agreement with self
                elif i < j:
                    result = self.cohen_kappa(raters_dict[rater1], raters_dict[rater2])
                    kappa_matrix[i, j] = result['kappa']
                    kappa_matrix[j, i] = result['kappa']  # Symmetric
        
        return pd.DataFrame(kappa_matrix, index=rater_names, columns=rater_names)
    
    def _interpret_kappa(self, kappa: float) -> str:
        """
        Interpret Kappa value according to Landis & Koch (1977).
        
        Reference:
        Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement
        for categorical data. Biometrics, 33(1), 159-174.
        """
        if kappa < 0.0:
            return "Poor agreement (worse than chance)"
        elif kappa < 0.20:
            return "Slight agreement"
        elif kappa < 0.40:
            return "Fair agreement"
        elif kappa < 0.60:
            return "Moderate agreement"
        elif kappa < 0.80:
            return "Substantial agreement"
        else:
            return "Almost perfect agreement"
    
    def calculate_all_agreements(
        self,
        chatgpt_scores: List[str],
        gemini_scores: List[str],
        lecturer_scores: List[str],
        criterion_name: str = "Overall"
    ) -> Dict[str, any]:
        """
        Calculate all agreement metrics for ChatGPT, Gemini, and Lecturer.
        
        This is the main function for the AES research paper.
        
        Args:
            chatgpt_scores: List of ChatGPT grades (e.g., average of 4 trials)
            gemini_scores: List of Gemini grades (e.g., average of 4 trials)
            lecturer_scores: List of Lecturer grades (ground truth)
            criterion_name: Name of the criterion being evaluated
        
        Returns:
            Comprehensive dictionary with all metrics
        """
        # Combine all ratings for Fleiss' Kappa
        ratings = np.column_stack([chatgpt_scores, gemini_scores, lecturer_scores])
        
        # Fleiss' Kappa (primary metric)
        fleiss = self.fleiss_kappa(ratings)
        
        # Cohen's Kappa pairwise
        cohen_chatgpt_lecturer = self.cohen_kappa(chatgpt_scores, lecturer_scores)
        cohen_gemini_lecturer = self.cohen_kappa(gemini_scores, lecturer_scores)
        cohen_chatgpt_gemini = self.cohen_kappa(chatgpt_scores, gemini_scores)
        
        # Pairwise agreement matrix
        raters_dict = {
            'ChatGPT': chatgpt_scores,
            'Gemini': gemini_scores,
            'Lecturer': lecturer_scores
        }
        agreement_matrix = self.pairwise_agreement_matrix(raters_dict)
        
        return {
            'criterion': criterion_name,
            'fleiss_kappa': fleiss,
            'cohen_kappa_pairwise': {
                'chatgpt_vs_lecturer': cohen_chatgpt_lecturer,
                'gemini_vs_lecturer': cohen_gemini_lecturer,
                'chatgpt_vs_gemini': cohen_chatgpt_gemini
            },
            'agreement_matrix': agreement_matrix.to_dict(),
            'n_essays': len(chatgpt_scores)
        }


if __name__ == "__main__":
    # Example usage
    print("=== Agreement Metrics Example ===\n")
    
    # Simulate ratings for 10 essays
    np.random.seed(42)
    chatgpt = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    gemini = ['A', 'B', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A']
    lecturer = ['A', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    
    calculator = AgreementMetrics()
    results = calculator.calculate_all_agreements(chatgpt, gemini, lecturer, "Pemahaman Konten")
    
    print(f"Criterion: {results['criterion']}")
    print(f"\nFleiss' Kappa: {results['fleiss_kappa']['kappa']:.3f}")
    print(f"Interpretation: {results['fleiss_kappa']['interpretation']}")
    
    print(f"\nCohen's Kappa:")
    print(f"  ChatGPT vs Lecturer: {results['cohen_kappa_pairwise']['chatgpt_vs_lecturer']['kappa']:.3f}")
    print(f"  Gemini vs Lecturer: {results['cohen_kappa_pairwise']['gemini_vs_lecturer']['kappa']:.3f}")
    print(f"  ChatGPT vs Gemini: {results['cohen_kappa_pairwise']['chatgpt_vs_gemini']['kappa']:.3f}")
    
    print(f"\nAgreement Matrix:")
    print(pd.DataFrame(results['agreement_matrix']).round(3))
