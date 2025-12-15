# Diagram Alur Penelitian AES - Implementasi Aktual

## Flowchart Alur Penelitian Multi-Baris

```mermaid
flowchart TD
    %% Row 1: Data Preparation
    A["📊 Pengumpulan Data Excel UTS"] --> B["👥 Seleksi Mahasiswa 10 Peserta"]
    B --> C["📋 Pengembangan Rubrik Penilaian"]
    
    %% Row 2: System & Model Setup  
    C --> D["⚙️ Persiapan Sistem Database + API"]
    D --> E["🤖 Implementasi Model ChatGPT + Gemini"]
    E --> F["📝 Pengembangan Strategi Zero/Few/Lenient"]
    
    %% Row 3: Execution & Analysis
    F --> G["⚡ Eksekusi Batch 4,473 Penilaian"]
    G --> H["📊 Analisis Statistik ICC/QWK/Kappa"]
    H --> I["📈 Analisis Perbandingan Performa"]
    
    %% Final Output
    I --> J["📖 Dokumentasi Akhir Skripsi + Publikasi"]
    
    %% Styling untuk readability
    classDef dataPhase fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef systemPhase fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef execPhase fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef analysisPhase fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef outputPhase fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class A,B,C dataPhase
    class D,E,F systemPhase
    class G,H,I execPhase
    class J outputPhase
    
    %% Styling dengan ukuran lebih besar
    classDef dataPrep fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,font-weight:bold
    classDef systemSetup fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,font-weight:bold
    classDef modelWork fill:#e8f5e8,stroke:#388e3c,stroke-width:3px,font-weight:bold
    classDef analysisWork fill:#fff3e0,stroke:#f57c00,stroke-width:3px,font-weight:bold
    classDef finalOutput fill:#fce4ec,stroke:#c2185b,stroke-width:3px,font-weight:bold
    
    class A,B,C dataPrep
    class D,E systemSetup
    class F,G modelWork
    class H,I analysisWork
    class J finalOutput
```

## Detail Implementasi Aktual

### 📊 **Data Preparation**
- **Input**: File Excel `jawaban UTS Capstone Project.xlsx`
- **Mahasiswa**: 16 mahasiswa awal → **10 terpilih** (selected_students.txt)
- **Essays**: **70 esai unik** (10 × 7 pertanyaan)

### 🔧 **System Setup** 
- **Rubrik**: 4 kriteria dengan bobot Content(60%), Organization(20%), Arguments(10%), Language(10%)
- **Scale**: A(4.0), B(3.0), C(2.0), D/E(1.0) + justifikasi detail
- **Database**: SQLite dengan table grading_results + comprehensive logging

### 🤖 **Model Testing**
```
Models & Strategies:
├── ChatGPT-4o
│   ├── Zero-shot: Standard academic prompt
│   ├── Few-shot: 2 contoh penilaian bahasa Indonesia  
│   └── Lenient: "Fokus pada KEKUATAN mahasiswa"
└── Gemini-2.5-Flash
    ├── Zero-shot: Standard academic prompt
    ├── Few-shot: 2 contoh penilaian bahasa Indonesia
    └── Lenient: "Bersikap SUPPORTIF dan POSITIF"
```

### ⚡ **Execution Results**
- **Total Gradings**: **4,473** completed records
- **Success Rate**: **99.7%** (13 API timeouts handled)
- **Duration**: 8 weeks systematic execution
- **Quality**: Comprehensive validation & error handling

### 📈 **Analysis Performed**
- **Reliability**: ICC untuk internal consistency
- **Validity**: QWK comparison vs human gold standard
- **Consistency**: Fleiss κ untuk multi-rater agreement  
- **Performance**: MAE, exact match, correlation analysis

### 📊 **Key Metrics Evaluated**
- **Agreement Analysis**: Cohen's κ, Fleiss κ
- **Classification Performance**: Confusion matrices per model-strategy
- **Cost-Effectiveness**: API costs, processing time, scalability
- **Practical Implications**: Implementation recommendations

### 📖 **Final Outputs**
- **Thesis**: BAB III Metodologi + BAB IV Hasil & Pembahasan
- **Publication**: Journal manuscript Q1-ready
- **Guidelines**: Practical implementation framework untuk institusi