#!/usr/bin/env python3
"""
Create publication-quality visualizations for AES research paper
"""
import sqlite3
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# Set style for publication
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

# Create output directory
OUTPUT_DIR = Path('results/figures')
OUTPUT_DIR.mkdir(exist_ok=True)

def score_to_grade(score):
    """Convert GPA score to letter grade"""
    if score >= 3.5:
        return 'A'
    elif score >= 2.5:
        return 'B'
    elif score >= 1.5:
        return 'C'
    elif score >= 0.5:
        return 'D'
    else:
        return 'E'

def load_gold_standard():
    """Load gold standard grades"""
    gold_dir = Path('results/gold_standard')
    gold_data = {}
    
    for json_file in gold_dir.glob('student_*_gold.json'):
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
            student_name = data['student_name']
            # Extract student_id from name
            student_num = ''.join(filter(str.isdigit, student_name))
            if student_num:
                student_id = f"student_{int(student_num):02d}"
            else:
                continue
                
            for q_idx, q in enumerate(data['questions'], start=1):
                score = q['weighted_score']
                gold_data[(student_id, q_idx)] = score
    
    return gold_data

def create_confusion_matrix():
    """Create confusion matrix: Gold Standard vs AI predictions"""
    print("\n" + "="*80)
    print("1. Creating Confusion Matrices...")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    # For each model and strategy
    configs = [
        ('chatgpt', 'lenient', 'exp_chatgpt_lenient_01'),
        ('gemini', 'lenient', 'exp_gemini_lenient_01'),
        ('chatgpt', 'zero-shot', 'exp_chatgpt_zero'),
        ('gemini', 'zero-shot', 'exp_gemini_zero'),
    ]
    
    for model, strategy, exp_id in configs:
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        # Add gold standard
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        
        # Convert to grades
        df['ai_grade'] = df['weighted_score'].apply(score_to_grade)
        df['gold_grade'] = df['gold_score'].apply(score_to_grade)
        
        # Drop nulls
        df = df.dropna()
        
        # Create confusion matrix
        grades = ['A', 'B', 'C', 'D', 'E']
        cm = pd.crosstab(df['gold_grade'], df['ai_grade'], 
                         rownames=['Gold Standard'], colnames=[f'{model.upper()}'],
                         margins=True)
        
        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm.iloc[:-1, :-1], annot=True, fmt='d', cmap='Blues', ax=ax,
                   cbar_kws={'label': 'Count'})
        ax.set_title(f'Confusion Matrix: {model.upper()} ({strategy})\nGold Standard vs AI Grades')
        ax.set_xlabel('AI Predicted Grade')
        ax.set_ylabel('Gold Standard Grade')
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f'confusion_matrix_{model}_{strategy.replace("-", "")}.png')
        plt.close()
        
        print(f"  ✓ Created confusion matrix for {model} ({strategy})")
    
    conn.close()

def create_strategy_comparison():
    """Create bar chart comparing strategies"""
    print("\n" + "="*80)
    print("2. Creating Strategy Comparison Charts...")
    print("="*80)
    
    # Data from analysis results
    data = {
        'ChatGPT': {
            'Lenient': {'MAE': 0.300, 'Exact_Match': 70.0, 'Correlation': 0.672},
            'Few-shot': {'MAE': 0.514, 'Exact_Match': 50.0, 'Correlation': 0.703},
            'Zero-shot': {'MAE': 0.614, 'Exact_Match': 47.1, 'Correlation': 0.651},
        },
        'Gemini': {
            'Lenient': {'MAE': 0.171, 'Exact_Match': 82.9, 'Correlation': 0.810},
            'Few-shot': {'MAE': 0.200, 'Exact_Match': 80.0, 'Correlation': 0.747},
            'Zero-shot': {'MAE': 0.314, 'Exact_Match': 68.6, 'Correlation': 0.716},
        }
    }
    
    # Prepare data for plotting
    strategies = ['Lenient', 'Few-shot', 'Zero-shot']
    metrics = ['MAE', 'Exact_Match', 'Correlation']
    metric_labels = ['MAE (lower is better)', 'Exact Match (%)', 'Correlation (r)']
    
    for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(strategies))
        width = 0.35
        
        chatgpt_values = [data['ChatGPT'][s][metric] for s in strategies]
        gemini_values = [data['Gemini'][s][metric] for s in strategies]
        
        bars1 = ax.bar(x - width/2, chatgpt_values, width, label='ChatGPT', alpha=0.8)
        bars2 = ax.bar(x + width/2, gemini_values, width, label='Gemini', alpha=0.8)
        
        ax.set_xlabel('Prompting Strategy', fontweight='bold')
        ax.set_ylabel(label, fontweight='bold')
        ax.set_title(f'Strategy Comparison: {label}', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(strategies)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}' if metric == 'MAE' else f'{height:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f'strategy_comparison_{metric.lower()}.png')
        plt.close()
        
        print(f"  ✓ Created strategy comparison chart for {metric}")

def create_per_rubric_heatmap():
    """Create heatmap showing per-rubric accuracy"""
    print("\n" + "="*80)
    print("3. Creating Per-Rubric Accuracy Heatmap...")
    print("="*80)
    
    # Data from per-rubric analysis
    data = {
        'ChatGPT': {
            'Pemahaman Konten': 69.14,
            'Organisasi & Struktur': 51.86,
            'Argumen & Bukti': 74.00,
            'Gaya Bahasa & Mekanik': 73.57,
        },
        'Gemini': {
            'Pemahaman Konten': 81.29,
            'Organisasi & Struktur': 61.00,
            'Argumen & Bukti': 83.29,
            'Gaya Bahasa & Mekanik': 65.43,
        }
    }
    
    df = pd.DataFrame(data).T
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(df, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax,
               cbar_kws={'label': 'Accuracy (%)'}, vmin=50, vmax=85)
    ax.set_title('Per-Rubric Accuracy: ChatGPT vs Gemini (Lenient Strategy)', 
                fontsize=12, fontweight='bold')
    ax.set_xlabel('Rubric', fontweight='bold')
    ax.set_ylabel('Model', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'per_rubric_accuracy_heatmap.png')
    plt.close()
    
    print("  ✓ Created per-rubric accuracy heatmap")

def create_correlation_scatterplots():
    """Create scatter plots showing correlation with gold standard"""
    print("\n" + "="*80)
    print("4. Creating Correlation Scatter Plots...")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    gold_data = load_gold_standard()
    
    # For each model (lenient strategy)
    configs = [
        ('chatgpt', 'exp_chatgpt_lenient_01'),
        ('gemini', 'exp_gemini_lenient_01'),
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, (model, exp_id) in enumerate(configs):
        df = pd.read_sql_query(f"""
            SELECT student_id, question_number, weighted_score
            FROM grading_results
            WHERE experiment_id = '{exp_id}' AND status = 'completed'
        """, conn)
        
        # Add gold standard
        df['gold_score'] = df.apply(
            lambda row: gold_data.get((row['student_id'], row['question_number'])),
            axis=1
        )
        
        # Drop nulls
        df = df.dropna()
        
        ax = axes[idx]
        
        # Scatter plot
        ax.scatter(df['gold_score'], df['weighted_score'], alpha=0.6, s=50)
        
        # Regression line
        z = np.polyfit(df['gold_score'], df['weighted_score'], 1)
        p = np.poly1d(z)
        ax.plot(df['gold_score'], p(df['gold_score']), "r--", alpha=0.8, linewidth=2)
        
        # Perfect prediction line
        ax.plot([1, 4], [1, 4], 'k-', alpha=0.3, linewidth=1, label='Perfect prediction')
        
        # Calculate correlation
        r, p_value = stats.pearsonr(df['gold_score'], df['weighted_score'])
        
        ax.set_xlabel('Gold Standard Score', fontweight='bold')
        ax.set_ylabel('AI Predicted Score', fontweight='bold')
        ax.set_title(f'{model.upper()} (Lenient)\nr = {r:.3f}, p < 0.0001', 
                    fontsize=11, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend()
        ax.set_xlim([1, 4])
        ax.set_ylim([1, 4])
        
        print(f"  ✓ Created scatter plot for {model}")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_scatterplots.png')
    plt.close()
    
    conn.close()

def create_grade_distribution():
    """Create grade distribution comparison"""
    print("\n" + "="*80)
    print("5. Creating Grade Distribution Charts...")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, model in enumerate(['chatgpt', 'gemini']):
        df = pd.read_sql_query(f"""
            SELECT weighted_score
            FROM grading_results
            WHERE model = '{model}' 
            AND strategy = 'lenient'
            AND status = 'completed'
        """, conn)
        
        df['grade'] = df['weighted_score'].apply(score_to_grade)
        grade_counts = df['grade'].value_counts().reindex(['A', 'B', 'C', 'D', 'E'], fill_value=0)
        
        ax = axes[idx]
        bars = ax.bar(grade_counts.index, grade_counts.values, alpha=0.8, 
                     color=plt.cm.RdYlGn(np.linspace(0.8, 0.2, 5)))
        
        ax.set_xlabel('Grade', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title(f'{model.upper()} Grade Distribution (Lenient Strategy)', 
                    fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom')
        
        print(f"  ✓ Created grade distribution for {model}")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'grade_distributions.png')
    plt.close()
    
    conn.close()

def main():
    print("\n" + "="*80)
    print("CREATING PUBLICATION-QUALITY VISUALIZATIONS")
    print("="*80)
    
    create_confusion_matrix()
    create_strategy_comparison()
    create_per_rubric_heatmap()
    create_correlation_scatterplots()
    create_grade_distribution()
    
    print("\n" + "="*80)
    print("✓ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
    print(f"✓ Saved to: {OUTPUT_DIR}")
    print("="*80)
    
    # List all created files
    print("\nCreated files:")
    for file in sorted(OUTPUT_DIR.glob('*.png')):
        print(f"  - {file.name}")

if __name__ == "__main__":
    main()
