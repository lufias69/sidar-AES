# RENCANA PENGERJAAN BAB IV - HASIL DAN PEMBAHASAN

## STRUKTUR LENGKAP BAB IV

### **4.1 Deskripsi Data Penelitian**
**Tujuan:** Gambaran umum dataset dan karakteristik sampel
**Sumber Data:** `results/grading_results.db` + `selected_students.txt`

#### 4.1.1 Karakteristik Sampel
- **Data:** 10 mahasiswa terpilih (student_00 to student_09)
- **Tabel:** Profil mahasiswa (ID, total esai, range grade, dll)
- **Interpretasi:** Representativitas sampel untuk populasi target

#### 4.1.2 Distribusi Data Eksperimen  
- **Data:** 2,369 gradings completed (70 esai × 6 kondisi × multiple trials)
- **Visualisasi:** Bar chart distribusi gradings per kondisi
- **Interpretasi:** Balance eksperimen dan completeness data

#### 4.1.3 Distribusi Grade per Kondisi
- **Data:** Frekuensi A/B/C/D/E per model-strategi combination
- **Visualisasi:** Stacked bar chart grade distribution
- **Interpretasi:** 
  - Apakah ada bias grade tertentu?
  - Pola distribusi normal vs skewed?
  - Konsistensi distribusi across conditions?

---

### **4.2 Analisis Reliabilitas (RQ1)**
**Research Question:** "Seberapa reliable sistem AES dalam pengukuran berulang?"

#### 4.2.1 Intraclass Correlation Coefficient (ICC)
- **Data Source:** Hasil analisis reliability per model-strategi
- **Metrics:** ICC(2,1) per model-strategi
- **Tabel Expected:**
  ```
  | Model-Strategi | ICC | 95% CI | Interpretation |
  |----------------|-----|--------|----------------|
  | ChatGPT Zero   | 0.xx| [a,b]  | Good/Moderate  |
  | ChatGPT Few    | 0.xx| [a,b]  | Good/Moderate  |
  | ...            |     |        |                |
  ```
- **Interpretasi Ilmiah:**
  - ICC > 0.75: "Excellent reliability untuk implementasi praktis"
  - ICC 0.60-0.74: "Good reliability dengan catatan monitoring"  
  - ICC < 0.60: "Poor reliability, perlu improvement model"
  - **Significance Test:** Bootstrap 95% CI, t-test antar model
  - **Practical Implication:** Threshold untuk deployment decision

#### 4.2.2 Internal Consistency (Cronbach's Alpha)
- **Data Source:** Analisis internal consistency rubrik per kondisi
- **Analysis:** Alpha per rubrik criteria (4 kriteria × 6 kondisi)
- **Expected Range:** α = 0.70-0.95 (acceptable untuk research)
- **Interpretasi:**
  - α ≥ 0.90: "Excellent internal consistency"
  - α 0.80-0.89: "Good consistency"
  - α < 0.70: "Questionable, perlu review rubrik"

#### 4.2.3 Reliability Comparison Across Conditions
- **Visualization:** Box plot ICC values per model-strategi
- **Statistical Test:** One-way ANOVA reliability differences
- **Key Finding Expected:** 
  - "ChatGPT Zero-shot menunjukkan reliability tertinggi (ICC=0.xx)"
  - "Lenient strategy menurunkan reliability sebesar X%"

---

### **4.3 Analisis Validitas (RQ2)**  
**Research Question:** "Seberapa valid sistem AES dibanding human expert?"

#### 4.3.1 Criterion Validity (QWK Analysis)
- **Data Source:** Hasil analisis QWK per model-strategi
- **Baseline:** Human expert grades sebagai gold standard
- **Tabel QWK Results:**
  ```
  | Model-Strategi | QWK | SE | p-value | Interpretation |
  |----------------|-----|----|---------| ---------------|
  | ChatGPT Zero   |0.xx |0.xx| < 0.001 | Substantial    |
  | Gemini Few     |0.xx |0.xx| < 0.001 | Moderate       |
  ```
- **Statistical Significance:** Bootstrap confidence intervals
- **Interpretasi Per Level:**
  - κw > 0.61: "Substantial agreement, suitable untuk high-stakes"
  - κw 0.41-0.60: "Moderate agreement, suitable dengan human oversight"
  - κw < 0.40: "Poor agreement, tidak suitable untuk praktis"

#### 4.3.2 Linear Correlation Analysis (Pearson r)
- **Data:** Hasil analisis korelasi AI vs Human per kondisi
- **Scatter plots:** AI vs Human scores per condition
- **Regression lines:** y = ax + b, R² values
- **Interpretasi:**
  - r > 0.80: "Strong linear relationship"
  - 0.60 < r ≤ 0.80: "Moderate relationship"  
  - r ≤ 0.60: "Weak relationship, sistematik bias suspected"

#### 4.3.3 Classification Performance (Confusion Matrix)
- **Data Source:** Confusion matrix results per model-strategi
- **6 Matrices:** Per model-strategi combination
- **Derived Metrics Per Grade:**
  ```
  | Grade | Precision | Recall | F1-Score | Support |
  |-------|-----------|--------|----------|---------|
  | A     | 0.xx      | 0.xx   | 0.xx     | n_A     |
  | B     | 0.xx      | 0.xx   | 0.xx     | n_B     |
  | C     | 0.xx      | 0.xx   | 0.xx     | n_C     |
  | D/E   | 0.xx      | 0.xx   | 0.xx     | n_DE    |
  ```

- **Key Interpretations Expected:**
  - "AI menunjukkan precision tinggi untuk grade ekstrem (A, D/E)"
  - "Confusion terbesar terjadi pada boundary grades (B-C)"
  - "ChatGPT lebih konservatif, Gemini lebih liberal dalam grading"

#### 4.3.4 Error Magnitude Analysis (MAE/RMSE)
- **Data:** Hasil analisis error magnitude per kondisi
- **Per-condition MAE/RMSE values**
- **Statistical significance:** Paired t-test antar conditions
- **Practical Thresholds:**
  - MAE < 0.5: "Excellent accuracy untuk praktis"
  - MAE 0.5-1.0: "Acceptable dengan monitoring"  
  - MAE > 1.0: "Poor accuracy, perlu major improvement"

---

### **4.4 Analisis Konsistensi (RQ3)**
**Research Question:** "Seberapa konsisten sistem AES dalam kondisi berulang?"

#### 4.4.1 Internal Consistency (Coefficient of Variation)
- **Data Source:** Hasil analisis CV per kondisi eksperimen
- **Analysis:** CV per esai, averaged per condition
- **Expected Results Table:**
  ```
  | Model-Strategi | Mean CV | SD CV | Min CV | Max CV | % Consistent (<15%) |
  |----------------|---------|-------|--------|--------|---------------------|
  | ChatGPT Zero   | x.x%    | x.x%  | x.x%   | x.x%   | xx%                 |
  | Gemini Lenient | x.x%    | x.x%  | x.x%   | x.x%   | xx%                 |
  ```

- **Consistency Interpretation:**
  - CV < 10%: "Highly consistent, excellent stability"
  - CV 10-15%: "Acceptable consistency untuk deployment"
  - CV 15-25%: "Moderate consistency, needs monitoring"  
  - CV > 25%: "Poor consistency, unreliable untuk praktis"

#### 4.4.2 Consistency Patterns Analysis  
- **Box plots:** CV distribution per condition
- **Outlier analysis:** Essays dengan CV tinggi (>25%)
- **Content analysis:** Jenis esai apa yang sulit dikonsistenkan?

---

### **4.5 Perbandingan Model dan Strategi (RQ4)**
**Research Question:** "Model dan strategi mana yang superior secara statistik?"

#### 4.5.1 Mixed-Effects ANOVA
- **Data Source:** Hasil analisis ANOVA model perbandingan
- **Model:** Grade ~ Model * Strategy + (1|Essay_ID)  
- **Expected ANOVA Table:**
  ```
  | Source | df | F | p-value | η² | Interpretation |
  |--------|----|----|---------|----| ---------------|
  | Model  | 1  | xx | < 0.001 |0.xx| Large effect   |
  | Strategy| 2 | xx | < 0.001 |0.xx| Medium effect  |
  | Model×Strategy| 2| xx| 0.xxx |0.xx| Small effect   |
  ```

#### 4.5.2 Post-Hoc Analysis (Pairwise Comparisons)  
- **Method:** Tukey HSD dengan Bonferroni correction
- **Expected Results:**
  - "ChatGPT Zero > ChatGPT Few > ChatGPT Lenient (p<0.001)"
  - "Gemini Zero ≈ Gemini Few > Gemini Lenient (p<0.05)"
  - "ChatGPT Zero > Gemini Zero (p<0.001)"

#### 4.5.3 Effect Size Analysis
- **Cohen's d untuk praktical significance**
- **Interpretation guidelines:**
  - d ≥ 0.8: Large difference, practically meaningful
  - 0.5 ≤ d < 0.8: Medium difference  
  - d < 0.5: Small difference, questionable praktical value

---

### **4.6 Analisis Error Patterns (RQ5)**
**Research Question:** "Pola kesalahan apa yang konsisten terjadi?"

#### 4.6.1 Systematic Error Analysis
- **Data:** Hasil analisis pola error sistematis per kondisi
- **Over-grading bias:** Frekuensi AI > Human per condition
- **Under-grading bias:** Frekuensi AI < Human per condition
- **Grade-specific patterns:** Error rate per grade level

#### 4.6.2 Content-Based Error Analysis
- **High-error essays:** Essays dengan MAE > 1.0
- **Content characteristics:** Panjang, kompleksitas, topik
- **Pattern identification:** Jenis konten yang sulit dinilai AI

---

### **4.7 Implementasi Praktis dan Cost-Benefit**
**Derived dari semua analisis di atas**

#### 4.7.1 Performance Summary Dashboard
- **Best performing:** Model-strategi dengan highest validity + reliability
- **Trade-offs:** Speed vs accuracy, consistency vs coverage
- **Recommendation matrix:** Use case → recommended configuration

#### 4.7.2 Deployment Guidelines  
- **High-stakes assessment:** Rekomendasi berdasarkan QWK > 0.61
- **Formative feedback:** Rekomendasi berdasarkan balance efficiency-accuracy  
- **Quality assurance protocols:** Threshold untuk human review

---

## DATA SOURCES MAPPING

### **Data Sources untuk Analisis:**
1. Database eksperimen → Raw data semua experiments
2. Hasil analisis reliability → ICC, QWK analysis results  
3. Hasil analisis consistency → CV analysis results
4. Hasil analisis model comparison → ANOVA results
5. Hasil analisis error patterns → Error patterns, confusion matrices

### **Technical Implementation:**
- Semua scripts analisis data disimpan dalam **LAMPIRAN B: Kode Program**
- BAB IV fokus pada interpretasi hasil, bukan teknis implementasi
- Reference ke lampiran hanya jika diperlukan untuk replikasi

### **Visualization Requirements:**
1. **Grade Distribution:** Stacked bar charts per condition
2. **Reliability Comparison:** Box plots ICC values
3. **Validity Scatter plots:** AI vs Human per condition  
4. **Confusion Matrices:** 6 heatmaps (2×3 grid)
5. **Consistency Trends:** Line plots CV over conditions
6. **Error Patterns:** Histogram error magnitudes

---

## INTERPRETASI GUIDELINES (Ilmiah + Praktis)

### **Statistical Significance + Practical Significance**
- Selalu report p-value + effect size + confidence intervals
- Interpretasi: "Statistically significant (p<0.001) dengan large effect size (d=0.85), menunjukkan perbedaan yang meaningful untuk implementasi praktis"

### **Contextual Interpretation**  
- Bandingkan dengan benchmarks literature AES
- Link ke implications untuk educational assessment
- Discuss limitations dan boundary conditions

### **Actionable Insights**
- Setiap finding berikan rekomendasi konkret
- Trade-off analysis untuk decision makers  
- Implementation roadmap berdasarkan evidence

---

---

## STRUKTUR LAMPIRAN

### **LAMPIRAN A: Hasil Analisis Detail**
- A.1: Tabel lengkap ICC per esai
- A.2: Confusion matrices semua kondisi
- A.3: Raw data distribusi CV
- A.4: ANOVA post-hoc results lengkap

### **LAMPIRAN B: Kode Program dan Scripts**
- B.1: Script analisis deskriptif (`generate_descriptive_stats.py`)
- B.2: Script reliability analysis (`analyze_rq1_reliability_detailed.py`)  
- B.3: Script validity analysis (`analyze_rq1_validity.py`)
- B.4: Script consistency analysis (`analyze_rq2_consistency.py`)
- B.5: Script model comparison (`analyze_rq3_model_comparison.py`)
- B.6: Script error analysis (`analyze_rq4_error_analysis.py`)

### **LAMPIRAN C: Visualisasi Tambahan**
- C.1: Scatter plots semua kondisi
- C.2: Box plots detail per grade
- C.3: Trend analysis over time

---

**TIMELINE PENGERJAAN:**
- Week 1: Section 4.1-4.2 (Descriptive + Reliability)
- Week 2: Section 4.3 (Validity Analysis)  
- Week 3: Section 4.4-4.5 (Consistency + Comparison)
- Week 4: Section 4.6-4.7 (Error Analysis + Implementation)