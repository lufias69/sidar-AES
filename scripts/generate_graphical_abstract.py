"""
Generate Graphical Abstract for LLM-Based AES Manuscript
Output: results_experiment_final/submission/graphical_abstract.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 9), facecolor='white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 95, 'LLM-Based Automated Essay Scoring', 
        ha='center', va='top', fontsize=24, fontweight='bold', 
        color='#1E3A8A')
ax.text(50, 90, 'Comprehensive Validity & Reliability Study', 
        ha='center', va='top', fontsize=16, color='#6B7280')

# Input Box
input_box = FancyBboxPatch((5, 60), 20, 25, 
                           boxstyle="round,pad=0.5", 
                           edgecolor='#1E3A8A', facecolor='#EFF6FF', 
                           linewidth=2)
ax.add_patch(input_box)
ax.text(15, 80, 'INPUT', ha='center', fontweight='bold', fontsize=12)
ax.text(15, 75, '4,473 Essays', ha='center', fontsize=10)
ax.text(15, 72, '10 Students', ha='center', fontsize=10)
ax.text(15, 69, '7 Questions', ha='center', fontsize=10)
ax.text(15, 66, '10 Trials', ha='center', fontsize=10)

# Models Box
models_box = FancyBboxPatch((35, 60), 25, 25, 
                            boxstyle="round,pad=0.5", 
                            edgecolor='#1E3A8A', facecolor='#EFF6FF', 
                            linewidth=2)
ax.add_patch(models_box)
ax.text(47.5, 80, 'MODELS', ha='center', fontweight='bold', fontsize=12)
ax.text(47.5, 75, 'ChatGPT-4o', ha='center', fontsize=10)
ax.text(47.5, 72, 'Gemini-2.5-Flash', ha='center', fontsize=10)
ax.text(47.5, 68, 'Zero/Few/Lenient', ha='center', fontsize=9, style='italic')

# Key Findings Box
findings_box = FancyBboxPatch((10, 30), 80, 25, 
                              boxstyle="round,pad=0.5", 
                              edgecolor='#10B981', facecolor='#D1FAE5', 
                              linewidth=3)
ax.add_patch(findings_box)
ax.text(50, 52, 'KEY FINDINGS', ha='center', fontweight='bold', fontsize=14, 
        color='#065F46')
ax.text(30, 47, '✓ Validity: QWK = 0.600', ha='left', fontsize=11)
ax.text(30, 44, '✓ Reliability: ICC = 0.969 (ChatGPT)', ha='left', fontsize=11)
ax.text(30, 41, '✓ Accuracy: 62.42%', ha='left', fontsize=11)
ax.text(30, 38, '✓ Cost Savings: 77.9%', ha='left', fontsize=11)
ax.text(30, 35, '⚠ Gemini few-shot unreliable (κ=0.346)', ha='left', fontsize=11, 
        color='#F59E0B')

# Implications Box
impl_box = FancyBboxPatch((10, 5), 35, 20, 
                          boxstyle="round,pad=0.5", 
                          edgecolor='#1E3A8A', facecolor='#EFF6FF', 
                          linewidth=2)
ax.add_patch(impl_box)
ax.text(27.5, 23, 'COST', ha='center', fontweight='bold', fontsize=12)
ax.text(27.5, 19, '$0.0064/essay', ha='center', fontsize=11, color='#10B981')
ax.text(27.5, 16, '234× cheaper', ha='center', fontsize=9)
ax.text(27.5, 12, '704 essays/hour', ha='center', fontsize=11, color='#10B981')
ax.text(27.5, 9, '141× faster', ha='center', fontsize=9)

# Hybrid Protocol Box
hybrid_box = FancyBboxPatch((55, 5), 35, 20, 
                            boxstyle="round,pad=0.5", 
                            edgecolor='#F59E0B', facecolor='#FEF3C7', 
                            linewidth=2)
ax.add_patch(hybrid_box)
ax.text(72.5, 23, 'HYBRID PROTOCOL', ha='center', fontweight='bold', fontsize=12)
ax.text(72.5, 19, 'Auto-grade 1-2 (50%)', ha='center', fontsize=10)
ax.text(72.5, 16, 'Spot-check 3 (30%)', ha='center', fontsize=10)
ax.text(72.5, 13, 'Human-verify 4-5 (20%)', ha='center', fontsize=10)
ax.text(72.5, 9, '→ 77.9% savings', ha='center', fontsize=11, 
        fontweight='bold', color='#10B981')

# Arrows
arrow1 = FancyArrowPatch((25, 72.5), (35, 72.5), 
                        arrowstyle='->', mutation_scale=20, 
                        linewidth=2, color='#1E3A8A')
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((50, 60), (50, 55), 
                        arrowstyle='->', mutation_scale=20, 
                        linewidth=2, color='#1E3A8A')
ax.add_patch(arrow2)

arrow3 = FancyArrowPatch((50, 30), (27.5, 25), 
                        arrowstyle='->', mutation_scale=20, 
                        linewidth=2, color='#1E3A8A')
ax.add_patch(arrow3)

arrow4 = FancyArrowPatch((50, 30), (72.5, 25), 
                        arrowstyle='->', mutation_scale=20, 
                        linewidth=2, color='#1E3A8A')
ax.add_patch(arrow4)

plt.tight_layout()
output_path = 'results_experiment_final/submission/graphical_abstract.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Graphical abstract saved to: {output_path}")
plt.close()
