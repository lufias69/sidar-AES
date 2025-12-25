# Tables - Quantitative Results

This folder contains tabular data summarizing the quantitative results from the automated essay scoring study.

## 📋 Summary Tables (Generated)

### Table 1: Comprehensive Performance Metrics
**File**: `table1_comprehensive_performance.csv`

Combined view of validity and reliability metrics for all 6 conditions (2 models × 3 strategies).

**Columns**:
- `Model`: ChatGPT or Gemini
- `Strategy`: lenient, few-shot, or zero-shot
- `Pearson_r`: Correlation with expert grades (0-1, higher = better)
- `ICC`: Intraclass Correlation Coefficient for reliability (0-1)
- `Fleiss_Kappa`: Multi-rater agreement (0-1)
- `MAE`: Mean Absolute Error in points (0-4, lower = better)
- `Accuracy_pct`: Exact grade match percentage (0-100%)
- `Adjacent_Errors_pct`: Errors within ±1 grade (%)
- `Major_Errors_pct`: Errors >1 grade difference (%)
- `Overall_Bias`: Systematic over/undergrading (-4 to +4, 0 = unbiased)

**Key Finding**: Gemini lenient achieved highest validity (r=0.89), while ChatGPT zero-shot had highest reliability (ICC=0.969).

---

### Table 2: Detailed Reliability Metrics
**File**: `table2_reliability_details.csv`

Extended reliability analysis with confidence intervals and statistical significance.

**Columns**:
- `Model`, `Strategy`: As above
- `Pearson_r`, `Pearson_p`: Correlation and p-value
- `ICC`, `ICC_CI_Lower`, `ICC_CI_Upper`: ICC with 95% confidence interval
- `Fleiss_Kappa`: Agreement statistic
- `CV_percent`: Coefficient of variation (%)
- `N_Trials`: Number of grading trials per condition

**Note**: ICC not calculated for single-trial conditions (shows NaN).

---

### Table 3: Validity Comparison Tables
**Files**: 
- `table3_validity_comparison.csv` (long format)
- `table3_validity_comparison_pivot.csv` (wide format for comparison)

Focused comparison of validity metrics across conditions.

**Columns** (long format):
- `Model`, `Strategy`
- `Pearson_r`: Correlation coefficient
- `MAE`: Mean Absolute Error
- `Exact_Match_pct`: Percentage of exact letter grade matches

**Use Case**: Quick comparison of model performance on validity metrics.

---

### Table 4: Error Patterns Summary
**File**: `table4_error_patterns_summary.csv`

Breakdown of error types and grading bias patterns.

**Columns**:
- `Model`, `Strategy`
- `Accuracy_pct`: Exact match rate
- `Adjacent_Errors_pct`: ±1 grade errors (usually acceptable)
- `Major_Errors_pct`: >1 grade errors (problematic)
- `Overall_Bias`: Mean grading bias
- `Bias_Direction`: Categorical interpretation (Overgrading/Undergrading/Minimal)

**Key Finding**: 
- Lenient prompts: Minimal bias (-0.01 to +0.08)
- Zero-shot: Tendency to overgrade (+0.14 to +0.22)
- Few-shot: Mixed patterns (-0.14 to +0.11)

---

## 🔢 Confusion Matrices (6 files)

### Individual Condition Matrices
**Files**: `confusion_matrix_[model]_[strategy].csv`

4×4 matrices showing expert grades (rows) vs AI grades (columns) for each condition.

**Format**:
```
          A    B    C    D
A        12    3    0    0
B         2   18    5    0
C         0    4   19    2
D         0    0    1    4
```

**Files**:
1. `confusion_matrix_chatgpt_lenient.csv`
2. `confusion_matrix_chatgpt_few-shot.csv`
3. `confusion_matrix_chatgpt_zero-shot.csv`
4. `confusion_matrix_gemini_lenient.csv`
5. `confusion_matrix_gemini_few-shot.csv`
6. `confusion_matrix_gemini_zero-shot.csv`

**Interpretation**:
- **Diagonal values**: Exact matches (desired)
- **Adjacent cells**: ±1 grade errors (acceptable)
- **Far off-diagonal**: Major errors (problematic)

**Use Case**: 
- Identify systematic grading patterns
- Detect grade-specific accuracy issues
- Visualize error distribution

---

## ❌ Error Analysis Tables (2 files)

### Error Summary
**File**: `error_summary.csv`

Aggregate error statistics across all conditions.

**Typical Columns**:
- Condition identifiers
- Error counts by type
- Error rates by grade level

### Critical Errors Summary
**File**: `critical_errors_summary.csv`

Analysis of severe grading errors (>1 grade difference).

**Typical Columns**:
- Error magnitude
- Affected students/questions
- Error patterns

---

## 📊 Usage Examples

### Loading in Python

```python
import pandas as pd

# Load comprehensive table
df = pd.read_csv('table1_comprehensive_performance.csv')

# Filter best performers
best_validity = df[df['Pearson_r'] == df['Pearson_r'].max()]
best_reliability = df[df['ICC'] == df['ICC'].max()]

print(f"Best validity: {best_validity[['Model', 'Strategy', 'Pearson_r']].values}")
print(f"Best reliability: {best_reliability[['Model', 'Strategy', 'ICC']].values}")
```

### Loading in R

```r
library(tidyverse)

# Load comprehensive table
df <- read_csv('table1_comprehensive_performance.csv')

# Compare models
df %>%
  group_by(Model) %>%
  summarise(
    mean_pearson = mean(Pearson_r),
    mean_icc = mean(ICC, na.rm = TRUE)
  )
```

### Loading in Excel

1. Open Excel
2. Data → From Text/CSV
3. Select any `.csv` file
4. Adjust delimiter (comma) and data types as needed
5. Load data

---

## 📈 Visualization Recommendations

**Recommended Charts**:

1. **Pearson r comparison**: Grouped bar chart
   - X-axis: Strategy
   - Grouped by: Model
   - Y-axis: Pearson r

2. **ICC with confidence intervals**: Error bar chart
   - X-axis: Condition
   - Y-axis: ICC
   - Error bars: CI_Lower to CI_Upper

3. **Confusion matrices**: Heatmap
   - Use diverging color scheme
   - Annotate cells with counts

4. **Error breakdown**: Stacked bar chart
   - Segments: Exact / Adjacent / Major errors
   - Compare across conditions

---

## 🔍 Key Findings Summary

**Best Overall Performance**:
- **Validity**: Gemini + lenient (r=0.89, MAE=0.28)
- **Reliability**: ChatGPT + zero-shot (ICC=0.969, κ=0.838)
- **Balanced**: ChatGPT + lenient (r=0.76, ICC=0.942, MAE=0.38)

**Error Patterns**:
- **Lenient**: 87% exact match, 13% adjacent, <1% major
- **Few-shot**: More conservative, reduces overgrading
- **Zero-shot**: Higher variance, more major errors

**Grading Bias**:
- Minimal bias overall (|mean| < 0.25 points)
- Zero-shot shows slight overgrading tendency
- Lenient most unbiased across models

---

## 📝 Citation

When using these tables, cite:

> [Author]. (2026). Automated essay scoring with large language models: A comparative study of ChatGPT and Gemini. *Australasian Journal of Educational Technology*, [volume]([issue]), [pages]. https://doi.org/[DOI]

For individual tables:
> Data from Table 1: Comprehensive Performance Metrics, available at https://osf.io/[project_id]/

---

## 📧 Questions?

For questions about table contents or additional analyses:
- **Email**: [corresponding author]
- **OSF Project**: https://osf.io/[project_id]/

---

## 📜 Version History

- **v1.0** (Dec 25, 2025): Initial release with 13 tables
  - 4 summary tables (generated from analysis)
  - 6 confusion matrices (per condition)
  - 2 error analysis tables
  - 1 pivot table for model comparison

---

*Last updated: December 25, 2025*
