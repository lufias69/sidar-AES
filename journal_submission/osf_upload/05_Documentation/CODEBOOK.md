# Study Codebook

**Study Title**: Test-Retest Reliability of Large Language Models for Automated Essay Scoring  
**Version**: 1.0  
**Date**: January 2026  
**Authors**: Samsidar, Syaiful Bachri Mustamin, Siti Fatmah

---

## Variable Definitions

### Gold Standard Data (`gold_standard_anonymized.csv`)

| Variable | Type | Range/Values | Description | Notes |
|----------|------|--------------|-------------|-------|
| `task_id` | String | T000_1 to T015_7 | Unique essay identifier | Format: T{student_num}_{question_num} |
| `student_id_anon` | String | S000-S015 | Anonymous student ID | Original IDs removed for privacy |
| `question_number` | String | Q1-Q7 | Question prompt number | 7 analytical essay questions |
| `essay_word_count` | Integer | 250-800 | Number of words in essay | Calculated automatically |
| `expert_score_content` | Float | 0.0-5.0 | Content Understanding score | Rubric dimension 1 (40% weight) |
| `expert_score_organization` | Float | 0.0-5.0 | Organization & Structure score | Rubric dimension 2 (30% weight) |
| `expert_score_arguments` | Float | 0.0-5.0 | Arguments & Evidence score | Rubric dimension 3 (20% weight) |
| `expert_score_language` | Float | 0.0-5.0 | Language & Mechanics score | Rubric dimension 4 (10% weight) |
| `expert_score_total` | Float | 0.0-4.0 | Weighted composite score | GPA scale: A=3.5-4.0, B=2.5-3.49, C=1.5-2.49, D=0.5-1.49, E=0-0.49 |
| `expert_grade` | String | A, B, C, D, E | Letter grade | Based on composite score thresholds |

**Scoring Rubric Details**:

**Content Understanding (40% weight)**:
- 5 = Excellent: Deep comprehension, accurate concepts, insightful analysis
- 4 = Good: Solid understanding, mostly accurate, some depth
- 3 = Satisfactory: Basic comprehension, minor inaccuracies
- 2 = Weak: Superficial understanding, significant gaps
- 1 = Very weak: Major misconceptions, limited grasp
- 0 = Fail: No understanding demonstrated

**Organization & Structure (30% weight)**:
- 5 = Excellent: Clear logical flow, coherent paragraphs, strong intro/conclusion
- 4 = Good: Organized structure, mostly coherent transitions
- 3 = Satisfactory: Basic structure, some organizational issues
- 2 = Weak: Disorganized, unclear transitions
- 1 = Very weak: Severely disorganized, no clear structure
- 0 = Fail: Incoherent, impossible to follow

**Arguments & Evidence (20% weight)**:
- 5 = Excellent: Sophisticated reasoning, strong evidence, well-supported claims
- 4 = Good: Sound arguments, adequate evidence
- 3 = Satisfactory: Basic arguments, some supporting evidence
- 2 = Weak: Weak reasoning, insufficient evidence
- 1 = Very weak: Illogical arguments, no evidence
- 0 = Fail: No coherent arguments

**Language & Mechanics (10% weight)**:
- 5 = Excellent: Polished grammar, varied vocabulary, sophisticated sentences
- 4 = Good: Minor errors, clear communication
- 3 = Satisfactory: Some errors, generally understandable
- 2 = Weak: Frequent errors, impedes understanding
- 1 = Very weak: Pervasive errors, very difficult to understand
- 0 = Fail: Incomprehensible

**Composite Score Calculation**:
```
weighted_score = (content × 0.40) + (organization × 0.30) + 
                 (arguments × 0.20) + (language × 0.10)
```

Then converted to 4.0 GPA scale:
```
gpa_score = weighted_score × 0.8
```

**Grade Conversion**:
- A: 3.50 - 4.00
- B: 2.50 - 3.49
- C: 1.50 - 2.49
- D: 0.50 - 1.49
- E: 0.00 - 0.49

---

### Reliability Metrics (`reliability_metrics.csv`)

| Variable | Type | Range | Description | Interpretation |
|----------|------|-------|-------------|----------------|
| `model` | String | chatgpt, gemini | AI model identifier | ChatGPT-4o or Gemini 2.0 Flash |
| `strategy` | String | lenient, few-shot, zero-shot | Prompting strategy | See Methods section for prompt details |
| `pearson_r` | Float | -1.0 to 1.0 | Pearson correlation coefficient | **Validity metric**: Linear association with expert grades |
| `pearson_p` | String | p-value or "<0.001" | Statistical significance | p < 0.05 = statistically significant |
| `icc_value` | Float | 0.0 to 1.0 | Intraclass correlation coefficient | **Reliability metric**: ICC(2,1) two-way random effects, absolute agreement |
| `icc_ci_lower` | Float | 0.0 to 1.0 | ICC 95% CI lower bound | Confidence interval for ICC |
| `icc_ci_upper` | Float | 0.0 to 1.0 | ICC 95% CI upper bound | Confidence interval for ICC |
| `fleiss_kappa` | Float | -1.0 to 1.0 | Fleiss' kappa statistic | **Reliability metric**: Multi-rater categorical agreement |
| `mae` | Float | 0.0 to 4.0 | Mean absolute error | Average grading discrepancy in grade points |
| `coefficient_variation` | Float | 0.0 to 1.0 | Coefficient of variation | CV = SD / Mean across trials |
| `exact_match_pct` | Float | 0.0 to 100.0 | Exact match percentage | % of grades identical to expert |
| `n_trials` | Integer | 1 or 10 | Number of independent trials | 10 for lenient, 1 for baselines |

**Interpretation Guidelines**:

**Pearson r (Validity)**:
- r > 0.90: Excellent validity
- r = 0.80-0.89: Good validity
- r = 0.70-0.79: Acceptable validity
- r = 0.60-0.69: Questionable validity
- r < 0.60: Poor validity

**ICC (Reliability)**:
- ICC > 0.90: Excellent reliability
- ICC = 0.75-0.90: Good reliability
- ICC = 0.50-0.75: Moderate reliability
- ICC < 0.50: Poor reliability

**Fleiss' Kappa (Agreement)**:
- κ > 0.81: Almost perfect agreement
- κ = 0.61-0.80: Substantial agreement
- κ = 0.41-0.60: Moderate agreement
- κ = 0.21-0.40: Fair agreement
- κ < 0.21: Slight/poor agreement

**MAE (Accuracy)**:
- MAE < 0.30: Excellent accuracy (<1/3 letter grade error)
- MAE = 0.30-0.50: Good accuracy (<1/2 letter grade error)
- MAE = 0.50-1.00: Acceptable accuracy
- MAE > 1.00: Poor accuracy (>1 letter grade error)

**CV (Consistency)**:
- CV < 0.05: Excellent consistency
- CV = 0.05-0.10: Good consistency
- CV = 0.10-0.20: Acceptable consistency
- CV > 0.20: Poor consistency

---

### Performance Summary (`performance_summary_by_condition.csv`)

| Variable | Type | Range | Description | Notes |
|----------|------|-------|-------------|-------|
| `model` | String | chatgpt, gemini | AI model identifier | |
| `strategy` | String | lenient, few-shot, zero-shot | Prompting strategy | |
| `exact_match_pct` | Float | 0-100 | Perfect grade matches (%) | AI grade = Expert grade |
| `adjacent_errors_pct` | Float | 0-100 | Adjacent errors (%) | ±1 grade level difference (e.g., B vs. C) |
| `major_errors_pct` | Float | 0-100 | Critical errors (%) | >1 grade level difference (e.g., A vs. C) |
| `mean_absolute_error` | Float | 0-4.0 | Average grading error | Mean |AI - Expert| in grade points |
| `mean_bias` | Float | -4.0 to 4.0 | Systematic over/under-grading | Positive = over-grading, Negative = under-grading |
| `t_statistic` | Float | Any | T-test statistic | Tests if bias ≠ 0 |
| `p_value` | Float/String | 0-1 or "<0.001" | Significance of bias | p < 0.05 = statistically significant bias |

**Error Classification**:
- **Exact match**: AI grade = Expert grade (e.g., both assign B)
- **Adjacent error**: ±1 grade level (e.g., AI assigns B, Expert assigns C or A)
- **Major/Critical error**: >1 grade level (e.g., AI assigns A, Expert assigns C or D)

**Bias Interpretation**:
- Positive bias: AI consistently assigns higher grades than expert (lenient grading)
- Negative bias: AI consistently assigns lower grades than expert (harsh grading)
- Zero bias (p > 0.05): No systematic over/under-grading

---

### Error Analysis (`error_analysis_summary.csv`)

Same variables as `performance_summary_by_condition.csv` - this is a consolidated file combining confusion patterns and bias detection.

---

## Study Design

**Experimental Design**: Within-subjects factorial  
**Factors**:
1. **Model** (2 levels): ChatGPT-4o, Gemini 2.0 Flash
2. **Strategy** (3 levels): Lenient, Few-shot, Zero-shot
3. **Trial** (varying levels): 10 trials for lenient, 1 trial for baselines

**Total Conditions**: 2 × 3 = 6 experimental conditions  
**Grading Instances**: 
- Lenient strategies: 70 essays × 10 trials × 2 models = 1,400
- Baseline strategies (few-shot, zero-shot): 70 essays × 1 trial × 2 models × 2 strategies = 280
- **Total**: 1,680 planned (1,956 actual after excluding 24 API failures)

**Data Collection Period**: September 1 - October 15, 2024

**Participant Characteristics**:
- Sample size: 10 undergraduate students
- Gender: 7 female, 3 male
- Age range: 21-23 years
- Mean GPA: 3.2/4.0
- Program: Health Sciences (final year)
- Language: Native Indonesian speakers

**Assessment Context**:
- Course: Capstone Project (final year requirement)
- Task type: Analytical essay questions
- Question format: Open-ended, requiring critical analysis
- Topics: Research methodology, literature synthesis, applied problem-solving
- Submission: Digital (Learning Management System)
- Anonymization: Done before AI grading (blind evaluation)

---

## Missing Data

### ICC Values (None/NA for single-trial conditions)
**Variables affected**: `icc_value`, `icc_ci_lower`, `icc_ci_upper`  
**Conditions**: Few-shot and zero-shot strategies (both models)  
**Reason**: ICC requires multiple independent measurements per subject. Single-trial baselines lack repeated measures needed for ICC calculation.  
**Alternative metric**: Fleiss' kappa used instead for reliability assessment.

### API Failures (24 of 1,958 instances)
**Affected trials**: 
- 18 ChatGPT API timeouts
- 6 Gemini JSON parsing errors

**Handling**: Excluded from analysis (not replaced)  
**Impact**: Minimal (<2% of total grading instances)  
**Distribution**: Random across essays and strategies (no systematic pattern)

---

## Data Quality Assurance

### Validation Procedures

**Expert Grading**:
- Single expert rater (course lecturer, 15+ years experience)
- Blind to student identities
- Used structured rubric with clear criteria
- Grading completed before AI experiments
- No re-grading or score adjustments during study

**AI Grading**:
- Temperature = 0.3 (balanced determinism/variation)
- JSON response validation (completeness, score ranges)
- Retry mechanism for API failures (max 3 attempts)
- Version tracking (model snapshots documented)
- Timestamp logging for all API calls

**Statistical Analysis**:
- Cross-validation using multiple statistical packages
- Manual verification of edge cases
- Outlier investigation (all confirmed as genuine)
- Reproducible code with version control

### Data Cleaning

**No imputation performed** - missing values left as NA  
**No outlier removal** - all values retained (verified as valid)  
**No score transformation** - raw scores reported  
**No post-hoc exclusions** - all completed grading instances included

---

## Ethical Considerations

### Informed Consent
- Students provided written consent
- Participation voluntary
- No impact on course grades
- Right to withdraw at any time
- Data use limited to academic research

### Privacy Protection
- All PII removed (names, IDs, contact info)
- Essay content excluded from public dataset
- Institutional affiliation anonymized in data files
- Aggregate reporting for small cell sizes

### Institutional Approval
- Ethics review conducted
- Approval obtained before data collection
- FERPA/GDPR compliance verified
- Data security protocols implemented

---

## Usage Notes

### Recommended Applications
✅ LLM-AES validation studies  
✅ Reliability meta-analysis  
✅ Cross-model benchmarking  
✅ Multilingual AES research  
✅ Educational measurement methodology

### Not Recommended For
❌ High-stakes assessment without local validation  
❌ Commercial applications without permission  
❌ Re-identification attempts  
❌ Non-academic purposes without authorization

### Citation Requirement
Any use of this data **must** cite the original study:

```bibtex
@article{samsidar2026llmaes,
  title={Test-Retest Reliability of Large Language Models for Automated Essay Scoring},
  author={Samsidar and Mustamin, Syaiful Bachri and Fatmah, Siti},
  journal={Australasian Journal of Educational Technology},
  year={2026},
  doi={[pending]}
}
```

---

## Contact Information

**Data Questions**: Syaifulbachri@mail.ugm.ac.id  
**Replication Support**: See `05_Documentation/REPLICATION_GUIDE.md`  
**Technical Issues**: Submit issue on OSF project page  
**Collaboration Inquiries**: Contact corresponding author

---

## Version History

**v1.0** (January 2026)
- Initial public release
- Corresponds to AJET manuscript submission
- 70 gold standard essays
- 6 experimental conditions
- Complete statistical analysis

---

*Document prepared by: Syaiful Bachri Mustamin*  
*Last updated: December 25, 2025*
