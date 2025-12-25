# Alt Text for Figures (AJET Accessibility Requirement)

AJET requires descriptive alt text for all images to assist readers using accessibility software (e.g., screen readers). Add these descriptions when embedding figures in Word document.

**How to add alt text in Word**:
1. Right-click the image → Select "View Alt Text"
2. OR select image → Picture Format tab → Alt Text button
3. Paste the appropriate description below

---

## Figure 1: Overall Performance Comparison

**File**: `overall_performance_comparison.png`  
**Dimensions**: 5369×1483px @ 300 DPI

**Alt Text**:
```
Grouped bar chart comparing ChatGPT-4o and Gemini 2.0 Flash across four performance metrics: validity (Pearson correlation coefficient), reliability (intraclass correlation coefficient), mean absolute error, and critical error percentage. The chart displays three prompting strategies (lenient, few-shot, zero-shot) for each model. Gemini consistently shows higher validity (r equals 0.89) and lower error rates across all strategies. Both models demonstrate excellent reliability with ICC values above 0.83. Error bars represent 95 percent confidence intervals.
```

---

## Figure 2: Reliability Coefficients Comparison

**File**: `reliability_coefficients_comparison.png`  
**Dimensions**: 4772×1472px @ 300 DPI

**Alt Text**:
```
Grouped bar chart displaying reliability metrics for ChatGPT-4o and Gemini 2.0 Flash across three prompting strategies. Two reliability coefficients are shown: intraclass correlation coefficient (ICC) and Fleiss' kappa. All conditions achieve ICC above 0.83 and kappa above 0.79, meeting thresholds for excellent reliability. Gemini's lenient strategy achieves the highest reliability (ICC equals 0.949, kappa equals 0.915). Error bars show standard deviations across 10 independent trials for lenient conditions and single measurements for few-shot and zero-shot baselines.
```

---

## Figure 3: Consistency Distribution

**File**: `consistency_distribution.png`  
**Dimensions**: 4771×2957px @ 300 DPI

**Alt Text**:
```
Violin plots showing the distribution of grading consistency scores across 10 independent trials for six experimental conditions combining two models (ChatGPT-4o, Gemini 2.0 Flash) and three prompting strategies (lenient, few-shot, zero-shot). The violin shape represents kernel density estimation of score distributions, with box plots embedded showing median, quartiles, and outliers. Gemini's lenient strategy shows the tightest distribution (smallest variance) with median consistency of 94.3 percent, while zero-shot strategies show wider distributions indicating greater variability across trials.
```

---

## Figure 4: Consistency SD Comparison

**File**: `consistency_sd_comparison.png`  
**Dimensions**: 4170×1467px @ 300 DPI

**Alt Text**:
```
Horizontal bar chart comparing standard deviations of grading consistency across 10 trials for six experimental conditions. Bars are color-coded by model (blue for ChatGPT, orange for Gemini) and ordered by magnitude. Lower standard deviation indicates more stable grading behavior. Gemini's lenient strategy shows the lowest variability (SD equals 2.1 percentage points), while ChatGPT's zero-shot shows the highest (SD equals 8.7 percentage points). The chart demonstrates that lenient prompting substantially reduces grading inconsistency for both models.
```

---

## Figure 5: Consistency Variance Heatmap

**File**: `consistency_variance_heatmap.png`  
**Dimensions**: 5338×2959px @ 300 DPI

**Alt Text**:
```
Color-coded heatmap displaying variance in grading consistency across three dimensions: essay questions (rows), students (columns), and experimental conditions (separate panels for each model-strategy combination). Cells are colored on a gradient from blue (low variance, high consistency) to red (high variance, low consistency). The heatmap reveals that variance clusters by question difficulty rather than student identity, suggesting that LLM grading consistency is more sensitive to task characteristics than individual writing styles. Gemini panels show predominantly blue cells indicating consistently low variance across questions and students.
```

---

## Figure 6: Consistency Boxplot by Strategy

**File**: `consistency_boxplot_by_strategy.png`  
**Dimensions**: 3571×1772px @ 300 DPI

**Alt Text**:
```
Box-and-whisker plots comparing grading consistency distributions for three prompting strategies pooled across both models (ChatGPT and Gemini). Each box shows median (center line), interquartile range (box edges), and whiskers extending to 1.5 times the IQR. Individual data points beyond whiskers are shown as outliers. Lenient strategy achieves median consistency of 92 percent with narrow IQR, few-shot shows 85 percent with moderate spread, and zero-shot displays 78 percent with widest variance. Statistical annotation indicates significant differences between all strategy pairs (ANOVA F equals 110.56, p less than 0.001).
```

---

## Figure 7: Per-Grade Classification Metrics

**File**: `per_grade_classification_metrics.png`  
**Dimensions**: 4765×3541px @ 300 DPI

**Alt Text**:
```
Multi-panel bar chart showing precision, recall, and F1-scores for each grade level (A, B-plus, B, C-plus, C, D, E) comparing ChatGPT-4o and Gemini 2.0 Flash performance. The chart consists of three sub-panels arranged vertically. Top panel displays precision (percentage of correctly assigned grades among all predicted grades at that level), middle panel shows recall (percentage of actual grades correctly identified), and bottom panel presents F1-scores (harmonic mean of precision and recall). Both models achieve highest precision and recall for middle grades (B, C-plus) exceeding 85 percent, while extreme grades (A, E) show lower metrics due to class imbalance. Gemini consistently outperforms ChatGPT by 5 to 15 percentage points across most grade categories.
```

---

## Figure 8: Confusion Matrices Heatmap

**File**: `confusion_matrices_heatmap.png`  
**Dimensions**: 5324×3593px @ 300 DPI

**Alt Text**:
```
Side-by-side confusion matrices presented as heatmaps for ChatGPT-4o (left panel) and Gemini 2.0 Flash (right panel) showing predicted grades versus actual expert-assigned grades. Rows represent expert grades, columns represent model predictions. Cell color intensity indicates frequency, with darker blues showing higher concentrations. Numbers in cells show count of essays. Both matrices display strong diagonal patterns indicating correct classifications, with Gemini showing more concentrated diagonal and fewer off-diagonal errors. Gemini's confusion matrix reveals 89 percent agreement along the diagonal compared to ChatGPT's 76 percent. Both models show slight tendency toward over-grading (entries above diagonal) rather than under-grading, particularly in the lenient condition.
```

---

## Implementation Notes

### For Word Manuscript:

1. **Add alt text to each figure** after inserting into Word document
2. **Keep descriptions concise** but informative (aim for 2-4 sentences)
3. **Avoid redundancy** with figure captions (alt text should complement, not duplicate)
4. **Include key numerical values** mentioned in alt text in figure captions for sighted readers

### Accessibility Best Practices:

- **Start with chart type** (bar chart, heatmap, violin plot, etc.)
- **Describe main visual patterns** (trends, comparisons, distributions)
- **Include critical numerical values** (percentages, correlations, statistical significance)
- **Explain color coding** if relevant to interpretation
- **Avoid subjective interpretations** - describe what is shown, not why it matters (save that for discussion)

### Testing Alt Text Quality:

**Good alt text should enable a vision-impaired reader to**:
- Understand the chart type and structure
- Grasp the main finding or pattern
- Compare key values between conditions
- Follow along when the figure is referenced in manuscript text

**Example of poor alt text**: "Chart showing results"  
**Example of good alt text**: See descriptions above with specific metrics and comparisons

---

## Verification Checklist

Before submitting to AJET:

- [ ] All 8 figures have alt text added in Word document
- [ ] Alt text length is 2-4 sentences (50-150 words each)
- [ ] Alt text describes visual structure (chart type, axes, color scheme)
- [ ] Alt text includes key numerical findings from the figure
- [ ] Alt text complements (not duplicates) the figure caption
- [ ] Tested by reading alt text alone - makes sense without seeing image
- [ ] Accessibility checker in Word returns no issues for figures

---

## Additional Resources

**AJET Accessibility Guidelines**: https://ajet.org.au/index.php/AJET/about/submissions  
**Web Content Accessibility Guidelines (WCAG)**: https://www.w3.org/WAI/WCAG21/quickref/  
**Microsoft Alt Text Guide**: https://support.microsoft.com/en-us/office/add-alternative-text-to-a-shape-picture-chart-smartart-graphic-or-other-object
