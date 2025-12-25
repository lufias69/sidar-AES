# Results Files

This folder contains all figures and tables from the published study.

## 📊 Figures (8 files)

All figures are high-resolution PNG (300 DPI) suitable for publication.

### Figure 1: Overall Performance Comparison
**File**: `figures/overall_performance_comparison.png` (404 KB)

Bar chart comparing accuracy, MAE, and Pearson r across 6 conditions (2 models × 3 strategies).

**Key Finding**: Gemini lenient achieved highest validity (r=0.89) while ChatGPT zero-shot had highest reliability (ICC=0.969).

---

### Figure 2: Reliability Coefficients Comparison
**File**: `figures/reliability_coefficients_comparison.png` (228 KB)

Grouped bar chart showing Pearson r, ICC, and Fleiss' kappa for each condition.

**Key Finding**: Few-shot prompting improved reliability (ICC: 0.942 vs 0.832) but reduced validity (r: 0.76 vs 0.89).

---

### Figure 3: Confusion Matrices Heatmap
**File**: `figures/confusion_matrices_heatmap.png` (805 KB)

6-panel heatmap showing grade distribution (A/B/C/D) for each model-strategy combination.

**Key Finding**: 
- Lenient: 87% exact match, 13% adjacent errors
- Zero-shot: More variability, 25% adjacent errors
- Few-shot: Balanced performance

---

### Figure 4: Per-Grade Classification Metrics
**File**: `figures/per_grade_classification_metrics.png` (340 KB)

Line plot showing precision, recall, and F1-score by letter grade (A/B/C/D).

**Key Finding**:
- Grade C: Hardest to classify (F1=0.65)
- Grade A/D: Easier (F1>0.85)
- Middle grades more challenging for AI

---

### Figure 5: Consistency Distribution
**File**: `figures/consistency_distribution.png` (328 KB)

Violin plot showing score variance distribution across students and questions.

**Key Finding**: 
- ChatGPT: Lower variance (CV=14.2%)
- Gemini: Higher variance (CV=18.7%)
- Lenient most consistent across trials

---

### Figure 6: Consistency Standard Deviation Comparison
**File**: `figures/consistency_sd_comparison.png` (233 KB)

Box plot comparing standard deviation of scores by strategy.

**Key Finding**: Few-shot reduced SD by 23% compared to zero-shot.

---

### Figure 7: Consistency Boxplot by Strategy
**File**: `figures/consistency_boxplot_by_strategy.png` (164 KB)

Box plot showing distribution of consistency scores (0-100) for each strategy.

**Key Finding**: Lenient strategy most consistent (median=92), zero-shot least (median=78).

---

### Figure 8: Consistency Variance Heatmap
**File**: `figures/consistency_variance_heatmap.png` (1.3 MB)

Heatmap showing variance across 10 students × 7 questions for each condition.

**Key Finding**: Question 5 (critical thinking) showed highest variance across all conditions.

---

## 📋 Tables

Summary statistics tables exported from analysis (not included - data already in CSV format in `01_Data/` folder).

For complete statistical tables, see:
- `01_Data/reliability_metrics.csv` - ICC, kappa, correlation
- `01_Data/performance_summary_by_condition.csv` - Accuracy, bias, errors
- `01_Data/error_analysis_summary.csv` - Error patterns

---

## 🔍 Usage

### Viewing Figures
All PNG files can be opened with any image viewer. Recommended:
- Windows: Photos app
- ImageMagick for batch processing
- Python: `matplotlib.pyplot.imread()`

### Figure Generation Code
See `02_Analysis_Scripts/` folder for Python code to regenerate all figures from raw data.

---

## 📝 Citation

When using these figures, please cite:

> [Author]. (2026). Automated essay scoring with large language models: A comparative study of ChatGPT and Gemini. *Australasian Journal of Educational Technology*, [volume]([issue]), [pages]. https://doi.org/[DOI]

---

## 📧 Contact

For questions about figures or high-resolution versions:
- Corresponding Author: [email]
- Co-authors: Samsidar, Siti Fatmah

---

*Last updated: December 25, 2025*
