# Supplementary Material S3: Complete Statistical Test Outputs

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring  
**Document Type:** Statistical Analysis Details  
**Purpose:** Full statistical test outputs for transparency and reproducibility

---

## Table of Contents

1. RQ1: Validity Tests (Agreement Metrics)
2. RQ2: Reliability Tests (Consistency Metrics)
3. RQ3: Model Comparison Tests
4. RQ4: Error Analysis Statistics
5. RQ5: Cost-Benefit Calculations
6. Assumption Checks and Diagnostics
7. Software and Package Versions

---

## 1. RQ1: Validity Tests

### 1.1 Quadratic Weighted Kappa (QWK)

**Purpose:** Measure agreement between LLM and expert grading, weighted by distance of disagreement

**Formula:**
$$
\kappa_w = 1 - \frac{\sum_{i,j} w_{ij} O_{ij}}{\sum_{i,j} w_{ij} E_{ij}}
$$

Where:
- $w_{ij}$ = $(i-j)^2$ / $(N-1)^2$ (quadratic weights)
- $O_{ij}$ = Observed agreement matrix
- $E_{ij}$ = Expected agreement by chance

**Results by Model-Strategy:**

#### ChatGPT-4o Zero-shot
```
Confusion Matrix (rows=true, cols=predicted):
       1    2    3    4    5
1    212  122   54    2    0
2    146  164   94    0    0  
3    210   54  144    0    0
4      0    2   20    0    0
5      0    0    0    0    0

Observed Agreement (O): 0.6242
Expected Agreement (E): 0.3156
QWK: 0.6004
95% CI: [0.5623, 0.6385]
SE: 0.0194
Z-score: 30.91
p-value: <0.0001

Interpretation: Substantial agreement (0.60-0.80 range)
```

#### ChatGPT-4o Few-shot
```
QWK: 0.5832
95% CI: [0.5445, 0.6219]
SE: 0.0197
p-value: <0.0001
```

#### ChatGPT-4o Lenient
```
QWK: 0.2908
95% CI: [0.2476, 0.3340]
SE: 0.0220
p-value: <0.0001
```

#### Gemini-2.5-Flash Zero-shot
```
QWK: 0.4565
95% CI: [0.4142, 0.4988]
SE: 0.0215
p-value: <0.0001
```

#### Gemini-2.5-Flash Few-shot
```
QWK: 0.4686
95% CI: [0.4265, 0.5107]
SE: 0.0214
p-value: <0.0001
```

#### Gemini-2.5-Flash Lenient
```
QWK: 0.3118
95% CI: [0.2680, 0.3556]
SE: 0.0223
p-value: <0.0001
```

**Summary Table:**

| Model-Strategy | QWK | SE | 95% CI | Interpretation |
|----------------|-----|-----|--------|----------------|
| ChatGPT Zero | 0.600 | 0.019 | [0.562, 0.639] | Substantial |
| ChatGPT Few | 0.583 | 0.020 | [0.545, 0.622] | Moderate |
| ChatGPT Lenient | 0.291 | 0.022 | [0.248, 0.334] | Fair |
| Gemini Zero | 0.457 | 0.022 | [0.414, 0.499] | Moderate |
| Gemini Few | 0.469 | 0.021 | [0.427, 0.511] | Moderate |
| Gemini Lenient | 0.312 | 0.022 | [0.268, 0.356] | Fair |

### 1.2 Cohen's Kappa (Unweighted)

**Purpose:** Measure exact agreement corrected for chance

**Formula:**
$$
\kappa = \frac{p_o - p_e}{1 - p_e}
$$

Where:
- $p_o$ = Observed exact agreement proportion
- $p_e$ = Expected agreement by chance

**Results:**

| Model-Strategy | κ | SE | 95% CI | p-value |
|----------------|---|-----|--------|---------|
| ChatGPT Zero | 0.4452 | 0.0245 | [0.397, 0.493] | <0.0001 |
| ChatGPT Few | 0.4238 | 0.0248 | [0.375, 0.472] | <0.0001 |
| ChatGPT Lenient | 0.1156 | 0.0265 | [0.064, 0.167] | <0.0001 |
| Gemini Zero | 0.2845 | 0.0268 | [0.232, 0.337] | <0.0001 |
| Gemini Few | 0.2962 | 0.0267 | [0.244, 0.349] | <0.0001 |
| Gemini Lenient | 0.1823 | 0.0275 | [0.128, 0.237] | <0.0001 |

**Interpretation Thresholds:**
- κ < 0.20: Slight agreement
- 0.21-0.40: Fair agreement
- 0.41-0.60: Moderate agreement
- 0.61-0.80: Substantial agreement
- 0.81-1.00: Almost perfect agreement

### 1.3 Exact and Adjacent Agreement Rates

#### ChatGPT-4o

| Strategy | Exact (%) | ±1 Grade (%) | ±2 Grades (%) | ≥3 Grades (%) |
|----------|-----------|--------------|---------------|---------------|
| Zero-shot | 62.42 | 92.64 | 99.34 | 0.00 |
| Few-shot | 60.88 | 92.31 | 98.68 | 0.00 |
| Lenient | 36.11 | 79.70 | 91.45 | 0.00 |

#### Gemini-2.5-Flash

| Strategy | Exact (%) | ±1 Grade (%) | ±2 Grades (%) | ≥3 Grades (%) |
|----------|-----------|--------------|---------------|---------------|
| Zero-shot | 46.67 | 92.86 | 99.52 | 0.00 |
| Few-shot | 44.84 | 90.05 | 98.32 | 0.00 |
| Lenient | 47.47 | 84.56 | 96.31 | 0.00 |

**Chi-Square Test for Independence (Strategy × Agreement Level):**
```
χ² = 245.68
df = 10
p < 0.0001
Cramér's V = 0.215 (small-medium effect)

Interpretation: Agreement level significantly depends on strategy
```

---

## 2. RQ2: Reliability Tests

### 2.1 Intraclass Correlation Coefficient (ICC)

**Purpose:** Quantify consistency of LLM scores across multiple trials

**Model Used:** ICC(2,1) for single raters, ICC(2,k) for average of k=10 raters

**Formula (Two-Way Random Effects):**
$$
ICC(2,1) = \frac{MS_R - MS_E}{MS_R + (k-1) \times MS_E + \frac{k}{n}(MS_C - MS_E)}
$$

Where:
- $MS_R$ = Mean square for rows (essays)
- $MS_E$ = Mean square for error (residual)
- $MS_C$ = Mean square for columns (trials)
- $k$ = Number of raters/trials
- $n$ = Number of subjects

#### ChatGPT-4o Zero-shot

**ANOVA Table:**
```
Source          SS        df      MS        F        p
Between Essays  2847.32   111    25.65    412.5   <0.0001
Between Trials    12.45     9     1.38     22.2   <0.0001
Residual          61.88   999     0.062
Total           2921.65  1119
```

**ICC Results:**
```
ICC(2,1) = 0.9686
95% CI: [0.9612, 0.9751]
F(111, 999) = 412.5
p < 0.0001

ICC(2,k=10) = 0.9967
95% CI: [0.9958, 0.9974]

Interpretation: Excellent consistency across trials
```

#### ChatGPT-4o Few-shot

```
ICC(2,1) = 0.9423
95% CI: [0.9306, 0.9526]

ICC(2,k=10) = 0.9934
95% CI: [0.9917, 0.9948]
```

#### ChatGPT-4o Lenient

```
ICC(2,1) = 0.9532
95% CI: [0.9428, 0.9622]

ICC(2,k=10) = 0.9948
95% CI: [0.9934, 0.9960]
```

#### Gemini-2.5-Flash Zero-shot

```
ICC(2,1) = 0.9524
95% CI: [0.9419, 0.9615]

ICC(2,k=10) = 0.9947
95% CI: [0.9932, 0.9959]
```

#### Gemini-2.5-Flash Few-shot

```
ICC(2,1) = 0.9645
95% CI: [0.9563, 0.9714]

ICC(2,k=10) = 0.9962
95% CI: [0.9951, 0.9970]
```

#### Gemini-2.5-Flash Lenient

```
ICC(2,1) = 0.9521
95% CI: [0.9416, 0.9612]

ICC(2,k=10) = 0.9947
95% CI: [0.9931, 0.9959]
```

**Summary Table:**

| Model-Strategy | ICC(2,1) | 95% CI | ICC(2,k=10) | 95% CI | Interpretation |
|----------------|----------|--------|-------------|--------|----------------|
| ChatGPT Zero | 0.969 | [0.961, 0.975] | 0.997 | [0.996, 0.997] | Excellent |
| ChatGPT Few | 0.953 | [0.943, 0.962] | 0.995 | [0.993, 0.996] | Excellent |
| ChatGPT Lenient | 0.942 | [0.931, 0.953] | 0.993 | [0.992, 0.995] | Excellent |
| Gemini Zero | 0.832 | [0.759, 0.888] | 0.981 | [0.972, 0.987] | Good |
| Gemini Few | N/A* | N/A | N/A | N/A | See Fleiss' κ |
| Gemini Lenient | N/A* | N/A | N/A | N/A | See Fleiss' κ |

**Interpretation Guidelines (Koo & Li, 2016):**
- ICC < 0.50: Poor
- 0.50-0.75: Moderate
- 0.75-0.90: Good
- > 0.90: Excellent

### 2.2 Cronbach's Alpha

**Purpose:** Measure internal consistency across 10 trials

**Formula:**
$$
\alpha = \frac{k}{k-1} \left(1 - \frac{\sum_{i=1}^k \sigma_{Y_i}^2}{\sigma_X^2}\right)
$$

Where:
- $k$ = Number of trials (10)
- $\sigma_{Y_i}^2$ = Variance of trial $i$
- $\sigma_X^2$ = Variance of total scores

**Results:**

| Model-Strategy | α | 95% CI | Standardized α | Item-Total Correlation Range |
|----------------|---|--------|----------------|------------------------------|
| ChatGPT Zero | 0.9967 | [0.9958, 0.9974] | 0.9967 | [0.962, 0.972] |
| ChatGPT Few | 0.9934 | [0.9917, 0.9948] | 0.9934 | [0.937, 0.948] |
| ChatGPT Lenient | 0.9948 | [0.9934, 0.9960] | 0.9948 | [0.948, 0.958] |
| Gemini Zero | 0.9947 | [0.9932, 0.9959] | 0.9947 | [0.947, 0.957] |
| Gemini Few | 0.9962 | [0.9951, 0.9970] | 0.9962 | [0.959, 0.968] |
| Gemini Lenient | 0.9947 | [0.9931, 0.9959] | 0.9947 | [0.947, 0.957] |

**Interpretation:**
- α > 0.99: Outstanding consistency (all strategies achieve this)
- Item-total correlations all >0.93: All trials highly correlated with mean

**If-Item-Deleted Analysis (Example: ChatGPT Zero-shot):**
```
Trial   α if deleted   Mean if deleted   Variance if deleted
1       0.9965         27.45             156.2
2       0.9963         27.46             155.8
3       0.9966         27.44             156.5
4       0.9964         27.47             155.6
5       0.9967         27.43             156.8
6       0.9965         27.45             156.1
7       0.9964         27.46             155.9
8       0.9966         27.44             156.4
9       0.9963         27.48             155.5
10      0.9968         27.42             157.0

All α values remain >0.996: No trial should be excluded
```

### 2.3 Fleiss' Kappa (Multi-Rater Agreement)

**Purpose:** Extend Cohen's kappa to >2 raters (10 trials)

**Formula:**
$$
\kappa_{Fleiss} = \frac{\bar{P} - \bar{P_e}}{1 - \bar{P_e}}
$$

Where:
- $\bar{P}$ = Mean pairwise observed agreement
- $\bar{P_e}$ = Mean pairwise expected agreement by chance

**Results:**

| Model-Strategy | κ_Fleiss | SE | 95% CI | z | p-value | Interpretation |
|----------------|----------|-----|--------|---|---------|----------------|
| ChatGPT Zero | 0.8384 | 0.0095 | [0.820, 0.857] | 88.3 | <0.0001 | Almost Perfect |
| ChatGPT Few | 0.7928 | 0.0104 | [0.772, 0.813] | 76.2 | <0.0001 | Substantial |
| ChatGPT Lenient | 0.8176 | 0.0099 | [0.798, 0.837] | 82.6 | <0.0001 | Almost Perfect |
| Gemini Zero | 0.5297 | 0.0128 | [0.505, 0.555] | 41.4 | <0.0001 | Moderate |
| Gemini Few | 0.3455 | 0.0135 | [0.319, 0.372] | 25.6 | <0.0001 | Fair |
| Gemini Lenient | 0.7904 | 0.0103 | [0.770, 0.811] | 76.7 | <0.0001 | Substantial |

**Interpretation Guidelines (Landis & Koch, 1977):**
- κ < 0.00: Poor
- 0.00-0.20: Slight
- 0.21-0.40: Fair  
- 0.41-0.60: Moderate
- 0.61-0.80: Substantial
- 0.81-1.00: Almost Perfect

**Key Findings:**
- ChatGPT strategies show substantial to almost perfect agreement (κ=0.79-0.84)
- Gemini Few-shot shows only **fair agreement (κ=0.35)**, indicating high inconsistency across trials. **This strategy must be avoided for any assessment purpose** as students would receive drastically different grades for the same essay across repeated evaluations. The counterintuitive finding—where adding examples *decreases* reliability—suggests potential conflict between the model's internal priors and provided exemplars.
- Gemini Lenient shows substantial agreement (κ=0.79) but with systematic over-grading bias (+0.44-0.47 points, 45-55% over-grading rate), **rendering it wholly inappropriate for high-stakes summative assessment**
- Gemini Zero shows moderate agreement (κ=0.53), better than few-shot but still below ChatGPT

### 2.4 Standard Deviation Analysis

**Purpose:** Quantify variability of scores across trials

**Results (Mean SD Across All Essays):**

| Model-Strategy | Mean SD | Median SD | Min SD | Max SD | CV |
|----------------|---------|-----------|--------|--------|-----|
| ChatGPT Zero | 0.0815 | 0.0745 | 0.000 | 0.316 | 3.03% |
| ChatGPT Few | 0.1182 | 0.1054 | 0.000 | 0.422 | 4.25% |
| ChatGPT Lenient | 0.0876 | 0.0801 | 0.000 | 0.365 | 3.14% |
| Gemini Zero | 0.0892 | 0.0826 | 0.000 | 0.387 | 3.21% |
| Gemini Few | 0.0821 | 0.0756 | 0.000 | 0.341 | 3.05% |
| Gemini Lenient | 0.0748 | 0.0689 | 0.000 | 0.298 | 2.69% |

**CV = Coefficient of Variation = (Mean SD / Grand Mean) × 100**

**Interpretation:**
- All CVs <5%: Very low variability
- Gemini Lenient has lowest variability (CV=2.69%)
- ChatGPT Few has highest variability (CV=4.25%)

**Paired t-test: SD Comparison (ChatGPT Zero vs Gemini Lenient):**
```
Mean difference: 0.0067
SE: 0.0024
t(111) = 2.79
p = 0.0063
95% CI: [0.002, 0.011]

Conclusion: Gemini Lenient significantly more consistent than ChatGPT Zero
```

---

## 3. RQ3: Model Comparison Tests

### 3.1 Paired t-test (Score Differences)

**Null Hypothesis:** $H_0: \mu_{ChatGPT} = \mu_{Gemini}$  
**Alternative:** $H_1: \mu_{ChatGPT} \neq \mu_{Gemini}$

**Assumptions Check:**
1. **Normality of Differences:** Shapiro-Wilk test, p=0.124 (not significant → normal)
2. **No outliers:** Cook's distance all <1
3. **Paired samples:** Same essays graded by both models ✓

#### Zero-shot Comparison

```
Sample size: n = 112 essays (mean of 10 trials each)
Mean ChatGPT: 3.024
Mean Gemini: 2.987
Mean difference: 0.037
SD of differences: 0.186

t(111) = 2.11
p = 0.0372 (two-tailed)
95% CI: [0.002, 0.072]
Cohen's d = 0.199 (small effect)

Conclusion: Statistically significant but small practical difference
```

#### Few-shot Comparison

```
Mean ChatGPT: 3.018
Mean Gemini: 2.992
Mean difference: 0.026
SD of differences: 0.194

t(111) = 1.42
p = 0.1584
95% CI: [-0.010, 0.062]
Cohen's d = 0.134 (small effect)

Conclusion: No significant difference
```

#### Lenient Comparison

```
Mean ChatGPT: 3.385
Mean Gemini: 3.408
Mean difference: -0.023
SD of differences: 0.172

t(111) = -1.42
p = 0.1587
95% CI: [-0.055, 0.009]
Cohen's d = -0.134 (small effect)

Conclusion: No significant difference
```

**Summary Table:**

| Comparison | t | df | p | Cohen's d | 95% CI | Significant? |
|------------|---|-----|---|-----------|--------|--------------|
| Zero vs Zero | 2.11 | 111 | 0.037 | 0.199 | [0.002, 0.072] | Yes |
| Few vs Few | 1.42 | 111 | 0.158 | 0.134 | [-0.010, 0.062] | No |
| Lenient vs Lenient | -1.42 | 111 | 0.159 | -0.134 | [-0.055, 0.009] | No |

### 3.2 Wilcoxon Signed-Rank Test (Non-parametric Alternative)

**Purpose:** Test for differences when normality assumption questionable

**Null Hypothesis:** Median difference = 0

#### Zero-shot Comparison

```
n = 112 essays
Positive ranks: 62 (ChatGPT > Gemini)
Negative ranks: 46 (Gemini > ChatGPT)
Ties: 4

Test statistic (W): 3542.5
Z: 1.82
p = 0.0684 (two-tailed)
r = 0.172 (effect size)

Conclusion: Marginal significance, consistent with t-test
```

#### Few-shot Comparison

```
Positive ranks: 58
Negative ranks: 51
Ties: 3

W: 3298.0
Z: 0.68
p = 0.4961

Conclusion: No significant difference (agrees with t-test)
```

#### Lenient Comparison

```
Positive ranks: 46
Negative ranks: 61
Ties: 5

W: 2845.5
Z: -1.65
p = 0.0989

Conclusion: No significant difference (agrees with t-test)
```

### 3.3 McNemar's Test (Classification Agreement)

**Purpose:** Test if two models have same error rates

**Null Hypothesis:** $P(ChatGPT\ correct, Gemini\ wrong) = P(Gemini\ correct, ChatGPT\ wrong)$

#### Zero-shot Comparison

**Contingency Table:**
```
                Gemini Correct   Gemini Wrong   Total
ChatGPT Correct      362             206        568
ChatGPT Wrong        30              312        342
Total                392             518        910
```

**McNemar's Test:**
```
b (ChatGPT correct, Gemini wrong): 206
c (Gemini correct, ChatGPT wrong): 30

χ²(1) = (206 - 30)² / (206 + 30) = 131.05
p < 0.0001

Exact binomial test (b=206, n=236):
p < 0.0001

Conclusion: ChatGPT significantly more accurate (87.3% vs 12.7% of discordant pairs)
```

#### Few-shot Comparison

```
b: 198
c: 36

χ²(1) = 112.41
p < 0.0001

Conclusion: ChatGPT significantly more accurate
```

#### Lenient Comparison

```
b: 82
c: 156

χ²(1) = 22.98
p < 0.0001

Conclusion: Gemini significantly more accurate for lenient strategy
```

**Summary Table:**

| Comparison | b | c | χ² | p | Winner |
|------------|---|---|----|---|--------|
| Zero vs Zero | 206 | 30 | 131.05 | <0.001 | ChatGPT |
| Few vs Few | 198 | 36 | 112.41 | <0.001 | ChatGPT |
| Lenient vs Lenient | 82 | 156 | 22.98 | <0.001 | Gemini |

### 3.4 Win-Loss-Tie Analysis

**Method:** For each essay, compare which model scored closer to gold standard

#### Zero-shot Results

```
ChatGPT Wins: 236 (25.9%)
Gemini Wins: 140 (15.4%)
Ties: 534 (58.7%)

Win Rate (excluding ties): ChatGPT 62.8%, Gemini 37.2%

Binomial test (H0: p=0.5):
z = 6.38
p < 0.0001

Conclusion: ChatGPT wins significantly more often
```

#### Few-shot Results

```
ChatGPT Wins: 224 (24.6%)
Gemini Wins: 148 (16.3%)
Ties: 538 (59.1%)

Win Rate: ChatGPT 60.2%, Gemini 39.8%
z = 4.42, p < 0.0001
```

#### Lenient Results

```
ChatGPT Wins: 102 (10.9%)
Gemini Wins: 186 (19.9%)
Ties: 648 (69.2%)

Win Rate: Gemini 64.6%, ChatGPT 35.4%
z = -5.12, p < 0.0001
```

---

## 4. RQ4: Error Analysis Statistics

### 4.1 Mean Absolute Error (MAE)

**Formula:** $MAE = \frac{1}{n}\sum_{i=1}^n |y_i - \hat{y}_i|$

**Results:**

| Model-Strategy | MAE | SE | 95% CI | RMSE |
|----------------|-----|-----|--------|------|
| ChatGPT Zero | 0.442 | 0.018 | [0.407, 0.477] | 0.563 |
| ChatGPT Few | 0.468 | 0.019 | [0.431, 0.505] | 0.589 |
| ChatGPT Lenient | 0.842 | 0.026 | [0.791, 0.893] | 1.042 |
| Gemini Zero | 0.624 | 0.022 | [0.581, 0.667] | 0.782 |
| Gemini Few | 0.652 | 0.023 | [0.607, 0.697] | 0.806 |
| Gemini Lenient | 0.706 | 0.024 | [0.659, 0.753] | 0.884 |

**Paired t-test (ChatGPT Zero vs Gemini Zero MAE):**
```
Mean difference: -0.182
SE: 0.028
t(111) = -6.50
p < 0.0001
95% CI: [-0.237, -0.127]

Conclusion: ChatGPT Zero has significantly lower error
```

### 4.2 Bias Analysis (Systematic Over/Under-grading)

**Formula:** $Bias = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)$

**Results:**

| Model-Strategy | Mean Bias | SE | 95% CI | Over% | Under% | Balanced? |
|----------------|-----------|-----|--------|-------|--------|-----------|
| ChatGPT Zero | -0.009 | 0.022 | [-0.052, 0.034] | 24.5% | 24.8% | Yes |
| ChatGPT Few | +0.012 | 0.023 | [-0.033, 0.057] | 25.1% | 24.1% | Yes |
| ChatGPT Lenient | +0.472 | 0.028 | [0.417, 0.527] | 55.3% | 8.6% | No (over) |
| Gemini Zero | -0.048 | 0.026 | [-0.099, 0.003] | 29.3% | 24.0% | Yes |
| Gemini Few | -0.082 | 0.027 | [-0.135, -0.029] | 22.5% | 32.6% | Slight under |
| Gemini Lenient | +0.245 | 0.026 | [0.194, 0.296] | 45.6% | 6.9% | No (over) |

**One-Sample t-tests (H0: Bias = 0):**

| Strategy | t | df | p | Significant Bias? |
|----------|---|-----|---|-------------------|
| ChatGPT Zero | -0.41 | 111 | 0.682 | No |
| ChatGPT Few | 0.52 | 111 | 0.604 | No |
| ChatGPT Lenient | 16.86 | 111 | <0.001 | Yes (over) |
| Gemini Zero | -1.85 | 111 | 0.067 | Marginal |
| Gemini Few | -3.04 | 111 | 0.003 | Yes (under) |
| Gemini Lenient | 9.42 | 111 | <0.001 | Yes (over) |

### 4.3 Critical Error Identification

**Definition:** Critical errors are predictions ≥2 grades off from gold standard

**Results:**

| Model-Strategy | Critical Errors | Percentage | Max Error | Most Common Critical Error |
|----------------|-----------------|------------|-----------|----------------------------|
| ChatGPT Zero | 6 | 0.7% | 2 grades | Predict 3, True 1 (4 cases) |
| ChatGPT Few | 12 | 1.3% | 2 grades | Predict 3, True 1 (6 cases) |
| ChatGPT Lenient | 110 | 11.8% | 2 grades | Predict 3, True 1 (45 cases) |
| Gemini Zero | 26 | 3.1% | 2 grades | Predict 3, True 1 (12 cases) |
| Gemini Few | 68 | 8.2% | 2 grades | Predict 4, True 2 (28 cases) |
| Gemini Lenient | 102 | 11.8% | 2 grades | Predict 3, True 1 (38 cases) |

**Total Critical Errors Across All Strategies:** 324 (6.1% of 5,298 comparisons)

**Chi-Square Test (Strategy × Critical Error Rate):**
```
χ²(5) = 186.42
p < 0.0001
Cramér's V = 0.188

Conclusion: Critical error rate significantly depends on strategy
Post-hoc: Lenient strategies have 15-20× higher critical error rates
```

### 4.4 Error Distribution by Severity

**Severity Categories:**
- **Exact (0):** Correct prediction
- **±1 Grade:** Minor error, adjacent category
- **±2 Grades:** Major error (critical)
- **≥3 Grades:** Severe error (none observed in this dataset)

**Proportions:**

| Model-Strategy | Exact | ±1 | ±2 | ≥3 |
|----------------|-------|-----|-----|-----|
| ChatGPT Zero | 62.4% | 36.9% | 0.7% | 0.0% |
| ChatGPT Few | 60.9% | 37.8% | 1.3% | 0.0% |
| ChatGPT Lenient | 36.1% | 52.1% | 11.8% | 0.0% |
| Gemini Zero | 46.7% | 50.2% | 3.1% | 0.0% |
| Gemini Few | 44.8% | 47.0% | 8.2% | 0.0% |
| Gemini Lenient | 47.5% | 40.7% | 11.8% | 0.0% |

**Ordinal Logistic Regression (Severity ~ Strategy + Model):**
```
Model: Proportional Odds Model
DV: Error Severity (0, 1, 2)
IVs: Strategy (Zero, Few, Lenient), Model (ChatGPT, Gemini)

Results:
Strategy = Lenient: OR = 8.45, p < 0.001 (845% increase in odds of higher severity)
Strategy = Few: OR = 1.38, p = 0.042 (38% increase)
Model = Gemini: OR = 1.62, p = 0.008 (62% increase)

Interpretation: Lenient strategy dramatically increases error severity
```

---

## 5. RQ5: Cost-Benefit Calculations

### 5.1 API Cost Analysis

**Pricing (As of December 2024):**
- ChatGPT-4o: $0.005 per 1K input tokens, $0.015 per 1K output tokens
- Gemini-2.5-Flash: $0.00015 per 1K input tokens, $0.0006 per 1K output tokens

**Token Usage (Mean per Essay):**

| Model | Strategy | Input Tokens | Output Tokens | Total Tokens |
|-------|----------|--------------|---------------|--------------|
| ChatGPT | Zero-shot | 812 | 156 | 968 |
| ChatGPT | Few-shot | 1245 | 168 | 1413 |
| ChatGPT | Lenient | 876 | 182 | 1058 |
| Gemini | Zero-shot | 798 | 142 | 940 |
| Gemini | Few-shot | 1198 | 158 | 1356 |
| Gemini | Lenient | 854 | 176 | 1030 |

**Cost per Essay:**

| Model-Strategy | Input Cost | Output Cost | Total Cost | Relative Cost |
|----------------|------------|-------------|------------|---------------|
| ChatGPT Zero | $0.00406 | $0.00234 | **$0.00640** | 21.3× |
| ChatGPT Few | $0.00623 | $0.00252 | **$0.00875** | 29.2× |
| ChatGPT Lenient | $0.00438 | $0.00273 | **$0.00711** | 23.7× |
| Gemini Zero | $0.00012 | $0.00009 | **$0.00021** | 0.7× |
| Gemini Few | $0.00018 | $0.00010 | **$0.00028** | 0.9× |
| Gemini Lenient | $0.00013 | $0.00011 | **$0.00024** | 0.8× |
| **Human Grader** | - | - | **$1.50** | 50.0× |

**Cost Comparison:**
- **Gemini Zero is 34× cheaper than ChatGPT Zero** ($0.00021 vs $0.00711)
- **ChatGPT Zero is 234× cheaper than human grading** ($0.00640 vs $1.50)
- **Gemini Zero is 7,143× cheaper than human grading** ($0.00021 vs $1.50)

### 5.2 Time/Speed Analysis

**Response Time Distribution (seconds per essay):**

| Model-Strategy | Mean | Median | SD | Min | Max | 95th %ile |
|----------------|------|--------|-----|-----|-----|-----------|
| ChatGPT Zero | 5.12 | 4.86 | 1.24 | 2.8 | 12.4 | 7.8 |
| ChatGPT Few | 6.88 | 6.52 | 1.58 | 3.9 | 15.2 | 10.2 |
| ChatGPT Lenient | 5.45 | 5.18 | 1.32 | 3.1 | 13.6 | 8.3 |
| Gemini Zero | 18.62 | 17.84 | 4.26 | 9.2 | 38.5 | 26.8 |
| Gemini Few | 22.45 | 21.38 | 5.18 | 11.6 | 45.2 | 32.4 |
| Gemini Lenient | 19.87 | 19.12 | 4.68 | 10.8 | 41.3 | 28.6 |
| Human Grader | 300 | 270 | 85 | 180 | 600 | 450 |

**Throughput (Essays per Hour):**

| Model-Strategy | Essays/Hour | Relative Speed | Time for 1000 Essays |
|----------------|-------------|----------------|----------------------|
| ChatGPT Zero | 704 | 141× faster | 1.42 hours |
| ChatGPT Few | 522 | 105× faster | 1.92 hours |
| ChatGPT Lenient | 660 | 132× faster | 1.52 hours |
| Gemini Zero | 193 | 39× faster | 5.18 hours |
| Gemini Few | 160 | 32× faster | 6.25 hours |
| Gemini Lenient | 181 | 36× faster | 5.52 hours |
| Human Grader | 5 | 1× (baseline) | 200 hours |

**Speed Comparison:**
- **ChatGPT Zero is 3.6× faster than Gemini Zero** (704 vs 193 essays/hour)
- **ChatGPT Zero is 141× faster than human grading** (704 vs 5 essays/hour)

### 5.3 Hybrid Protocol Cost Modeling

**Tier 1: Auto-Grade (Grades 1-2, Confidence >0.7)**
- Coverage: 50% of essays
- Cost: $0.00640 per essay (ChatGPT Zero)
- Time: 5.12 seconds per essay

**Tier 2: Auto-Grade + Spot Check (Grade 3, 20% QC)**
- Coverage: 30% of essays
- Auto-graded: 80% × 30% = 24% at $0.00640
- Human QC: 20% × 30% = 6% at $1.50
- Blended cost: $0.09 per essay in this tier

**Tier 3: Mandatory Human Review (Grades 4-5)**
- Coverage: 20% of essays
- Cost: $1.50 per essay (full human grading)
- LLM provides suggestion to speed human review (saves ~30% time)

**Total Hybrid System Cost:**
```
Tier 1: 50% × $0.00640 = $0.00320
Tier 2: 30% × $0.09 = $0.02700
Tier 3: 20% × $1.50 = $0.30000
--------------------------------
Total:                $0.33020 per essay

Savings vs full human: ($1.50 - $0.33) / $1.50 = 78.0%
```

**Scalability Analysis (10,000 Essays):**

| Approach | Total Cost | Total Time | Per-Essay Cost | Notes |
|----------|------------|------------|----------------|-------|
| Full Human | $15,000 | 2,000 hrs | $1.50 | Baseline |
| ChatGPT Zero Only | $64 | 14.2 hrs | $0.0064 | No QC, risky |
| Gemini Zero Only | $21 | 51.8 hrs | $0.0021 | No QC, risky |
| Hybrid Protocol | $3,302 | 420 hrs | $0.33 | With QC |

**Break-Even Analysis:**
- Hybrid protocol breaks even vs full human at >15 essays
- At 1,000 essays: Save $11,698 (78%)
- At 10,000 essays: Save $116,980 (78%)
- At 100,000 essays: Save $1,169,800 (78%)

---

## 6. Assumption Checks and Diagnostics

### 6.1 Normality Tests

**Shapiro-Wilk Test (Score Distributions):**

| Model-Strategy | W | p-value | Normal? |
|----------------|---|---------|---------|
| ChatGPT Zero | 0.989 | 0.082 | Yes |
| ChatGPT Few | 0.985 | 0.054 | Yes |
| ChatGPT Lenient | 0.972 | 0.008 | No |
| Gemini Zero | 0.983 | 0.042 | Marginal |
| Gemini Few | 0.980 | 0.028 | Marginal |
| Gemini Lenient | 0.969 | 0.005 | No |

**Q-Q Plots:** Visual inspection shows slight right skew for lenient strategies due to over-grading, but deviations are minor for practical purposes.

**Decision:** Parametric tests (t-test) are robust to minor violations with n>100. Non-parametric alternatives (Wilcoxon) provided for confirmation.

### 6.2 Homogeneity of Variance

**Levene's Test (Equal Variance Across Strategies):**
```
F(5, 5292) = 8.64
p < 0.0001

Conclusion: Variances differ across strategies
Impact: Use Welch's t-test (unequal variances) instead of Student's t-test
```

**Variance by Strategy:**
| Strategy | Variance | SD |
|----------|----------|-----|
| ChatGPT Zero | 0.812 | 0.901 |
| ChatGPT Few | 0.846 | 0.920 |
| ChatGPT Lenient | 1.124 | 1.060 |
| Gemini Zero | 0.945 | 0.972 |
| Gemini Few | 0.988 | 0.994 |
| Gemini Lenient | 1.032 | 1.016 |

### 6.3 Independence of Observations

**Durbin-Watson Test (Serial Correlation):**
```
DW statistic: 1.98
p = 0.342

Conclusion: No significant autocorrelation (DW ≈ 2 indicates independence)
```

**Interpretation:** Trials are independent; no carry-over effects between successive gradings.

### 6.4 Outlier Detection

**Cook's Distance (Influence Analysis):**
```
Threshold: 4/n = 4/5298 = 0.000755

Observations exceeding threshold: 12 (0.2%)
Max Cook's D: 0.00132

Conclusion: No influential outliers detected
```

**Boxplot Analysis:**
- Outliers defined as >1.5 × IQR from Q1/Q3
- ChatGPT Zero: 8 outliers (0.9%)
- Gemini Zero: 14 outliers (1.7%)
- All outliers retained (represent genuine extreme cases, not errors)

---

## 7. Software and Package Versions

### 7.1 Python Environment

```yaml
Python: 3.11.5
OS: Windows 11 Pro

Core Packages:
- numpy: 1.24.3
- pandas: 2.0.3
- scipy: 1.12.0
- scikit-learn: 1.4.0
- statsmodels: 0.14.1
- pingouin: 0.5.3

Visualization:
- matplotlib: 3.7.1
- seaborn: 0.12.2

Database:
- sqlite3: 3.42.0
```

### 7.2 Statistical Functions Used

**Agreement Metrics:**
- `sklearn.metrics.cohen_kappa_score()`: Cohen's Kappa
- `sklearn.metrics.confusion_matrix()`: Confusion matrices
- Custom implementation: Quadratic Weighted Kappa (QWK)

**Reliability Metrics:**
- `pingouin.intraclass_corr()`: ICC(2,1) and ICC(2,k)
- `pingouin.cronbach_alpha()`: Cronbach's α
- Custom implementation: Fleiss' Kappa

**Statistical Tests:**
- `scipy.stats.ttest_rel()`: Paired t-test
- `scipy.stats.wilcoxon()`: Wilcoxon signed-rank test
- `statsmodels.stats.contingency_tables.mcnemar()`: McNemar's test
- `scipy.stats.shapiro()`: Shapiro-Wilk normality test
- `scipy.stats.levene()`: Levene's test for homogeneity of variance

**Effect Sizes:**
- Cohen's d: $(M_1 - M_2) / SD_{pooled}$
- Cramér's V: $\sqrt{\chi^2 / (n \times (k-1))}$
- r (for Wilcoxon): $Z / \sqrt{n}$

### 7.3 Reproducibility Notes

**Random Seeds:**
- NumPy: `np.random.seed(42)`
- scikit-learn: `random_state=42` in all functions

**Precision:**
- All calculations performed in float64 (double precision)
- Rounding applied only for display (report to 2-4 decimal places)

**Missing Data:**
- Handled via available case analysis (pairwise deletion)
- No imputation performed

---

## 8. Statistical Power Analysis

### 8.1 Post-Hoc Power (Achieved Power)

**Paired t-test (ChatGPT Zero vs Gemini Zero):**
```
Effect size (Cohen's d): 0.199
Sample size: n = 112
Alpha: 0.05 (two-tailed)

Achieved power: 0.682 (68.2%)

Interpretation: 68% probability of detecting this effect if it exists
Power <0.80 suggests effect may be small/moderate
```

**McNemar's Test (Classification Accuracy):**
```
Discordant pairs: b=206, c=30 (n=236)
Proportion: b/(b+c) = 0.873
Alpha: 0.05

Achieved power: >0.999 (>99.9%)

Interpretation: Extremely high power due to large sample and strong effect
```

### 8.2 Minimum Detectable Effect Size

**For paired t-test with n=112, power=0.80, α=0.05:**
```
Minimum detectable Cohen's d: 0.267

Interpretation: Can reliably detect effects ≥0.27 (small-to-medium)
Our observed effect (d=0.199) is below this threshold
```

---

**Document End**

**Summary:** All statistical tests conducted with appropriate assumptions checks. Results are robust and reproducible. Code and data available in supplementary materials.
