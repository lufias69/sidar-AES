# Project Plan: AI-Based Automated Essay Scoring System
## Research for Q1 Scopus Publication

---

## 📋 Executive Summary

**Judul Penelitian:**  
"Comparative Analysis of Large Language Models (ChatGPT vs Gemini) for Automated Essay Scoring: A Multi-Criteria Assessment with Fleiss' Kappa Agreement"

**Tujuan:**
1. Mengembangkan sistem AES menggunakan ChatGPT dan Gemini
2. Mengukur konsistensi penilaian melalui 4x percobaan
3. Membandingkan akurasi dengan ground truth dosen
4. Menganalisis inter-rater agreement menggunakan Fleiss' Kappa

---

## 🎯 Research Questions

1. **RQ1:** Seberapa konsisten ChatGPT dan Gemini dalam memberikan skor esai pada multiple trials?
2. **RQ2:** Bagaimana akurasi ChatGPT dan Gemini dibandingkan dengan penilaian dosen?
3. **RQ3:** Seberapa tinggi kesepakatan (agreement) antara AI models dan dosen menggunakan Fleiss' Kappa?
4. **RQ4:** Model mana yang lebih reliable untuk automated essay scoring?

---

## 📊 Metodologi Research

### A. Data Collection
- **Jumlah Soal:** 8 soal esai
- **Jumlah Mahasiswa:** 10 mahasiswa (80 esai total)
- **Rubrik:** 4 kriteria penilaian dengan skala A, B, C, D/E

### B. Eksperimen Design
```
Setiap Jawaban Mahasiswa → Dinilai oleh:
├── ChatGPT (4x percobaan)
├── Gemini (4x percobaan)
└── Dosen (1x sebagai ground truth)

Total: 10 mahasiswa × 8 soal × 4 trials × 2 models = 640 API calls

Output per jawaban:
- 4 nilai per kriteria (total 16 nilai per model)
- Skor akhir weighted
- Consistency metrics
```

### C. Evaluation Metrics

#### 1. Consistency Metrics (4x Trials)
- Standard Deviation (SD)
- Coefficient of Variation (CV)
- Range (Max - Min)
- Intraclass Correlation Coefficient (ICC)

#### 2. Accuracy Metrics (vs Dosen)
- Accuracy (exact match)
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Precision, Recall, F1-Score (per grade)
- Confusion Matrix

#### 3. Inter-Rater Agreement
- **Primary:** Fleiss' Kappa (ChatGPT + Gemini + Dosen)
- **Secondary:** Cohen's Kappa (pairwise)
  - ChatGPT vs Dosen
  - Gemini vs Dosen
  - ChatGPT vs Gemini

---

## 🗂️ Project Structure

```
AES/
├── 📁 config/
│   ├── rubrics.json              # Default & custom rubrics
│   ├── models_config.yaml        # API keys, parameters
│   └── experiment_config.yaml    # Trials, batch size, etc.
│
├── 📁 data/
│   ├── raw/
│   │   ├── questions.csv         # Bank soal esai
│   │   ├── student_answers.csv   # Jawaban mahasiswa
│   │   └── lecturer_scores.csv   # Ground truth dari dosen
│   ├── processed/
│   │   └── dataset.json          # Unified dataset
│   └── results/
│       ├── chatgpt_trials/       # 4x percobaan ChatGPT
│       ├── gemini_trials/        # 4x percobaan Gemini
│       └── analysis/             # Statistical results
│
├── 📁 src/
│   ├── __init__.py
│   ├── 📁 agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Abstract class
│   │   ├── chatgpt_agent.py      # OpenAI implementation
│   │   └── gemini_agent.py       # Google Gemini implementation
│   │
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   ├── rubric.py             # Rubric management
│   │   ├── prompt_builder.py     # Dynamic prompt generation
│   │   └── scorer.py             # Weighted scoring calculation
│   │
│   ├── 📁 experiment/
│   │   ├── __init__.py
│   │   ├── runner.py             # Run 4x trials
│   │   ├── consistency.py        # Consistency analysis
│   │   └── batch_processor.py    # Batch processing
│   │
│   ├── 📁 evaluation/
│   │   ├── __init__.py
│   │   ├── accuracy.py           # Accuracy metrics
│   │   ├── agreement.py          # Fleiss' Kappa, Cohen's Kappa
│   │   └── visualizer.py         # Plots & charts
│   │
│   └── 📁 utils/
│       ├── __init__.py
│       ├── logger.py             # Logging system
│       ├── data_loader.py        # Load/save data
│       └── statistics.py         # Statistical utilities
│
├── 📁 notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_experiment_analysis.ipynb
│   ├── 03_statistical_tests.ipynb
│   └── 04_visualization.ipynb
│
├── 📁 tests/
│   ├── test_agents.py
│   ├── test_rubric.py
│   ├── test_scorer.py
│   └── test_metrics.py
│
├── 📁 scripts/
│   ├── setup_environment.py      # Initial setup
│   ├── run_experiment.py         # Main experiment runner
│   ├── generate_report.py        # Auto-generate report
│   └── export_for_paper.py       # Export data for publication
│
├── 📁 docs/
│   ├── API.md                    # API documentation
│   ├── METHODOLOGY.md            # Research methodology
│   └── RESULTS_TEMPLATE.md       # Template for paper
│
├── .env.example                  # Template for API keys
├── .gitignore
├── requirements.txt
├── setup.py
├── README.md
└── PROJECT_PLAN.md (this file)
```

---

## 🚀 Implementation Roadmap

### Phase 1: Setup & Foundation (Week 1-2)
#### ✅ Checklist
- [ ] Setup Python environment (3.9+)
- [ ] Install dependencies (OpenAI, Google GenAI, pandas, numpy, scikit-learn, statsmodels)
- [ ] Setup API keys (OpenAI, Google Gemini)
- [ ] Create project structure
- [ ] Initialize Git repository
- [ ] Create default rubric configuration
- [ ] Setup logging system
- [ ] Write unit tests for core modules

**Deliverables:**
- ✓ Working development environment
- ✓ Core project structure
- ✓ Configuration files

---

### Phase 2: Core Development (Week 3-4)
#### ✅ Checklist

**2.1 Rubric System**
- [ ] Implement `Rubric` class
- [ ] Default rubric loader
- [ ] Custom rubric validator
- [ ] Dynamic weighting system
- [ ] Export/Import rubric JSON

**2.2 Agent Development**
- [ ] `BaseAgent` abstract class
- [ ] ChatGPT Agent implementation
  - [ ] API integration
  - [ ] Prompt engineering for rubric-based grading
  - [ ] Response parsing
  - [ ] Error handling & retry logic
- [ ] Gemini Agent implementation
  - [ ] API integration
  - [ ] Prompt adaptation
  - [ ] Response parsing
  - [ ] Error handling
- [ ] Test both agents with sample essays

**2.3 Scoring System**
- [ ] Grade to point conversion (A→4, B→3, etc.)
- [ ] Weighted scoring calculation
- [ ] Multi-criteria aggregation
- [ ] Result validation

**Deliverables:**
- ✓ Working AI agents
- ✓ Rubric management system
- ✓ Scoring calculator

---

### Phase 3: Experiment Framework (Week 5-6)
#### ✅ Checklist

**3.1 Experiment Runner**
- [ ] Batch processing system
- [ ] 4x trial automation per model
- [ ] Progress tracking & logging
- [ ] Result serialization (JSON/CSV)
- [ ] Error recovery mechanism
- [ ] API rate limiting handler

**3.2 Data Management**
- [ ] Data loader for questions/answers
- [ ] Lecturer scores importer
- [ ] Data validation & cleaning
- [ ] Unified dataset generator
- [ ] Result storage structure

**3.3 Consistency Analysis**
- [ ] Standard Deviation calculator
- [ ] Coefficient of Variation
- [ ] ICC (Intraclass Correlation)
- [ ] Range analysis
- [ ] Per-criteria consistency report

**Deliverables:**
- ✓ Automated experiment pipeline
- ✓ Consistency metrics implementation

---

### Phase 4: Evaluation Metrics (Week 7-8)
#### ✅ Checklist

**4.1 Accuracy Metrics**
- [ ] Exact match accuracy
- [ ] Mean Absolute Error (MAE)
- [ ] Root Mean Square Error (RMSE)
- [ ] Precision/Recall/F1-Score (per grade)
- [ ] Confusion matrix generator
- [ ] Per-criteria accuracy breakdown

**4.2 Agreement Metrics**
- [ ] Fleiss' Kappa implementation
  - [ ] Multi-rater agreement (3 raters)
  - [ ] Per-criteria Fleiss' Kappa
  - [ ] Overall agreement score
- [ ] Cohen's Kappa (pairwise)
  - [ ] ChatGPT vs Dosen
  - [ ] Gemini vs Dosen
  - [ ] ChatGPT vs Gemini
- [ ] Agreement interpretation (slight/fair/moderate/substantial)

**4.3 Statistical Tests**
- [ ] ANOVA (compare models)
- [ ] Paired t-test (significance testing)
- [ ] Wilcoxon signed-rank test (non-parametric)
- [ ] Effect size calculation (Cohen's d)

**Deliverables:**
- ✓ Complete evaluation toolkit
- ✓ Statistical analysis functions

---

### Phase 5: Visualization & Reporting (Week 9)
#### ✅ Checklist

**5.1 Visualization**
- [ ] Consistency plots (box plots, violin plots)
- [ ] Confusion matrices heatmaps
- [ ] Agreement comparison charts
- [ ] Accuracy comparison bar charts
- [ ] Scatter plots (AI vs Dosen scores)
- [ ] Distribution plots per grade

**5.2 Automated Reporting**
- [ ] Summary statistics generator
- [ ] LaTeX table formatter
- [ ] Result export to CSV/Excel
- [ ] Publication-ready figures (high-res)

**Deliverables:**
- ✓ Visualization library
- ✓ Auto-report generator

---

### Phase 6: Data Collection & Experiment (Week 10-12)
#### ✅ Checklist

**6.1 Data Preparation**
- [ ] Collect 8 essay questions
- [ ] Gather 10 student answers per question (80 total)
- [ ] Obtain lecturer ground truth scores for all 80 essays
- [ ] Validate data quality
- [ ] Organize by student ID and question ID

**6.2 Run Experiments**
- [ ] Pilot test (5 essays) to validate pipeline
- [ ] Run ChatGPT trials (4x per essay)
- [ ] Run Gemini trials (4x per essay)
- [ ] Monitor API costs & performance
- [ ] Validate all results

**6.3 Quality Checks**
- [ ] Check for missing data
- [ ] Verify consistency metrics
- [ ] Validate scoring calculations
- [ ] Review outliers

**Deliverables:**
- ✓ Complete experimental dataset
- ✓ Raw results from all trials

---

### Phase 7: Analysis & Results (Week 13-14)
#### ✅ Checklist

**7.1 Statistical Analysis**
- [ ] Calculate all metrics
- [ ] Perform significance tests
- [ ] Generate comparison tables
- [ ] Interpret Fleiss' Kappa results
- [ ] Identify patterns & insights

**7.2 Jupyter Notebook Analysis**
- [ ] Data exploration notebook
- [ ] Statistical tests notebook
- [ ] Visualization notebook
- [ ] Final results notebook

**7.3 Results Interpretation**
- [ ] Answer RQ1 (Consistency)
- [ ] Answer RQ2 (Accuracy)
- [ ] Answer RQ3 (Agreement)
- [ ] Answer RQ4 (Best Model)

**Deliverables:**
- ✓ Complete statistical analysis
- ✓ Interpreted results
- ✓ Publication-ready tables & figures

---

### Phase 8: Paper Writing (Week 15-18)
#### ✅ Checklist

**8.1 Paper Structure (IMRaD)**
- [ ] Abstract
- [ ] Introduction
  - [ ] Background
  - [ ] Problem statement
  - [ ] Research questions
  - [ ] Contribution
- [ ] Related Work
  - [ ] AES systems
  - [ ] LLM for education
  - [ ] Inter-rater agreement studies
- [ ] Methodology
  - [ ] System architecture
  - [ ] Rubric design
  - [ ] Experiment design
  - [ ] Evaluation metrics
- [ ] Results
  - [ ] Consistency analysis
  - [ ] Accuracy comparison
  - [ ] Fleiss' Kappa results
  - [ ] Statistical significance
- [ ] Discussion
  - [ ] Interpretation
  - [ ] Implications
  - [ ] Limitations
- [ ] Conclusion & Future Work
- [ ] References

**8.2 Submission Preparation**
- [ ] Format to journal template
- [ ] Proofread & edit
- [ ] Co-author review
- [ ] Ethics & reproducibility statement
- [ ] Data availability statement
- [ ] Code repository link (GitHub)

**Deliverables:**
- ✓ Complete manuscript
- ✓ Supplementary materials

---

## 📦 Dependencies

### Core Libraries
```
openai>=1.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### Data Processing
```
pandas>=2.0.0
numpy>=1.24.0
```

### Machine Learning & Statistics
```
scikit-learn>=1.3.0
scipy>=1.11.0
statsmodels>=0.14.0
```

### Visualization
```
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
```

### Testing
```
pytest>=7.4.0
pytest-cov>=4.1.0
```

### Jupyter
```
jupyter>=1.0.0
ipykernel>=6.25.0
```

---

## 🎓 Expected Contributions for Q1 Paper

### Novel Contributions:
1. **Comparative study** ChatGPT vs Gemini untuk essay scoring (belum banyak research)
2. **Multi-criteria rubric-based** dengan weighted scoring
3. **Consistency analysis** melalui multiple trials (metodologi robust)
4. **Fleiss' Kappa** untuk multi-rater agreement (rigorous statistical method)
5. **Real-world educational dataset** dengan ground truth dari dosen

### Target Journals (Q1 Scopus):
- IEEE Transactions on Learning Technologies
- Computers & Education
- Educational Technology & Society
- Journal of Educational Computing Research
- International Journal of Artificial Intelligence in Education

---

## 🔬 Quality Assurance

### Code Quality
- [ ] Type hints di semua functions
- [ ] Docstrings (Google style)
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Code review checklist
- [ ] PEP 8 compliance

### Research Quality
- [ ] Reproducibility: Random seed fixed
- [ ] Documentation lengkap
- [ ] Version control (Git)
- [ ] Data versioning
- [ ] Experiment logging
- [ ] Ethics approval (jika perlu)

---

## 📈 Success Criteria

### Technical Success:
- ✅ System dapat grading 1500 essays dalam <24 jam
- ✅ API error rate <5%
- ✅ Consistency CV <15%
- ✅ Code coverage >80%

### Research Success:
- ✅ Fleiss' Kappa >0.60 (substantial agreement)
- ✅ Accuracy >75% (exact match)
- ✅ Statistical significance p<0.05
- ✅ Novel insights untuk publikasi

---

## 📝 Notes

### API Cost Estimation (approx):
- ChatGPT (GPT-4o): ~$0.015-0.03 per essay × 4 trials × 80 essays = **$5-10**
- Gemini (2.0 Flash): ~$0.00025 per essay × 4 trials × 80 essays = **$0.08**
- **Total:** ~$5-15 (sangat terjangkau!)

### Timeline Risk:
- **API downtime:** Use retry logic & backup keys
- **Data collection delay:** Start early, work with lecturers
- **Analysis complexity:** Use established libraries

---

## 🤝 Team Roles (if applicable)

- **Researcher/Developer:** System development, experimentation
- **Domain Expert:** Rubric validation, result interpretation
- **Statistician:** Statistical analysis validation
- **Writer:** Paper writing & revision

---

## 📚 References to Study

1. Ke, Z., & Ng, V. (2019). Automated essay scoring: A survey of the state of the art. IJCAI.
2. Hussein, M. A., et al. (2019). Automated language essay scoring systems: a literature review. PeerJ Computer Science.
3. Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters. Psychological bulletin.
4. Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics.

---

**Last Updated:** December 10, 2025  
**Version:** 1.0  
**Status:** Planning Phase
