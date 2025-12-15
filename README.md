# 🎓 AES - Automated Essay Scoring System

> Comparative Analysis of Large Language Models (ChatGPT vs Gemini) for Automated Essay Scoring using Multi-Criteria Rubric Assessment

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Research](https://img.shields.io/badge/Status-Research-orange.svg)]()

## 📋 Overview

This research project implements an AI-powered automated essay scoring system that:
- Uses **ChatGPT (GPT-4o)** and **Gemini 2.0 Flash** to grade essays based on multi-criteria rubrics
- Provides **detailed justifications** for each score
- Analyzes **consistency** through 4 independent trials
- Measures **inter-rater agreement** using Fleiss' Kappa
- Compares AI scores with human lecturer ground truth

**Research Goal:** Submit findings to Q1 Scopus journals in educational technology.

## 🎯 Key Features

- ✅ Multi-criteria rubric-based grading (customizable)
- ✅ Weighted scoring system
- ✅ **Justification generation** for each criterion
- ✅ 4x trial consistency analysis
- ✅ Fleiss' Kappa & Cohen's Kappa agreement metrics
- ✅ Comprehensive accuracy metrics (MAE, RMSE, F1-Score)
- ✅ Automated visualization & reporting
- ✅ Export-ready for publication

## 📊 Dataset

- **Students:** 10
- **Questions:** 8 essay questions
- **Total Essays:** 80
- **Trials per Model:** 4
- **Total API Calls:** 640 (320 per model)

## 🏗️ Project Structure

```
AES/
├── config/                    # Configuration files
│   ├── rubrics.json          # Default & custom rubrics
│   └── models_config.yaml    # API settings
├── data/
│   ├── raw/                  # Original data
│   ├── processed/            # Cleaned datasets
│   └── results/              # Experiment results
├── src/
│   ├── agents/               # AI grading agents
│   ├── core/                 # Core logic (rubric, scorer, prompts)
│   ├── experiment/           # Experiment runner & consistency
│   ├── evaluation/           # Metrics & statistical tests
│   └── utils/                # Utilities
├── notebooks/                # Jupyter analysis notebooks
├── tests/                    # Unit tests
└── scripts/                  # Automation scripts
```

## 🚀 Quick Start

### 1. Installation

```powershell
# Clone the repository
git clone <repo-url>
cd AES

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```powershell
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...
```

### 3. Run Experiments

```powershell
# Run pilot test (2-3 essays)
python scripts/run_experiment.py --pilot

# Run full experiment (80 essays)
python scripts/run_experiment.py --full

# Generate report
python scripts/generate_report.py
```

## 📈 Evaluation Metrics

### Consistency Metrics (4 Trials)
- Standard Deviation (SD)
- Coefficient of Variation (CV)
- Intraclass Correlation Coefficient (ICC)
- Range Analysis

### Accuracy Metrics (vs Lecturer)
- Exact Match Accuracy
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Precision, Recall, F1-Score (per grade)
- Confusion Matrix

### Agreement Metrics
- **Fleiss' Kappa** (3 raters: ChatGPT + Gemini + Lecturer)
- Cohen's Kappa (pairwise comparisons)
- Agreement interpretation

### Justification Quality (Optional)
- Semantic similarity between models
- Length & specificity analysis
- Human evaluation scores

## 📝 Example Output

```json
{
  "student_id": "S001",
  "question_id": "Q1",
  "trial": 1,
  "model": "chatgpt",
  "scores": {
    "Pemahaman Konten": {
      "grade": "A",
      "points": 4,
      "justification": "Mahasiswa menunjukkan pemahaman mendalam..."
    },
    "Organisasi & Struktur": {
      "grade": "B",
      "points": 3,
      "justification": "Esai terorganisir dengan baik namun..."
    }
  },
  "weighted_score": 3.7
}
```

## 🧪 Testing

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_agents.py
```

## 📚 Research Questions

1. **RQ1:** How consistent are ChatGPT and Gemini across multiple trials?
2. **RQ2:** What is the accuracy compared to human lecturers?
3. **RQ3:** What is the inter-rater agreement (Fleiss' Kappa)?
4. **RQ4:** Which model is more reliable for automated essay scoring?

## 💰 Cost Estimation

- **ChatGPT (GPT-4):** ~$10-20 for 80 essays × 4 trials
- **Gemini Pro:** ~$0.08 for 80 essays × 4 trials
- **Total:** ~$15 (very affordable!)

## 📖 Documentation

- [Project Plan](PROJECT_PLAN.md) - Detailed methodology & timeline
- [Checklist](CHECKLIST.md) - Implementation task tracking
- [Roadmap](ROADMAP.md) - Visual timeline & milestones
- [API Documentation](docs/API.md) - Code documentation

## 🤝 Contributing

This is a research project. For collaboration inquiries, please contact the authors.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions about the research or methodology, please open an issue.

## 🎓 Citation

If you use this work in your research, please cite:

```bibtex
@article{aes2025,
  title={Comparative Analysis of Large Language Models for Automated Essay Scoring},
  author={[Your Name]},
  journal={[Target Journal]},
  year={2025}
}
```

---

**Status:** Development Phase  
**Target:** Q1 Scopus Journal Publication  
**Timeline:** 18 weeks (4.5 months)
