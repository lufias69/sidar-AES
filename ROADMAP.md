# 🗺️ AES Project Roadmap
## Visual Timeline for Q1 Scopus Publication

---

```
📅 TIMELINE OVERVIEW (18 Weeks = ~4.5 Months)

Week 1-2    ████░░░░░░░░░░░░░░  Setup & Foundation
Week 3-4    ░░░░████░░░░░░░░░░  Core Development
Week 5-6    ░░░░░░░░████░░░░░░  Experiment Framework
Week 7-8    ░░░░░░░░░░░░████░░  Evaluation Metrics
Week 9      ░░░░░░░░░░░░░░░░██  Visualization & Reporting
Week 10-12  ░░░░░░░░░░░░░░░░░░  Data Collection & Experiments
Week 13-14  ░░░░░░░░░░░░░░░░░░  Analysis & Results
Week 15-18  ░░░░░░░░░░░░░░░░░░  Paper Writing & Submission
```

---

## 📊 Gantt Chart

```
TASK                          W1 W2 W3 W4 W5 W6 W7 W8 W9 W10 W11 W12 W13 W14 W15 W16 W17 W18
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment Setup             ██ ██ 
Project Structure             ██ ██ 
API Configuration             ░░ ██ 
Rubric System                       ██ ██ 
Agent Development                   ██ ██ ██ 
Scoring System                         ██ ██ 
Experiment Runner                         ██ ██ ██ 
Data Loader                                  ██ ██ 
Consistency Metrics                             ██ ██ 
Accuracy Metrics                                   ██ ██ 
Agreement Metrics                                     ██ ██ 
Statistical Tests                                        ██ ██ 
Visualization                                               ██ ██ 
Report Generator                                            ░░ ██ 
Data Collection (CRITICAL)                                      ██ ██ ██ ░░ 
Pilot Experiment                                                ░░ ██ ░░ ░░ 
Full Experiment Run                                                ░░ ██ ██ ░░ 
Quality Checks                                                           ░░ ██ ░░ 
Statistical Analysis                                                           ░░ ██ ██ 
Jupyter Notebooks                                                                 ░░ ██ ██ 
Answer RQs                                                                           ░░ ██ 
Paper Writing                                                                           ░░ ██ ██ ██ ██
Revision & Review                                                                              ░░ ░░ ██ ██
Submission Prep                                                                                       ░░ ██

Legend: ██ Active Work  ░░ Supporting/Review  ░░ Parallel Work
```

---

## 🎯 Milestone Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PROJECT MILESTONES                          │
└─────────────────────────────────────────────────────────────────────┘

📍 M1: Environment Ready (End of Week 2)
   ├── Python environment configured
   ├── APIs tested
   ├── Project structure created
   └── Git repository initialized
   
📍 M2: Core System Complete (End of Week 4)
   ├── Rubric system functional
   ├── ChatGPT agent working
   ├── Gemini agent working
   └── Scoring calculator validated
   
📍 M3: Experiment Framework Ready (End of Week 6)
   ├── 4x trial automation working
   ├── Batch processing implemented
   ├── Consistency metrics coded
   └── Data loader functional
   
📍 M4: Evaluation System Complete (End of Week 8)
   ├── All accuracy metrics implemented
   ├── Fleiss' Kappa working
   ├── Cohen's Kappa working
   └── Statistical tests ready
   
📍 M5: Visualization Ready (End of Week 9)
   ├── All plots/charts functional
   ├── Report generator working
   └── Export utilities ready
   
📍 M6: Pilot Test Passed (Week 11) ⚠️ CRITICAL
   ├── 2-3 essays successfully graded
   ├── Results validated
   ├── Pipeline debugged
   └── API costs estimated (~$1)
   
📍 M7: Full Experiment Complete (End of Week 12) ⚠️ CRITICAL
   ├── All 80 essays graded (4x trials each model)
   ├── ChatGPT results: 320 API calls
   ├── Gemini results: 320 API calls
   └── Quality checks passed
   
📍 M8: Analysis Complete (End of Week 14)
   ├── All metrics calculated
   ├── Research questions answered
   ├── Statistical tests performed
   └── Jupyter notebooks finished
   
📍 M9: First Draft Complete (End of Week 16)
   ├── All paper sections written
   ├── Tables & figures included
   ├── References added
   └── Internal review done
   
📍 M10: Paper Submitted (End of Week 18) 🎉
   ├── Manuscript finalized
   ├── Co-author approval
   ├── Formatted to journal
   └── Submitted to Q1 journal
```

---

## 🚦 Critical Path Analysis

### 🔴 CRITICAL PATH (Cannot be delayed)

```
Setup → Agent Development → Experiment Framework → 
Data Collection → Run Experiments → Analysis → Paper Writing
```

**Total Duration:** 18 weeks  
**Buffer Time:** 2 weeks (built into paper writing phase)

### ⚠️ High-Risk Tasks

1. **Data Collection (Week 10-11)**
   - **Risk:** Lecturers delay providing ground truth
   - **Mitigation:** Start coordination in Week 1, have backup lecturers
   
2. **API Costs/Rate Limits (Week 11-12)**
   - **Risk:** API costs exceed budget or rate limiting issues
   - **Mitigation:** Use Gemini as primary (cheaper), batch requests
   
3. **Experiment Failures (Week 12)**
   - **Risk:** Technical failures during 4x trials
   - **Mitigation:** Implement checkpointing, save after each essay

### ✅ Parallel Opportunities

- Weeks 3-6: Develop agents + experiment framework simultaneously
- Weeks 7-9: Implement metrics + create visualizations in parallel
- Weeks 10-12: Start initial analysis while experiments run
- Weeks 15-18: Write paper sections while doing revisions

---

## 📈 Weekly Breakdown

### 🗓️ Week 1-2: Foundation
**Goal:** Get environment ready to code

**Day 1-2:**
- Install Python, create venv
- Install all dependencies
- Test API keys

**Day 3-4:**
- Create full directory structure
- Setup Git + .gitignore
- Create configuration templates

**Day 5-7:**
- Write default rubric
- Setup logging system
- Create first unit tests

**Day 8-10:**
- Document setup process
- Create README
- Test everything works

**Deliverable:** ✅ Working dev environment

---

### 🗓️ Week 3-4: Core Development
**Goal:** Build the AI grading engine

**Week 3:**
- Day 1-2: Rubric class + tests
- Day 3-4: BaseAgent abstract class
- Day 5-7: ChatGPT agent implementation

**Week 4:**
- Day 1-3: Gemini agent implementation
- Day 4-5: Scoring system
- Day 6-7: Integration testing with sample essays

**Deliverable:** ✅ Working AI agents that can grade essays

---

### 🗓️ Week 5-6: Experiment Framework
**Goal:** Automate the 4x trial process

**Week 5:**
- Day 1-2: Experiment runner skeleton
- Day 3-4: 4x trial loop logic
- Day 5-7: Batch processing + rate limiting

**Week 6:**
- Day 1-3: Data loader for questions/answers
- Day 4-5: Consistency metrics implementation
- Day 6-7: Result storage system

**Deliverable:** ✅ Automated experiment pipeline

---

### 🗓️ Week 7-8: Evaluation Metrics
**Goal:** Implement all statistical measures

**Week 7:**
- Day 1-3: Accuracy metrics (MAE, RMSE, F1)
- Day 4-5: Confusion matrix generator
- Day 6-7: Start Fleiss' Kappa

**Week 8:**
- Day 1-2: Complete Fleiss' Kappa
- Day 3-4: Cohen's Kappa (pairwise)
- Day 5-7: Statistical tests (ANOVA, t-test)

**Deliverable:** ✅ Complete evaluation toolkit

---

### 🗓️ Week 9: Visualization
**Goal:** Create publication-ready figures

**Day 1-2:**
- Box plots, violin plots for consistency

**Day 3-4:**
- Confusion matrices, heatmaps

**Day 5-6:**
- Agreement charts, scatter plots

**Day 7:**
- Report generator, export utilities

**Deliverable:** ✅ Automated visualization system

---

### 🗓️ Week 10-12: EXPERIMENTS ⚠️ CRITICAL
**Goal:** Collect data and run all trials

**Week 10:**
- Day 1-3: Finalize dataset collection
- Day 4-7: Validate data quality, create CSV files

**Week 11:**
- Day 1-2: Pilot test (2-3 essays, 4x trials)
- Day 3-4: Fix bugs, optimize pipeline
- Day 5-7: Start full experiment (ChatGPT - 80 essays)

**Week 12:**
- Day 1-2: Complete ChatGPT trials (320 calls)
- Day 3-5: Run Gemini trials (320 calls - faster/cheaper)
- Day 6-7: Quality checks & validation

**Deliverable:** ✅ Complete experimental dataset (640 graded results)

---

### 🗓️ Week 13-14: Analysis
**Goal:** Answer all research questions

**Week 13:**
- Day 1-2: Load results, calculate consistency
- Day 3-4: Calculate accuracy vs dosen
- Day 5-7: Calculate Fleiss' Kappa

**Week 14:**
- Day 1-2: Statistical significance tests
- Day 3-5: Create all Jupyter notebooks
- Day 6-7: Interpret results, write insights

**Deliverable:** ✅ Complete statistical analysis

---

### 🗓️ Week 15-18: Paper Writing
**Goal:** Submit to Q1 journal

**Week 15:**
- Day 1-2: Abstract + Introduction
- Day 3-4: Related Work
- Day 5-7: Methodology section

**Week 16:**
- Day 1-3: Results section (tables/figures)
- Day 4-5: Discussion
- Day 6-7: Conclusion

**Week 17:**
- Day 1-3: Format to journal template
- Day 4-5: Internal review + revisions
- Day 6-7: Co-author feedback

**Week 18:**
- Day 1-2: Final revisions
- Day 3-4: Proofread, check references
- Day 5: Submit! 🎉

**Deliverable:** ✅ Submitted manuscript

---

## 📊 Resource Allocation

### Time Distribution
```
Phase                    Hours    Percentage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Setup                    40h      11%
Core Development         80h      22%
Experiment Framework     60h      17%
Evaluation Metrics       60h      17%
Visualization            20h       6%
Data + Experiments       40h      11%
Analysis                 40h      11%
Paper Writing            60h      17%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                   400h     100%
```

### Budget
```
Item                     Cost      Notes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OpenAI API (GPT-4o)      $5-10     80 essays × 4 trials (cheaper!)
Google Gemini 2.0 Flash  $0.08     Very cheap alternative
Development Tools        $0        Open source
Total                    ~$8       Sangat terjangkau!
```

---

## 🎓 Publication Timeline

```
Week 18  📤 Submit to Target Journal
Week 20  📧 Acknowledgment received
Week 24  📝 Reviews received (typical: 4-6 weeks)
Week 26  ✍️  Revision & resubmission
Week 28  ✅ Acceptance (if minor revisions)
Week 32  📰 Published online

TOTAL: ~8 months from start to publication
```

---

## 🎯 Key Success Factors

### Technical
1. ✅ Robust error handling (API failures)
2. ✅ Checkpointing (resume experiments)
3. ✅ Comprehensive logging
4. ✅ Unit tests (>80% coverage)

### Research
1. ✅ Sufficient sample size (1500 essays)
2. ✅ Quality ground truth (dosen scores)
3. ✅ Rigorous statistics (Fleiss' Kappa)
4. ✅ Reproducible methodology

### Writing
1. ✅ Clear contribution statement
2. ✅ Strong related work
3. ✅ Detailed methodology
4. ✅ Honest limitations

---

## 🚨 Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API rate limits | High | Medium | Batch requests, use Gemini primary |
| Data collection delay | High | High | Start early, backup lecturers |
| Low Fleiss' Kappa | High | Low | Pilot test, refine prompts |
| Budget overrun | Medium | Low | Monitor costs, use Gemini |
| Technical bugs | Medium | Medium | Unit tests, code review |
| Paper rejection | Medium | Medium | Target multiple journals |

---

## 📞 Weekly Check-ins

### Every Monday (30 min):
- [ ] Review last week's progress
- [ ] Update checklist
- [ ] Identify blockers
- [ ] Plan current week

### Every Friday (15 min):
- [ ] Document completed tasks
- [ ] Update roadmap status
- [ ] Prepare for next week

---

## 🎉 Celebration Milestones

- ✅ Week 2: Environment setup party! 🎊
- ✅ Week 4: First AI grading working! 🤖
- ✅ Week 9: Pipeline complete! 🚀
- ✅ Week 12: Experiments done! 🧪
- ✅ Week 14: Analysis complete! 📊
- ✅ Week 18: PAPER SUBMITTED! 🎓🍾

---

**Next Step:** Start Phase 1 - Week 1 Day 1  
**First Task:** Install Python 3.9+ and create virtual environment  
**Estimated Time:** 30 minutes

Ready? Let's build this! 💪
