# Analysis Scripts

This folder contains Python scripts for reproducible data analysis.

## 📁 Files

Currently, detailed analysis scripts are **not included** in this initial OSF release to keep the repository focused on essential data and results.

## 🔄 Reproducibility

The complete analysis workflow is documented in the manuscript Methods section. Key steps:

### 1. Data Preparation
- Load expert grades from `01_Data/gold_standard_anonymized.csv`
- Load AI grades from experiment results
- Merge datasets by student ID and question number

### 2. Validity Analysis
Calculate:
- **Pearson correlation** (r): Agreement between AI and expert scores
- **Mean Absolute Error** (MAE): Average difference in scores
- **Exact match %**: Percentage of identical letter grades
- **Adjacent match %**: Percentage within ±1 letter grade

Python example:
```python
from scipy.stats import pearsonr
import pandas as pd

# Load data
df_expert = pd.read_csv('01_Data/gold_standard_anonymized.csv')
df_ai = pd.read_csv('ai_grades.csv')  # Your AI results

# Calculate Pearson r
r, p_value = pearsonr(df_expert['expert_score_total'], 
                       df_ai['ai_score_total'])
print(f"Pearson r: {r:.3f}, p={p_value:.4f}")
```

### 3. Reliability Analysis
Calculate:
- **Intraclass Correlation Coefficient (ICC)**: Between-trial consistency
- **Fleiss' Kappa**: Multi-rater agreement
- **Coefficient of Variation (CV)**: Score variability

Python example (using pingouin):
```python
import pingouin as pg

# ICC calculation (requires trial × student matrix)
icc = pg.intraclass_corr(data=df, 
                          targets='student_id', 
                          raters='trial', 
                          ratings='score')
print(icc)
```

### 4. Error Pattern Analysis
Generate:
- **Confusion matrices**: Grade distribution (A/B/C/D)
- **Systematic bias**: Tendency to over/under-grade
- **Error by dimension**: Which rubric dimension has most errors

Python example:
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Confusion matrix
cm = confusion_matrix(df_expert['expert_grade'], 
                       df_ai['ai_grade'],
                       labels=['A', 'B', 'C', 'D'])

# Visualize
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

### 5. Statistical Tests
- **ANOVA**: Compare accuracy across conditions
- **Post-hoc tests**: Pairwise comparisons (Bonferroni correction)
- **Effect sizes**: Cohen's d, eta-squared

Python example:
```python
from scipy.stats import f_oneway
import scikit_posthocs as sp

# One-way ANOVA
groups = [df[df['strategy']=='lenient']['accuracy'],
          df[df['strategy']=='few-shot']['accuracy'],
          df[df['strategy']=='zero-shot']['accuracy']]
f_stat, p_value = f_oneway(*groups)

# Post-hoc (if significant)
if p_value < 0.05:
    posthoc = sp.posthoc_dunn(df, val_col='accuracy', 
                               group_col='strategy', p_adjust='bonferroni')
    print(posthoc)
```

---

## 🛠️ Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

```bash
# Clone repository
git clone https://osf.io/[YOUR_DOI]

# Navigate to scripts folder
cd 02_Analysis_Scripts

# Install dependencies
pip install -r requirements.txt

# Or using conda
conda create -n aes_analysis python=3.11
conda activate aes_analysis
pip install -r requirements.txt
```

---

## 📊 Key Statistical Formulas

### 1. Pearson Correlation
$$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$

Where:
- $x_i$ = Expert score
- $y_i$ = AI score
- $\bar{x}, \bar{y}$ = Mean scores

### 2. Intraclass Correlation (ICC 2,1)
$$ICC(2,1) = \frac{MS_R - MS_E}{MS_R + (k-1)MS_E + \frac{k}{n}(MS_C - MS_E)}$$

Where:
- $MS_R$ = Mean square for rows (students)
- $MS_E$ = Mean square error
- $MS_C$ = Mean square for columns (trials)
- $k$ = Number of trials
- $n$ = Number of students

### 3. Fleiss' Kappa
$$\kappa = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e}$$

Where:
- $\bar{P}$ = Overall agreement proportion
- $\bar{P}_e$ = Expected agreement by chance

### 4. Cohen's d (Effect Size)
$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{pooled}}$$

Where:
- $s_{pooled} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$

---

## 🔬 Advanced Analysis

For researchers wanting to extend this work:

### Custom Rubric Analysis
Modify grading dimensions by editing:
```python
RUBRIC_DIMENSIONS = {
    'content': 0.40,      # Weight
    'organization': 0.30,
    'arguments': 0.20,
    'language': 0.10
}
```

### Different Essay Types
Adapt prompts for:
- Argumentative essays
- Narrative writing
- Research reports
- Short-answer responses

See `04_Supplementary_Materials/S4_Prompts_Complete.md` for prompt templates.

---

## 📚 References

**Statistical Methods**:
- Koo, T. K., & Li, M. Y. (2016). A guideline of selecting and reporting intraclass correlation coefficients for reliability research. *Journal of Chiropractic Medicine*, 15(2), 155-163.
- Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159-174.

**Python Packages**:
- pandas: McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 51-56.
- pingouin: Vallat, R. (2018). Pingouin: statistics in Python. *Journal of Open Source Software*, 3(31), 1026.

---

## 📧 Support

For questions about analysis methods:
- Open an issue on OSF
- Email: [corresponding author email]

---

*Note: Complete executable scripts will be added in future OSF versions (v1.1+). Current version focuses on data sharing and methodological transparency.*

*Last updated: December 25, 2025*
