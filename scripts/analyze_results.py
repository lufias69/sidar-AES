"""
Analysis Script - Process Experiment Results

This script processes experiment results and generates comprehensive analysis:
1. Load experiment results
2. Calculate all metrics (agreement, consistency, accuracy)
3. Generate visualizations
4. Create LaTeX-formatted tables
5. Export comprehensive report
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation.agreement import AgreementMetrics
from src.evaluation.consistency import ConsistencyMetrics
from src.evaluation.accuracy import AccuracyMetrics
from src.evaluation.visualizer import MetricsVisualizer
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultsAnalyzer:
    """
    Comprehensive analyzer for AES experiment results.
    """
    
    def __init__(self, results_dir: str = "results"):
        """
        Initialize analyzer.
        
        Args:
            results_dir: Directory containing experiment results
        """
        self.results_dir = Path(results_dir)
        self.agreement_calc = AgreementMetrics()
        self.consistency_calc = ConsistencyMetrics()
        self.accuracy_calc = AccuracyMetrics()
        self.visualizer = MetricsVisualizer()
    
    def load_experiment_results(self, experiment_name: str = "experiment") -> Dict:
        """Load all results from an experiment."""
        exp_dir = self.results_dir / experiment_name
        
        if not exp_dir.exists():
            raise FileNotFoundError(f"Experiment directory not found: {exp_dir}")
        
        # Load all_results.json
        results_file = exp_dir / "all_results.json"
        with open(results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        logger.info(f"Loaded results from {results_file}")
        return results
    
    def organize_results_by_criterion(self, results: Dict) -> Dict[str, Dict]:
        """
        Organize results by criterion for analysis.
        
        Returns:
            Dict mapping criterion names to organized data
        """
        organized = {}
        
        # Get rubric criteria
        rubric = results['metadata']['rubric']
        criteria = list(rubric['criteria'].keys())
        
        # Organize by criterion
        for criterion in criteria:
            organized[criterion] = {
                'chatgpt': {'trials': [[] for _ in range(4)]},
                'gemini': {'trials': [[] for _ in range(4)]},
                'lecturer': []
            }
        
        # Process each trial
        for trial_idx, trial_data in enumerate(results['trials']):
            for essay in trial_data['results']:
                # Get lecturer scores
                if trial_idx == 0:  # Only add lecturer once
                    for criterion in criteria:
                        lecturer_grade = essay['lecturer_scores'][criterion]['grade']
                        organized[criterion]['lecturer'].append(lecturer_grade)
                
                # ChatGPT scores
                if 'chatgpt_result' in essay and essay['chatgpt_result']:
                    for criterion in criteria:
                        grade = essay['chatgpt_result']['grades'][criterion]['grade']
                        organized[criterion]['chatgpt']['trials'][trial_idx].append(grade)
                
                # Gemini scores
                if 'gemini_result' in essay and essay['gemini_result']:
                    for criterion in criteria:
                        grade = essay['gemini_result']['grades'][criterion]['grade']
                        organized[criterion]['gemini']['trials'][trial_idx].append(grade)
        
        return organized
    
    def calculate_all_metrics(self, organized_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Calculate all metrics for all criteria.
        
        Returns:
            Comprehensive metrics dictionary
        """
        all_metrics = {}
        
        for criterion, data in organized_data.items():
            logger.info(f"Calculating metrics for criterion: {criterion}")
            
            # Get average scores across trials for agreement analysis
            chatgpt_avg = self._get_average_grades(data['chatgpt']['trials'])
            gemini_avg = self._get_average_grades(data['gemini']['trials'])
            lecturer = data['lecturer']
            
            # Agreement metrics (Fleiss' Kappa)
            agreement = self.agreement_calc.calculate_all_agreements(
                chatgpt_avg, gemini_avg, lecturer, criterion
            )
            
            # Consistency metrics (per agent)
            chatgpt_consistency = self.consistency_calc.calculate_all_consistency(
                data['chatgpt']['trials'], "ChatGPT", criterion
            )
            gemini_consistency = self.consistency_calc.calculate_all_consistency(
                data['gemini']['trials'], "Gemini", criterion
            )
            
            # Accuracy metrics (per agent)
            chatgpt_accuracy = self.accuracy_calc.calculate_all_accuracy(
                chatgpt_avg, lecturer, "ChatGPT", criterion
            )
            gemini_accuracy = self.accuracy_calc.calculate_all_accuracy(
                gemini_avg, lecturer, "Gemini", criterion
            )
            
            all_metrics[criterion] = {
                'agreement': agreement,
                'consistency': {
                    'ChatGPT': chatgpt_consistency,
                    'Gemini': gemini_consistency
                },
                'accuracy': {
                    'ChatGPT': chatgpt_accuracy,
                    'Gemini': gemini_accuracy
                }
            }
        
        return all_metrics
    
    def _get_average_grades(self, trials: List[List[str]]) -> List[str]:
        """
        Get average grade across trials using mode (most common).
        """
        if not trials or not trials[0]:
            return []
        
        n_essays = len(trials[0])
        avg_grades = []
        
        for i in range(n_essays):
            essay_grades = [trial[i] for trial in trials if i < len(trial)]
            # Use mode (most common grade)
            mode_grade = pd.Series(essay_grades).mode()[0]
            avg_grades.append(mode_grade)
        
        return avg_grades
    
    def generate_summary_table(self, metrics: Dict[str, Dict]) -> pd.DataFrame:
        """
        Generate summary table for all criteria.
        
        Returns:
            DataFrame with key metrics for each criterion
        """
        rows = []
        
        for criterion, data in metrics.items():
            # Agreement
            fleiss_kappa = data['agreement']['fleiss_kappa']['kappa']
            
            # Consistency
            chatgpt_icc = data['consistency']['ChatGPT']['intraclass_correlation']['icc']
            gemini_icc = data['consistency']['Gemini']['intraclass_correlation']['icc']
            chatgpt_cv = data['consistency']['ChatGPT']['coefficient_of_variation']['mean_cv']
            gemini_cv = data['consistency']['Gemini']['coefficient_of_variation']['mean_cv']
            
            # Accuracy
            chatgpt_mae = data['accuracy']['ChatGPT']['mae']['mae']
            gemini_mae = data['accuracy']['Gemini']['mae']['mae']
            chatgpt_f1 = data['accuracy']['ChatGPT']['precision_recall_f1']['f1_score']
            gemini_f1 = data['accuracy']['Gemini']['precision_recall_f1']['f1_score']
            
            rows.append({
                'Criterion': criterion,
                'Fleiss Kappa': f"{fleiss_kappa:.3f}",
                'ChatGPT ICC': f"{chatgpt_icc:.3f}",
                'Gemini ICC': f"{gemini_icc:.3f}",
                'ChatGPT CV (%)': f"{chatgpt_cv:.1f}",
                'Gemini CV (%)': f"{gemini_cv:.1f}",
                'ChatGPT MAE': f"{chatgpt_mae:.3f}",
                'Gemini MAE': f"{gemini_mae:.3f}",
                'ChatGPT F1': f"{chatgpt_f1:.3f}",
                'Gemini F1': f"{gemini_f1:.3f}"
            })
        
        return pd.DataFrame(rows)
    
    def export_latex_table(self, df: pd.DataFrame, output_path: str):
        """Export summary table as LaTeX."""
        latex = df.to_latex(
            index=False,
            caption="Summary of Evaluation Metrics Across Criteria",
            label="tab:metrics_summary",
            position='htbp',
            column_format='l' + 'c' * (len(df.columns) - 1)
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex)
        
        logger.info(f"Exported LaTeX table to {output_path}")
    
    def create_comprehensive_report(
        self,
        experiment_name: str = "experiment",
        output_dir: Optional[str] = None
    ):
        """
        Create comprehensive analysis report.
        
        This is the main function to run after experiments complete.
        """
        if output_dir is None:
            output_dir = self.results_dir / experiment_name / "analysis"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("="*50)
        logger.info("STARTING COMPREHENSIVE ANALYSIS")
        logger.info("="*50)
        
        # Step 1: Load results
        logger.info("\n[1/5] Loading experiment results...")
        results = self.load_experiment_results(experiment_name)
        
        # Step 2: Organize data
        logger.info("\n[2/5] Organizing data by criterion...")
        organized = self.organize_results_by_criterion(results)
        
        # Step 3: Calculate metrics
        logger.info("\n[3/5] Calculating all metrics...")
        metrics = self.calculate_all_metrics(organized)
        
        # Step 4: Generate visualizations
        logger.info("\n[4/5] Generating visualizations...")
        figures_dir = output_dir / "figures"
        for criterion, criterion_metrics in metrics.items():
            self.visualizer.create_comprehensive_report(
                criterion_metrics['agreement'],
                criterion_metrics['consistency'],
                criterion_metrics['accuracy'],
                criterion,
                str(figures_dir)
            )
        
        # Step 5: Create summary tables
        logger.info("\n[5/5] Creating summary tables...")
        summary_df = self.generate_summary_table(metrics)
        
        # Save summary
        summary_csv = output_dir / "metrics_summary.csv"
        summary_df.to_csv(summary_csv, index=False)
        logger.info(f"Saved CSV summary: {summary_csv}")
        
        # Export LaTeX
        summary_latex = output_dir / "metrics_summary.tex"
        self.export_latex_table(summary_df, str(summary_latex))
        
        # Save complete metrics as JSON
        metrics_json = output_dir / "complete_metrics.json"
        with open(metrics_json, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Saved complete metrics: {metrics_json}")
        
        # Print summary to console
        logger.info("\n" + "="*50)
        logger.info("METRICS SUMMARY")
        logger.info("="*50)
        print("\n" + summary_df.to_string(index=False))
        
        logger.info("\n" + "="*50)
        logger.info(f"✅ ANALYSIS COMPLETE! Results saved to: {output_dir}")
        logger.info("="*50)
        
        return metrics, summary_df


def main():
    """Main entry point for analysis script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyze AES experiment results and generate comprehensive report"
    )
    parser.add_argument(
        '--experiment',
        type=str,
        default='experiment',
        help='Name of experiment directory (default: experiment)'
    )
    parser.add_argument(
        '--results-dir',
        type=str,
        default='results',
        help='Base results directory (default: results)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output directory for analysis (default: results/<experiment>/analysis)'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = ResultsAnalyzer(results_dir=args.results_dir)
    
    # Run comprehensive analysis
    try:
        metrics, summary = analyzer.create_comprehensive_report(
            experiment_name=args.experiment,
            output_dir=args.output
        )
        print("\n✅ Analysis completed successfully!")
        return 0
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
