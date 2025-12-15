# Sistem Eksperimen dengan Checkpoint/Resume

## ✨ Fitur Baru

### 1. **Database SQLite dengan Checkpoint**
- Semua hasil penilaian disimpan di database
- Otomatis resume jika proses crash/berhenti
- Tidak perlu mengulangi dari awal

### 2. **6 Strategi Prompting**
- `zero-shot`: Prompt standar tanpa contoh
- `few-shot`: Dengan 2 contoh penilaian
- `cot` (Chain-of-Thought): Instruksi berpikir step-by-step
- `detailed-rubric`: Rubrik super detail per kriteria
- `strict`: Mode penilaian ketat/galak
- `lenient`: Mode penilaian longgar/baik hati

### 3. **Progress Monitoring**
- Real-time progress tracking
- Statistik lengkap per eksperimen
- Error logging otomatis

---

## 📁 File-File Baru

### Database & Core
```
src/database/
├── __init__.py
└── db_manager.py          # Manager untuk SQLite operations
```

### Scripts
```
scripts/
├── run_experiment.py       # Run 1 eksperimen (NEW VERSION)
├── run_all_experiments.py  # Run semua 10 eksperimen
├── db_status.py            # Monitor progress & statistics
└── export_to_json.py       # Export database → JSON files
```

### Updated Files
```
src/core/prompt_builder.py  # Tambah support 6 strategies
src/agents/base_agent.py    # Pass strategy ke PromptBuilder
src/agents/chatgpt_agent.py # Tambah parameter strategy
src/agents/gemini_agent.py  # Tambah parameter strategy
```

---

## 🚀 Cara Penggunaan

### **A. Run 1 Eksperimen**

```powershell
# Zero-shot dengan ChatGPT
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt --trials 4

# Few-shot dengan Gemini
python scripts/run_experiment.py --experiment_id exp_03 --strategy few-shot --model gemini --trials 4

# Chain-of-Thought dengan ChatGPT
python scripts/run_experiment.py --experiment_id exp_05 --strategy cot --model chatgpt --trials 4

# Resume dari checkpoint (jika crash)
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt --resume
```

**Parameter:**
- `--experiment_id`: ID unik (exp_01, exp_02, ...)
- `--strategy`: Pilih: `zero-shot`, `few-shot`, `cot`, `detailed-rubric`, `strict`, `lenient`
- `--model`: Pilih: `chatgpt` atau `gemini`
- `--trials`: Jumlah trial (default: 4)
- `--language`: `indonesian` atau `english` (default: indonesian)
- `--resume`: Flag untuk resume dari checkpoint

---

### **B. Run Semua 10 Eksperimen**

```powershell
# Run semua dari awal
python scripts/run_all_experiments.py

# Mulai dari eksperimen ke-3
python scripts/run_all_experiments.py --start 3

# Run hanya eksperimen tertentu (misal: 1, 5, 9)
python scripts/run_all_experiments.py --only 1 5 9
```

**10 Eksperimen yang Akan Dijalankan:**
1. `exp_01`: Zero-shot + ChatGPT
2. `exp_02`: Zero-shot + Gemini
3. `exp_03`: Few-shot + ChatGPT
4. `exp_04`: Few-shot + Gemini
5. `exp_05`: Chain-of-Thought + ChatGPT
6. `exp_06`: Chain-of-Thought + Gemini
7. `exp_07`: Detailed Rubric + ChatGPT
8. `exp_08`: Detailed Rubric + Gemini
9. `exp_09`: Strict Mode + ChatGPT
10. `exp_10`: Lenient Mode + ChatGPT

**Estimasi:**
- Total tasks: 2,800 penilaian (10 × 280)
- Waktu: ~12-15 jam
- Biaya: ~$80-100

---

### **C. Monitor Progress**

```powershell
# Lihat semua eksperimen
python scripts/db_status.py

# Detail eksperimen tertentu
python scripts/db_status.py --experiment exp_01

# Lihat task yang gagal
python scripts/db_status.py --experiment exp_01 --failed

# Reset task yang gagal (untuk retry)
python scripts/db_status.py --experiment exp_01 --reset-failed
```

**Output Contoh:**
```
================================================================================
EXPERIMENT: exp_01
================================================================================

Overall Progress:
  Total tasks:     280
  Completed:       150 (53.6%)
  Failed:          5
  Processing:      0
  Pending:         125

Performance:
  Avg tokens/task: 1250
  Total tokens:    187,500
  Avg time/task:   2.3s

Progress by Trial:
┌─────────┬───────────┬───────┬──────────┐
│ Trial   │ Completed │ Total │ Progress │
├─────────┼───────────┼───────┼──────────┤
│ Trial 1 │ 70        │ 70    │ 100.0%   │
│ Trial 2 │ 70        │ 70    │ 100.0%   │
│ Trial 3 │ 10        │ 70    │ 14.3%    │
│ Trial 4 │ 0         │ 70    │ 0.0%     │
└─────────┴───────────┴───────┴──────────┘
```

---

### **D. Export ke JSON**

```powershell
# Export semua trial dari exp_01
python scripts/export_to_json.py --experiment exp_01

# Export trial tertentu
python scripts/export_to_json.py --experiment exp_01 --trial 1

# Export ke direktori custom
python scripts/export_to_json.py --experiment exp_01 --output results/my_custom_dir
```

**Output:**
```
results/experiments/exp_01/
├── trial_1/
│   ├── student_00_Mahasiswa_1_trial1.json
│   ├── student_01_Mahasiswa_2_trial1.json
│   └── ...
├── trial_2/
│   └── ...
└── ...
```

---

## 🔄 Skenario Penggunaan

### **Skenario 1: Proses Crash di Tengah Jalan**

```powershell
# Mulai eksperimen
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt

# ❌ Crash setelah 150/280 tasks...

# ✅ Resume otomatis
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt --resume

# Akan lanjut dari task ke-151!
```

### **Skenario 2: Cek Progress Sebelum Tidur**

```powershell
# Jalankan semua eksperimen
python scripts/run_all_experiments.py

# (Biarkan running 2 jam, lalu cek)
python scripts/db_status.py

# Output:
# exp_01: 280/280 (100%) ✓
# exp_02: 150/280 (53.6%)
# exp_03: 0/280 (0%)
# ...
```

### **Skenario 3: Ada Task yang Gagal**

```powershell
# Cek task yang gagal
python scripts/db_status.py --experiment exp_01 --failed

# Output:
# Trial 2 | student_05 | Q3
#   Error: API rate limit exceeded
# Trial 3 | student_02 | Q1
#   Error: Invalid JSON response

# Reset dan retry
python scripts/db_status.py --experiment exp_01 --reset-failed
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt --resume
```

---

## 📊 Database Schema

```sql
CREATE TABLE grading_results (
    id INTEGER PRIMARY KEY,
    experiment_id TEXT,      -- 'exp_01', 'exp_02', ...
    trial_number INTEGER,    -- 1, 2, 3, 4
    student_id TEXT,         -- 'student_00', 'student_01', ...
    student_name TEXT,       -- 'Mahasiswa 1', ...
    question_number INTEGER, -- 1-7
    question_text TEXT,
    answer_text TEXT,
    model TEXT,              -- 'chatgpt', 'gemini'
    strategy TEXT,           -- 'zero-shot', 'few-shot', ...
    grades JSON,             -- {"Pemahaman Konten": "A", ...}
    weighted_score REAL,
    justification TEXT,
    overall_comment TEXT,
    tokens_used INTEGER,
    api_call_time REAL,
    timestamp DATETIME,
    status TEXT,             -- 'pending', 'completed', 'failed'
    error_message TEXT,
    UNIQUE(experiment_id, trial_number, student_id, question_number)
)
```

**Status Values:**
- `pending`: Belum diproses
- `processing`: Sedang diproses
- `completed`: Berhasil
- `failed`: Gagal (ada error)

---

## ⚙️ Konfigurasi Strategi

### **1. Zero-Shot (Baseline)**
- Prompt standar tanpa tambahan
- Tidak ada contoh
- Untuk baseline comparison

### **2. Few-Shot**
- Tambah 2 contoh penilaian:
  - Contoh jawaban BAIK → nilai B
  - Contoh jawaban BURUK → nilai D/E
- AI belajar dari contoh

### **3. Chain-of-Thought (CoT)**
- Instruksi berpikir step-by-step:
  1. BACA poin utama
  2. BANDINGKAN dengan rubrik
  3. EVALUASI kekuatan/kelemahan
  4. PUTUSKAN nilai
  5. JUSTIFIKASI reasoning
- AI lebih teliti

### **4. Detailed Rubric**
- Rubrik SUPER detail per kriteria
- Contoh untuk A, B, C, D/E dijelaskan lengkap
- Misal untuk "Pemahaman Konten":
  - A: minimal 5 kalimat, detail teknis, dll
  - B: 3-4 kalimat, cukup jelas, dll
  - C: 2-3 kalimat, superfisial, dll
  - D/E: < 2 kalimat, tidak relevan

### **5. Strict Mode**
- Instruksi: "Nilai dengan SANGAT KETAT"
- Fokus pada KELEMAHAN
- Hanya kasih A jika SEMPURNA
- Test apakah AI terlalu generous

### **6. Lenient Mode**
- Instruksi: "Nilai dengan SUPPORTIF"
- Fokus pada KEKUATAN
- Apresiasi usaha mahasiswa
- Hanya kasih D/E jika tidak ada usaha
- Test bias dari sisi lain

---

## 🎯 Workflow Lengkap

```
┌─────────────────────────────────────────────┐
│  1. SETUP                                   │
│     - Gold standard sudah ada ✓             │
│     - 10 mahasiswa × 7 soal                 │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  2. RUN EXPERIMENTS                         │
│     python scripts/run_all_experiments.py   │
│     - 10 eksperimen × 4 trial each          │
│     - Otomatis save ke database             │
│     - Auto-resume jika crash                │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  3. MONITOR PROGRESS                        │
│     python scripts/db_status.py             │
│     - Cek berapa % selesai                  │
│     - Lihat statistik                       │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  4. EXPORT RESULTS                          │
│     python scripts/export_to_json.py        │
│     - Convert database → JSON               │
│     - Untuk compatibility dengan scripts    │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  5. ANALYSIS (TODO - Next Phase)            │
│     - Calculate metrics                     │
│     - Compare with gold standard            │
│     - Generate visualizations               │
│     - Create LaTeX tables                   │
└─────────────────────────────────────────────┘
```

---

## 🛡️ Error Handling

### **Automatic Retry**
- API error → Auto retry 3× dengan delay
- Rate limit → Exponential backoff
- Timeout → Retry dengan timeout lebih lama

### **Error Logging**
- Semua error disimpan di database
- Bisa cek dengan `--failed` flag
- Bisa reset dengan `--reset-failed`

### **Status Tracking**
- `pending`: Siap diproses
- `processing`: Sedang jalan
- `completed`: Sukses ✓
- `failed`: Ada error ✗

---

## 📝 Tips & Best Practices

### **1. Mulai dengan Test Run**
```powershell
# Test 1 eksperimen dulu (trial 1 saja)
python scripts/run_experiment.py --experiment_id test_01 --strategy zero-shot --model chatgpt --trials 1
```

### **2. Monitor Secara Berkala**
```powershell
# Cek progress setiap 1-2 jam
python scripts/db_status.py
```

### **3. Backup Database**
```powershell
# Copy database sebelum run eksperimen besar
cp results/grading_results.db results/grading_results.backup.db
```

### **4. Export Hasil Secara Berkala**
```powershell
# Export setiap eksperimen selesai
python scripts/export_to_json.py --experiment exp_01
```

### **5. Cek Failed Tasks**
```powershell
# Setelah selesai, cek ada yang gagal atau tidak
python scripts/db_status.py --experiment exp_01 --failed
```

---

## 🆘 Troubleshooting

### **Q: Experiment tidak resume setelah crash?**
A: Pastikan gunakan `--resume` flag dan `--experiment_id` yang sama

### **Q: Terlalu banyak task yang failed?**
A: Cek error dengan `--failed`, kemungkinan API issue atau rate limit

### **Q: Database corrupt?**
A: Restore dari backup, atau hapus dan mulai lagi (data hilang!)

### **Q: Ingin clear/reset eksperimen?**
A: Belum ada command, manual: hapus rows di database atau hapus file `.db`

---

## 📦 Dependencies Baru

Tambahan di `requirements.txt`:
```
tqdm>=4.66.0        # Progress bar
tabulate>=0.9.0     # Table formatting untuk db_status
```

Install:
```powershell
pip install tqdm tabulate
```

---

## 🔜 Next Steps

Setelah semua eksperimen selesai:

1. **Evaluation**
   - Calculate Agreement with gold standard
   - Calculate Consistency across trials
   - Calculate Accuracy metrics
   - Statistical significance tests

2. **Visualization**
   - Heatmaps
   - Box plots
   - Scatter plots
   - Comparison charts

3. **Reporting**
   - Generate LaTeX tables
   - Create final report
   - Export for paper

---

## 📞 Quick Reference

```powershell
# Run 1 experiment
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt

# Run all 10 experiments
python scripts/run_all_experiments.py

# Check progress
python scripts/db_status.py

# Check specific experiment
python scripts/db_status.py --experiment exp_01

# Check failed tasks
python scripts/db_status.py --experiment exp_01 --failed

# Reset failed tasks
python scripts/db_status.py --experiment exp_01 --reset-failed

# Resume from checkpoint
python scripts/run_experiment.py --experiment_id exp_01 --strategy zero-shot --model chatgpt --resume

# Export to JSON
python scripts/export_to_json.py --experiment exp_01
```

---

**🎉 Sistem siap digunakan!**

Sekarang Anda bisa menjalankan eksperimen dengan aman tanpa takut data hilang jika crash di tengah jalan.
