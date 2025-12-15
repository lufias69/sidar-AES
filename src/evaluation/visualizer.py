"""
Metrics Visualizer Module

Creates publication-ready visualizations for AES research paper:
- Box plots for consistency
- Confusion matrices
- Agreement heatmaps
- Distribution comparisons
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class MetricsVisualizer:
    """
    Create publication-ready visualizations for AES metrics.
    
    All plots optimized for academic publications (300 DPI, proper fonts).
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-paper', dpi: int = 300):
        """
        Initialize visualizer with publication settings.
        
        Args:
            style: Matplotlib style (default: seaborn-paper)
            dpi: Resolution for saved figures (default: 300 for publication)
        """
        # Set publication-ready style
        plt.style.use('default')
        sns.set_theme(style='whitegrid', palette='muted')
        
        self.dpi = dpi
        self.figsize_single = (8, 6)
        self.figsize_double = (12, 6)
        self.figsize_grid = (10, 8)
        
        # Color palette for agents
        self.colors = {
            'ChatGPT': '#10a37f',  # OpenAI green
            'Gemini': '#4285f4',    # Google blue
            'Lecturer': '#ea4335'   # Reference red
        }
    
    def plot_consistency_boxplot(
        self,
        consistency_results: Dict[str, Dict],
        criterion_name: str = "Overall",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create box plot showing consistency across trials for each agent.
        
        Args:
            consistency_results: Dictionary mapping agent names to consistency metrics
                                Example: {'ChatGPT': {...}, 'Gemini': {...}}
            criterion_name: Name of criterion
            save_path: Path to save figure (optional)
        
        Returns:
            Matplotlib figure object
        """
        fig, axes = plt.subplots(1, 2, figsize=self.figsize_double)
        
        # Extract data
        agents = list(consistency_results.keys())
        sd_data = [consistency_results[agent]['standard_deviation']['sd_per_essay'] 
                   for agent in agents]
        cv_data = [consistency_results[agent]['coefficient_of_variation']['cv_per_essay'] 
                   for agent in agents]
        
        # Standard Deviation box plot
        bp1 = axes[0].boxplot(sd_data, labels=agents, patch_artist=True)
        for patch, agent in zip(bp1['boxes'], agents):
            patch.set_facecolor(self.colors.get(agent, '#999999'))
        axes[0].set_ylabel('Standard Deviation', fontsize=12)
        axes[0].set_title(f'Consistency: SD across Trials\n({criterion_name})', fontsize=13, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Coefficient of Variation box plot
        bp2 = axes[1].boxplot(cv_data, labels=agents, patch_artist=True)
        for patch, agent in zip(bp2['boxes'], agents):
            patch.set_facecolor(self.colors.get(agent, '#999999'))
        axes[1].set_ylabel('Coefficient of Variation (%)', fontsize=12)
        axes[1].set_title(f'Consistency: CV across Trials\n({criterion_name})', fontsize=13, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_confusion_matrix(
        self,
        confusion_matrix: np.ndarray,
        labels: List[str],
        agent_name: str = "Agent",
        criterion_name: str = "Overall",
        normalize: bool = True,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create confusion matrix heatmap.
        
        Args:
            confusion_matrix: Confusion matrix array
            labels: Grade labels
            agent_name: Name of agent
            criterion_name: Name of criterion
            normalize: If True, normalize by row (true label)
            save_path: Path to save figure
        
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize_single)
        
        # Normalize if requested
        if normalize:
            cm = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]
            cm = np.nan_to_num(cm)
            fmt = '.2%'
            values = cm * 100  # Show as percentage
        else:
            cm = confusion_matrix
            fmt = 'd'
            values = cm
        
        # Create heatmap
        sns.heatmap(
            values,
            annot=True,
            fmt=fmt if normalize else 'd',
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
            cbar_kws={'label': 'Percentage' if normalize else 'Count'},
            ax=ax,
            square=True
        )
        
        ax.set_xlabel('Predicted Grade', fontsize=12, fontweight='bold')
        ax.set_ylabel('True Grade (Lecturer)', fontsize=12, fontweight='bold')
        ax.set_title(f'Confusion Matrix: {agent_name}\n({criterion_name})', 
                     fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_agreement_heatmap(
        self,
        agreement_matrix: pd.DataFrame,
        criterion_name: str = "Overall",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create heatmap of pairwise agreement (Cohen's Kappa).
        
        Args:
            agreement_matrix: DataFrame with pairwise kappa values
            criterion_name: Name of criterion
            save_path: Path to save figure
        
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize_single)
        
        # Create heatmap
        sns.heatmap(
            agreement_matrix,
            annot=True,
            fmt='.3f',
            cmap='RdYlGn',
            center=0.5,
            vmin=0,
            vmax=1,
            cbar_kws={'label': "Cohen's Kappa"},
            ax=ax,
            square=True
        )
        
        ax.set_title(f"Pairwise Agreement (Cohen's Kappa)\n({criterion_name})", 
                     fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_grade_distribution_comparison(
        self,
        distributions: Dict[str, Dict[str, int]],
        criterion_name: str = "Overall",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare grade distributions between agents and lecturer.
        
        Args:
            distributions: Dict mapping agent names to grade distributions
                          Example: {'ChatGPT': {'A': 10, 'B': 20, ...}, ...}
            criterion_name: Name of criterion
            save_path: Path to save figure
        
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize_single)
        
        # Prepare data
        df = pd.DataFrame(distributions).fillna(0)
        
        # Create grouped bar plot
        df.plot(kind='bar', ax=ax, color=[self.colors.get(col, '#999999') for col in df.columns])
        
        ax.set_xlabel('Grade', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title(f'Grade Distribution Comparison\n({criterion_name})', 
                     fontsize=13, fontweight='bold')
        ax.legend(title='Rater', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=0)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_accuracy_comparison(
        self,
        accuracy_results: Dict[str, Dict],
        criterion_name: str = "Overall",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare accuracy metrics across agents.
        
        Args:
            accuracy_results: Dict mapping agent names to accuracy metrics
            criterion_name: Name of criterion
            save_path: Path to save figure
        
        Returns:
            Matplotlib figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=self.figsize_grid)
        
        agents = list(accuracy_results.keys())
        
        # Extract metrics
        mae_values = [accuracy_results[agent]['mae']['mae'] for agent in agents]
        rmse_values = [accuracy_results[agent]['rmse']['rmse'] for agent in agents]
        f1_values = [accuracy_results[agent]['precision_recall_f1']['f1_score'] for agent in agents]
        exact_match = [accuracy_results[agent]['mae']['exact_match_pct'] for agent in agents]
        
        colors_list = [self.colors.get(agent, '#999999') for agent in agents]
        
        # MAE
        axes[0, 0].bar(agents, mae_values, color=colors_list)
        axes[0, 0].set_ylabel('MAE', fontsize=11)
        axes[0, 0].set_title('Mean Absolute Error', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # RMSE
        axes[0, 1].bar(agents, rmse_values, color=colors_list)
        axes[0, 1].set_ylabel('RMSE', fontsize=11)
        axes[0, 1].set_title('Root Mean Square Error', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # F1-Score
        axes[1, 0].bar(agents, f1_values, color=colors_list)
        axes[1, 0].set_ylabel('F1-Score', fontsize=11)
        axes[1, 0].set_title('F1-Score (Weighted)', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylim([0, 1])
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Exact Match %
        axes[1, 1].bar(agents, exact_match, color=colors_list)
        axes[1, 1].set_ylabel('Exact Match (%)', fontsize=11)
        axes[1, 1].set_title('Exact Match Percentage', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylim([0, 100])
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        fig.suptitle(f'Accuracy Metrics Comparison\n({criterion_name})', 
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_icc_comparison(
        self,
        icc_results: Dict[str, Dict],
        criterion_name: str = "Overall",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare ICC values across agents with confidence intervals.
        
        Args:
            icc_results: Dict mapping agent names to ICC metrics
            criterion_name: Name of criterion
            save_path: Path to save figure
        
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize_single)
        
        agents = list(icc_results.keys())
        icc_values = [icc_results[agent]['intraclass_correlation']['icc'] for agent in agents]
        ci_lower = [icc_results[agent]['intraclass_correlation']['ci_95_lower'] for agent in agents]
        ci_upper = [icc_results[agent]['intraclass_correlation']['ci_95_upper'] for agent in agents]
        
        colors_list = [self.colors.get(agent, '#999999') for agent in agents]
        
        # Create bar plot with error bars
        x_pos = np.arange(len(agents))
        bars = ax.bar(x_pos, icc_values, color=colors_list, alpha=0.7, edgecolor='black')
        
        # Add confidence intervals
        errors = [[icc_values[i] - ci_lower[i], ci_upper[i] - icc_values[i]] 
                  for i in range(len(agents))]
        errors = np.array(errors).T
        ax.errorbar(x_pos, icc_values, yerr=errors, fmt='none', ecolor='black', capsize=5, capthick=2)
        
        # Add ICC interpretation lines
        ax.axhline(y=0.75, color='green', linestyle='--', alpha=0.5, label='Excellent (≥0.75)')
        ax.axhline(y=0.60, color='orange', linestyle='--', alpha=0.5, label='Good (≥0.60)')
        ax.axhline(y=0.40, color='red', linestyle='--', alpha=0.5, label='Fair (≥0.40)')
        
        ax.set_ylabel('ICC Value', fontsize=12, fontweight='bold')
        ax.set_xlabel('Agent', fontsize=12)
        ax.set_title(f'Intraclass Correlation Coefficient (ICC)\n({criterion_name})', 
                     fontsize=13, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(agents)
        ax.set_ylim([0, 1])
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        
        return fig
    
    def create_comprehensive_report(
        self,
        agreement_results: Dict,
        consistency_results: Dict[str, Dict],
        accuracy_results: Dict[str, Dict],
        criterion_name: str = "Overall",
        output_dir: str = "results/figures"
    ) -> Dict[str, str]:
        """
        Create all visualizations for a comprehensive report.
        
        Args:
            agreement_results: Results from AgreementMetrics
            consistency_results: Results from ConsistencyMetrics per agent
            accuracy_results: Results from AccuracyMetrics per agent
            criterion_name: Name of criterion
            output_dir: Directory to save figures
        
        Returns:
            Dictionary mapping figure names to file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_figures = {}
        
        # Consistency box plots
        fig1_path = output_path / f"consistency_boxplot_{criterion_name}.png"
        self.plot_consistency_boxplot(consistency_results, criterion_name, str(fig1_path))
        saved_figures['consistency_boxplot'] = str(fig1_path)
        plt.close()
        
        # Agreement heatmap
        agreement_matrix = pd.DataFrame(agreement_results['agreement_matrix'])
        fig2_path = output_path / f"agreement_heatmap_{criterion_name}.png"
        self.plot_agreement_heatmap(agreement_matrix, criterion_name, str(fig2_path))
        saved_figures['agreement_heatmap'] = str(fig2_path)
        plt.close()
        
        # Accuracy comparison
        fig3_path = output_path / f"accuracy_comparison_{criterion_name}.png"
        self.plot_accuracy_comparison(accuracy_results, criterion_name, str(fig3_path))
        saved_figures['accuracy_comparison'] = str(fig3_path)
        plt.close()
        
        # ICC comparison
        fig4_path = output_path / f"icc_comparison_{criterion_name}.png"
        self.plot_icc_comparison(consistency_results, criterion_name, str(fig4_path))
        saved_figures['icc_comparison'] = str(fig4_path)
        plt.close()
        
        # Confusion matrices for each agent
        for agent_name, accuracy_data in accuracy_results.items():
            cm = np.array(accuracy_data['confusion_matrix']['confusion_matrix'])
            labels = accuracy_data['confusion_matrix']['labels']
            fig_cm_path = output_path / f"confusion_matrix_{agent_name}_{criterion_name}.png"
            self.plot_confusion_matrix(cm, labels, agent_name, criterion_name, 
                                      normalize=True, save_path=str(fig_cm_path))
            saved_figures[f'confusion_matrix_{agent_name}'] = str(fig_cm_path)
            plt.close()
        
        print(f"✅ Created {len(saved_figures)} figures in {output_dir}")
        return saved_figures


if __name__ == "__main__":
    # Example usage
    print("=== Metrics Visualizer Example ===\n")
    
    # Simulate some data
    import numpy as np
    np.random.seed(42)
    
    visualizer = MetricsVisualizer()
    
    # Example: Consistency box plot
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
    
    fig = visualizer.plot_consistency_boxplot(consistency_data, "Pemahaman Konten")
    plt.show()
    print("Created consistency box plot")
