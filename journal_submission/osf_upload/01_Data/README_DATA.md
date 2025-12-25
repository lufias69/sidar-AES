# Data Documentation

## Overview
This folder contains anonymized research data from the study "Test-Retest Reliability of Large Language Models for Automated Essay Scoring in Indonesian Higher Education."

**Study Period**: September-October 2024  
**Sample Size**: 10 students × 7 questions = 70 essays  
**Grading Instances**: 1,958 (2 models × 3 strategies × varying trials)

## Files

### 1. gold_standard_anonymized.csv (70 rows)
**Description**: Expert human grades for Indonesian Capstone Project essays

**Variables**:
- `task_id`: Unique essay identifier (T000_1 to T015_7 format)
- `student_id_anon`: Anonymous student ID (S000-S015)
- `question_number`: Question prompt (Q1-Q7)
- `essay_word_count`: Number of words in essay (250-800 range)
- `expert_score_content`: Score for Content Understanding dimension (0-5 scale)
- `expert_score_organization`: Score for Organization & Structure (0-5 scale)
- `expert_score_arguments`: Score for Arguments & Evidence (0-5 scale)
- `expert_score_language`: Score for Language & Mechanics (0-5 scale)
- `expert_score_total`: Weighted composite score (0-4 GPA scale)
- `expert_grade`: Letter grade (A, B, C, D, E)

**Rubric Weighting**:
- Content Understanding: 40%
- Organization & Structure: 30%
- Arguments & Evidence: 20%
- Language & Mechanics: 10%

### 2. reliability_metrics.csv (6 rows)
**Description**: Statistical metrics for each model-strategy combination

**Variables**:
- `model`: AI model (chatgpt, gemini)
- `strategy`: Prompting strategy (lenient, few-shot, zero-shot)
- `pearson_r`: Pearson correlation with expert grades (-1 to 1)
- `pearson_p`: Statistical significance (p-value)
- `icc_value`: Intraclass correlation coefficient (0-1)
- `icc_ci_lower`: ICC 95% confidence interval lower bound
- `icc_ci_upper`: ICC 95% confidence interval upper bound
- `fleiss_kappa`: Fleiss' kappa multi-rater agreement (-1 to 1)
- `mae`: Mean absolute error (grade points)
- `coefficient_variation`: CV across trials (proportion)
- `exact_match_pct`: Percentage of exact grade matches
- `n_trials`: Number of independent grading trials

**Interpretation**:
- Pearson r > 0.80: Excellent validity
- ICC > 0.75: Good to excellent reliability
- Fleiss' kappa > 0.61: Substantial agreement
- MAE < 0.50: Less than half a letter grade error on average

### 3. performance_summary_by_condition.csv (6 rows)
**Description**: Performance metrics aggregated by experimental condition

**Variables**:
- `model`: AI model identifier
- `strategy`: Prompting strategy
- `exact_match_pct`: Percentage of perfect grade matches
- `adjacent_errors_pct`: Percentage of ±1 grade level errors
- `major_errors_pct`: Percentage of >1 grade level errors (critical)
- `mean_absolute_error`: Average grading discrepancy
- `mean_bias`: Systematic over/under-grading (positive = over-grade)
- `t_statistic`: T-test statistic for bias significance
- `p_value`: Statistical significance of bias

### 4. error_analysis_summary.csv (6 rows)
**Description**: Combined error patterns and bias analysis

## Data Privacy & Ethics

**Anonymization**:
- All personally identifiable information (PII) removed
- Student names replaced with anonymous IDs (S000-S015)
- Essay content NOT included (privacy protection)
- Only scores and metadata provided

**Consent & Approval**:
- Students provided informed consent for research use
- Institutional ethics approval obtained
- Data use limited to academic research

**FERPA Compliance**:
- No direct identifiers included
- No indirect identifiers that could reveal identity
- Aggregate-level reporting only for small cell sizes

## Missing Data

**ICC Values**:
- Not calculated for single-trial conditions (few-shot, zero-shot baselines)
- Reported as `None` or blank in CSV
- Only calculated for lenient strategy with 10 trials

**Rationale**: ICC requires multiple independent measurements per subject. Single-trial baselines use Fleiss' kappa instead.

## Data Quality

**Validation Checks**:
- All expert scores verified by course lecturer
- AI grading results validated against API responses
- Statistical calculations cross-checked with multiple methods
- Outliers investigated and confirmed as genuine

**Completeness**:
- 1,956 of 1,958 grading tasks completed (99.9% success rate)
- 2 API failures excluded from analysis
- No missing expert grades

## Usage Guidelines

### Citation
If you use this data, please cite:

```
Samsidar, Mustamin, S. B., & Fatmah, S. (2026). Test-Retest Reliability of 
Large Language Models for Automated Essay Scoring: A Comparative Study of 
ChatGPT and Gemini in Indonesian Higher Education. Australasian Journal of 
Educational Technology. [DOI pending]
```

### License
CC BY 4.0 (Creative Commons Attribution 4.0 International)

You are free to:
- Share: copy and redistribute
- Adapt: remix, transform, build upon

Under the condition:
- **Attribution**: Give appropriate credit, provide link to license, indicate changes

### Recommended Uses
- Validation of LLM-based grading systems
- Meta-analysis of AES reliability
- Comparative model benchmarking
- Cross-lingual AES research
- Educational assessment methodology studies

### Prohibited Uses
- Commercial applications without permission
- Re-identification attempts of students
- Use in high-stakes assessment without local validation

## Contact

**Corresponding Author**: Syaiful Bachri Mustamin  
**Email**: Syaifulbachri@mail.ugm.ac.id  
**Institution**: Institut Sains Teknologi dan Kesehatan 'Aisyiyah Kendari, Indonesia

**Questions about**:
- Data interpretation → Contact corresponding author
- Technical issues → Submit issue on OSF project page
- Replication → See `05_Documentation/REPLICATION_GUIDE.md`

## Version History

- **v1.0** (January 2026): Initial release with AJET manuscript submission
  - 70 gold standard essays
  - 6 experimental conditions
  - Complete reliability metrics
  
---

*Last updated: December 25, 2025*
