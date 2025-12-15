# Supplementary Material S4: Implementation Code and Reproducibility Guide

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring  
**Document Type:** Code Documentation and Reproducibility Instructions  
**Purpose:** Enable full reproduction of all analyses

---

## Table of Contents

1. Environment Setup
2. Data Preparation Scripts
3. Analysis Scripts (RQ1-RQ5)
4. Visualization Scripts
5. Key Functions Documentation
6. Execution Instructions
7. Troubleshooting Guide
8. Code Repository Structure

---

## 1. Environment Setup

### 1.1 System Requirements

**Hardware:**
- CPU: Multi-core processor (recommended 4+ cores)
- RAM: 16 GB minimum, 32 GB recommended
- Storage: 5 GB free space for data and results
- GPU: Not required (CPU-only execution)

**Operating System:**
- Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- Python 3.11+ required

### 1.2 Python Environment Configuration

**Option 1: Conda Environment (Recommended)**

```bash
# Create new conda environment
conda create -n aes_analysis python=3.11 -y
conda activate aes_analysis

# Install packages from conda-forge
conda install -c conda-forge numpy=1.24.3 pandas=2.0.3 matplotlib=3.7.1 seaborn=0.12.2 -y
conda install -c conda-forge scikit-learn=1.4.0 scipy=1.12.0 statsmodels=0.14.1 -y
conda install -c conda-forge pingouin=0.5.3 openpyxl=3.1.2 -y

# Install pip packages
pip install openai==1.3.5 google-generativeai==0.3.1
```

**Option 2: Virtual Environment (venv)**

```bash
# Create virtual environment
python -m venv aes_env

# Activate (Windows)
aes_env\Scripts\activate

# Activate (macOS/Linux)
source aes_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

**requirements.txt:**
```txt
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.1
seaborn==0.12.2
scikit-learn==1.4.0
scipy==1.12.0
statsmodels==0.14.1
pingouin==0.5.3
openpyxl==3.1.2
openai==1.3.5
google-generativeai==0.3.1
```

### 1.3 API Keys Configuration

**Create `.env` file in project root:**

```bash
# OpenAI API Key (for ChatGPT-4o)
OPENAI_API_KEY=sk-your-key-here

# Google AI API Key (for Gemini-2.5-Flash)
GOOGLE_AI_API_KEY=your-google-api-key-here
```

**Alternative: Environment Variables**

```bash
# Windows
set OPENAI_API_KEY=sk-your-key-here
set GOOGLE_AI_API_KEY=your-google-api-key-here

# macOS/Linux
export OPENAI_API_KEY=sk-your-key-here
export GOOGLE_AI_API_KEY=your-google-api-key-here
```

### 1.4 Directory Structure Setup

```bash
# Create project directories
mkdir -p data/{raw,processed,results}
mkdir -p results_experiment_final/{data,figures,tables,reports}
mkdir -p results_experiment_final/{rq1_validity,rq2_consistency,rq3_model_comparison,rq4_error_analysis,rq5_practical}
mkdir -p scripts
mkdir -p config
```

---

## 2. Data Preparation Scripts

### 2.1 Gold Standard Creation

**File:** `scripts/create_gold_standard.py`

**Purpose:** Create gold standard from expert rater annotations

**Usage:**
```bash
python scripts/create_gold_standard.py
```

**Key Code Excerpt:**
```python
import pandas as pd
import numpy as np
from pathlib import Path

def create_gold_standard(rater1_file, rater2_file, output_file):
    """
    Combine two expert raters and create gold standard.
    
    Args:
        rater1_file: CSV with columns [student_id, question, score]
        rater2_file: CSV with columns [student_id, question, score]
        output_file: Output CSV path
        
    Returns:
        DataFrame with gold standard scores
    """
    # Load raters
    df1 = pd.read_csv(rater1_file)
    df2 = pd.read_csv(rater2_file)
    
    # Merge
    df = df1.merge(df2, on=['student_id', 'question'], 
                   suffixes=('_rater1', '_rater2'))
    
    # Calculate gold standard (average)
    df['gold_score'] = (df['score_rater1'] + df['score_rater2']) / 2
    
    # Round to nearest grade if difference <= 1
    df['diff'] = abs(df['score_rater1'] - df['score_rater2'])
    df.loc[df['diff'] <= 1, 'gold_score'] = df.loc[df['diff'] <= 1, 'gold_score'].round()
    
    # For differences > 1, flag for third rater (manual resolution)
    if (df['diff'] > 1).any():
        print(f"Warning: {(df['diff'] > 1).sum()} cases need third rater")
        df.loc[df['diff'] > 1].to_csv('needs_third_rater.csv', index=False)
    
    # Save
    df[['student_id', 'question', 'gold_score']].to_csv(output_file, index=False)
    
    return df

# Execute
if __name__ == "__main__":
    df_gold = create_gold_standard(
        'data/raw/rater1_scores.csv',
        'data/raw/rater2_scores.csv',
        'results_experiment_final/data/gold_standard.csv'
    )
    print(f"Gold standard created: {len(df_gold)} essays")
```

**Output:**
- `results_experiment_final/data/gold_standard.csv`
- `needs_third_rater.csv` (if any conflicts)

### 2.2 Experiment Data Extraction

**File:** `scripts/extract_data_for_analysis.py`

**Purpose:** Extract completed gradings from database

**Usage:**
```bash
python scripts/extract_data_for_analysis.py
```

**Key Code:**
```python
import sqlite3
import pandas as pd
from pathlib import Path

def extract_experiment_data(db_path, output_path):
    """Extract all completed gradings from database."""
    
    conn = sqlite3.connect(db_path)
    
    # Query
    query = """
    SELECT 
        student_id,
        question_number,
        model,
        strategy,
        trial,
        predicted_score,
        timestamp,
        tokens_used,
        response_time_seconds
    FROM grading_results
    WHERE status = 'completed'
    ORDER BY model, strategy, student_id, question_number, trial
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Clean data
    df['predicted_score'] = df['predicted_score'].astype(float)
    df['question_number'] = df['question_number'].astype(int)
    df['trial'] = df['trial'].astype(int)
    
    # Save
    df.to_csv(output_path, index=False)
    
    print(f"Extracted {len(df)} grading records")
    print(f"Models: {df['model'].unique()}")
    print(f"Strategies: {df['strategy'].unique()}")
    print(f"Trials: {df['trial'].min()}-{df['trial'].max()}")
    
    return df

# Execute
if __name__ == "__main__":
    df = extract_experiment_data(
        'results/grading_results.db',
        'results_experiment_final/data/experiment_data_complete.csv'
    )
```

**Output:**
- `results_experiment_final/data/experiment_data_complete.csv`

---

## 3. Analysis Scripts (RQ1-RQ5)

### 3.1 RQ1: Validity Analysis

**File:** `scripts/analyze_rq1_validity.py`

**Purpose:** Calculate QWK, Cohen's Kappa, agreement rates

**Key Functions:**

```python
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix

def quadratic_weighted_kappa(y_true, y_pred, min_rating=1, max_rating=5):
    """
    Calculate Quadratic Weighted Kappa (QWK).
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        min_rating: Minimum rating value
        max_rating: Maximum rating value
        
    Returns:
        float: QWK score
    """
    # Confusion matrix
    conf_mat = confusion_matrix(y_true, y_pred, 
                                labels=range(min_rating, max_rating+1))
    
    # Weight matrix (quadratic)
    num_ratings = max_rating - min_rating + 1
    weights = np.zeros((num_ratings, num_ratings))
    for i in range(num_ratings):
        for j in range(num_ratings):
            weights[i, j] = ((i - j) ** 2) / ((num_ratings - 1) ** 2)
    
    # Observed and expected agreement
    hist_true = np.bincount(y_true - min_rating, minlength=num_ratings)
    hist_pred = np.bincount(y_pred - min_rating, minlength=num_ratings)
    
    expected = np.outer(hist_true, hist_pred).astype(float)
    expected /= expected.sum()
    
    observed = conf_mat.astype(float) / conf_mat.sum()
    
    # QWK
    numerator = (weights * observed).sum()
    denominator = (weights * expected).sum()
    
    if denominator == 0:
        return 0.0
    
    kappa = 1.0 - (numerator / denominator)
    
    return kappa

def calculate_agreement_rates(y_true, y_pred):
    """Calculate exact and adjacent agreement rates."""
    
    diff = np.abs(y_true - y_pred)
    
    exact = (diff == 0).sum() / len(diff)
    adjacent = (diff <= 1).sum() / len(diff)
    within_2 = (diff <= 2).sum() / len(diff)
    
    return {
        'exact': exact,
        'adjacent': adjacent,
        'within_2': within_2
    }

# Usage example
if __name__ == "__main__":
    # Load data
    df_gold = pd.read_csv('results_experiment_final/data/gold_standard.csv')
    df_exp = pd.read_csv('results_experiment_final/data/experiment_data_complete.csv')
    
    # Merge
    df = df_exp.merge(df_gold, on=['student_id', 'question_number'])
    
    # Calculate metrics by model-strategy
    results = []
    for (model, strategy), group in df.groupby(['model', 'strategy']):
        
        # Get mean prediction per essay (average across trials)
        mean_pred = group.groupby(['student_id', 'question_number'])['predicted_score'].mean()
        mean_pred_rounded = mean_pred.round().astype(int)
        
        gold = group.drop_duplicates(['student_id', 'question_number'])['gold_score'].astype(int)
        
        # Calculate metrics
        qwk = quadratic_weighted_kappa(gold.values, mean_pred_rounded.values)
        kappa = cohen_kappa_score(gold.values, mean_pred_rounded.values)
        agreement = calculate_agreement_rates(gold.values, mean_pred_rounded.values)
        
        results.append({
            'model': model,
            'strategy': strategy,
            'qwk': qwk,
            'cohen_kappa': kappa,
            'exact_agreement': agreement['exact'],
            'adjacent_agreement': agreement['adjacent']
        })
    
    df_results = pd.DataFrame(results)
    df_results.to_csv('results_experiment_final/rq1_validity/validity_metrics.csv', index=False)
    print(df_results)
```

**Output:**
- `results_experiment_final/rq1_validity/validity_metrics.csv`

### 3.2 RQ2: Reliability Analysis

**File:** `scripts/analyze_rq2bc_reliability.py`

**Purpose:** Calculate ICC, Cronbach's α, Fleiss' κ

**Key Functions:**

```python
import pingouin as pg
import pandas as pd
import numpy as np

def calculate_icc(df, essay_col, trial_col, score_col):
    """
    Calculate Intraclass Correlation Coefficient.
    
    Args:
        df: DataFrame with columns [essay_col, trial_col, score_col]
        essay_col: Column name for essay identifier
        trial_col: Column name for trial/rater identifier
        score_col: Column name for scores
        
    Returns:
        dict: ICC(2,1) and ICC(2,k) values
    """
    # Reshape to wide format
    df_wide = df.pivot(index=essay_col, columns=trial_col, values=score_col)
    
    # Calculate ICC using pingouin
    icc_result = pg.intraclass_corr(
        data=df,
        targets=essay_col,
        raters=trial_col,
        ratings=score_col
    )
    
    # Extract ICC(2,1) and ICC(2,k)
    icc_2_1 = icc_result[icc_result['Type'] == 'ICC2']['ICC'].values[0]
    icc_2_k = icc_result[icc_result['Type'] == 'ICC2k']['ICC'].values[0]
    
    return {
        'ICC(2,1)': icc_2_1,
        'ICC(2,k)': icc_2_k,
        'full_results': icc_result
    }

def calculate_cronbach_alpha(df_wide):
    """
    Calculate Cronbach's Alpha.
    
    Args:
        df_wide: DataFrame where rows=essays, columns=trials
        
    Returns:
        float: Cronbach's Alpha
    """
    alpha = pg.cronbach_alpha(data=df_wide)
    return alpha[0]  # Returns (alpha, confidence_interval)

def calculate_fleiss_kappa(df, essay_col, trial_col, score_col):
    """Calculate Fleiss' Kappa for multiple raters."""
    
    # Reshape to matrix: rows=essays, columns=trials
    df_wide = df.pivot(index=essay_col, columns=trial_col, values=score_col)
    
    # Convert to integer categories
    df_wide = df_wide.round().astype(int)
    
    # Count occurrences of each category per essay
    categories = sorted(df_wide.values.flatten())
    min_cat, max_cat = min(categories), max(categories)
    
    n_essays, n_raters = df_wide.shape
    n_categories = max_cat - min_cat + 1
    
    # Build frequency matrix
    freq_matrix = np.zeros((n_essays, n_categories))
    for i, row in enumerate(df_wide.values):
        for rating in row:
            freq_matrix[i, rating - min_cat] += 1
    
    # Calculate Fleiss' Kappa
    P_i = (freq_matrix ** 2).sum(axis=1) - n_raters
    P_i = P_i / (n_raters * (n_raters - 1))
    P_bar = P_i.mean()
    
    p_j = freq_matrix.sum(axis=0) / (n_essays * n_raters)
    P_e_bar = (p_j ** 2).sum()
    
    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    
    return kappa

# Usage
if __name__ == "__main__":
    df = pd.read_csv('results_experiment_final/data/experiment_data_complete.csv')
    
    results = []
    for (model, strategy), group in df.groupby(['model', 'strategy']):
        
        # Create essay identifier
        group['essay_id'] = group['student_id'] + '_Q' + group['question_number'].astype(str)
        
        # ICC
        icc_results = calculate_icc(group, 'essay_id', 'trial', 'predicted_score')
        
        # Cronbach's Alpha
        df_wide = group.pivot(index='essay_id', columns='trial', values='predicted_score')
        alpha = calculate_cronbach_alpha(df_wide)
        
        # Fleiss' Kappa
        fleiss_k = calculate_fleiss_kappa(group, 'essay_id', 'trial', 'predicted_score')
        
        results.append({
            'model': model,
            'strategy': strategy,
            'ICC(2,1)': icc_results['ICC(2,1)'],
            'ICC(2,k)': icc_results['ICC(2,k)'],
            'cronbach_alpha': alpha,
            'fleiss_kappa': fleiss_k
        })
    
    df_results = pd.DataFrame(results)
    df_results.to_csv('results_experiment_final/rq2_consistency/reliability_coefficients.csv', index=False)
    print(df_results)
```

**Output:**
- `results_experiment_final/rq2_consistency/reliability_coefficients.csv`

### 3.3 Confusion Matrix Analysis

**File:** `scripts/analyze_confusion_matrix_detailed.py`

**Purpose:** Generate detailed classification metrics

**Key Functions:**

```python
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

def calculate_detailed_metrics(y_true, y_pred, labels=None):
    """
    Calculate comprehensive classification metrics per class.
    
    Returns:
        DataFrame with columns: precision, recall, specificity, f1, support, TP, FP, TN, FN
    """
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Calculate per-class metrics
    metrics = []
    for i, label in enumerate(labels):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        tn = cm.sum() - tp - fp - fn
        
        # Precision, Recall, Specificity, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        metrics.append({
            'grade': label,
            'precision': precision,
            'recall': recall,
            'specificity': specificity,
            'f1_score': f1,
            'support': cm[i, :].sum(),
            'tp': tp,
            'fp': fp,
            'tn': tn,
            'fn': fn
        })
    
    return pd.DataFrame(metrics)

# Usage
if __name__ == "__main__":
    # Load and merge data
    df_gold = pd.read_csv('results_experiment_final/data/gold_standard.csv')
    df_exp = pd.read_csv('results_experiment_final/data/experiment_data_complete.csv')
    
    df = df_exp.merge(df_gold, on=['student_id', 'question_number'])
    
    # Calculate for each model-strategy
    all_metrics = []
    for (model, strategy), group in df.groupby(['model', 'strategy']):
        
        # Get mean predictions
        mean_pred = group.groupby(['student_id', 'question_number'])['predicted_score'].mean()
        mean_pred_rounded = mean_pred.round().astype(int)
        
        gold = group.drop_duplicates(['student_id', 'question_number'])['gold_score'].astype(int)
        
        # Calculate metrics
        metrics = calculate_detailed_metrics(gold.values, mean_pred_rounded.values, labels=[1,2,3,4,5])
        metrics['model'] = model
        metrics['strategy'] = strategy
        
        all_metrics.append(metrics)
    
    df_all = pd.concat(all_metrics, ignore_index=True)
    df_all.to_csv('results_experiment_final/rq1_validity/detailed_classification_metrics.csv', index=False)
```

**Output:**
- `results_experiment_final/rq1_validity/detailed_classification_metrics.csv`

### 3.4 RQ3: Model Comparison Tests

**File:** `scripts/analyze_rq3_model_comparison.py`

**Purpose:** Paired t-test, Wilcoxon, McNemar's

**Key Code:**

```python
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar

def paired_comparison(chatgpt_scores, gemini_scores):
    """Perform paired t-test and Wilcoxon test."""
    
    # Paired t-test
    t_stat, t_pvalue = stats.ttest_rel(chatgpt_scores, gemini_scores)
    
    # Cohen's d
    diff = chatgpt_scores - gemini_scores
    cohens_d = diff.mean() / diff.std()
    
    # Wilcoxon signed-rank test
    w_stat, w_pvalue = stats.wilcoxon(chatgpt_scores, gemini_scores)
    
    return {
        't_statistic': t_stat,
        't_pvalue': t_pvalue,
        'cohens_d': cohens_d,
        'wilcoxon_statistic': w_stat,
        'wilcoxon_pvalue': w_pvalue
    }

def mcnemar_test(chatgpt_correct, gemini_correct):
    """Perform McNemar's test on classification accuracy."""
    
    # Build contingency table
    both_correct = ((chatgpt_correct == 1) & (gemini_correct == 1)).sum()
    chatgpt_only = ((chatgpt_correct == 1) & (gemini_correct == 0)).sum()
    gemini_only = ((chatgpt_correct == 0) & (gemini_correct == 1)).sum()
    both_wrong = ((chatgpt_correct == 0) & (gemini_correct == 0)).sum()
    
    table = [[both_correct, chatgpt_only],
             [gemini_only, both_wrong]]
    
    result = mcnemar(table, exact=True)
    
    return {
        'statistic': result.statistic,
        'pvalue': result.pvalue,
        'chatgpt_only_correct': chatgpt_only,
        'gemini_only_correct': gemini_only
    }
```

**Output:**
- `results_experiment_final/rq3_model_comparison/statistical_tests.csv`

### 3.5 RQ4: Error Analysis

**File:** `scripts/analyze_rq4_error_analysis.py`

**Purpose:** MAE, bias analysis, critical error identification

**Key Code:**

```python
def calculate_error_metrics(y_true, y_pred):
    """Calculate comprehensive error metrics."""
    
    errors = y_pred - y_true
    abs_errors = np.abs(errors)
    
    mae = abs_errors.mean()
    rmse = np.sqrt((errors ** 2).mean())
    bias = errors.mean()
    
    # Error distribution
    exact = (abs_errors == 0).sum() / len(errors)
    within_1 = (abs_errors <= 1).sum() / len(errors)
    within_2 = (abs_errors <= 2).sum() / len(errors)
    critical = (abs_errors >= 2).sum() / len(errors)
    
    # Over/under grading
    overgrading = (errors > 0).sum() / len(errors)
    undergrading = (errors < 0).sum() / len(errors)
    
    return {
        'mae': mae,
        'rmse': rmse,
        'bias': bias,
        'exact_rate': exact,
        'adjacent_rate': within_1,
        'within_2_rate': within_2,
        'critical_error_rate': critical,
        'overgrading_rate': overgrading,
        'undergrading_rate': undergrading
    }
```

**Output:**
- `results_experiment_final/rq4_error_analysis/error_metrics.csv`

### 3.6 RQ5: Cost-Benefit Analysis

**File:** `scripts/analyze_rq5_practical.py`

**Purpose:** Calculate cost per essay, throughput, hybrid protocol costs

**Key Code:**

```python
def calculate_costs(tokens_input, tokens_output, model):
    """Calculate API costs."""
    
    pricing = {
        'chatgpt': {'input': 0.005 / 1000, 'output': 0.015 / 1000},
        'gemini': {'input': 0.00015 / 1000, 'output': 0.0006 / 1000}
    }
    
    cost_input = tokens_input * pricing[model]['input']
    cost_output = tokens_output * pricing[model]['output']
    
    return cost_input + cost_output

def calculate_throughput(response_times):
    """Calculate essays per hour."""
    
    mean_time = np.mean(response_times)  # seconds per essay
    essays_per_hour = 3600 / mean_time
    
    return essays_per_hour

def hybrid_protocol_cost(accuracy_tier1, accuracy_tier2, coverage_tier1, coverage_tier2):
    """Calculate hybrid protocol costs."""
    
    cost_llm = 0.0064  # ChatGPT zero-shot
    cost_human = 1.50
    qc_rate = 0.20  # 20% spot check for tier 2
    
    # Tier 1: Auto-grade
    cost_t1 = coverage_tier1 * cost_llm
    
    # Tier 2: Auto-grade + QC
    cost_t2_auto = coverage_tier2 * (1 - qc_rate) * cost_llm
    cost_t2_human = coverage_tier2 * qc_rate * cost_human
    cost_t2 = cost_t2_auto + cost_t2_human
    
    # Tier 3: Full human review
    coverage_tier3 = 1.0 - coverage_tier1 - coverage_tier2
    cost_t3 = coverage_tier3 * cost_human
    
    total_cost = cost_t1 + cost_t2 + cost_t3
    
    return {
        'tier1_cost': cost_t1,
        'tier2_cost': cost_t2,
        'tier3_cost': cost_t3,
        'total_cost': total_cost,
        'savings_vs_human': (cost_human - total_cost) / cost_human
    }
```

**Output:**
- `results_experiment_final/rq5_practical/cost_analysis.csv`

---

## 4. Visualization Scripts

### 4.1 Confusion Matrix Heatmap

**File:** `scripts/visualize_confusion_matrices.py`

**Key Code:**

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrices(models_strategies, cms, output_path):
    """
    Plot confusion matrices in a 2×3 grid.
    
    Args:
        models_strategies: List of (model, strategy) tuples
        cms: List of confusion matrices
        output_path: Output file path
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for idx, ((model, strategy), cm) in enumerate(zip(models_strategies, cms)):
        ax = axes[idx]
        
        # Normalize for percentages
        cm_pct = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Create annotations
        annot = np.empty_like(cm, dtype=object)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                annot[i, j] = f"{cm[i,j]}\n({cm_pct[i,j]:.1f}%)"
        
        # Heatmap
        sns.heatmap(cm, annot=annot, fmt='', cmap='Blues', 
                    xticklabels=['E(1)', 'D(2)', 'C(3)', 'B(4)', 'A(5)'],
                    yticklabels=['E(1)', 'D(2)', 'C(3)', 'B(4)', 'A(5)'],
                    cbar_kws={'label': 'Count'},
                    ax=ax, vmin=0, vmax=cm.max())
        
        ax.set_title(f'{model.upper()} - {strategy.capitalize()}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Predicted Grade', fontsize=12)
        ax.set_ylabel('True Grade', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

### 4.2 Reliability Coefficients Comparison

**File:** `scripts/visualize_reliability.py`

**Key Code:**

```python
def plot_reliability_comparison(df_reliability, output_path):
    """
    Plot ICC, Cronbach's Alpha, Fleiss' Kappa comparison.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    metrics = ['ICC(2,1)', 'cronbach_alpha', 'fleiss_kappa']
    titles = ['ICC(2,1)', "Cronbach's Alpha", "Fleiss' Kappa"]
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx]
        
        # Bar plot
        x = range(len(df_reliability))
        heights = df_reliability[metric]
        colors = ['#1f77b4' if m == 'chatgpt' else '#ff7f0e' 
                  for m in df_reliability['model']]
        
        bars = ax.bar(x, heights, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=10)
        
        ax.set_ylabel(title, fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f"{row['model']}\n{row['strategy']}" 
                            for _, row in df_reliability.iterrows()],
                           rotation=45, ha='right')
        ax.set_ylim(0.85, 1.0)
        ax.axhline(y=0.90, color='red', linestyle='--', alpha=0.5, label='Excellent (0.90)')
        ax.grid(axis='y', alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

---

## 5. Key Functions Documentation

### 5.1 calculate_detailed_metrics()

**Purpose:** Compute TP/FP/TN/FN and derive precision/recall/specificity/F1 per grade

**Parameters:**
- `y_true` (array): True labels
- `y_pred` (array): Predicted labels
- `labels` (list): List of possible labels (default: [1,2,3,4,5])

**Returns:** DataFrame with columns:
- `grade`: Grade level (1-5)
- `precision`: TP / (TP + FP)
- `recall`: TP / (TP + FN)
- `specificity`: TN / (TN + FP)
- `f1_score`: Harmonic mean of precision and recall
- `support`: Number of true instances
- `tp, fp, tn, fn`: Confusion matrix components

**Example:**
```python
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

# Sample data
y_true = np.array([1, 1, 2, 2, 3, 3, 3, 4, 5])
y_pred = np.array([1, 2, 2, 2, 3, 3, 4, 4, 4])

# Calculate
metrics = calculate_detailed_metrics(y_true, y_pred)
print(metrics)

# Output:
#    grade  precision  recall  specificity  f1_score  support  tp  fp  tn  fn
# 0      1       1.00    0.50         1.00      0.67        2   1   0   7   1
# 1      2       0.75    1.00         0.83      0.86        2   2   1   5   0
# 2      3       0.67    0.67         0.83      0.67        3   2   1   5   1
# 3      4       0.33    1.00         0.75      0.50        1   1   2   6   0
# 4      5       0.00    0.00         0.88      0.00        1   0   1   7   1
```

### 5.2 quadratic_weighted_kappa()

**Purpose:** Calculate QWK for ordinal data with quadratic penalties

**Formula:**
$$\kappa_w = 1 - \frac{\sum_{i,j} w_{ij} O_{ij}}{\sum_{i,j} w_{ij} E_{ij}}$$

Where $w_{ij} = \frac{(i-j)^2}{(N-1)^2}$ (quadratic weights)

**Parameters:**
- `y_true`: True labels
- `y_pred`: Predicted labels
- `min_rating`: Minimum rating (default: 1)
- `max_rating`: Maximum rating (default: 5)

**Returns:** float (QWK score, 0-1)

### 5.3 calculate_icc()

**Purpose:** Calculate ICC(2,1) and ICC(2,k) for consistency analysis

**ICC Types:**
- ICC(2,1): Single rater, two-way random effects
- ICC(2,k): Average of k raters, two-way random effects

**Interpretation:**
- <0.50: Poor
- 0.50-0.75: Moderate
- 0.75-0.90: Good
- >0.90: Excellent

---

## 6. Execution Instructions

### 6.1 Full Pipeline Execution

**Step 1: Prepare Data**
```bash
# Create gold standard
python scripts/create_gold_standard.py

# Extract experiment data
python scripts/extract_data_for_analysis.py
```

**Step 2: Run All Analyses**
```bash
# RQ1: Validity
python scripts/analyze_rq1_validity.py

# RQ2: Reliability
python scripts/analyze_rq2bc_reliability.py

# Confusion Matrix
python scripts/analyze_confusion_matrix_detailed.py

# RQ3: Model Comparison
python scripts/analyze_rq3_model_comparison.py

# RQ4: Error Analysis
python scripts/analyze_rq4_error_analysis.py

# RQ5: Practical Implications
python scripts/analyze_rq5_practical.py
```

**Step 3: Generate Visualizations**
```bash
python scripts/visualize_confusion_matrices.py
python scripts/visualize_reliability.py
```

**Step 4: Generate Report**
```bash
python scripts/generate_comprehensive_report.py
```

### 6.2 Parallel Execution (Optional)

For faster processing, run analyses in parallel:

```bash
# Using GNU Parallel (Linux/macOS)
parallel python scripts/analyze_{}.py ::: rq1_validity rq2bc_reliability rq3_model_comparison rq4_error_analysis rq5_practical

# Using PowerShell parallel (Windows)
$scripts = @('rq1_validity', 'rq2bc_reliability', 'rq3_model_comparison', 'rq4_error_analysis', 'rq5_practical')
$scripts | ForEach-Object -Parallel { python scripts/analyze_$_.py }
```

### 6.3 Expected Runtime

| Task | Runtime (Typical) | Runtime (Worst Case) |
|------|-------------------|----------------------|
| Data Preparation | 2-5 min | 10 min |
| RQ1 Analysis | 3-7 min | 15 min |
| RQ2 Analysis | 5-10 min | 20 min |
| Confusion Matrix | 8-12 min | 25 min |
| RQ3 Analysis | 2-5 min | 10 min |
| RQ4 Analysis | 3-7 min | 15 min |
| RQ5 Analysis | 1-3 min | 5 min |
| Visualizations | 5-10 min | 20 min |
| **Total** | **25-50 min** | **2 hours** |

---

## 7. Troubleshooting Guide

### 7.1 Common Issues

**Issue 1: ModuleNotFoundError**
```
Error: ModuleNotFoundError: No module named 'pingouin'
```
**Solution:**
```bash
pip install pingouin==0.5.3
```

**Issue 2: File Not Found**
```
Error: FileNotFoundError: [Errno 2] No such file or directory: 'results_experiment_final/data/gold_standard.csv'
```
**Solution:**
```bash
# Create directories
mkdir -p results_experiment_final/data

# Run data preparation
python scripts/create_gold_standard.py
```

**Issue 3: Memory Error**
```
Error: MemoryError: Unable to allocate array
```
**Solution:**
```python
# Reduce batch size in analysis scripts
# Or process data in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process_chunk(chunk)
```

**Issue 4: Inconsistent Student IDs**
```
Warning: Student IDs don't match between gold standard and experiment data
```
**Solution:**
```python
# Standardize student_id format
df['student_id'] = 'student_' + df['student_id'].astype(str).str.zfill(2)
```

### 7.2 Debugging Tips

**Enable Verbose Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Processing student: %s", student_id)
```

**Check Data Integrity:**
```python
# Verify no missing values
assert df['predicted_score'].notna().all(), "Missing scores detected"

# Verify score range
assert df['predicted_score'].between(1, 5).all(), "Scores out of range"

# Verify gold standard matches
assert len(df_merged) == len(df_exp), "Merge resulted in mismatches"
```

---

## 8. Code Repository Structure

```
AES/
├── README.md                      # Project overview
├── requirements.txt               # Python dependencies
├── .env                          # API keys (not committed)
├── .gitignore                    # Git ignore patterns
│
├── config/
│   ├── models_config.yaml        # Model configuration
│   └── rubrics.json              # Grading rubric
│
├── data/
│   ├── raw/                      # Original data
│   ├── processed/                # Processed data
│   └── results/                  # Experiment results
│
├── scripts/
│   ├── create_gold_standard.py
│   ├── extract_data_for_analysis.py
│   ├── analyze_rq1_validity.py
│   ├── analyze_rq2bc_reliability.py
│   ├── analyze_confusion_matrix_detailed.py
│   ├── analyze_rq3_model_comparison.py
│   ├── analyze_rq4_error_analysis.py
│   ├── analyze_rq5_practical.py
│   ├── visualize_confusion_matrices.py
│   ├── visualize_reliability.py
│   └── generate_comprehensive_report.py
│
├── results_experiment_final/
│   ├── data/
│   │   ├── gold_standard.csv
│   │   └── experiment_data_complete.csv
│   ├── figures/                  # All visualizations
│   ├── tables/                   # All tables
│   ├── reports/                  # Final manuscripts
│   ├── rq1_validity/            # RQ1 outputs
│   ├── rq2_consistency/         # RQ2 outputs
│   ├── rq3_model_comparison/    # RQ3 outputs
│   ├── rq4_error_analysis/      # RQ4 outputs
│   └── rq5_practical/           # RQ5 outputs
│
└── tests/
    ├── test_metrics.py           # Unit tests for metrics
    ├── test_data_loading.py      # Unit tests for data
    └── test_visualizations.py    # Unit tests for plots
```

---

**Document End**

**Status:** Complete implementation guide with all key functions documented  
**Next:** Execute full pipeline to validate reproducibility  
**Contact:** [Research team email] for questions or issues
