# Graphical Abstract
## Large Language Models for Automated Essay Scoring: A Comprehensive Validity, Reliability, and Error Analysis Study

---

## Visual Summary Design Specification

**Purpose:** Single-figure visual summary for journal landing page and social media

**Recommended Size:** 1600 × 900 pixels (16:9 ratio) or 1200 × 800 pixels (3:2 ratio)

**Format:** High-resolution PNG or SVG with clear typography

---

## Proposed Design Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  LLM-Based Automated Essay Scoring: Comprehensive Evaluation   │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │   INPUT          │         │   MODELS         │             │
│  │                  │    →    │                  │             │
│  │  4,473 Essays    │         │  ChatGPT-4o      │             │
│  │  10 Students     │         │  Gemini-2.5-Flash│             │
│  │  7 Questions     │         │                  │             │
│  │  10 Trials       │         │  3 Strategies:   │             │
│  │                  │         │  • Zero-shot     │             │
│  │                  │         │  • Few-shot      │             │
│  │                  │         │  • Lenient       │             │
│  └──────────────────┘         └──────────────────┘             │
│                                        │                        │
│                                        ↓                        │
│         ┌──────────────────────────────────────────┐           │
│         │         KEY FINDINGS                      │           │
│         │                                           │           │
│         │  Validity: QWK = 0.600 (ChatGPT zero)    │           │
│         │  Reliability: ICC = 0.969                │           │
│         │  Accuracy: 62.42% (exact match)          │           │
│         │  Conservative Bias: High specificity     │           │
│         │  Cost Savings: 77.9% (hybrid protocol)   │           │
│         └──────────────────────────────────────────┘           │
│                                        │                        │
│         ┌──────────────────────────────────────────┐           │
│         │      CONFUSION MATRIX INSIGHT            │           │
│         │                                           │           │
│         │   Predicted: E   D   C   B   A           │           │
│         │   Gold E:  212  74  10   0   0  [71.6%] │           │
│         │   Gold D:   56 164  15   0   0  [69.8%] │           │
│         │   Gold C:   28 100 144   1   0  [52.7%] │           │
│         │   Gold B:    0   2  17   0   1  [0.0%]  │           │
│         │   Gold A:    0   0   0   0   0  [N/A]   │           │
│         │                                           │           │
│         │  Grade-dependent performance              │           │
│         │  Class imbalance challenge                │           │
│         └──────────────────────────────────────────┘           │
│                                        │                        │
│                                        ↓                        │
│         ┌──────────────────────────────────────────┐           │
│         │      PRACTICAL IMPLICATIONS               │           │
│         │                                           │           │
│         │  💰 Cost: $0.0064/essay (ChatGPT)        │           │
│         │           234× cheaper than human         │           │
│         │                                           │           │
│         │  ⚡ Speed: 704 essays/hour                │           │
│         │           141× faster than human          │           │
│         │                                           │           │
│         │  🎯 Hybrid Protocol:                      │           │
│         │     • Auto-grade: Grades 1-2 (50%)       │           │
│         │     • Spot-check: Grade 3 (30%)          │           │
│         │     • Human-verify: Grades 4-5 (20%)     │           │
│         │     → 77.9% cost savings                  │           │
│         └──────────────────────────────────────────┘           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Alternative Design: Flowchart Style

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                     │
│    RESEARCH QUESTION: Can LLMs reliably grade argumentative essays?│
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐       │
│  │   RQ1    │   │   RQ2    │   │   RQ3    │   │   RQ4    │       │
│  │          │   │          │   │          │   │          │       │
│  │ VALIDITY │   │RELIABILITY│   │COMPARISON│   │  ERRORS  │       │
│  │          │   │          │   │          │   │          │       │
│  │ QWK:     │   │ ICC:     │   │ Winner:  │   │ MAE:     │       │
│  │ 0.600    │   │ 0.969    │   │ ChatGPT  │   │ 0.442    │       │
│  │          │   │          │   │ 63%      │   │ grades   │       │
│  │ 62.42%   │   │ α: 0.997 │   │ win rate │   │          │       │
│  │ accuracy │   │          │   │          │   │ 0.7%     │       │
│  │          │   │ SD: 0.12 │   │ p=0.037  │   │ critical │       │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘       │
│       └──────────────┴──────────────┴──────────────┘              │
│                            │                                       │
│                            ↓                                       │
│                   ┌──────────────────┐                            │
│                   │       RQ5        │                            │
│                   │  PRACTICAL       │                            │
│                   │  IMPLICATIONS    │                            │
│                   │                  │                            │
│                   │  Cost: $0.0064   │                            │
│                   │  Speed: 704/hr   │                            │
│                   │  Hybrid: 77.9%↓  │                            │
│                   └──────────────────┘                            │
│                                                                    │
│  CONCLUSION: Zero-shot ChatGPT achieves moderate validity with    │
│  excellent reliability. Hybrid human-AI protocol recommended.     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Design Elements

### Color Scheme
- **Primary:** Deep Blue (#1E3A8A) for headers and key metrics
- **Secondary:** Emerald Green (#10B981) for positive findings
- **Accent:** Amber (#F59E0B) for warnings/cautions
- **Neutral:** Gray (#6B7280) for supporting text
- **Background:** White (#FFFFFF) or Light Gray (#F3F4F6)

### Typography
- **Title:** Sans-serif, bold, 24-28pt
- **Section Headers:** Sans-serif, semibold, 18-20pt
- **Body Text:** Sans-serif, regular, 12-14pt
- **Numbers/Metrics:** Sans-serif, bold, 16-18pt

### Icons (Optional)
- 📊 Charts/graphs for data
- ⚖️ Scale for validity
- 🔄 Circular arrows for reliability
- 💰 Money bag for cost savings
- ⚡ Lightning bolt for speed
- 🎯 Target for accuracy

---

## Key Messages to Highlight

1. **Scale:** 4,473 gradings across comprehensive conditions
2. **Performance:** 62.42% accuracy, QWK 0.600 (moderate validity)
3. **Reliability:** ICC 0.969 (excellent consistency)
4. **Cost-Effectiveness:** 77.9% savings with hybrid protocol
5. **Conservative Bias:** High specificity but grade-dependent recall
6. **Practical Recommendation:** Tiered human-AI grading approach

---

## Implementation Tools

### Option 1: Design Software
- **Adobe Illustrator:** Professional vector graphics
- **Canva Pro:** Template-based with education theme
- **Figma:** Collaborative design with export options
- **PowerPoint:** Simple and accessible

### Option 2: Code-Based Generation
```python
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
ax.text(30, 44, '✓ Reliability: ICC = 0.969', ha='left', fontsize=11)
ax.text(30, 41, '✓ Accuracy: 62.42%', ha='left', fontsize=11)
ax.text(30, 38, '✓ Cost Savings: 77.9%', ha='left', fontsize=11)
ax.text(30, 35, '⚠ Grade-dependent performance', ha='left', fontsize=11, 
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
plt.savefig('results_experiment_final/submission/graphical_abstract.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
```

### To Execute:
```bash
python -c "exec(open('results_experiment_final/submission/GRAPHICAL_ABSTRACT.md').read().split('```python')[1].split('```')[0])"
```

Or save as standalone script:
```bash
python scripts/generate_graphical_abstract.py
```

---

## Usage Guidelines

### Journal Submission
- Submit as separate file during manuscript upload
- Label as "Graphical Abstract" in submission system
- Ensure meets journal size requirements (typically <2MB)
- Use RGB color mode for digital display

### Social Media
- Twitter/X: Crop to 1200×675 px for optimal display
- LinkedIn: Use full 1600×900 px
- ResearchGate: Upload as project cover image
- Include hashtags: #AES #LLM #EdTech #AI #Assessment

### Conference Presentations
- Use as opening slide summary
- Include in poster top banner
- Reference in talk introduction

---

## Alternative Simplified Version (Text-Heavy)

```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│   Large Language Models for Automated Essay Scoring      │
│   ─────────────────────────────────────────────────      │
│                                                           │
│   📊 4,473 essays × 6 AI strategies = comprehensive test │
│                                                           │
│   ✓ ChatGPT-4o achieves 62.4% accuracy (QWK=0.600)      │
│   ✓ Excellent reliability (ICC=0.969, α=0.997)          │
│   ✓ Conservative grading bias (high specificity)        │
│   ⚠ Grade-dependent performance (class imbalance)       │
│                                                           │
│   💰 Cost: $0.0064/essay (234× cheaper than human)      │
│   ⚡ Speed: 704 essays/hour (141× faster)                │
│                                                           │
│   🎯 RECOMMENDATION: Hybrid human-AI protocol            │
│      → 77.9% cost savings with quality assurance         │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## Review Checklist

- [ ] All key findings represented
- [ ] Numbers accurate (verify against manuscript)
- [ ] Visual hierarchy clear
- [ ] Color blind accessible (test with simulators)
- [ ] Text legible at thumbnail size
- [ ] File size under journal limits
- [ ] High resolution (300 DPI minimum)
- [ ] Proper attribution/copyright
- [ ] Matches manuscript data exactly

---

## Next Steps

1. Choose design approach (manual design vs Python generation)
2. Create high-resolution version (1600×900 px, 300 DPI)
3. Test legibility at multiple sizes
4. Get feedback from co-authors
5. Export in required format (PNG/TIFF for submission)
6. Prepare alt text for accessibility
7. Submit with manuscript as separate file
