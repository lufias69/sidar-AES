# Supplementary Materials Index

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring

---

## Document Organization

```
submission/
├── main_manuscript/
│   ├── COMPREHENSIVE_ANALYSIS_REPORT.md     [Main manuscript - 40+ pages]
│   └── figures/                              [8 publication-ready figures]
│
├── supplementary_materials/
│   ├── S1_CONFUSION_MATRIX_ANALYSIS.md      [Detailed confusion matrix analysis]
│   ├── S2_RAW_DATA_SUMMARY.md               [Dataset characteristics]
│   ├── S3_STATISTICAL_TESTS.md              [Complete statistical outputs]
│   ├── S4_IMPLEMENTATION_CODE.md            [Reproducible analysis scripts]
│   └── S5_EXTENDED_TABLES.md                [Additional tables not in main text]
│
├── data/
│   ├── detailed_classification_metrics.csv   [Per-grade TP/FP/TN/FN, P/R/F1]
│   ├── misclassification_analysis.csv        [Error patterns by severity]
│   ├── consistency_metrics_by_trial.csv      [ICC, Cronbach's α per trial]
│   ├── model_comparison_pairwise.csv         [Pairwise statistical tests]
│   └── cost_benefit_calculations.csv         [Cost per essay, time estimates]
│
└── figures_highres/
    ├── confusion_matrices_heatmap.png        [2×3 grid, 300+ DPI]
    ├── per_grade_classification_metrics.png  [4-panel performance]
    ├── overall_performance_comparison.png    [3-panel comparison]
    ├── consistency_boxplot_by_strategy.png   [Variance analysis]
    ├── consistency_distribution.png          [Distribution histograms]
    ├── consistency_sd_comparison.png         [Standard deviation comparison]
    ├── consistency_variance_heatmap.png      [Variance heatmap]
    └── reliability_coefficients_comparison.png [ICC/α/κ comparison]
```

---

## Supplementary Document 1: Confusion Matrix Analysis

**File:** `S1_CONFUSION_MATRIX_ANALYSIS.md` (17,000+ words)  
**Purpose:** Detailed analysis of classification performance beyond basic agreement metrics

**Contents:**
- Quick reference: Classification metrics dictionary (accuracy, precision, recall, etc.)
- Executive summary: 5 main findings from confusion matrices
- Confusion matrix heatmap analysis with interpretation guide
- Per-grade deep dive (grades 1-5) with best performers and common errors
- Misclassification risk assessment (low/medium/high risk errors)
- Implementation guidelines: 3-tier grading protocol with code examples
- Comparison to human inter-rater reliability benchmarks
- Recommended manuscript tables and figures
- Anticipated reviewer questions with evidence-based responses

**Key Insights:**
- Precision > Recall pattern indicates conservative grading bias
- Grade-dependent performance requires tiered confidence thresholds
- Lenient prompting causes 45-55% over-grading (14-23% severe errors)
- Hybrid protocol achieves 77% cost savings while maintaining quality

**Use Case:** Provides technical depth for reviewers with ML/classification background; can be cited in main manuscript when space is limited

---

## Supplementary Document 2: Raw Data Summary

**File:** `S2_RAW_DATA_SUMMARY.md` (To be created)  
**Purpose:** Dataset characteristics and collection methodology

**Planned Contents:**
- Dataset description: 10 students × 7 questions × 10 trials × 6 strategies
- Sampling methodology: Student selection criteria, question types
- Gold standard creation: Expert rater profiles, inter-rater reliability (ICC=0.75, κ=0.58)
- Grade distribution: 83% grades 1-3, 17% grades 4-5 (class imbalance discussion)
- Rubric details: 5-point scale, grading criteria per level
- Essay characteristics: Length distribution, topic diversity, language complexity
- Missing data handling: Trial completion rates, reasons for exclusions
- Ethical considerations: Anonymization procedures, consent process

**Statistical Summary Table:**
```
Metric                          | Value
--------------------------------|------------------
Total grading instances         | 4,473
Completed successfully          | 4,473 (100%)
Comparisons with gold standard  | 5,298
Unique students                 | 16
Unique questions                | 7
Trials per configuration        | 10
Model-strategy combinations     | 6
Mean essay length (words)       | [To be calculated]
Grade distribution E/D/C/B/A    | 21%/18%/37%/12%/10%
```

---

## Supplementary Document 3: Statistical Tests Details

**File:** `S3_STATISTICAL_TESTS.md` (To be created)  
**Purpose:** Complete statistical outputs for transparency and reproducibility

**Planned Contents:**

### RQ1: Validity Tests
- Quadratic Weighted Kappa calculation details
- Cohen's Kappa with confidence intervals
- Agreement matrices (exact, adjacent, ±2, ±3)
- Confusion matrix statistics per model-strategy

### RQ2: Reliability Tests
- Intraclass Correlation Coefficient (ICC) calculation: ICC(2,1) and ICC(2,k)
- Cronbach's Alpha with item-total statistics
- Fleiss' Kappa for multi-rater agreement
- Variance decomposition: Within-trial vs between-trial
- Bland-Altman plots for agreement analysis

### RQ3: Model Comparison Tests
- Paired t-test: Assumptions check, normality tests, full output
- Wilcoxon signed-rank test: Exact p-values, effect sizes
- McNemar's test: Contingency tables, chi-square values
- Cohen's d effect size calculation
- Win-loss-tie analysis with bootstrap confidence intervals

### RQ4: Error Analysis Statistics
- Mean Absolute Error (MAE) with confidence intervals
- Root Mean Square Error (RMSE)
- Bias calculation: Systematic over/under-grading
- Error distribution: Histogram, Q-Q plots
- Critical error identification: Threshold justification (±2 grades)

### RQ5: Cost-Benefit Analysis
- Cost per essay calculation: API pricing breakdown
- Time per essay: Response time distribution
- Throughput estimates: Essays per hour per strategy
- Hybrid protocol cost modeling: 3-tier system analysis
- Break-even analysis: When to use which strategy

**Software Used:**
- Python 3.11
- scikit-learn 1.4.0 (classification metrics, confusion matrices)
- statsmodels 0.14.1 (ICC, statistical tests)
- scipy 1.12.0 (Wilcoxon, paired t-test)
- pingouin 0.5.3 (Cronbach's alpha, reliability coefficients)

---

## Supplementary Document 4: Implementation Code

**File:** `S4_IMPLEMENTATION_CODE.md` (To be created)  
**Purpose:** Enable reproducibility and transparency

**Planned Contents:**

### Analysis Scripts
```
scripts/
├── analyze_confusion_matrix_detailed.py    [Confusion matrix generation]
├── calculate_validity_metrics.py           [QWK, kappa, agreement rates]
├── calculate_reliability_coefficients.py   [ICC, Cronbach's α, Fleiss' κ]
├── perform_model_comparison_tests.py       [t-test, Wilcoxon, McNemar's]
├── analyze_errors_and_bias.py              [MAE, error patterns, critical errors]
└── cost_benefit_analysis.py                [Cost, speed, hybrid protocol]
```

### Key Functions Documentation
- `calculate_detailed_metrics()`: Computes TP/FP/TN/FN and derives precision/recall/specificity/F1
- `generate_confusion_matrix_heatmap()`: Creates annotated 2×3 grid visualization
- `calculate_icc()`: Intraclass correlation with multiple models
- `perform_pairwise_tests()`: Statistical comparison between strategies
- `identify_critical_errors()`: Flags ±2 grade errors with justifications

### Environment Setup
```yaml
# conda environment specification
name: aes_analysis
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy=1.24.3
  - pandas=2.0.3
  - matplotlib=3.7.1
  - seaborn=0.12.2
  - scikit-learn=1.4.0
  - scipy=1.12.0
  - statsmodels=0.14.1
  - pingouin=0.5.3
```

### Reproducibility Checklist
- [ ] Random seeds set for all stochastic operations
- [ ] Software versions documented
- [ ] Input data checksums provided
- [ ] Step-by-step execution instructions
- [ ] Expected runtime and computational requirements

---

## Supplementary Document 5: Extended Tables

**File:** `S5_EXTENDED_TABLES.md` (To be created)  
**Purpose:** Additional tables that support main findings but are too detailed for main text

**Planned Contents:**

### Table S1: Per-Grade Classification Metrics (All 6 Strategies)
- Columns: Model-Strategy, Grade, Precision, Recall, Specificity, F1, Support, TP, FP, TN, FN
- Rows: 6 strategies × 5 grades = 30 rows + 6 macro-average rows

### Table S2: Trial-by-Trial Consistency Metrics
- Columns: Strategy, Trial, Mean Score, SD, ICC(2,1), ICC(2,k), Cronbach's α
- Rows: 6 strategies × 10 trials = 60 rows

### Table S3: Pairwise Model Comparison (All Combinations)
- Columns: Comparison, t-statistic, p-value, Cohen's d, Wilcoxon Z, p-value, McNemar's χ²
- Rows: 15 combinations (6 choose 2)

### Table S4: Error Distribution by Severity
- Columns: Strategy, Correct%, ±1 Grade%, ±2 Grades%, ≥3 Grades%, Over%, Under%
- Rows: 6 strategies

### Table S5: Cost Analysis Breakdown
- Columns: Strategy, Cost/Essay, Time/Essay, Essays/Hour, Cost/1000 Essays, Time/1000 Essays
- Rows: 6 strategies + Hybrid protocol

### Table S6: Confusion Matrix Raw Counts (All 6 Strategies)
- 6 separate 5×5 matrices with absolute counts
- Row: True grade, Column: Predicted grade
- Annotations: Count + percentage

### Table S7: Grade-Specific Best Performers Summary
- Columns: Grade, Best Strategy, Precision, Recall, F1, Second Best, Third Best
- Rows: 5 grades

---

## Data Files Description

### `detailed_classification_metrics.csv`
**Rows:** 36 (6 strategies × 5 grades + 6 macro-average rows)  
**Columns:** Model, Strategy, Grade, Precision, Recall, Specificity, F1, Support, TP, FP, TN, FN  
**Size:** ~5 KB  
**Format:** UTF-8 CSV with header

**Sample:**
```csv
Model,Strategy,Grade,Precision,Recall,Specificity,F1,Support,TP,FP,TN,FN
ChatGPT,zero-shot,1,0.635,0.716,0.935,0.673,190,136,78,318,54
ChatGPT,zero-shot,2,0.471,0.608,0.885,0.531,169,103,116,355,66
...
```

### `misclassification_analysis.csv`
**Rows:** 6 (one per strategy)  
**Columns:** Model, Strategy, Total, Correct, Correct%, ±1_Grade, ±1%, ±2_Grades, ±2%, ≥3_Grades, ≥3%, Over%, Under%  
**Size:** ~2 KB  
**Format:** UTF-8 CSV with header

**Sample:**
```csv
Model,Strategy,Total,Correct,Correct%,±1_Grade,±1%,±2_Grades,±2%,≥3_Grades,≥3%,Over%,Under%
ChatGPT,zero-shot,664,415,62.5,275,41.4,53,8.0,0,0.0,24.5,24.8
ChatGPT,lenient,664,240,36.1,264,39.8,160,24.1,0,0.0,55.3,8.6
...
```

### Other CSV Files (To be Generated)
- `consistency_metrics_by_trial.csv`: ICC, α, SD per trial
- `model_comparison_pairwise.csv`: All pairwise statistical test results
- `cost_benefit_calculations.csv`: Detailed cost modeling with assumptions

---

## Figures High-Resolution

All figures provided at **300 DPI minimum** in PNG format for print quality.

### Figure Specifications

**Figure 1: Confusion Matrices Heatmap**
- File: `confusion_matrices_heatmap.png`
- Dimensions: 3600×2400 pixels (12"×8" at 300 DPI)
- Format: PNG with transparency
- Color scheme: Blue gradient (sequential)
- Annotations: Count + percentage per cell
- Usage: Main manuscript Section 3.3A

**Figure 2: Per-Grade Classification Metrics**
- File: `per_grade_classification_metrics.png`
- Dimensions: 3600×3600 pixels (12"×12" at 300 DPI)
- Format: PNG with transparency
- Layout: 2×2 grid (Precision, Recall, F1, Specificity)
- Usage: Main manuscript Section 3.3A or Supplement

**Figure 3: Overall Performance Comparison**
- File: `overall_performance_comparison.png`
- Dimensions: 4800×1800 pixels (16"×6" at 300 DPI)
- Format: PNG with transparency
- Layout: 3-panel horizontal (Agreement, P-R-F1, QWK vs F1)
- Usage: Main manuscript Section 3.3A

**Figures 4-8: Consistency/Reliability Visualizations**
- Files: `consistency_boxplot_by_strategy.png`, etc.
- Dimensions: 3000×2400 pixels (10"×8" at 300 DPI)
- Format: PNG with transparency
- Usage: Main manuscript Section 3.2 or Supplement

---

## Usage Guidelines

### For Manuscript Submission:
1. **Main Text:** Include 3-5 key figures (confusion matrices, consistency comparison, overall performance)
2. **In-Text Tables:** Include 6 main tables (summarized results)
3. **Supplementary Materials:** Upload all 5 supplementary documents + data files + high-res figures
4. **Data Availability Statement:** "All data and analysis scripts are available in Supplementary Materials S1-S5"

### For Reviewer Response:
- **S1 (Confusion Matrix Analysis):** Addresses classification methodology questions
- **S2 (Raw Data Summary):** Addresses sampling and data quality questions
- **S3 (Statistical Tests):** Addresses statistical rigor questions
- **S4 (Implementation Code):** Addresses reproducibility questions
- **S5 (Extended Tables):** Provides detailed breakdowns for specific comparisons

### For Reader Access:
- All supplementary materials will be:
  - Uploaded to journal's supplementary portal (if accepted)
  - Archived in institutional repository with DOI
  - Available in GitHub repository with CC BY 4.0 license

---

## Next Steps

### To Complete Supplementary Package:

1. **Generate S2 (Raw Data Summary):**
   - Run dataset statistics script
   - Calculate essay length distribution
   - Document rubric details
   - Add ethical statement

2. **Generate S3 (Statistical Tests Details):**
   - Export complete statistical outputs from analysis scripts
   - Add interpretation for each test
   - Include assumption checks

3. **Generate S4 (Implementation Code):**
   - Clean and document all analysis scripts
   - Add docstrings to all functions
   - Create environment.yml file
   - Write step-by-step execution guide

4. **Generate S5 (Extended Tables):**
   - Export all tables from analysis results
   - Format consistently (APA style)
   - Add footnotes explaining abbreviations

5. **Package Everything:**
   - Create ZIP archive with organized folder structure
   - Generate README.md for archive
   - Calculate checksums for all data files
   - Test reproducibility on clean environment

---

**Document End**

**Status:** Index created, S1 complete, S2-S5 pending generation  
**Estimated Time to Complete:** 4-6 hours for all supplementary documents  
**Ready for:** Author review and target journal selection
