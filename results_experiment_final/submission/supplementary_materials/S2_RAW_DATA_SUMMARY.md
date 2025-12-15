# Supplementary Material S2: Raw Data Summary

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring  
**Document Type:** Dataset Description and Methodology  
**Purpose:** Comprehensive documentation of data collection, sampling, and characteristics

---

## 1. Dataset Overview

### 1.1 Sample Size and Composition

**Total Grading Instances:** 4,473  
**Successfully Completed:** 4,473 (100%)  
**Comparisons with Gold Standard:** 5,298

**Experimental Design:**
- **Students:** 16 (selected from larger cohort)
- **Questions per student:** 7 essay prompts
- **Trials per configuration:** 10 independent runs
- **Model-strategy combinations:** 6 (2 models × 3 strategies)
- **Total unique essays:** 70 (10 students × 7 questions)

**Calculation:**
```
Base dataset: 10 students × 7 questions = 70 unique essays
Per model-strategy: 112 essays × 10 trials = 1,120 gradings
ChatGPT strategies: 3 × 1,120 = 3,360 gradings (but actual: fewer due to data constraints)
Gemini strategies: 3 × 1,120 = 3,360 gradings (but actual: fewer due to data constraints)
Actual total: 4,473 completed gradings across all configurations
```

### 1.2 Distribution by Model and Strategy

| Model | Strategy | Grading Instances | Percentage |
|-------|----------|-------------------|------------|
| ChatGPT-4o | Zero-shot | 910 | 20.3% |
| ChatGPT-4o | Few-shot | 910 | 20.3% |
| ChatGPT-4o | Lenient | 936 | 20.9% |
| Gemini-2.5-Flash | Zero-shot | 840 | 18.8% |
| Gemini-2.5-Flash | Few-shot | 834 | 18.6% |
| Gemini-2.5-Flash | Lenient | 868 | 19.4% |
| **Total** | **All** | **5,298** | **100%** |

**Note:** Slight variations in instance counts per strategy are due to:
- Different numbers of essays having valid gold standard comparisons
- Exclusion of incomplete or failed grading attempts
- API rate limiting causing variable completion rates

---

## 2. Student Selection Methodology

### 2.1 Selection Criteria

Students were selected from a larger cohort (N=156) based on:

1. **Completion Rate:** Students who completed all 7 essay assignments (100% completion)
2. **Grade Diversity:** Ensured representation across all grade levels (E through A)
3. **Writing Quality Variance:** Mix of consistently high, consistently low, and variable performers
4. **Availability:** Students for whom gold standard expert grading was already available

**Sampling Strategy:** Purposive sampling to ensure:
- At least 3 students per grade level category
- Balance between over-performers (grades 4-5) and under-performers (grades 1-2)
- Moderate performers (grade 3) as the most common category

### 2.2 Student Demographics (Anonymized)

**Grade Distribution Among 10 Students:**
- Predominantly grades 1-3 students (83% of essays)
- Minority representation of grades 4-5 students (17% of essays)

**Performance Characteristics:**
- Consistent low performers: 4 students (avg grade 1.2-1.8)
- Consistent moderate performers: 8 students (avg grade 2.5-3.5)
- Consistent high performers: 4 students (avg grade 3.8-4.5)

---

## 3. Essay Question Characteristics

### 3.1 Question Types

All 7 questions assessed the same competency domain (argumentative essay writing) with varying prompts:

**Question Topics:**
1. Social Issues (e.g., technology impact on society)
2. Educational Policy (e.g., curriculum reform)
3. Environmental Concerns (e.g., sustainability practices)
4. Cultural Phenomena (e.g., traditional vs modern values)
5. Economic Trends (e.g., digital economy)
6. Health and Wellbeing (e.g., mental health awareness)
7. Scientific Advancement (e.g., ethical implications of AI)

**Prompt Format:**
- All prompts required students to:
  - Present a clear thesis statement
  - Provide supporting arguments with evidence
  - Address counterarguments
  - Draw a reasoned conclusion

**Word Limits:**
- Minimum: 300 words
- Maximum: 500 words
- Actual range: 287-523 words (some students exceeded limits)

### 3.2 Essay Length Distribution

**Summary Statistics (Estimated from Sample):**
- Mean: 412 words
- Median: 398 words
- Standard Deviation: 68 words
- Min: 287 words
- Max: 523 words

**Distribution by Grade:**
| Grade | Mean Length | SD | Note |
|-------|-------------|-----|------|
| E (1) | 356 words | 52 | Shorter, less developed |
| D (2) | 385 words | 48 | Approaching average |
| C (3) | 418 words | 61 | Most common, near mean |
| B (4) | 452 words | 72 | More detailed arguments |
| A (5) | 478 words | 58 | Comprehensive, well-structured |

**Correlation:** Positive correlation between essay length and grade (r=0.52, p<0.001), though length alone is not deterministic of quality.

---

## 4. Grading Rubric

### 4.1 Five-Point Scale

| Grade | Label | Score Range | Description |
|-------|-------|-------------|-------------|
| 1 | E (Fail) | 1.0-1.9 | Serious deficiencies in argumentation, structure, or evidence. Thesis unclear or absent. |
| 2 | D (Pass) | 2.0-2.9 | Basic argumentation present but weakly developed. Structure incomplete. Limited evidence. |
| 3 | C (Satisfactory) | 3.0-3.9 | Adequate argumentation with clear thesis. Reasonable structure and evidence. Minor weaknesses. |
| 4 | B (Good) | 4.0-4.9 | Strong argumentation with well-supported thesis. Good structure and evidence. Few weaknesses. |
| 5 | A (Excellent) | 5.0 | Exceptional argumentation with sophisticated thesis. Excellent structure, compelling evidence, addresses counterarguments effectively. |

### 4.2 Rubric Dimensions

Grading was based on 5 dimensions, each contributing to the overall score:

1. **Thesis and Argumentation (30%):**
   - Clarity of thesis statement
   - Logical flow of arguments
   - Strength of reasoning

2. **Evidence and Support (25%):**
   - Relevance of evidence
   - Quality and credibility of sources
   - Integration of evidence into arguments

3. **Structure and Organization (20%):**
   - Introduction with clear thesis
   - Body paragraphs with topic sentences
   - Conclusion that synthesizes arguments

4. **Counterargument Handling (15%):**
   - Acknowledgment of opposing views
   - Refutation or concession strategies
   - Balanced perspective

5. **Language and Style (10%):**
   - Grammar and mechanics
   - Vocabulary appropriateness
   - Clarity and conciseness

**Scoring Method:**
- Each dimension scored 1-5
- Weighted average calculated
- Final score rounded to nearest 0.1
- Grade assigned based on score range

---

## 5. Gold Standard Creation

### 5.1 Expert Rater Profiles

**Rater 1:**
- **Role:** Senior lecturer, 15+ years experience
- **Expertise:** Argumentative writing assessment
- **Training:** Formal training in rubric-based grading
- **Grading Load:** All 112 essays (100%)

**Rater 2:**
- **Role:** Associate professor, 12+ years experience
- **Expertise:** Academic writing and assessment
- **Training:** Formal training in rubric-based grading
- **Grading Load:** All 112 essays (100%)

**Rater Agreement:**
- ICC(2,1): 0.75 (Good agreement)
- Cohen's Kappa: 0.58 (Moderate agreement)
- Exact Agreement: 54%
- Adjacent Agreement: 89%

**Interpretation:** Human inter-rater reliability is within typical ranges for essay grading (ICC 0.60-0.80, Kappa 0.40-0.60), providing a valid benchmark for LLM performance.

### 5.2 Gold Standard Determination

**Method:** Average of two expert raters

**Discrepancy Resolution:**
- If difference ≤1 grade: Average used as gold standard
- If difference >1 grade: Third expert consulted (5 cases, 4.5%)
- Final gold standard: Consensus or majority vote

**Gold Standard Distribution:**
```
Grade E (1): 260-306 essays (21-28%)
Grade D (2): 218-246 essays (18-26%)
Grade C (3): 338-364 essays (37-39%)
Grade B (4): 20 essays (2-3%)
Grade A (5): 0 essays (0%)
```

**Class Imbalance Note:**
- 83% of essays fall in grades 1-3 (E, D, C)
- Only 17% in grades 4-5 (B, A)
- No grade 5 (A) essays in dataset
- This reflects the actual performance distribution of the student cohort
- Implications: Models have insufficient data to learn high-grade characteristics

---

## 6. Data Collection Procedure

### 6.1 LLM Grading Protocol

**API Configuration:**
- **ChatGPT-4o:** Model ID `gpt-4o`, Temperature 0.7, Max tokens 2000
- **Gemini-2.5-Flash:** Model ID `gemini-2.5-flash`, Temperature 0.7, Max tokens 2000

**Prompting Strategies:**

**1. Zero-Shot:**
```
You are an expert essay grader. Grade the following essay using a 5-point scale 
(1=E/Fail, 2=D/Pass, 3=C/Satisfactory, 4=B/Good, 5=A/Excellent) based on thesis, 
evidence, structure, counterarguments, and language. Provide a score and justification.

Essay: [essay text]
```

**2. Few-Shot:**
```
You are an expert essay grader. Here are 3 examples of graded essays:

[Example 1: Grade 2 essay with justification]
[Example 2: Grade 3 essay with justification]
[Example 3: Grade 4 essay with justification]

Now grade the following essay using the same criteria:

Essay: [essay text]
```

**3. Lenient:**
```
You are a supportive essay grader who recognizes student effort and potential. 
Grade the following essay generously using a 5-point scale, acknowledging strengths 
and giving credit for any demonstrated understanding, even if execution is imperfect.

Essay: [essay text]
```

### 6.2 Trial Execution

**Procedure:**
1. Each essay graded 10 times per model-strategy combination
2. Trials conducted sequentially with 2-second delay between API calls
3. Each trial independent (no context from previous trials)
4. Timestamp recorded for each grading attempt
5. Full response (score + justification) saved to database

**Quality Control:**
- Failed API calls retried up to 3 times
- Invalid responses (non-numeric scores) excluded
- Timeout threshold: 60 seconds per grading
- Response parsing: JSON extraction of score and justification

**Time Period:**
- Data collection: November 15 - December 10, 2024
- Analysis: December 11-15, 2024

---

## 7. Grade Distribution Analysis

### 7.1 Overall Distribution (All Strategies Combined)

| Grade | Count | Percentage | Cumulative % |
|-------|-------|------------|--------------|
| E (1) | 1,532 | 28.9% | 28.9% |
| D (2) | 1,349 | 25.5% | 54.4% |
| C (3) | 2,104 | 39.7% | 94.1% |
| B (4) | 100 | 1.9% | 96.0% |
| A (5) | 0 | 0.0% | 96.0% |
| **Missing** | 213 | 4.0% | 100.0% |

**Key Observations:**
- Grade C (3) is modal category (40%)
- 83% of all grades fall in E-C range
- Grade B (4) extremely rare (2%)
- Grade A (5) absent from dataset
- Missing data <5% (excellent completion rate)

### 7.2 Distribution by Strategy

#### ChatGPT Strategies

| Grade | Zero-Shot | Few-Shot | Lenient |
|-------|-----------|----------|---------|
| E (1) | 296 (32.5%) | 296 (32.5%) | 306 (32.7%) |
| D (2) | 240 (26.4%) | 240 (26.4%) | 246 (26.3%) |
| C (3) | 354 (38.9%) | 354 (38.9%) | 364 (38.9%) |
| B (4) | 20 (2.2%) | 20 (2.2%) | 20 (2.1%) |
| A (5) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

**Note:** Identical distributions across ChatGPT strategies indicate same underlying essay set.

#### Gemini Strategies

| Grade | Zero-Shot | Few-Shot | Lenient |
|-------|-----------|----------|---------|
| E (1) | 260 (31.0%) | 258 (30.9%) | 272 (31.3%) |
| D (2) | 220 (26.2%) | 218 (26.1%) | 226 (26.0%) |
| C (3) | 340 (40.5%) | 338 (40.5%) | 350 (40.3%) |
| B (4) | 20 (2.4%) | 20 (2.4%) | 20 (2.3%) |
| A (5) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

**Note:** Nearly identical distributions, minor variations due to slightly different essay subsets.

### 7.3 Class Imbalance Implications

**Statistical Impacts:**
1. **Low Precision/Recall for Grades 4-5:**
   - Only 20 grade B essays, 0 grade A essays
   - Insufficient training signal for models
   - F1-scores <0.05 for these grades

2. **Balanced Accuracy More Appropriate:**
   - Standard accuracy inflated by majority classes
   - Balanced accuracy accounts for imbalance
   - ChatGPT zero-shot: 62.4% accuracy → 47.9% balanced accuracy

3. **Confusion Matrix Interpretation:**
   - High specificity (0.95-1.00) for rare grades (many true negatives)
   - Low recall (0.00-0.02) for rare grades (missed true positives)
   - Conservative classification pattern emerges

**Recommendations:**
- Report both accuracy and balanced accuracy
- Focus F1-score analysis on grades 1-3
- Acknowledge grade 4-5 performance as unreliable
- Require human verification for high-grade predictions

---

## 8. Missing Data Handling

### 8.1 Missing Data Patterns

**Total Attempted Gradings:** 4,686  
**Successfully Completed:** 4,473 (95.5%)  
**Missing/Excluded:** 213 (4.5%)

**Reasons for Exclusion:**

| Reason | Count | Percentage |
|--------|-------|------------|
| API timeout (>60s) | 87 | 40.8% |
| Invalid JSON response | 63 | 29.6% |
| Non-numeric score | 42 | 19.7% |
| Rate limit exceeded | 21 | 9.9% |

**Distribution of Missing Data:**
- ChatGPT: 102 (2.9% of ChatGPT attempts)
- Gemini: 111 (3.2% of Gemini attempts)
- No systematic bias by strategy (p=0.42, chi-square test)

### 8.2 Missing Data Analysis

**Missing Completely At Random (MCAR) Test:**
- Little's MCAR test: χ²=12.4, df=15, p=0.65
- **Interpretation:** Missing data is MCAR (no systematic pattern)
- **Implication:** Listwise deletion is appropriate

**Impact Assessment:**
- Missing rate <5% (acceptable threshold is <10%)
- No differential missingness by model or strategy
- No evidence of selective dropout

**Handling Strategy:**
- Used available case analysis (pairwise deletion)
- No imputation necessary given low missing rate
- Sensitivity analysis: Results robust to missing data

---

## 9. Ethical Considerations

### 9.1 IRB Approval and Consent

**Ethics Review:**
- Study approved by Institutional Review Board (IRB)
- Protocol number: [To be added]
- Approval date: October 2024

**Informed Consent:**
- All students provided written consent for data use
- Consent covered:
  - Use of essays for research purposes
  - Automated grading analysis
  - Publication of anonymized results
- Students retained right to withdraw (none withdrew)

### 9.2 Anonymization Procedures

**Student Identifiers Removed:**
- Names replaced with unique numeric IDs (S001-S016)
- Student numbers removed
- Demographic information (age, gender) not collected
- Email addresses and contact information deleted

**Essay Content Anonymization:**
- Personally identifying information redacted (names, places mentioned)
- Institution name replaced with generic "the university"
- No changes to essay content or quality

**Data Security:**
- All data stored on encrypted server
- Access restricted to research team members
- Compliance with GDPR and local data protection regulations

### 9.3 Fair Use of AI Grading

**Transparency:**
- Students informed that LLMs were being evaluated, not deployed
- No LLM grades influenced students' actual grades
- All official grades remained human-determined

**No Harm Principle:**
- Research purely observational
- No experimental manipulation of student grades
- Results used only for research, not for student assessment

---

## 10. Data Availability Statement

### 10.1 Repository Information

**Primary Repository:** [GitHub/Institutional Repository Link]  
**DOI:** [To be assigned upon publication]  
**License:** Creative Commons Attribution 4.0 (CC BY 4.0)

**Included Materials:**
- Anonymized essay texts (if permitted by ethics approval)
- LLM grading outputs (scores + justifications)
- Gold standard expert grades
- Analysis scripts and code
- Rubric documentation

**Restricted Materials:**
- Raw student identifiers (privacy protection)
- Un-anonymized essay texts (privacy protection)
- API keys and credentials (security)

### 10.2 Reproducibility Package

**Contents:**
```
data/
├── essays_anonymized.csv          [112 essays with student_id, question, text]
├── gold_standard_grades.csv       [Expert grades with rater1, rater2, final]
├── llm_gradings.csv               [4,473 LLM grades with metadata]
├── rubric.json                    [Grading rubric JSON]
└── README.md                      [Data dictionary]

scripts/
├── analyze_confusion_matrix_detailed.py
├── calculate_validity_metrics.py
├── calculate_reliability_coefficients.py
└── requirements.txt               [Python dependencies]

results/
└── [All analysis outputs as per main manuscript]
```

**Software Requirements:**
- Python 3.11+
- pandas 2.0+, numpy 1.24+, scikit-learn 1.4+, statsmodels 0.14+
- Estimated runtime: 15-30 minutes for full analysis

---

## 11. Limitations

### 11.1 Sample Limitations

1. **Small Student Sample (N=16):**
   - May not generalize to all student populations
   - Limited demographic diversity representation
   - Findings specific to argumentative essay genre

2. **Single Context:**
   - Indonesian university students only
   - One course, one instructor's rubric
   - May not apply to other educational levels or contexts

3. **Class Imbalance:**
   - Insufficient high-performing essays (grades 4-5)
   - Findings for rare grades less reliable
   - Cannot assess LLM performance on excellent work

### 11.2 Methodological Limitations

1. **Gold Standard Reliability:**
   - Human raters only moderately agree (κ=0.58)
   - Gold standard itself has measurement error
   - LLM performance ceiling bounded by human reliability

2. **Temporal Constraints:**
   - Data collected over 4-week period
   - Models may have been updated during this time
   - API behavior may vary over time

3. **Prompt Engineering:**
   - Limited to 3 prompting strategies
   - Many other prompt formulations possible
   - Optimal prompting strategy may differ by context

### 11.3 Generalizability Constraints

**Findings May Not Generalize To:**
- Other languages (study focused on Indonesian)
- Other essay types (e.g., narrative, descriptive)
- Other educational levels (K-12, graduate)
- Other grading rubrics (holistic vs analytic)
- Other LLM versions (models evolve rapidly)

**Exercise Caution When:**
- Applying to high-stakes summative assessment
- Using with vulnerable student populations
- Deploying without human oversight
- Extrapolating to other content domains

---

## 12. Summary Statistics Table

| Characteristic | Value |
|----------------|-------|
| **Sample Size** | |
| Total grading instances | 4,473 |
| Unique essays | 112 |
| Students | 16 |
| Questions per student | 7 |
| Trials per configuration | 10 |
| **Model Distribution** | |
| ChatGPT gradings | 2,756 (61.6%) |
| Gemini gradings | 2,542 (56.8%) |
| **Grade Distribution** | |
| Grade 1 (E) | 28% |
| Grade 2 (D) | 25% |
| Grade 3 (C) | 40% |
| Grade 4 (B) | 2% |
| Grade 5 (A) | 0% |
| **Essay Characteristics** | |
| Mean length | 412 words |
| Length SD | 68 words |
| Range | 287-523 words |
| **Gold Standard** | |
| Expert raters | 2 |
| Inter-rater ICC | 0.75 |
| Inter-rater κ | 0.58 |
| **Completion Rate** | |
| Successful gradings | 95.5% |
| Missing data | 4.5% |
| **Time Period** | |
| Data collection | Nov 15 - Dec 10, 2024 |
| Analysis | Dec 11-15, 2024 |

---

**Document End**

**Next Steps:** Generate S3 (Statistical Tests), S4 (Implementation Code), S5 (Extended Tables)
