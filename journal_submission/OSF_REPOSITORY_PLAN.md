# Rencana OSF Repository Creation
## LLM-based Automated Essay Scoring in Indonesian Higher Education

**Target Deadline**: 29-30 Desember 2025 (2 hari sebelum final proofread)  
**Estimasi Waktu**: 2-3 jam  
**Status**: Belum dimulai

---

## 1. REGISTRASI & SETUP (30 menit)

### Langkah 1: Buat Akun OSF
- Kunjungi: https://osf.io/
- Klik "Sign Up" (kanan atas)
- Gunakan email institusi: **Syaifulbachri@mail.ugm.ac.id** (corresponding author)
- Verifikasi email
- Lengkapi profil:
  - Name: Syaiful Bachri Mustamin
  - Institution: Institut Sains Teknologi dan Kesehatan 'Aisyiyah Kendari
  - ORCID iD: [Setelah registrasi ORCID]

### Langkah 2: Buat Project Baru
- Dashboard → "Create new project"
- **Project Title**: "Test-Retest Reliability of Large Language Models for Automated Essay Scoring: A Comparative Study of ChatGPT and Gemini in Indonesian Higher Education"
- **Category**: Analysis
- **Description**: 
  ```
  This repository contains research data, analysis scripts, and supplementary materials 
  for a comprehensive study evaluating the reliability and validity of LLM-based automated 
  essay scoring in Indonesian higher education contexts. The study compares ChatGPT-4o and 
  Gemini 2.0 Flash across 1,958 grading instances using a within-subjects factorial design.
  
  Publication: Submitted to Australasian Journal of Educational Technology (AJET)
  Authors: Samsidar, Syaiful Bachri Mustamin, Siti Fatmah
  Institution: Institut Sains Teknologi dan Kesehatan 'Aisyiyah Kendari, Indonesia
  ```

### Langkah 3: Tambahkan Contributors
- Settings → Contributors → Add
- **Contributor 1**: Samsidar (samsydar401@gmail.com)
  - Role: Co-author
  - Permissions: Read + Write
- **Contributor 2**: Siti Fatmah (email diperlukan)
  - Role: Co-author
  - Permissions: Read + Write
- **Contributor 3**: Syaiful Bachri Mustamin
  - Role: Administrator (corresponding author)
  - Permissions: Admin

---

## 2. STRUKTUR REPOSITORY (15 menit)

### Buat Komponen/Folder Utama:

```
Root Project
├── 📁 01_Data
│   ├── gold_standard_anonymized.csv
│   ├── experiment_results_summary.csv
│   ├── reliability_metrics.csv
│   └── README_DATA.md
│
├── 📁 02_Analysis_Scripts
│   ├── validity_analysis.py
│   ├── reliability_analysis.py
│   ├── error_pattern_analysis.py
│   ├── statistical_tests.py
│   └── README_SCRIPTS.md
│
├── 📁 03_Results
│   ├── tables/
│   ├── figures/
│   └── README_RESULTS.md
│
├── 📁 04_Supplementary_Materials
│   ├── S1_Experimental_Design.pdf
│   ├── S2_Statistical_Analysis_Details.pdf
│   ├── S3_Error_Analysis_Extended.pdf
│   ├── S4_Prompts_Complete.md
│   └── rubric_specifications.pdf
│
├── 📁 05_Documentation
│   ├── CODEBOOK.md
│   ├── METHODS_DETAILED.md
│   └── REPLICATION_GUIDE.md
│
└── README.md (root)
```

---

## 3. FILES YANG DIUPLOAD (1 jam)

### A. Data Files (`01_Data/`)

#### 1. `gold_standard_anonymized.csv` (WAJIB)
**Sumber**: `data/processed/gold_standard_70_tasks.csv`  
**Preprocessing yang diperlukan**:
```python
import pandas as pd

# Load original gold standard
df = pd.read_csv('data/processed/gold_standard_70_tasks.csv')

# Anonymize: Remove PII
df_anon = df[[
    'task_id',           # Keep: T001, T002, etc.
    'question_number',   # Keep: Q1-Q7
    'essay_word_count',  # Keep: word count
    'expert_score_total', # Keep: 0-4 GPA scale
    'expert_grade',      # Keep: A, B, C, D
    # Remove: student_id, student_name, essay_text
]]

# Add metadata
df_anon['dataset_version'] = '1.0'
df_anon['collection_date'] = '2024-09-01 to 2024-10-15'

# Export
df_anon.to_csv('journal_submission/osf_upload/gold_standard_anonymized.csv', 
               index=False)
```
**Size**: ~5 KB  
**Description**: Expert human grades for 70 Indonesian Capstone Project essays (anonymized)

#### 2. `experiment_results_summary.csv` (WAJIB)
**Sumber**: Aggregate dari `results_experiment_final/`  
**Struktur**:
```csv
model,strategy,trial,task_id,ai_score_total,ai_grade,expert_score_total,expert_grade,absolute_error,exact_match,adjacent_error,critical_error
chatgpt,lenient,1,T001,3.2,B,3.0,B,0.2,1,0,0
chatgpt,lenient,1,T002,2.8,B,3.5,A,0.7,0,1,0
...
```
**Script untuk generate**:
```python
# Aggregate all experiment results
import pandas as pd
import glob

all_results = []
for file in glob.glob('results_experiment_final/**/*_results.csv', recursive=True):
    df = pd.read_csv(file)
    all_results.append(df)

df_combined = pd.concat(all_results, ignore_index=True)

# Select relevant columns only (remove essay_text, justifications)
df_summary = df_combined[[
    'model', 'strategy', 'trial', 'task_id', 
    'ai_score_total', 'ai_grade', 
    'expert_score_total', 'expert_grade',
    'absolute_error', 'exact_match', 'adjacent_error', 'critical_error'
]]

df_summary.to_csv('journal_submission/osf_upload/experiment_results_summary.csv', 
                   index=False)
```
**Size**: ~200 KB (1,958 rows)  
**Description**: Complete grading results for all 24 experimental conditions

#### 3. `reliability_metrics.csv`
**Sumber**: Calculated from analysis  
**Struktur**:
```csv
model,strategy,pearson_r,pearson_p,icc_value,icc_ci_lower,icc_ci_upper,fleiss_kappa,mae,coefficient_variation
chatgpt,lenient,0.76,<0.001,0.942,0.918,0.961,0.818,0.38,0.048
gemini,lenient,0.89,<0.001,NA,NA,NA,0.790,0.28,0.042
...
```
**Size**: ~2 KB  
**Description**: Validity and reliability metrics for each experimental condition

#### 4. `README_DATA.md`
**Isi**:
```markdown
# Data Documentation

## Overview
This folder contains anonymized research data from the study "Test-Retest Reliability 
of Large Language Models for Automated Essay Scoring."

## Files

### gold_standard_anonymized.csv (70 rows)
- **Description**: Expert human grades for Indonesian Capstone Project essays
- **Variables**:
  - task_id: Unique essay identifier (T001-T070)
  - question_number: Question prompt (Q1-Q7)
  - essay_word_count: Number of words (250-800 range)
  - expert_score_total: Weighted composite score (0-4 GPA scale)
  - expert_grade: Letter grade (A, B, C, D, E)
  
### experiment_results_summary.csv (1,958 rows)
- **Description**: AI grading results for all experimental conditions
- **Variables**:
  - model: AI model used (chatgpt, gemini)
  - strategy: Prompting strategy (lenient, few-shot, zero-shot)
  - trial: Trial number (1-10 for lenient, 1 for baselines)
  - task_id: Essay identifier matching gold_standard
  - ai_score_total: AI-assigned composite score (0-4 scale)
  - ai_grade: AI-assigned letter grade
  - absolute_error: |AI score - Expert score|
  - exact_match: 1 if grades match exactly, 0 otherwise
  - adjacent_error: 1 if ±1 grade level difference
  - critical_error: 1 if >1 grade level difference

### reliability_metrics.csv (6 rows)
- **Description**: Statistical metrics for each model-strategy combination
- **Key metrics**: Pearson r, ICC, Fleiss' kappa, MAE, CV

## Ethical Compliance
- All personally identifiable information removed
- Student consent obtained for research use
- Essay content NOT included (privacy protection)
- Institutional IRB approval: [Approval number if available]

## Citation
If using this data, please cite:
[Authors]. (2026). Test-Retest Reliability of Large Language Models for Automated 
Essay Scoring. Australasian Journal of Educational Technology. DOI: [pending]
```

---

### B. Analysis Scripts (`02_Analysis_Scripts/`)

#### 1. `validity_analysis.py`
**Sumber**: Copy dari `scripts/analyze_validity.py` atau extract dari notebooks  
**Cleanup needed**:
- Remove API keys/credentials
- Add clear comments in English
- Include requirements at top:
  ```python
  """
  Validity Analysis for LLM-AES Study
  
  Requirements:
  - pandas >= 2.0.0
  - scipy >= 1.11.0
  - numpy >= 1.24.0
  
  Usage:
  python validity_analysis.py --input experiment_results_summary.csv
  """
  ```

#### 2. `reliability_analysis.py`
**Functions**:
- Calculate ICC using two-way random effects model
- Calculate Fleiss' kappa for multi-rater agreement
- Compute coefficient of variation
- Bootstrap confidence intervals

#### 3. `error_pattern_analysis.py`
**Functions**:
- Generate confusion matrices
- Classify errors by severity
- Detect systematic bias (t-tests)
- Per-rubric dimension analysis

#### 4. `statistical_tests.py`
**Functions**:
- ANOVA for strategy comparisons
- Independent t-tests for model comparisons
- Post-hoc Bonferroni corrections
- Effect size calculations (Cohen's d, η²)

#### 5. `README_SCRIPTS.md`
```markdown
# Analysis Scripts Documentation

## Setup
```bash
pip install -r requirements.txt
```

## Script Descriptions

### validity_analysis.py
Calculates Pearson correlation, MAE, exact match rates

### reliability_analysis.py
Computes ICC, Fleiss' kappa, coefficient of variation

### error_pattern_analysis.py
Generates confusion matrices and error classifications

### statistical_tests.py
Performs ANOVA, t-tests, effect size calculations

## Workflow
1. Run validity_analysis.py
2. Run reliability_analysis.py
3. Run error_pattern_analysis.py
4. Run statistical_tests.py
5. Results saved to ../03_Results/

## Contact
For questions: Syaifulbachri@mail.ugm.ac.id
```

---

### C. Results (`03_Results/`)

#### Upload semua files dari:
- `results_experiment_final/rq1_validity/` → `tables/validity/`
- `results_experiment_final/rq2_consistency/` → `tables/reliability/`
- `results_experiment_final/figures/` → `figures/`
  - confusion_matrices_combined.png
  - reliability_coefficients_comparison.png
  - consistency_distribution.png
  - overall_performance_comparison.png
  - per_grade_classification_accuracy.png
  - consistency_variance_analysis.png

#### `README_RESULTS.md`
```markdown
# Results Documentation

## Figures (300 DPI PNG)
- Figure 1: Confusion matrices for all model-strategy combinations
- Figure 2: ICC and kappa values comparison
- Figure 3: Consistency score distributions (violin plots)
- Figure 4: Overall performance metrics
- Figure 5: Per-grade classification accuracy
- Figure 6: Consistency variance analysis

## Tables (CSV format)
- Table 1: Validity metrics summary
- Table 2: Reliability metrics summary
- Table 3: Strategy comparison (ANOVA results)
- Table 4: Model comparison (t-test results)
- Table 5: Error patterns and bias analysis

All results correspond to manuscript submitted to AJET (2026).
```

---

### D. Supplementary Materials (`04_Supplementary_Materials/`)

#### 1. `S1_Experimental_Design.pdf`
**Content**:
- Complete prompt text for all 3 strategies (lenient, few-shot, zero-shot)
- Rubric specifications (4 dimensions with scoring criteria)
- Few-shot example essays (3 examples: excellent, average, weak)
- Temperature settings and API parameters

**Generate from**: Compile from BASELINE_GUIDE.md + config/rubrics.json

#### 2. `S2_Statistical_Analysis_Details.pdf`
**Content**:
- Full ANOVA tables with F-statistics, p-values, η²
- Complete post-hoc comparison matrices (Bonferroni corrected)
- ICC calculation methodology (two-way random effects)
- Fleiss' kappa computation details
- Confidence interval calculations (bootstrap methods)

#### 3. `S3_Error_Analysis_Extended.pdf`
**Content**:
- Example critical errors with AI justifications vs. expert rationale
- Dimension-specific performance breakdown
- Systematic bias detection methodology
- Misclassification pattern examples

#### 4. `S4_Prompts_Complete.md`
```markdown
# Complete Prompt Text

## Lenient Strategy Prompt
```
You are a generous university instructor grading Capstone Project essays...
[Full prompt text]
```

## Zero-shot Strategy Prompt
```
Grade the following Indonesian essay using this rubric...
[Full prompt text]
```

## Few-shot Strategy Prompt
```
Here are three example graded essays for calibration:
[Example 1: Excellent (A grade)]
[Example 2: Average (B-C grade)]
[Example 3: Weak (D-E grade)]

Now grade the following essay:
[Full prompt text]
```

## Rubric JSON
```json
{
  "dimensions": [...]
}
```
```

#### 5. `rubric_specifications.pdf`
- Visual rubric table dengan scoring criteria untuk setiap dimensi
- Contoh student work untuk setiap grade level
- Weighting scheme (40% + 30% + 20% + 10%)

---

### E. Documentation (`05_Documentation/`)

#### 1. `CODEBOOK.md`
```markdown
# Study Codebook

## Variable Definitions

### Gold Standard Data
| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| task_id | String | T001-T070 | Unique essay identifier |
| question_number | String | Q1-Q7 | Question prompt number |
| essay_word_count | Integer | 250-800 | Number of words in essay |
| expert_score_total | Float | 0.0-4.0 | Weighted composite score (GPA scale) |
| expert_grade | String | A,B,C,D,E | Letter grade |

### Experiment Results
| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| model | String | chatgpt, gemini | AI model identifier |
| strategy | String | lenient, few-shot, zero-shot | Prompting strategy |
| trial | Integer | 1-10 | Independent trial number |
| ai_score_total | Float | 0.0-4.0 | AI-assigned composite score |
| ai_grade | String | A,B,C,D,E | AI-assigned letter grade |
| absolute_error | Float | 0.0-4.0 | |AI - Expert| score |
| exact_match | Binary | 0,1 | 1 if grades match exactly |
| adjacent_error | Binary | 0,1 | 1 if ±1 grade difference |
| critical_error | Binary | 0,1 | 1 if >1 grade difference |

### Reliability Metrics
| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| pearson_r | Float | -1.0 to 1.0 | Pearson correlation coefficient |
| icc_value | Float | 0.0 to 1.0 | Intraclass correlation (2-way random) |
| fleiss_kappa | Float | -1.0 to 1.0 | Multi-rater agreement coefficient |
| mae | Float | 0.0-4.0 | Mean absolute error |
| coefficient_variation | Float | 0.0-1.0 | CV across trials |

## Missing Data
- ICC not calculated for single-trial baselines (zero-shot, few-shot)
- Reported as "NA" in reliability_metrics.csv

## Study Design
- Within-subjects factorial: 2 models × 3 strategies × varying trials
- Total: 1,958 grading instances across 70 essays
- Data collection: September-October 2024
```

#### 2. `METHODS_DETAILED.md`
```markdown
# Detailed Methodology

## Sample Selection
- 10 undergraduate students (7 female, 3 male)
- Ages: 21-23 years
- Mean GPA: 3.2/4.0
- All native Indonesian speakers
- Health sciences program, final year

## Assessment Task
- Capstone Project examination
- 7 analytical essay questions
- Topics: research methodology, literature synthesis
- Required length: 300-800 words
- Submission: Digital (LMS platform)

## Grading Procedure

### Gold Standard Creation
- Single expert grader (course lecturer)
- 15+ years teaching experience
- PhD in Educational Technology
- Blind to student identities
- Used 4-dimensional analytic rubric

### AI Grading Implementation
- API calls: OpenAI (ChatGPT-4o), Google (Gemini 2.0 Flash)
- Temperature: 0.3 (balanced determinism/variation)
- JSON-formatted responses
- Checkpoint system for fault tolerance
- 10 independent trials for lenient strategy
- Single trials for baseline strategies

### Quality Control
- Response validation (completeness, score ranges)
- Error handling (retry mechanisms)
- Version tracking (model snapshots)
- Timestamp logging

## Statistical Analysis

### Validity Metrics
- Pearson r: Linear association strength
- MAE: Average grading discrepancy
- Exact match rate: Percentage identical grades

### Reliability Metrics
- ICC(2,1): Two-way random effects, absolute agreement
- Fleiss' κ: Multi-rater categorical agreement
- CV: Coefficient of variation across trials

### Hypothesis Testing
- ANOVA: Strategy effects (within-subjects)
- Independent t-tests: Model comparisons
- Bonferroni correction: Multiple comparisons (α=0.017)
- Effect sizes: Cohen's d, η²

### Software
- Python 3.13
- pandas 2.1.0
- scipy 1.11.0
- statsmodels 0.14.0
- scikit-learn 1.3.0
```

#### 3. `REPLICATION_GUIDE.md`
```markdown
# Study Replication Guide

## Prerequisites
- Python 3.11+
- OpenAI API access (ChatGPT-4o)
- Google AI API access (Gemini 2.0 Flash)
- Institutional IRB approval

## Step-by-Step Replication

### 1. Environment Setup (30 min)
```bash
git clone [repository URL]
cd llm-aes-study
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 2. API Configuration (15 min)
Create `.env` file:
```
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

### 3. Data Preparation (1 hour)
- Collect 50-100 student essays
- Obtain expert grades using provided rubric
- Anonymize student information
- Format as CSV (see gold_standard_anonymized.csv structure)

### 4. Run Experiments (variable time)
```bash
# Single model test
python scripts/run_experiment.py --model chatgpt --strategy lenient --trials 10

# Full factorial design
python scripts/run_all_experiments.py
```

Expected runtime: ~40 hours for 2,000 grading instances (API rate limits)

### 5. Analysis (2 hours)
```bash
python scripts/validity_analysis.py
python scripts/reliability_analysis.py
python scripts/error_pattern_analysis.py
python scripts/statistical_tests.py
```

### 6. Generate Figures (30 min)
```bash
python scripts/create_visualizations.py
```

## Modifications for Different Contexts

### Different Languages
- Translate prompts to target language
- Maintain rubric structure (4 dimensions)
- Re-validate with local expert graders

### Different Essay Types
- Adapt rubric dimensions to genre
- Adjust word count ranges
- Modify few-shot examples

### Different Models
- Update API endpoints
- Adjust temperature if needed
- Re-calibrate bias correction

## Troubleshooting
- **API errors**: Check rate limits, retry with exponential backoff
- **JSON parsing failures**: Validate response format, implement error handling
- **Low agreement**: Review prompt clarity, check rubric ambiguity

## Expected Results
- Validity: r = 0.70-0.90 (language/domain dependent)
- Reliability: ICC > 0.80, κ > 0.70
- Processing speed: 300-500 essays/hour

## Contact
For replication support: Syaifulbachri@mail.ugm.ac.id
```

---

### F. Root `README.md`

```markdown
# Test-Retest Reliability of Large Language Models for Automated Essay Scoring

[![DOI](https://img.shields.io/badge/DOI-[pending]-blue)]()
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

This repository contains research materials for a comprehensive study evaluating the reliability and validity of large language model (LLM) based automated essay scoring in Indonesian higher education contexts.

**Study Design**: Within-subjects factorial (2 models × 3 strategies × varying trials)  
**Sample**: 70 Indonesian Capstone Project essays, 1,958 grading instances  
**Models**: ChatGPT-4o, Gemini 2.0 Flash  
**Key Finding**: Gemini achieves r=0.89 validity; both models show ICC >0.83 reliability

## Publication

**Journal**: Australasian Journal of Educational Technology (AJET)  
**Status**: Submitted (January 2026)  
**Authors**: Samsidar, Syaiful Bachri Mustamin, Siti Fatmah  
**Institution**: Institut Sains Teknologi dan Kesehatan 'Aisyiyah Kendari, Indonesia

## Repository Contents

- **`01_Data/`**: Anonymized gold standard and experiment results
- **`02_Analysis_Scripts/`**: Python code for validity, reliability, error analysis
- **`03_Results/`**: Tables and figures (300 DPI)
- **`04_Supplementary_Materials/`**: Prompts, rubric, extended analysis
- **`05_Documentation/`**: Codebook, methods, replication guide

## Key Results

| Model | Strategy | Pearson r | ICC | Fleiss' κ | MAE | Critical Errors |
|-------|----------|-----------|-----|-----------|-----|-----------------|
| Gemini | Lenient | 0.89*** | - | 0.790 | 0.28 | 11.8% |
| ChatGPT | Lenient | 0.76*** | 0.942 | 0.818 | 0.38 | 11.8% |
| ChatGPT | Zero-shot | 0.69*** | 0.969 | 0.838 | 0.65 | 7.3% |
| Gemini | Zero-shot | 0.75*** | 0.832 | 0.530 | 0.46 | 3.1% |

***p < 0.001

## Quick Start

```bash
# Clone repository
git clone [this repository URL]

# Install dependencies
pip install -r requirements.txt

# Run validity analysis
python 02_Analysis_Scripts/validity_analysis.py

# Generate figures
python 02_Analysis_Scripts/create_visualizations.py
```

## Citation

If you use this data or code, please cite:

```bibtex
@article{samsidar2026llmaes,
  title={Test-Retest Reliability of Large Language Models for Automated Essay Scoring: 
         A Comparative Study of ChatGPT and Gemini in Indonesian Higher Education},
  author={Samsidar and Mustamin, Syaiful Bachri and Fatmah, Siti},
  journal={Australasian Journal of Educational Technology},
  year={2026},
  note={Submitted}
}
```

## License

**Data**: CC BY 4.0 (Creative Commons Attribution 4.0 International)  
**Code**: MIT License

You are free to:
- Share: copy and redistribute the material
- Adapt: remix, transform, and build upon the material

Under the following terms:
- **Attribution**: You must give appropriate credit, provide a link to the license, 
  and indicate if changes were made.

## Ethical Considerations

- All personally identifiable information has been removed
- Essay content is NOT included to protect student privacy
- Students provided informed consent for research use
- Institutional ethics approval obtained

## Contact

**Corresponding Author**: Syaiful Bachri Mustamin  
**Email**: Syaifulbachri@mail.ugm.ac.id  
**Institution**: Institut Sains Teknologi dan Kesehatan 'Aisyiyah Kendari

## Acknowledgments

We thank the students who participated in this study and provided consent for their 
assessment data to be used for research purposes.

## Version History

- v1.0 (January 2026): Initial release with manuscript submission
```

---

## 4. METADATA & SETTINGS (30 menit)

### Tambahkan Tags/Keywords:
- automated essay scoring
- large language models
- ChatGPT
- Gemini
- test-retest reliability
- educational assessment
- Indonesian higher education
- validity
- reliability
- LLM grading
- AI assessment

### Pilih License:
**Recommended**: **CC BY 4.0** (Creative Commons Attribution 4.0 International)
- Allows reuse with attribution
- Standard for open science
- Complies with AJET requirements

**Alternative**: CC0 (Public Domain) jika ingin maksimal open

### Link to Related Work:
- Add preprint link (jika ada)
- Link to AJET submission tracker (setelah submit)

---

## 5. MAKE PUBLIC & GET DOI (15 menit)

### Langkah Publikasi:
1. Review semua files uploaded
2. Pastikan semua README lengkap
3. Settings → "Make Public"
4. **Generate DOI**:
   - Settings → Create DOI
   - Confirm project is complete
   - DOI akan muncul dalam format: `10.17605/OSF.IO/XXXXX`

### Update Manuscript:
Setelah dapat DOI, update Data Availability Statement di manuscript:

```markdown
## Data Availability Statement

All research data, analysis scripts, and supplementary materials are openly available 
at the Open Science Framework (OSF): https://doi.org/10.17605/OSF.IO/[XXXXX]

The repository includes:
- Anonymized gold standard grades (n=70 essays)
- Complete experiment results (n=1,958 grading instances)
- Python analysis scripts for all statistical analyses
- High-resolution figures and tables
- Supplementary materials (prompts, rubric, extended analysis)
- Comprehensive documentation and replication guide

No personally identifiable information or essay content is included to protect 
student privacy.
```

---

## 6. TIMELINE & CHECKLIST

### **29 Desember 2025** (Hari 1 - Setup & Upload Data)

**Pagi (9:00-12:00)**:
- [ ] Registrasi OSF account (30 min)
- [ ] Buat project structure (15 min)
- [ ] Tambah contributors (15 min)
- [ ] Prepare data files: anonymize dan export (90 min)
- [ ] Upload `01_Data/` folder (30 min)

**Siang (13:00-15:00)**:
- [ ] Cleanup analysis scripts (remove API keys) (60 min)
- [ ] Add script documentation/comments (30 min)
- [ ] Upload `02_Analysis_Scripts/` folder (30 min)

**Sore (15:00-17:00)**:
- [ ] Copy results tables & figures (30 min)
- [ ] Upload `03_Results/` folder (30 min)
- [ ] Create README for each folder (60 min)

### **30 Desember 2025** (Hari 2 - Supplementary & Documentation)

**Pagi (9:00-12:00)**:
- [ ] Create S1-S4 supplementary PDFs (90 min)
- [ ] Upload `04_Supplementary_Materials/` (30 min)
- [ ] Write CODEBOOK.md (60 min)

**Siang (13:00-16:00)**:
- [ ] Write METHODS_DETAILED.md (60 min)
- [ ] Write REPLICATION_GUIDE.md (90 min)
- [ ] Write root README.md (30 min)

**Sore (16:00-17:30)**:
- [ ] Add tags/keywords (15 min)
- [ ] Select license (CC BY 4.0) (5 min)
- [ ] Final review semua files (30 min)
- [ ] Make public (5 min)
- [ ] Generate DOI (5 min)
- [ ] Copy DOI untuk manuscript (5 min)
- [ ] Update manuscript Data Availability Statement (15 min)

---

## 7. UKURAN FILE & BATASAN

### OSF Storage Limits:
- **Free account**: 5 GB per project (cukup untuk study ini)
- **Private projects**: Unlimited
- **Public projects**: Unlimited

### Estimasi Total Size:
- Data CSVs: ~500 KB
- Analysis scripts: ~200 KB
- Figures (PNG 300 DPI): ~15 MB
- Supplementary PDFs: ~5 MB
- Documentation: ~100 KB
- **Total**: ~20-25 MB (jauh di bawah limit)

### File Format Recommendations:
- **Data**: CSV (universal, readable)
- **Scripts**: .py (Python) dengan comments lengkap
- **Figures**: PNG 300 DPI (publikasi quality)
- **Supplementary**: PDF (preserve formatting)
- **Documentation**: Markdown (.md) - GitHub-style

---

## 8. QUALITY CHECKLIST

Sebelum make public, verify:

### Data Quality:
- [ ] No PII (personally identifiable information)
- [ ] No essay content (privacy protection)
- [ ] All IDs are anonymized (T001-T070)
- [ ] Missing data documented (NA for ICC baselines)
- [ ] Variable names clear and consistent

### Code Quality:
- [ ] No API keys/credentials in code
- [ ] Clear comments explaining logic
- [ ] Requirements.txt included
- [ ] Paths are relative (not absolute E:\project\AES)
- [ ] Functions have docstrings

### Documentation Quality:
- [ ] README in every folder
- [ ] Root README comprehensive
- [ ] Codebook defines all variables
- [ ] Replication guide step-by-step
- [ ] Contact information correct

### Compliance:
- [ ] CC BY 4.0 license applied
- [ ] Citation info provided
- [ ] Ethics statement included
- [ ] AJET requirements met
- [ ] FAIR principles followed (Findable, Accessible, Interoperable, Reusable)

---

## 9. POST-UPLOAD ACTIONS

### Update Manuscript:
1. Copy DOI dari OSF
2. Update Data Availability Statement
3. Add OSF link ke References (optional)
4. Mention dalam Methods section

### Notify Co-authors:
Email template:
```
Subject: OSF Repository Created for AJET Submission

Dear Samsidar and Siti Fatmah,

I have created an Open Science Framework (OSF) repository for our study:
https://osf.io/[project-id]

The repository contains:
- All anonymized research data
- Analysis scripts
- Results (tables & figures)
- Supplementary materials
- Comprehensive documentation

DOI: 10.17605/OSF.IO/[XXXXX]

Please review and confirm you're comfortable with the public release. 
The repository is currently public and linked in our AJET manuscript.

Best regards,
Syaiful Bachri Mustamin
```

### Share on Social Media (Optional):
- Twitter/X: Share OSF link dengan hashtag #OpenScience #AES #LLM
- LinkedIn: Announce research data release
- ResearchGate: Add OSF link to project

---

## 10. TROUBLESHOOTING

### Common Issues:

**Q: Upload gagal / file terlalu besar**  
A: OSF limit 5GB, tapi bisa upload multiple files. Compress figures jika perlu.

**Q: Lupa tambahkan file penting**  
A: OSF allows updates - just upload lagi. DOI tetap sama.

**Q: Co-author tidak bisa akses**  
A: Check permissions di Settings → Contributors. Pastikan "Read + Write" enabled.

**Q: DOI belum muncul**  
A: Generation bisa memakan 5-10 menit. Refresh page.

**Q: Ingin ubah sesuatu setelah public**  
A: OSF allows updates. Upload new version dengan version number (v1.1, v2.0, etc.)

---

## RESOURCES

### OSF Documentation:
- User Guide: https://help.osf.io/
- Video Tutorials: https://www.youtube.com/c/OSFramework
- Best Practices: https://osf.io/49t8x/

### Data Sharing Guidelines:
- AJET requirements: https://ajet.org.au/
- FAIR principles: https://www.go-fair.org/
- CC Licenses: https://creativecommons.org/licenses/

### Contact Support:
- OSF Support: support@osf.io
- Response time: Usually 24-48 hours

---

**TOTAL ESTIMASI WAKTU**: 6-8 jam jika dikerjakan dengan teliti  
**RECOMMENDED**: Kerjakan dalam 2 hari (29-30 Des) untuk quality assurance  
**DEADLINE**: Selesai sebelum 31 Desember untuk final manuscript update
