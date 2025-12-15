"""
Consistency Metrics Module

Measures consistency of AI agents across multiple trials:
- Standard Deviation (SD)
- Coefficient of Variation (CV)
- Intraclass Correlation Coefficient (ICC)
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from scipy import stats
from scipy.stats import f


class ConsistencyMetrics:
    """
    Calculate consistency metrics for multiple trials of AI grading.
    
    Use case: Measure how consistent ChatGPT and Gemini are across 4 trials.
    """
    
    def __init__(self):
        """Initialize consistency metrics calculator."""
        self.grade_to_numeric = {'A': 4, 'B': 3, 'C': 2, 'D/E': 1, 'D': 1, 'E': 1}
        self.numeric_to_grade = {4: 'A', 3: 'B', 2: 'C', 1: 'D/E'}
    
    def convert_grades_to_numeric(self, grades: List[str]) -> np.ndarray:
        """Convert letter grades to numeric values."""
        return np.array([self.grade_to_numeric.get(g, np.nan) for g in grades])
    
    def standard_deviation(
        self,
        trials: List[List[str]],
        per_essay: bool = True
    ) -> Dict[str, any]:
        """
        Calculate standard deviation across trials.
        
        Args:
            trials: List of trial results, each trial is a list of grades
                   Example: [['A', 'B', 'C', ...], ['A', 'B', 'B', ...], ...]
            per_essay: If True, calculate SD per essay; if False, overall SD
        
        Returns:
            Dictionary with SD statistics
        """
        # Convert to numeric
        trials_numeric = [self.convert_grades_to_numeric(trial) for trial in trials]
        trials_array = np.array(trials_numeric)  # Shape: (n_trials, n_essays)
        
        if per_essay:
            # SD for each essay across trials
            sd_per_essay = np.std(trials_array, axis=0, ddof=1)
            mean_per_essay = np.mean(trials_array, axis=0)
            
            return {
                'sd_per_essay': sd_per_essay.tolist(),
                'mean_sd': float(np.mean(sd_per_essay)),
                'median_sd': float(np.median(sd_per_essay)),
                'min_sd': float(np.min(sd_per_essay)),
                'max_sd': float(np.max(sd_per_essay)),
                'mean_per_essay': mean_per_essay.tolist(),
                'n_essays': len(sd_per_essay),
                'n_trials': len(trials)
            }
        else:
            # Overall SD
            all_scores = trials_array.flatten()
            return {
                'sd': float(np.std(all_scores, ddof=1)),
                'mean': float(np.mean(all_scores)),
                'n_total': len(all_scores)
            }
    
    def coefficient_of_variation(
        self,
        trials: List[List[str]],
        per_essay: bool = True
    ) -> Dict[str, any]:
        """
        Calculate Coefficient of Variation (CV = SD / Mean).
        
        CV is a normalized measure of dispersion, useful for comparing
        consistency across different scales.
        
        Args:
            trials: List of trial results
            per_essay: If True, calculate CV per essay; if False, overall CV
        
        Returns:
            Dictionary with CV statistics (as percentage)
        """
        sd_result = self.standard_deviation(trials, per_essay)
        
        if per_essay:
            sd_per_essay = np.array(sd_result['sd_per_essay'])
            mean_per_essay = np.array(sd_result['mean_per_essay'])
            
            # CV = (SD / Mean) * 100%
            cv_per_essay = np.where(mean_per_essay > 0, 
                                    (sd_per_essay / mean_per_essay) * 100, 
                                    0)
            
            return {
                'cv_per_essay': cv_per_essay.tolist(),
                'mean_cv': float(np.mean(cv_per_essay)),
                'median_cv': float(np.median(cv_per_essay)),
                'min_cv': float(np.min(cv_per_essay)),
                'max_cv': float(np.max(cv_per_essay)),
                'interpretation': self._interpret_cv(np.mean(cv_per_essay)),
                'n_essays': len(cv_per_essay),
                'n_trials': sd_result['n_trials']
            }
        else:
            cv = (sd_result['sd'] / sd_result['mean']) * 100 if sd_result['mean'] > 0 else 0
            return {
                'cv': float(cv),
                'interpretation': self._interpret_cv(cv),
                'sd': sd_result['sd'],
                'mean': sd_result['mean']
            }
    
    def intraclass_correlation(
        self,
        trials: List[List[str]],
        icc_type: str = 'ICC(2,1)'
    ) -> Dict[str, any]:
        """
        Calculate Intraclass Correlation Coefficient (ICC).
        
        ICC measures reliability/consistency of measurements across trials.
        
        Args:
            trials: List of trial results
            icc_type: Type of ICC to calculate:
                     'ICC(1,1)': One-way random effects
                     'ICC(2,1)': Two-way random effects, single measurement
                     'ICC(3,1)': Two-way mixed effects, single measurement
        
        Returns:
            Dictionary with ICC value, confidence interval, and interpretation
        
        Interpretation:
            < 0.40: Poor reliability
            0.40 - 0.59: Fair reliability
            0.60 - 0.74: Good reliability
            0.75 - 1.00: Excellent reliability
        """
        # Convert to numeric
        trials_numeric = [self.convert_grades_to_numeric(trial) for trial in trials]
        data = np.array(trials_numeric).T  # Shape: (n_essays, n_trials)
        
        n_essays, n_trials = data.shape
        
        # Grand mean
        grand_mean = np.mean(data)
        
        # Between-target (essay) variance
        essay_means = np.mean(data, axis=1)
        ms_between = n_trials * np.var(essay_means, ddof=1)
        
        # Within-target variance
        ms_within = np.mean(np.var(data, axis=1, ddof=1))
        
        # Between-rater (trial) variance
        trial_means = np.mean(data, axis=0)
        ms_trials = n_essays * np.var(trial_means, ddof=1)
        
        # Residual variance
        ms_error = ms_within
        
        if icc_type == 'ICC(1,1)':
            # One-way random effects
            icc = (ms_between - ms_within) / (ms_between + (n_trials - 1) * ms_within)
            
        elif icc_type == 'ICC(2,1)':
            # Two-way random effects, single measurement
            icc = (ms_between - ms_error) / (ms_between + (n_trials - 1) * ms_error + n_trials * (ms_trials - ms_error) / n_essays)
            
        elif icc_type == 'ICC(3,1)':
            # Two-way mixed effects, single measurement
            icc = (ms_between - ms_error) / (ms_between + (n_trials - 1) * ms_error)
            
        else:
            raise ValueError(f"Unknown ICC type: {icc_type}")
        
        # Confidence interval (approximate)
        df1 = n_essays - 1
        df2 = n_essays * (n_trials - 1)
        f_stat = ms_between / ms_error
        
        f_lower = f_stat / f.ppf(0.975, df1, df2)
        f_upper = f_stat / f.ppf(0.025, df1, df2)
        
        ci_lower = (f_lower - 1) / (f_lower + n_trials - 1)
        ci_upper = (f_upper - 1) / (f_upper + n_trials - 1)
        
        interpretation = self._interpret_icc(icc)
        
        return {
            'icc': float(icc),
            'icc_type': icc_type,
            'interpretation': interpretation,
            'ci_95_lower': float(max(0, ci_lower)),
            'ci_95_upper': float(min(1, ci_upper)),
            'n_essays': int(n_essays),
            'n_trials': int(n_trials),
            'ms_between': float(ms_between),
            'ms_within': float(ms_within),
            'f_statistic': float(f_stat)
        }
    
    def agreement_percentage(
        self,
        trials: List[List[str]]
    ) -> Dict[str, any]:
        """
        Calculate percentage of essays where all trials agree.
        
        Args:
            trials: List of trial results
        
        Returns:
            Dictionary with agreement statistics
        """
        trials_array = np.array(trials).T  # Shape: (n_essays, n_trials)
        n_essays = len(trials_array)
        
        # Count perfect agreement (all trials give same grade)
        perfect_agreement = 0
        partial_agreement = 0
        no_agreement = 0
        
        agreement_per_essay = []
        
        for essay_trials in trials_array:
            unique_grades = set(essay_trials)
            n_unique = len(unique_grades)
            
            if n_unique == 1:
                perfect_agreement += 1
                agreement_per_essay.append(100.0)
            elif n_unique == 2:
                partial_agreement += 1
                # Calculate percentage based on majority
                grade_counts = pd.Series(essay_trials).value_counts()
                majority_pct = (grade_counts.iloc[0] / len(essay_trials)) * 100
                agreement_per_essay.append(majority_pct)
            else:
                no_agreement += 1
                agreement_per_essay.append(0.0)
        
        return {
            'perfect_agreement_count': perfect_agreement,
            'perfect_agreement_pct': (perfect_agreement / n_essays) * 100,
            'partial_agreement_count': partial_agreement,
            'partial_agreement_pct': (partial_agreement / n_essays) * 100,
            'no_agreement_count': no_agreement,
            'no_agreement_pct': (no_agreement / n_essays) * 100,
            'agreement_per_essay': agreement_per_essay,
            'mean_agreement': float(np.mean(agreement_per_essay)),
            'n_essays': n_essays,
            'n_trials': len(trials)
        }
    
    def _interpret_cv(self, cv: float) -> str:
        """Interpret Coefficient of Variation."""
        if cv < 10:
            return "Excellent consistency (CV < 10%)"
        elif cv < 20:
            return "Good consistency (10% ≤ CV < 20%)"
        elif cv < 30:
            return "Moderate consistency (20% ≤ CV < 30%)"
        else:
            return "Poor consistency (CV ≥ 30%)"
    
    def _interpret_icc(self, icc: float) -> str:
        """
        Interpret ICC value according to Koo & Li (2016).
        
        Reference:
        Koo, T. K., & Li, M. Y. (2016). A guideline of selecting and reporting
        intraclass correlation coefficients for reliability research.
        Journal of Chiropractic Medicine, 15(2), 155-163.
        """
        if icc < 0.40:
            return "Poor reliability"
        elif icc < 0.60:
            return "Fair reliability"
        elif icc < 0.75:
            return "Good reliability"
        else:
            return "Excellent reliability"
    
    def calculate_all_consistency(
        self,
        trials: List[List[str]],
        agent_name: str = "Agent",
        criterion_name: str = "Overall"
    ) -> Dict[str, any]:
        """
        Calculate all consistency metrics for an agent.
        
        This is the main function for analyzing trial consistency.
        
        Args:
            trials: List of trial results (4 trials expected)
            agent_name: Name of the agent (e.g., "ChatGPT", "Gemini")
            criterion_name: Name of the criterion being evaluated
        
        Returns:
            Comprehensive dictionary with all consistency metrics
        """
        sd = self.standard_deviation(trials, per_essay=True)
        cv = self.coefficient_of_variation(trials, per_essay=True)
        icc = self.intraclass_correlation(trials, icc_type='ICC(2,1)')
        agreement = self.agreement_percentage(trials)
        
        return {
            'agent': agent_name,
            'criterion': criterion_name,
            'n_trials': len(trials),
            'n_essays': len(trials[0]) if trials else 0,
            'standard_deviation': sd,
            'coefficient_of_variation': cv,
            'intraclass_correlation': icc,
            'agreement': agreement,
            'overall_assessment': self._overall_consistency_assessment(cv, icc, agreement)
        }
    
    def _overall_consistency_assessment(
        self,
        cv: Dict,
        icc: Dict,
        agreement: Dict
    ) -> str:
        """Generate overall consistency assessment."""
        cv_val = cv['mean_cv']
        icc_val = icc['icc']
        perfect_pct = agreement['perfect_agreement_pct']
        
        if icc_val >= 0.75 and cv_val < 20 and perfect_pct >= 60:
            return "Excellent: Agent shows very high consistency across trials"
        elif icc_val >= 0.60 and cv_val < 30 and perfect_pct >= 40:
            return "Good: Agent shows acceptable consistency across trials"
        elif icc_val >= 0.40:
            return "Fair: Agent shows moderate consistency, may need improvement"
        else:
            return "Poor: Agent shows low consistency, significant variability across trials"


if __name__ == "__main__":
    # Example usage
    print("=== Consistency Metrics Example ===\n")
    
    # Simulate 4 trials of grading 10 essays
    np.random.seed(42)
    trial1 = ['A', 'B', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']
    trial2 = ['A', 'B', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A']
    trial3 = ['A', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'A']
    trial4 = ['A', 'B', 'B', 'B', 'C', 'B', 'A', 'B', 'C', 'A']
    
    trials = [trial1, trial2, trial3, trial4]
    
    calculator = ConsistencyMetrics()
    results = calculator.calculate_all_consistency(trials, "ChatGPT", "Pemahaman Konten")
    
    print(f"Agent: {results['agent']}")
    print(f"Criterion: {results['criterion']}")
    print(f"Trials: {results['n_trials']}, Essays: {results['n_essays']}")
    
    print(f"\nStandard Deviation:")
    print(f"  Mean SD: {results['standard_deviation']['mean_sd']:.3f}")
    print(f"  Range: [{results['standard_deviation']['min_sd']:.3f}, {results['standard_deviation']['max_sd']:.3f}]")
    
    print(f"\nCoefficient of Variation:")
    print(f"  Mean CV: {results['coefficient_of_variation']['mean_cv']:.2f}%")
    print(f"  {results['coefficient_of_variation']['interpretation']}")
    
    print(f"\nIntraclass Correlation:")
    print(f"  ICC: {results['intraclass_correlation']['icc']:.3f}")
    print(f"  95% CI: [{results['intraclass_correlation']['ci_95_lower']:.3f}, {results['intraclass_correlation']['ci_95_upper']:.3f}]")
    print(f"  {results['intraclass_correlation']['interpretation']}")
    
    print(f"\nAgreement:")
    print(f"  Perfect agreement: {results['agreement']['perfect_agreement_pct']:.1f}%")
    print(f"  Mean agreement: {results['agreement']['mean_agreement']:.1f}%")
    
    print(f"\nOverall: {results['overall_assessment']}")
