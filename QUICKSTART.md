# 🚀 Quick Start Guide

## Instalasi & Setup (5 menit)

### 1. Activate Virtual Environment
```powershell
cd E:\project\AES
.\venv\Scripts\Activate.ps1
```

### 2. Setup API Keys
Buat file `.env` dari template:
```powershell
Copy-Item .env.example .env
```

Edit `.env` dan tambahkan API keys:
```
OPENAI_API_KEY=sk-proj-your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

### 3. Test Installation
```powershell
# Test imports
python -c "from src.core.rubric import RubricManager; print('✓ Rubric OK')"
python -c "from src.agents.chatgpt_agent import ChatGPTAgent; print('✓ ChatGPT Agent OK')"
python -c "from src.agents.gemini_agent import GeminiAgent; print('✓ Gemini Agent OK')"
```

---

## Running Your First Experiment (10 menit)

### Option A: Test dengan Example Data

```powershell
# 1. Generate example data
python -c "from src.utils.data_loader import DataLoader; DataLoader().create_example_data()"

# 2. Run pilot test (2-3 essays)
python scripts/run_experiment.py --pilot --models chatgpt
```

### Option B: Test dengan Data Real

```powershell
# 1. Prepare your data files:
# - data/raw/questions.csv
# - data/raw/student_answers.csv
# - data/raw/lecturer_scores.csv (optional)

# 2. Create unified dataset
python -c "from src.utils.data_loader import DataLoader; loader = DataLoader(); questions = loader.load_questions(); answers = loader.load_student_answers(); dataset = loader.create_unified_dataset(questions, answers); loader.save_unified_dataset(dataset)"

# 3. Run pilot
python scripts/run_experiment.py --pilot
```

---

## Running Full Experiment (80 essays)

```powershell
# Both ChatGPT and Gemini, 4 trials each
python scripts/run_experiment.py --full

# Only ChatGPT (cheaper for testing)
python scripts/run_experiment.py --full --models chatgpt

# Only Gemini (very cheap!)
python scripts/run_experiment.py --full --models gemini

# Custom: 10 essays, 2 trials
python scripts/run_experiment.py --essays 10 --trials 2
```

**Estimated Time:**
- 80 essays × 2 models × 4 trials = 640 API calls
- ~5-10 seconds per call
- **Total: 1-2 hours**

**Estimated Cost:**
- ChatGPT (GPT-4o): $5-10 (cheaper than GPT-4 Turbo!)
- Gemini 2.0 Flash: $0.08
- **Total: ~$8**

---

## Viewing Results

### Check Results Directory
```powershell
ls data/results/
```

You should see:
```
chatgpt_trials/
  trial_1.json
  trial_2.json
  trial_3.json
  trial_4.json
gemini_trials/
  trial_1.json
  trial_2.json
  trial_3.json
  trial_4.json
all_results.json
experiment_metadata.json
```

### View Sample Result
```powershell
# View first ChatGPT result
python -c "import json; data = json.load(open('data/results/chatgpt_trials/trial_1.json')); print(json.dumps(data[0], indent=2, ensure_ascii=False))"
```

### View Statistics
```powershell
python -c "import json; meta = json.load(open('data/results/experiment_metadata.json')); print('Duration:', meta['end_time']); print('ChatGPT Stats:', json.dumps(meta['chatgpt_stats'], indent=2))"
```

---

## Understanding the Output

Each result contains:

```json
{
  "student_id": "S001",
  "question_id": "Q1",
  "trial": 1,
  "model": "chatgpt",
  "scores": {
    "Pemahaman Konten": {
      "grade": "A",
      "justification": "Detailed explanation why grade A was given..."
    },
    "Organisasi & Struktur": {
      "grade": "B",
      "justification": "Explanation for grade B..."
    }
  },
  "weighted_score": 3.7,
  "timestamp": "2025-12-10T15:30:45"
}
```

**Key Fields:**
- `grade`: A, B, C, or D/E
- `justification`: 2-4 sentence explanation
- `weighted_score`: Final score (0-4 scale)

---

## Data Preparation Guide

### Format 1: Questions CSV
```csv
question_id,question_text,topic,difficulty
Q1,"Jelaskan konsep AES",AES,Medium
Q2,"Diskusikan AI ethics",Ethics,Hard
```

### Format 2: Student Answers CSV
```csv
student_id,question_id,answer_text
S001,Q1,"Essay text here..."
S001,Q2,"Another essay..."
S002,Q1,"Student 2 essay..."
```

### Format 3: Lecturer Scores CSV (Optional)
```csv
student_id,question_id,Pemahaman_Konten,Organisasi_Struktur,Argumen_Bukti,Gaya_Bahasa
S001,Q1,A,B,B,A
S001,Q2,B,C,C,B
```

**Or simplified format:**
```csv
student_id,question_id,overall_score
S001,Q1,3.7
S001,Q2,2.9
```

---

## Troubleshooting

### Problem: API Key Not Found
```powershell
# Check if .env exists
ls .env

# Check if keys are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI:', 'OK' if os.getenv('OPENAI_API_KEY') else 'NOT FOUND')"
```

### Problem: Import Error
```powershell
# Make sure you're in project root
pwd  # Should show E:\project\AES

# Make sure venv is activated
where python  # Should show ...\AES\venv\Scripts\python.exe
```

### Problem: "File Not Found"
```powershell
# Check data directory
ls data/raw/

# Create example data
python -c "from src.utils.data_loader import DataLoader; DataLoader().create_example_data()"
```

### Problem: API Rate Limit
```
Edit config/models_config.yaml:
  rate_limits:
    chatgpt: 30  # Reduce from 60
    gemini: 30
```

---

## Next Steps After Experiment

### 1. Analyze Consistency (Manual for now)
```python
import json
import pandas as pd

# Load ChatGPT results
results = []
for trial in range(1, 5):
    with open(f'data/results/chatgpt_trials/trial_{trial}.json') as f:
        results.extend(json.load(f))

df = pd.DataFrame(results)
print(df.groupby(['student_id', 'question_id'])['weighted_score'].agg(['mean', 'std']))
```

### 2. Compare with Lecturer Scores
```python
# Load your lecturer scores
lecturer_df = pd.read_csv('data/raw/lecturer_scores.csv')

# Compare (manual for now)
# Will be automated in evaluation metrics module
```

### 3. Calculate Fleiss' Kappa
```python
# Will be implemented in src/evaluation/agreement.py
# For now, use external tools or wait for implementation
```

---

## Tips for Research

### 1. Start Small
- Test with 2-3 essays first
- Validate output format
- Check justification quality
- Estimate costs

### 2. Use Gemini for Testing
- Gemini is 200x cheaper than GPT-4
- Great for testing pipeline
- Use ChatGPT for final results

### 3. Save Everything
- All results are automatically saved
- Checkpoints every 10 essays
- Can resume if interrupted

### 4. Monitor Costs
```powershell
# Check token usage after pilot
python -c "import json; meta = json.load(open('data/results/experiment_metadata.json')); print('Tokens:', meta['chatgpt_stats']['total_tokens'])"

# Estimate cost: tokens * $0.00001 (GPT-4 Turbo)
```

---

## Getting Help

### Test Individual Components
```powershell
# Test rubric
python src/core/rubric.py

# Test prompts
python src/core/prompt_builder.py

# Test ChatGPT (requires API key)
python src/agents/chatgpt_agent.py

# Test data loader
python src/utils/data_loader.py
```

### Check Logs
```powershell
ls logs/
Get-Content logs/aes_*.log | Select-Object -Last 50
```

### Review Documentation
- `README.md` - Overview
- `PROJECT_PLAN.md` - Detailed methodology
- `IMPLEMENTATION_SUMMARY.md` - What's implemented
- `CHECKLIST.md` - Progress tracking

---

## Ready to Go! 🎉

**Minimal working example:**
```powershell
# 1. Activate
.\venv\Scripts\Activate.ps1

# 2. Setup keys in .env
# OPENAI_API_KEY=sk-...
# GOOGLE_API_KEY=...

# 3. Run pilot
python scripts/run_experiment.py --pilot --models gemini

# 4. Check results
ls data/results/
```

**That's it!** Your AES system is ready for research. 🚀
