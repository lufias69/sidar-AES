"""
Visualize Test-Retest Reliability for ChatGPT and Gemini
Creates box plots and heatmaps showing consistency across 10 trials
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def grade_to_numeric(grade):
    """Convert letter grade to numeric (4-0 scale)"""
    mapping = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    if isinstance(grade, str):
        return mapping.get(grade.upper(), None)
    return grade

def create_consistency_visualizations():
    """Create box plots and heatmaps for test-retest reliability"""
    
    # Connect to database
    db_path = Path(__file__).parent.parent / 'results' / 'grading_results.db'
    conn = sqlite3.connect(db_path)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'results' / 'figures'
    output_dir.mkdir(exist_ok=True)
    
    print("Creating consistency visualizations...")
    
    # ========== 1. BOX PLOTS: Score Distribution Across 10 Trials ==========
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, model in enumerate(['chatgpt', 'gemini']):
        # Query data
        query = f"""
        SELECT student_id, question_number, weighted_score, experiment_id
        FROM grading_results
        WHERE experiment_id LIKE 'exp_{model}_lenient_%'
        AND status = 'completed'
        ORDER BY student_id, question_number, experiment_id
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Create box plot showing distribution for each student-question pair
        # Group by student+question
        df['pair_id'] = df['student_id'] + '_Q' + df['question_number'].astype(str)
        
        # Get data for box plot (scores for each pair across 10 trials)
        plot_data = []
        pair_labels = []
        
        for pair_id, group in df.groupby('pair_id'):
            scores = group['weighted_score'].values
            if len(scores) >= 5:  # Only include pairs with sufficient data
                plot_data.append(scores)
                pair_labels.append(pair_id)
        
        # Create box plot
        ax = axes[idx]
        bp = ax.boxplot(plot_data, patch_artist=True, widths=0.6)
        
        # Color boxes
        for patch in bp['boxes']:
            patch.set_facecolor('#3498db' if model == 'chatgpt' else '#2ecc71')
            patch.set_alpha(0.6)
        
        # Styling
        ax.set_xlabel('Student-Question Pair', fontsize=12, fontweight='bold')
        ax.set_ylabel('Weighted Score (0-4 GPA Scale)', fontsize=12, fontweight='bold')
        ax.set_title(f'{"ChatGPT" if model == "chatgpt" else "Gemini"} - Score Consistency Across 10 Trials\n(ICC = {"0.9417" if model == "chatgpt" else "0.9487"})',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 4.2)
        
        # Reduce x-axis clutter (show every 5th label)
        ax.set_xticks(range(1, len(pair_labels)+1, 5))
        ax.set_xticklabels([pair_labels[i] for i in range(0, len(pair_labels), 5)], 
                          rotation=45, ha='right', fontsize=8)
        
        # Add horizontal line at median
        median_score = np.median([np.median(scores) for scores in plot_data])
        ax.axhline(y=median_score, color='red', linestyle='--', alpha=0.5, 
                  label=f'Overall Median = {median_score:.2f}')
        ax.legend()
        
        print(f"  - {model.upper()}: Box plot created ({len(plot_data)} pairs)")
    
    plt.tight_layout()
    plt.savefig(output_dir / 'consistency_boxplots.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Saved: {output_dir / 'consistency_boxplots.png'}")
    plt.close()
    
    # ========== 2. HEATMAP: Standard Deviation per Student-Question ==========
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    for idx, model in enumerate(['chatgpt', 'gemini']):
        # Query data
        query = f"""
        SELECT student_id, question_number, weighted_score
        FROM grading_results
        WHERE experiment_id LIKE 'exp_{model}_lenient_%'
        AND status = 'completed'
        ORDER BY student_id, question_number
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Calculate SD for each student-question pair
        sd_data = df.groupby(['student_id', 'question_number'])['weighted_score'].std().reset_index()
        sd_data.columns = ['student_id', 'question_number', 'sd']
        
        # Pivot to create heatmap matrix
        heatmap_matrix = sd_data.pivot(index='student_id', columns='question_number', values='sd')
        
        # Create heatmap
        ax = axes[idx]
        sns.heatmap(heatmap_matrix, annot=True, fmt='.3f', cmap='RdYlGn_r', 
                   cbar_kws={'label': 'Standard Deviation'},
                   vmin=0, vmax=0.5, ax=ax, linewidths=0.5)
        
        ax.set_title(f'{"ChatGPT" if model == "chatgpt" else "Gemini"} - Score Variability Heatmap\n(Mean SD = {"0.102" if model == "chatgpt" else "0.075"})',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Question Number', fontsize=12, fontweight='bold')
        ax.set_ylabel('Student ID', fontsize=12, fontweight='bold')
        
        print(f"  - {model.upper()}: Heatmap created")
    
    plt.tight_layout()
    plt.savefig(output_dir / 'consistency_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_dir / 'consistency_heatmap.png'}")
    plt.close()
    
    # ========== 3. HISTOGRAM: Distribution of Standard Deviations ==========
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, model in enumerate(['chatgpt', 'gemini']):
        # Query data
        query = f"""
        SELECT student_id, question_number, weighted_score
        FROM grading_results
        WHERE experiment_id LIKE 'exp_{model}_lenient_%'
        AND status = 'completed'
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Calculate SD for each pair
        sd_values = df.groupby(['student_id', 'question_number'])['weighted_score'].std()
        
        # Create histogram
        ax = axes[idx]
        ax.hist(sd_values, bins=20, color='#3498db' if model == 'chatgpt' else '#2ecc71', 
               alpha=0.7, edgecolor='black')
        
        # Add vertical lines for thresholds
        ax.axvline(x=0.1, color='green', linestyle='--', linewidth=2, 
                  label='High Consistency Threshold (SD ≤ 0.1)')
        ax.axvline(x=0.3, color='orange', linestyle='--', linewidth=2, 
                  label='Moderate Consistency Threshold (SD ≤ 0.3)')
        
        # Add statistics text
        mean_sd = sd_values.mean()
        median_sd = sd_values.median()
        high_pct = (sd_values <= 0.1).sum() / len(sd_values) * 100
        
        stats_text = f'Mean SD: {mean_sd:.3f}\nMedian SD: {median_sd:.3f}\nHigh Consistency: {high_pct:.1f}%'
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
               fontsize=11, fontweight='bold')
        
        # Styling
        ax.set_xlabel('Standard Deviation (SD)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency (Number of Student-Question Pairs)', fontsize=12, fontweight='bold')
        ax.set_title(f'{"ChatGPT" if model == "chatgpt" else "Gemini"} - Distribution of Score Variability',
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
        
        print(f"  - {model.upper()}: Histogram created")
    
    plt.tight_layout()
    plt.savefig(output_dir / 'consistency_histogram.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_dir / 'consistency_histogram.png'}")
    plt.close()
    
    # ========== 4. COMPARISON BAR CHART: Key Metrics ==========
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    metrics_data = {
        'ICC(2,1)': [0.9417, 0.9487],
        'Mean SD': [0.102, 0.075],
        'CV (%)': [4.21, 2.99],
        '% High\nConsistency': [70.0, 67.1],
        '% Low\nConsistency': [10.0, 4.3]
    }
    
    x = np.arange(len(metrics_data))
    width = 0.35
    
    chatgpt_values = [metrics_data[k][0] for k in metrics_data.keys()]
    gemini_values = [metrics_data[k][1] for k in metrics_data.keys()]
    
    # Normalize values for visualization (different scales)
    # ICC and % are already 0-100 scale, but SD and CV need scaling
    display_values_chatgpt = [
        0.9417 * 100,  # ICC to percentage
        0.102 * 100,   # SD to percentage-like scale
        4.21,          # CV already in %
        70.0,          # Already in %
        10.0           # Already in %
    ]
    
    display_values_gemini = [
        0.9487 * 100,
        0.075 * 100,
        2.99,
        67.1,
        4.3
    ]
    
    bars1 = ax.bar(x - width/2, display_values_chatgpt, width, 
                   label='ChatGPT', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, display_values_gemini, width,
                   label='Gemini', color='#2ecc71', alpha=0.8)
    
    # Add value labels on bars
    for bars, values in [(bars1, chatgpt_values), (bars2, gemini_values)]:
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.3f}' if val < 10 else f'{val:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Value (Normalized Scale)', fontsize=12, fontweight='bold')
    ax.set_title('Test-Retest Reliability: ChatGPT vs Gemini Comparison',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_data.keys(), fontsize=11, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add note about normalization
    note_text = 'Note: ICC and SD values scaled to 0-100 for visualization\nOriginal values shown on bars'
    ax.text(0.98, 0.02, note_text, transform=ax.transAxes,
           verticalalignment='bottom', horizontalalignment='right',
           fontsize=9, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'consistency_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {output_dir / 'consistency_comparison.png'}")
    plt.close()
    
    conn.close()
    
    print("\n" + "="*60)
    print("🎨 ALL CONSISTENCY VISUALIZATIONS COMPLETED!")
    print("="*60)
    print("\nCreated 4 figures:")
    print("  1. consistency_boxplots.png - Score distributions across trials")
    print("  2. consistency_heatmap.png - SD heatmap by student-question")
    print("  3. consistency_histogram.png - SD distribution with thresholds")
    print("  4. consistency_comparison.png - Key metrics comparison")
    print(f"\nAll saved to: {output_dir}")

if __name__ == '__main__':
    create_consistency_visualizations()
