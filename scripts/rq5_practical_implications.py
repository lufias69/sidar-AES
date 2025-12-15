"""
RQ5: Practical Implications Analysis

Operational metrics, cost analysis, and deployment considerations.

Analyses:
- Execution time and throughput
- API cost comparison
- Scalability projections
- Resource requirements
- Deployment recommendations
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def calculate_throughput_metrics(df, model_name):
    """Calculate throughput and timing metrics."""
    # Average time per grading
    avg_time = df['api_call_time'].mean()
    std_time = df['api_call_time'].std()
    
    # Throughput (gradings per minute)
    throughput_per_min = 60 / avg_time if avg_time > 0 else 0
    
    # Tokens
    avg_tokens = df['tokens_used'].mean()
    std_tokens = df['tokens_used'].std()
    
    # Time per question (since we have 7 questions per essay)
    # Assuming sequential processing
    time_per_essay = avg_time * 7
    
    return {
        'model': model_name,
        'avg_time': avg_time,
        'std_time': std_time,
        'avg_tokens': avg_tokens,
        'std_tokens': std_tokens,
        'throughput_per_min': throughput_per_min,
        'throughput_per_hour': throughput_per_min * 60,
        'time_per_essay': time_per_essay
    }


def calculate_cost_metrics(df, model_name):
    """Calculate cost metrics with realistic API pricing."""
    # Realistic API pricing (as of Dec 2024)
    # ChatGPT-4o: ~$0.005/1K input tokens, ~$0.015/1K output tokens
    # Gemini-1.5-Pro: ~$0.00125/1K input tokens, ~$0.005/1K output tokens
    
    avg_tokens = df['tokens_used'].mean()
    
    if model_name == 'ChatGPT':
        # Assume 70% input, 30% output ratio
        input_tokens = avg_tokens * 0.7
        output_tokens = avg_tokens * 0.3
        cost_per_grading = (input_tokens / 1000 * 0.005) + (output_tokens / 1000 * 0.015)
    else:  # Gemini
        input_tokens = avg_tokens * 0.7
        output_tokens = avg_tokens * 0.3
        cost_per_grading = (input_tokens / 1000 * 0.00125) + (output_tokens / 1000 * 0.005)
    
    # Cost per essay (7 questions)
    cost_per_essay = cost_per_grading * 7
    
    # Scaling scenarios
    costs = {
        'model': model_name,
        'cost_per_grading': cost_per_grading,
        'cost_per_essay': cost_per_essay,
        'cost_100_essays': cost_per_essay * 100,
        'cost_1000_essays': cost_per_essay * 1000,
        'cost_10000_essays': cost_per_essay * 10000,
        'avg_tokens': avg_tokens
    }
    
    return costs


def project_scalability(throughput, costs):
    """Project scalability for different use cases."""
    scenarios = {
        'Small class (30 students)': {
            'students': 30,
            'essays_per_semester': 30 * 5,  # 5 essays
            'grading_time': (30 * 5 * throughput['time_per_essay']) / 60,  # hours
            'cost': 30 * 5 * costs['cost_per_essay']
        },
        'Medium class (100 students)': {
            'students': 100,
            'essays_per_semester': 100 * 5,
            'grading_time': (100 * 5 * throughput['time_per_essay']) / 60,
            'cost': 100 * 5 * costs['cost_per_essay']
        },
        'Large institution (1000 students)': {
            'students': 1000,
            'essays_per_semester': 1000 * 5,
            'grading_time': (1000 * 5 * throughput['time_per_essay']) / 60,
            'cost': 1000 * 5 * costs['cost_per_essay']
        },
        'National scale (100k students)': {
            'students': 100000,
            'essays_per_semester': 100000 * 5,
            'grading_time': (100000 * 5 * throughput['time_per_essay']) / 60,
            'cost': 100000 * 5 * costs['cost_per_essay']
        }
    }
    
    return scenarios


def plot_throughput_comparison(chatgpt_metrics, gemini_metrics, save_path):
    """Plot throughput and timing comparison."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    models = ['ChatGPT', 'Gemini']
    colors = ['#2E86AB', '#A23B72']
    
    # 1. Average time per grading
    ax = axes[0]
    times = [chatgpt_metrics['avg_time'], gemini_metrics['avg_time']]
    bars = ax.bar(models, times, color=colors)
    ax.set_ylabel('Seconds', fontsize=11, fontweight='bold')
    ax.set_title('Average Time per Grading', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    for bar, val in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
               f'{val:.2f}s', ha='center', fontweight='bold')
    
    # 2. Throughput (gradings per hour)
    ax = axes[1]
    throughputs = [chatgpt_metrics['throughput_per_hour'], 
                   gemini_metrics['throughput_per_hour']]
    bars = ax.bar(models, throughputs, color=colors)
    ax.set_ylabel('Gradings per Hour', fontsize=11, fontweight='bold')
    ax.set_title('Throughput Capacity', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    for bar, val in zip(bars, throughputs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
               f'{val:.0f}', ha='center', fontweight='bold')
    
    # 3. Time per complete essay (7 questions)
    ax = axes[2]
    essay_times = [chatgpt_metrics['time_per_essay'], 
                   gemini_metrics['time_per_essay']]
    bars = ax.bar(models, essay_times, color=colors)
    ax.set_ylabel('Minutes', fontsize=11, fontweight='bold')
    ax.set_title('Time per Complete Essay', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    for bar, val in zip(bars, essay_times):
        minutes = val / 60
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
               f'{minutes:.1f}m', ha='center', fontweight='bold')
    
    plt.suptitle('Throughput and Timing Analysis',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_cost_comparison(chatgpt_costs, gemini_costs, save_path):
    """Plot cost comparison across scales."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Cost per unit
    ax = axes[0]
    categories = ['Per Grading', 'Per Essay\n(7 questions)']
    chatgpt_vals = [chatgpt_costs['cost_per_grading'], chatgpt_costs['cost_per_essay']]
    gemini_vals = [gemini_costs['cost_per_grading'], gemini_costs['cost_per_essay']]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, chatgpt_vals, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_vals, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Cost (USD)', fontsize=11, fontweight='bold')
    ax.set_title('Unit Cost Comparison', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.001,
                   f'${height:.4f}', ha='center', fontsize=9, fontweight='bold')
    
    # 2. Scaled cost comparison
    ax = axes[1]
    scales = ['100\nEssays', '1K\nEssays', '10K\nEssays']
    chatgpt_scaled = [chatgpt_costs['cost_100_essays'], 
                     chatgpt_costs['cost_1000_essays'],
                     chatgpt_costs['cost_10000_essays']]
    gemini_scaled = [gemini_costs['cost_100_essays'],
                    gemini_costs['cost_1000_essays'],
                    gemini_costs['cost_10000_essays']]
    
    x = np.arange(len(scales))
    bars1 = ax.bar(x - width/2, chatgpt_scaled, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_scaled, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Total Cost (USD)', fontsize=11, fontweight='bold')
    ax.set_title('Scaled Cost Projection', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scales)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    ax.set_yscale('log')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height * 1.2,
                   f'${height:.0f}', ha='center', fontsize=9, fontweight='bold')
    
    plt.suptitle('Cost Analysis: ChatGPT vs Gemini',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def plot_scalability_scenarios(chatgpt_scenarios, gemini_scenarios, save_path):
    """Plot scalability projections."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    scenario_names = list(chatgpt_scenarios.keys())
    
    # 1. Cost by scenario
    ax = axes[0]
    chatgpt_costs = [chatgpt_scenarios[s]['cost'] for s in scenario_names]
    gemini_costs = [gemini_scenarios[s]['cost'] for s in scenario_names]
    
    x = np.arange(len(scenario_names))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, chatgpt_costs, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_costs, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Cost per Semester (USD)', fontsize=11, fontweight='bold')
    ax.set_title('Deployment Cost by Use Case', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height < 1000:
                label = f'${height:.0f}'
            else:
                label = f'${height/1000:.1f}K'
            ax.text(bar.get_x() + bar.get_width()/2, height * 1.3,
                   label, ha='center', fontsize=9, fontweight='bold')
    
    # 2. Grading time by scenario
    ax = axes[1]
    chatgpt_times = [chatgpt_scenarios[s]['grading_time'] for s in scenario_names]
    gemini_times = [gemini_scenarios[s]['grading_time'] for s in scenario_names]
    
    bars1 = ax.bar(x - width/2, chatgpt_times, width, label='ChatGPT', color='#2E86AB')
    bars2 = ax.bar(x + width/2, gemini_times, width, label='Gemini', color='#A23B72')
    
    ax.set_ylabel('Total Grading Time (hours)', fontsize=11, fontweight='bold')
    ax.set_title('Processing Time by Use Case', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scenario_names, rotation=15, ha='right')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height < 1:
                label = f'{height*60:.0f}m'
            elif height < 24:
                label = f'{height:.1f}h'
            else:
                label = f'{height/24:.1f}d'
            ax.text(bar.get_x() + bar.get_width()/2, height * 1.3,
                   label, ha='center', fontsize=9, fontweight='bold')
    
    plt.suptitle('Scalability Projections for Different Use Cases',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_operational_metrics_table(chatgpt_metrics, gemini_metrics, 
                                       chatgpt_costs, gemini_costs, save_path):
    """Generate operational metrics summary table."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ5: PRACTICAL IMPLICATIONS - OPERATIONAL METRICS\n")
        f.write("="*80 + "\n\n")
        
        f.write("THROUGHPUT METRICS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Metric':<35} {'ChatGPT':<20} {'Gemini':<20}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Avg time per grading (sec)':<35} "
               f"{chatgpt_metrics['avg_time']:<20.2f} "
               f"{gemini_metrics['avg_time']:<20.2f}\n")
        
        f.write(f"{'Time per essay (min)':<35} "
               f"{chatgpt_metrics['time_per_essay']/60:<20.2f} "
               f"{gemini_metrics['time_per_essay']/60:<20.2f}\n")
        
        f.write(f"{'Throughput (gradings/hour)':<35} "
               f"{chatgpt_metrics['throughput_per_hour']:<20.0f} "
               f"{gemini_metrics['throughput_per_hour']:<20.0f}\n")
        
        f.write(f"{'Throughput (essays/hour)':<35} "
               f"{chatgpt_metrics['throughput_per_hour']/7:<20.0f} "
               f"{gemini_metrics['throughput_per_hour']/7:<20.0f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("COST METRICS (USD)\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Scale':<35} {'ChatGPT':<20} {'Gemini':<20}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Cost per grading':<35} "
               f"${chatgpt_costs['cost_per_grading']:<19.4f} "
               f"${gemini_costs['cost_per_grading']:<19.4f}\n")
        
        f.write(f"{'Cost per essay (7 questions)':<35} "
               f"${chatgpt_costs['cost_per_essay']:<19.4f} "
               f"${gemini_costs['cost_per_essay']:<19.4f}\n")
        
        f.write(f"{'Cost for 100 essays':<35} "
               f"${chatgpt_costs['cost_100_essays']:<19.2f} "
               f"${gemini_costs['cost_100_essays']:<19.2f}\n")
        
        f.write(f"{'Cost for 1,000 essays':<35} "
               f"${chatgpt_costs['cost_1000_essays']:<19.2f} "
               f"${gemini_costs['cost_1000_essays']:<19.2f}\n")
        
        f.write(f"{'Cost for 10,000 essays':<35} "
               f"${chatgpt_costs['cost_10000_essays']:<19.2f} "
               f"${gemini_costs['cost_10000_essays']:<19.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("RESOURCE REQUIREMENTS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Metric':<35} {'ChatGPT':<20} {'Gemini':<20}\n")
        f.write("-"*80 + "\n")
        
        f.write(f"{'Avg tokens per grading':<35} "
               f"{chatgpt_metrics['avg_tokens']:<20.0f} "
               f"{gemini_metrics['avg_tokens']:<20.0f}\n")
        
        f.write(f"{'Tokens per essay (7 questions)':<35} "
               f"{chatgpt_metrics['avg_tokens']*7:<20.0f} "
               f"{gemini_metrics['avg_tokens']*7:<20.0f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("EFFICIENCY COMPARISON\n")
        f.write("-"*80 + "\n\n")
        
        # Cost efficiency
        cost_ratio = chatgpt_costs['cost_per_essay'] / gemini_costs['cost_per_essay']
        if cost_ratio > 1:
            f.write(f"Cost Efficiency Winner: GEMINI\n")
            f.write(f"  Gemini is {cost_ratio:.1f}x cheaper than ChatGPT\n")
            f.write(f"  Cost savings: ${(chatgpt_costs['cost_per_essay'] - gemini_costs['cost_per_essay']):.4f} per essay\n")
        else:
            f.write(f"Cost Efficiency Winner: CHATGPT\n")
            f.write(f"  ChatGPT is {1/cost_ratio:.1f}x cheaper than Gemini\n")
        
        f.write("\n")
        
        # Speed efficiency
        speed_ratio = chatgpt_metrics['time_per_essay'] / gemini_metrics['time_per_essay']
        if speed_ratio > 1:
            f.write(f"Speed Winner: GEMINI\n")
            f.write(f"  Gemini is {speed_ratio:.1f}x faster than ChatGPT\n")
        else:
            f.write(f"Speed Winner: CHATGPT\n")
            f.write(f"  ChatGPT is {1/speed_ratio:.1f}x faster than Gemini\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def generate_deployment_recommendations_table(chatgpt_metrics, gemini_metrics,
                                              chatgpt_costs, gemini_costs,
                                              chatgpt_scenarios, gemini_scenarios,
                                              save_path):
    """Generate deployment recommendations."""
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RQ5: PRACTICAL IMPLICATIONS - DEPLOYMENT RECOMMENDATIONS\n")
        f.write("="*80 + "\n\n")
        
        f.write("DEPLOYMENT SCENARIOS\n")
        f.write("-"*80 + "\n\n")
        
        for scenario_name in chatgpt_scenarios.keys():
            f.write(f"{scenario_name.upper()}\n")
            f.write("-"*40 + "\n")
            
            chatgpt_sc = chatgpt_scenarios[scenario_name]
            gemini_sc = gemini_scenarios[scenario_name]
            
            f.write(f"Students: {chatgpt_sc['students']}\n")
            f.write(f"Essays per semester: {chatgpt_sc['essays_per_semester']}\n\n")
            
            f.write(f"ChatGPT:\n")
            f.write(f"  Cost: ${chatgpt_sc['cost']:.2f}\n")
            f.write(f"  Time: {chatgpt_sc['grading_time']:.2f} hours\n\n")
            
            f.write(f"Gemini:\n")
            f.write(f"  Cost: ${gemini_sc['cost']:.2f}\n")
            f.write(f"  Time: {gemini_sc['grading_time']:.2f} hours\n\n")
            
            # Recommendation
            cost_savings = chatgpt_sc['cost'] - gemini_sc['cost']
            if cost_savings > 0:
                f.write(f"Recommendation: GEMINI\n")
                f.write(f"  Cost savings: ${cost_savings:.2f} per semester\n")
                f.write(f"  Additional benefit: Higher accuracy (80.4% vs 69.1%)\n")
            else:
                f.write(f"Recommendation: CHATGPT\n")
            
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write("OVERALL RECOMMENDATIONS\n")
        f.write("-"*80 + "\n\n")
        
        f.write("PRIMARY RECOMMENDATION: GEMINI-1.5-PRO\n\n")
        
        f.write("Advantages:\n")
        f.write("  1. Superior accuracy: 80.4% vs 69.1% exact agreement\n")
        f.write("  2. Better consistency: ICC = 0.993 vs 0.989\n")
        f.write("  3. Lower error rate: 19.6% vs 30.9%\n")
        
        cost_diff = chatgpt_costs['cost_per_essay'] - gemini_costs['cost_per_essay']
        if cost_diff > 0:
            f.write(f"  4. More cost-effective: ${cost_diff:.4f} cheaper per essay\n")
        
        f.write("\n")
        f.write("Use Cases:\n")
        f.write("  • Small to medium classes (30-100 students)\n")
        f.write("  • Large institutional deployments (1000+ students)\n")
        f.write("  • High-stakes assessments requiring accuracy\n")
        f.write("  • Budget-conscious implementations\n")
        
        f.write("\n" + "-"*80 + "\n\n")
        
        f.write("ALTERNATIVE: CHATGPT-4O\n\n")
        
        f.write("Consider if:\n")
        f.write("  • Already integrated with ChatGPT ecosystem\n")
        f.write("  • Require specific ChatGPT features\n")
        f.write("  • 69.1% accuracy acceptable for use case\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("IMPLEMENTATION CONSIDERATIONS\n")
        f.write("-"*80 + "\n\n")
        
        f.write("Technical Requirements:\n")
        f.write("  • API access to chosen model (ChatGPT or Gemini)\n")
        f.write("  • Secure storage for student essays and rubrics\n")
        f.write("  • Error handling and retry logic\n")
        f.write("  • Rate limiting compliance\n")
        f.write("  • Result validation and human review workflow\n\n")
        
        f.write("Best Practices:\n")
        f.write("  1. Use lenient strategy (proven superior consistency)\n")
        f.write("  2. Implement human oversight for borderline cases\n")
        f.write("  3. Maintain audit logs of all gradings\n")
        f.write("  4. Regular calibration with expert graders\n")
        f.write("  5. Transparent communication with students\n\n")
        
        f.write("Quality Assurance:\n")
        f.write("  • Random sampling for expert review (10-20%)\n")
        f.write("  • Flag disagreements > 1 grade for review\n")
        f.write("  • Monitor consistency across batches\n")
        f.write("  • Periodic revalidation studies\n\n")
        
        f.write("="*80 + "\n")
    
    print(f"  ✓ Saved: {save_path.name}")


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("RQ5: PRACTICAL IMPLICATIONS ANALYSIS")
    print("="*80)
    
    # Paths
    data_dir = project_root / "results" / "lenient_analysis"
    output_dir = project_root / "results" / "rq5_practical_implications"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nInput: {data_dir}")
    print(f"Output: {output_dir}")
    
    # Load data
    print("\n[1/7] Loading data...")
    df_chatgpt = pd.read_csv(data_dir / "lenient_chatgpt.csv")
    df_gemini = pd.read_csv(data_dir / "lenient_gemini.csv")
    
    print(f"  ChatGPT: {len(df_chatgpt)} records")
    print(f"  Gemini: {len(df_gemini)} records")
    
    # Calculate metrics
    print("\n[2/7] Calculating throughput metrics...")
    chatgpt_metrics = calculate_throughput_metrics(df_chatgpt, 'ChatGPT')
    gemini_metrics = calculate_throughput_metrics(df_gemini, 'Gemini')
    
    print(f"  ✓ ChatGPT: {chatgpt_metrics['throughput_per_hour']:.0f} gradings/hour")
    print(f"  ✓ Gemini: {gemini_metrics['throughput_per_hour']:.0f} gradings/hour")
    
    print("\n[3/7] Calculating cost metrics...")
    chatgpt_costs = calculate_cost_metrics(df_chatgpt, 'ChatGPT')
    gemini_costs = calculate_cost_metrics(df_gemini, 'Gemini')
    
    print(f"  ✓ ChatGPT: ${chatgpt_costs['cost_per_essay']:.4f} per essay")
    print(f"  ✓ Gemini: ${gemini_costs['cost_per_essay']:.4f} per essay")
    
    print("\n[4/7] Projecting scalability scenarios...")
    chatgpt_scenarios = project_scalability(chatgpt_metrics, chatgpt_costs)
    gemini_scenarios = project_scalability(gemini_metrics, gemini_costs)
    
    print(f"  ✓ Analyzed 4 deployment scenarios")
    
    # Visualizations
    print("\n[5/7] Generating visualizations...")
    plot_throughput_comparison(chatgpt_metrics, gemini_metrics,
                              output_dir / "throughput_comparison.png")
    plot_cost_comparison(chatgpt_costs, gemini_costs,
                        output_dir / "cost_comparison.png")
    plot_scalability_scenarios(chatgpt_scenarios, gemini_scenarios,
                              output_dir / "scalability_projections.png")
    
    # Tables
    print("\n[6/7] Generating operational metrics table...")
    generate_operational_metrics_table(chatgpt_metrics, gemini_metrics,
                                      chatgpt_costs, gemini_costs,
                                      output_dir / "operational_metrics.txt")
    
    print("[7/7] Generating deployment recommendations...")
    generate_deployment_recommendations_table(chatgpt_metrics, gemini_metrics,
                                             chatgpt_costs, gemini_costs,
                                             chatgpt_scenarios, gemini_scenarios,
                                             output_dir / "deployment_recommendations.txt")
    
    # Final summary
    print("\n" + "="*80)
    print("RQ5 ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  1. throughput_comparison.png")
    print("  2. cost_comparison.png")
    print("  3. scalability_projections.png")
    print("  4. operational_metrics.txt")
    print("  5. deployment_recommendations.txt")
    
    print("\nKey Findings:")
    print(f"  • Throughput: ChatGPT {chatgpt_metrics['throughput_per_hour']/7:.0f} essays/hour, "
          f"Gemini {gemini_metrics['throughput_per_hour']/7:.0f} essays/hour")
    print(f"  • Cost: ChatGPT ${chatgpt_costs['cost_per_essay']:.4f}/essay, "
          f"Gemini ${gemini_costs['cost_per_essay']:.4f}/essay")
    
    cost_savings = chatgpt_costs['cost_per_essay'] - gemini_costs['cost_per_essay']
    if cost_savings > 0:
        print(f"  • Gemini is ${cost_savings:.4f} cheaper per essay")
    
    print(f"  • Recommendation: GEMINI (superior accuracy + cost efficiency)")
    
    print("\nNext step: Phase 7 - Comprehensive Report Generation")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
