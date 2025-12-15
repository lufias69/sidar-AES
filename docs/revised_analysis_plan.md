# RENCANA ANALISIS REVISI - FOKUS LENIENT STRATEGY

**Tanggal:** 11 Desember 2025  
**Status:** Draft Revisi - Fokus pada data 10 trials

---

## EXECUTIVE SUMMARY

### Perubahan Strategi
- **Sebelumnya:** Analisis 6 strategies (lenient, zero-shot, few-shot × 2 models)
- **Sekarang:** Fokus pada **lenient strategy only** (10 trials, 1,538 tasks)
- **Alasan:** Zero-shot dan few-shot hanya punya 1 trial → tidak cukup untuk analisis statistik yang robust

### Data yang Digunakan
| Strategy | Model | Trials | Tasks | Status |
|----------|-------|--------|-------|--------|
| **Lenient** | **ChatGPT** | **10** | **770** | ✅ **DIGUNAKAN** |
| **Lenient** | **Gemini** | **10** | **768** | ✅ **DIGUNAKAN** |
| Zero-shot | ChatGPT | 1 | 70 | ❌ DIABAIKAN |
| Zero-shot | Gemini | 1 | 70 | ❌ DIABAIKAN |
| Few-shot | ChatGPT | 2 | 140 | ❌ DIABAIKAN |
| Few-shot | Gemini | 2 | 140 | ❌ DIABAIKAN |

**Total data analysis:** 1,538 grading tasks (lenient strategy, 10 trials)

---

## RESEARCH QUESTIONS (REVISI)

### RQ1: Reliability vs Expert Grading
**Pertanyaan:** Seberapa akurat AES dengan lenient strategy dibandingkan expert grading?

**Analisis:**
1. **Agreement Metrics**
   - Exact Agreement (EA)
   - Adjacent Agreement (AA)
   - Cohen's Kappa (κ)
   - Quadratic Weighted Kappa (QWK)

2. **Classification Metrics**
   - Accuracy per grade level (A, B, C, D)
   - Precision, Recall, F1-Score
   - Confusion Matrix analysis

3. **Perbandingan Model**
   - ChatGPT-lenient vs Expert
   - Gemini-lenient vs Expert
   - Statistical significance testing

**Visualisasi:**
- Figure 1: Overall agreement comparison (bar chart)
- Figure 2: Confusion matrices (ChatGPT & Gemini)
- Figure 3: Agreement by grade level (grouped bar)
- Figure 4: QWK score comparison
- Table 1: Comprehensive metrics summary

---

### RQ2: Inter-Rater Reliability
**Pertanyaan:** Seberapa konsisten AES lenient across 10 trials?

**Analisis:**
1. **Intraclass Correlation Coefficient (ICC)**
   - ICC(2,1) untuk consistency
   - ICC(2,k) untuk average measures
   - Confidence intervals (95%)

2. **Internal Consistency**
   - Cronbach's Alpha
   - Split-half reliability

3. **Multi-Rater Agreement**
   - Fleiss' Kappa (10 trials sebagai 10 raters)
   - Kendall's W (coefficient of concordance)

4. **Variance Analysis**
   - Between-trial variance
   - Within-trial variance
   - Question-level consistency

**Visualisasi:**
- Figure 5: ICC scores per question (forest plot)
- Figure 6: Trial-to-trial consistency heatmap
- Figure 7: Variance decomposition
- Figure 8: Reliability by question difficulty
- Table 2: ICC and reliability metrics summary

---

### RQ3: Model Comparison (ChatGPT vs Gemini)
**Pertanyaan:** Model mana yang lebih baik untuk AES dengan lenient strategy?

**Analisis:**
1. **Head-to-Head Comparison**
   - Agreement dengan expert (per model)
   - Consistency across trials (ICC per model)
   - Error rates per grade level

2. **Statistical Testing**
   - Paired t-test (mean scores)
   - Wilcoxon signed-rank test (non-parametric)
   - McNemar's test (categorical agreement)
   - Effect size (Cohen's d)

3. **Performance Metrics**
   - API call success rate
   - Average tokens per grading
   - Time per grading task
   - Cost efficiency

4. **Qualitative Analysis**
   - Error pattern differences
   - Justification quality
   - Edge case handling

**Visualisasi:**
- Figure 9: Side-by-side performance comparison
- Figure 10: Win-loss-tie analysis per question
- Figure 11: Error distribution comparison
- Figure 12: Efficiency metrics (time, tokens, cost)
- Table 3: Statistical test results
- Table 4: Performance summary by model

---

### RQ4: Error Analysis
**Pertanyaan:** Kapan dan mengapa AES lenient melakukan kesalahan?

**Analisis:**
1. **Error Distribution**
   - Error rate by grade level (A, B, C, D)
   - Over-grading vs under-grading patterns
   - Question difficulty correlation

2. **Confusion Patterns**
   - Most common confusions (B↔C, C↔D, etc.)
   - Systematic vs random errors
   - Model-specific error patterns

3. **Answer Characteristics**
   - Length correlation with errors
   - Keyword presence analysis
   - Language quality indicators

4. **Critical Errors**
   - 2+ grade level differences
   - Fail → Pass misclassifications
   - Consistency of errors across trials

**Visualisasi:**
- Figure 13: Error rate by grade level (both models)
- Figure 14: Confusion pattern heatmap
- Figure 15: Over/under-grading distribution
- Figure 16: Error consistency across trials
- Table 5: Detailed error breakdown
- Table 6: Critical errors analysis

---

### RQ5: Practical Implications
**Pertanyaan:** Apakah AES lenient feasible untuk implementasi praktis?

**Analisis:**
1. **Operational Metrics**
   - Total execution time (10 trials)
   - Average time per student
   - Peak performance periods
   - Failure/retry rates

2. **Cost Analysis**
   - Total API costs (per model)
   - Cost per grading task
   - Cost per student
   - Projected annual costs

3. **Scalability Assessment**
   - Throughput capacity
   - Concurrent request handling
   - Database performance
   - Resource utilization

4. **Deployment Recommendations**
   - Optimal strategy selection
   - Model selection criteria
   - Quality assurance mechanisms
   - Human-in-the-loop integration

**Visualisasi:**
- Figure 17: Execution time distribution
- Figure 18: Cost breakdown by component
- Figure 19: Throughput analysis
- Table 7: Operational metrics summary
- Table 8: Cost comparison (AES vs manual grading)

---

## IMPLEMENTATION PLAN

### Phase 1: Data Preparation (1 hour)
- [ ] Extract lenient data only from database
- [ ] Validate data completeness (1,538 tasks)
- [ ] Merge with expert grades
- [ ] Check for missing values
- [ ] Prepare analysis datasets

**Script:** `extract_lenient_data.py`

### Phase 2: RQ1 Analysis (2 hours)
- [ ] Calculate agreement metrics
- [ ] Generate confusion matrices
- [ ] Statistical significance tests
- [ ] Create visualizations (4 figures, 1 table)
- [ ] Write analysis narrative

**Script:** `rq1_reliability_lenient.py`

### Phase 3: RQ2 Analysis (2 hours)
- [ ] Calculate ICC for all questions
- [ ] Compute Cronbach's Alpha
- [ ] Fleiss' Kappa analysis
- [ ] Variance decomposition
- [ ] Create visualizations (4 figures, 1 table)

**Script:** `rq2_consistency_lenient.py`

### Phase 4: RQ3 Analysis (2 hours)
- [ ] Model comparison metrics
- [ ] Statistical testing (t-test, Wilcoxon, McNemar)
- [ ] Performance analysis
- [ ] Efficiency comparison
- [ ] Create visualizations (4 figures, 2 tables)

**Script:** `rq3_model_comparison.py`

### Phase 5: RQ4 Analysis (3 hours)
- [ ] Error classification
- [ ] Pattern identification
- [ ] Answer characteristic analysis
- [ ] Critical errors review
- [ ] Create visualizations (4 figures, 2 tables)

**Script:** `rq4_error_analysis_lenient.py`

### Phase 6: RQ5 Analysis (1 hour)
- [ ] Operational metrics calculation
- [ ] Cost analysis
- [ ] Scalability assessment
- [ ] Deployment recommendations
- [ ] Create visualizations (3 figures, 2 tables)

**Script:** `rq5_practical_implications.py`

### Phase 7: Report Generation (2 hours)
- [ ] Compile all results
- [ ] Generate comprehensive PDF report
- [ ] Create executive summary
- [ ] Write discussion section
- [ ] Prepare journal submission draft

**Script:** `generate_comprehensive_report.py`

---

## DELIVERABLES

### 1. Figures (19 total)
- RQ1: 4 figures (agreement, confusion, by-grade, QWK)
- RQ2: 4 figures (ICC, consistency, variance, reliability)
- RQ3: 4 figures (comparison, win-loss, errors, efficiency)
- RQ4: 4 figures (error rates, patterns, distribution, consistency)
- RQ5: 3 figures (time, cost, throughput)

### 2. Tables (8 total)
- RQ1: 1 table (metrics summary)
- RQ2: 1 table (reliability metrics)
- RQ3: 2 tables (statistical tests, performance)
- RQ4: 2 tables (error breakdown, critical errors)
- RQ5: 2 tables (operational metrics, cost analysis)

### 3. Reports
- Comprehensive analysis report (PDF, 50-70 pages)
- Executive summary (2-3 pages)
- Journal submission draft (IEEE format)
- Supplementary materials

---

## EXPECTED OUTCOMES

### Key Findings (Predicted)
1. **High reliability:** QWK > 0.85 for lenient strategy
2. **Strong consistency:** ICC > 0.90 across 10 trials
3. **Model differences:** ChatGPT likely superior in exact agreement
4. **Grade-specific patterns:** Difficulty with borderline cases (C/D)
5. **Practical feasibility:** Cost-effective compared to manual grading

### Publication Focus
- **Title:** "Validating Large Language Models for Automated Essay Scoring in Indonesian Higher Education: A Multi-Trial Reliability Study"
- **Contribution:** First comprehensive validation of LLM-based AES in Indonesian context with 10-trial reliability testing
- **Target:** IEEE Access, Education and Information Technologies, or similar Q1/Q2 journal

---

## TIMELINE

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Data Preparation | 1 hour | ⏳ Pending |
| 2 | RQ1 Analysis | 2 hours | ⏳ Pending |
| 3 | RQ2 Analysis | 2 hours | ⏳ Pending |
| 4 | RQ3 Analysis | 2 hours | ⏳ Pending |
| 5 | RQ4 Analysis | 3 hours | ⏳ Pending |
| 6 | RQ5 Analysis | 1 hour | ⏳ Pending |
| 7 | Report Generation | 2 hours | ⏳ Pending |
| **TOTAL** | | **13 hours** | |

**Target Completion:** 12 Desember 2025  
**Publication Submission:** 15 Desember 2025

---

## ADVANTAGES OF THIS APPROACH

### Methodological Strengths
✅ **Robust statistics:** 10 trials provide solid statistical power  
✅ **Reliable ICC:** Can calculate proper inter-rater reliability  
✅ **Comparative analysis:** 2 models × 10 trials = strong comparison  
✅ **Variance analysis:** Can assess trial-to-trial consistency  
✅ **Publication ready:** Sufficient data for peer review

### Practical Benefits
✅ **Focused narrative:** Single strategy, clear conclusions  
✅ **Faster completion:** No need for additional experiments  
✅ **Clear recommendations:** Lenient strategy validation  
✅ **Cost-effective:** Use existing data only  
✅ **Actionable insights:** Direct implementation guidance

### Limitations (Acknowledged)
⚠️ **Single strategy:** Cannot compare lenient vs zero-shot/few-shot  
⚠️ **No prompt comparison:** Cannot evaluate prompt engineering impact  
⚠️ **Single dataset:** Limited to UTS Capstone Project exams  

**Mitigation:** Frame as validation study, suggest future work for strategy comparison

---

## NEXT STEPS

1. **Confirm approval:** User confirms this analysis plan
2. **Create extraction script:** `extract_lenient_data.py`
3. **Run Phase 1:** Data preparation and validation
4. **Sequential execution:** RQ1 → RQ2 → RQ3 → RQ4 → RQ5
5. **Generate report:** Comprehensive analysis document
6. **Prepare submission:** Format for journal submission

---

**READY TO START?** 🚀
