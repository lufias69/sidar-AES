# 🎯 Baseline Analysis - Panduan Lengkap

## Tujuan
Menjalankan **analisis PERTAMA** untuk 1 mahasiswa yang hasilnya akan:
1. Direview oleh **DOSEN**
2. Dikoreksi oleh **DOSEN** 
3. Dijadikan **BASELINE/Gold Standard**
4. Digunakan sebagai pembanding untuk **10 pengujian berikutnya**

---

## Alur Kerja

```
Excel (Data Mentah)
    ↓
AI Grade (ChatGPT + Gemini)
    ↓
File Review untuk Dosen
    ↓
Dosen Review & Koreksi
    ↓
BASELINE (Gold Standard) ✅
    ↓
10 Pengujian Penuh dengan Pembanding
```

---

## 📋 Prerequisites

### 1. Setup API Keys
```powershell
# Edit file .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

### 2. Aktivasi Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 🚀 Cara Menggunakan

### **Opsi 1: Mahasiswa Pertama (Default)**
```powershell
python scripts/baseline_analysis.py
```
Ini akan:
- Grade **Mahasiswa 1** (index 0)
- Menggunakan **ChatGPT + Gemini**
- Generate file review

### **Opsi 2: Mahasiswa Tertentu**
```powershell
# Mahasiswa ke-2
python scripts/baseline_analysis.py --student 1

# Mahasiswa ke-3
python scripts/baseline_analysis.py --student 2
```

### **Opsi 3: Hanya ChatGPT**
```powershell
python scripts/baseline_analysis.py --no-gemini
```

### **Opsi 4: Hanya Gemini (Lebih Murah)**
```powershell
python scripts/baseline_analysis.py --no-chatgpt
```

---

## 📊 Output yang Dihasilkan

### **1. File JSON (Raw Data)**
```
results/baseline/baseline_raw_Mahasiswa 1.json
```
Berisi:
- Data mahasiswa
- Hasil grading lengkap dari ChatGPT & Gemini
- Metadata (timestamp, rubric, dll)

### **2. File Review (Untuk Dosen)**
```
results/baseline/baseline_review_Mahasiswa 1.txt
```
Format:
```
================================================================================
BASELINE ANALYSIS - HASIL UNTUK REVIEW DOSEN
================================================================================

Mahasiswa: Mahasiswa 1
Tanggal Analisis: 2025-12-10 14:30:00
Total Pertanyaan: 7

================================================================================

PERTANYAAN 1
================================================================================

[Pertanyaan]
...

JAWABAN MAHASISWA:
...

--------------------------------------------------------------------------------

[HASIL CHATGPT GPT-4o]
Nilai Akhir: 75.50/100

Penilaian Per Kriteria:

  • Pemahaman Konten: B
    Justifikasi: Mahasiswa menunjukkan pemahaman yang cukup baik...

  • Organisasi & Struktur: C
    Justifikasi: Struktur jawaban agak kacau...

--------------------------------------------------------------------------------

[HASIL GEMINI 2.0 FLASH]
Nilai Akhir: 72.00/100
...

================================================================================
INSTRUKSI UNTUK DOSEN:
================================================================================

1. Review setiap penilaian AI di atas
2. Koreksi jika ada yang tidak sesuai
3. Hasil koreksi → BASELINE
```

---

## 👨‍🏫 Proses Review Dosen

### **Langkah 1: Buka File Review**
```powershell
notepad results/baseline/baseline_review_Mahasiswa*.txt
```

### **Langkah 2: Review Penilaian AI**
Untuk setiap pertanyaan, cek:
- ✅ Apakah grade (A/B/C/D/E) sudah tepat?
- ✅ Apakah justifikasi masuk akal?
- ✅ Apakah nilai akhir sesuai?

### **Langkah 3: Koreksi (Jika Perlu)**
Buat catatan koreksi:
```
KOREKSI DOSEN:

Pertanyaan 1, Pemahaman Konten:
- AI: B → DOSEN: A
- Alasan: Jawaban mahasiswa sebenarnya sudah sangat lengkap dan mendalam

Pertanyaan 2, Organisasi:
- AI: C → DOSEN: B
- Alasan: Struktur cukup baik meskipun ada minor issues

Nilai Akhir Pertanyaan 1: 85/100 (AI: 75.50)
```

### **Langkah 4: Save Koreksi**
Simpan di file terpisah:
```
results/baseline/baseline_corrected_by_dosen.txt
```

---

## 🎯 Next Steps Setelah Review Dosen

1. **Input Koreksi Dosen** → Sistem
2. **Finalisasi Baseline** → Gold Standard
3. **Run 10 Pengujian Penuh**
4. **Bandingkan dengan Baseline**
5. **Hitung Metrik:**
   - Agreement (Fleiss' Kappa)
   - Consistency (ICC, SD, CV)
   - Accuracy (MAE, RMSE, F1)

---

## 💰 Estimasi Biaya

**Untuk 1 Mahasiswa (7 Pertanyaan):**
- ChatGPT (GPT-4o): ~$0.10-0.20
- Gemini 2.0 Flash: ~$0.002
- **Total: ~$0.20** (sangat murah!)

---

## 🔧 Troubleshooting

### Error: "OPENAI_API_KEY not found"
```powershell
# Pastikan .env sudah ada
ls .env

# Pastikan isinya benar
cat .env
# Harus ada:
# OPENAI_API_KEY=sk-...
# GEMINI_API_KEY=...
```

### Error: "openpyxl not installed"
```powershell
pip install openpyxl
```

### Error: File Excel tidak ditemukan
```powershell
# Cek lokasi file
ls "data/Jawaban/jawaban UTS  Capstone Project.xlsx"
```

---

## 📞 Support

Jika ada masalah:
1. Cek log error di console
2. Cek file `logs/` untuk detail
3. Pastikan semua dependencies terinstall: `pip list`

---

## ✅ Checklist

- [ ] API keys sudah dikonfigurasi
- [ ] Virtual environment aktif
- [ ] File Excel tersedia
- [ ] Run baseline analysis
- [ ] File review dihasilkan
- [ ] Dosen review hasil AI
- [ ] Koreksi dosen disimpan
- [ ] Ready untuk 10 pengujian penuh!

---

**Good luck! 🚀**
