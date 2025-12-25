# Supplementary Materials

This folder contains additional documentation and materials supporting the main manuscript.

## 📄 Files

### S1: Complete Rubric Specifications
**File**: `S1_Rubric_Complete.md`

Detailed scoring rubric with:
- 4 assessment dimensions (Content, Organization, Arguments, Language)
- 5-point scale for each dimension (0-4)
- Complete criteria for each score level
- Weighting formula (Content 40%, Org 30%, Args 20%, Lang 10%)
- Grade conversion table (A: 3.50-4.00, B: 2.50-3.49, etc.)
- Example scored essays

---

### S2: AI Prompts and Configuration
**File**: `S2_Prompts_Complete.md`

Full text of all prompts used:

1. **Lenient Prompt** (~400 words):
   - Rubric embedded in system message
   - JSON output format specified
   - Justification requirement
   - Temperature: 0.3

2. **Few-Shot Prompt** (~800 words):
   - Includes 3 example essays with expert grades
   - Demonstrates scoring process
   - Shows justification format

3. **Zero-Shot Prompt** (~200 words):
   - Minimal instruction
   - Basic rubric reference
   - No examples provided

**API Configuration**:
```json
{
  "model": "gpt-4-turbo-preview / gemini-1.5-pro",
  "temperature": 0.3,
  "response_format": {"type": "json_object"},
  "max_tokens": 2048
}
```

---

### S3: Statistical Analysis Details
**File**: `S3_Statistical_Tables.md`

Complete statistical results:

**Table S1: ANOVA Results**
- Effect of model on accuracy: F(1,68)=12.45, p<.001, η²=0.155
- Effect of strategy on accuracy: F(2,68)=8.73, p<.001, η²=0.204
- Interaction: F(2,68)=1.92, p=.154, η²=0.053

**Table S2: Post-hoc Comparisons (Bonferroni)**
- Lenient vs Few-shot: t=3.21, p=.006, d=0.76
- Lenient vs Zero-shot: t=4.87, p<.001, d=1.15
- Few-shot vs Zero-shot: t=2.12, p=.112, d=0.50

**Table S3: ICC Confidence Intervals**
- ChatGPT lenient: ICC=0.942 [95% CI: 0.891, 0.971]
- ChatGPT few-shot: ICC=0.896 [95% CI: 0.812, 0.948]
- Gemini lenient: ICC=0.914 [95% CI: 0.849, 0.958]
- Gemini few-shot: ICC=0.874 [95% CI: 0.772, 0.936]

**Table S4: Fleiss' Kappa by Dimension**
| Dimension | Lenient | Few-shot | Zero-shot |
|-----------|---------|----------|-----------|
| Content | 0.72 | 0.68 | 0.42 |
| Organization | 0.65 | 0.61 | 0.38 |
| Arguments | 0.59 | 0.54 | 0.35 |
| Language | 0.81 | 0.76 | 0.51 |

---

### S4: Error Analysis Examples
**File**: `S4_Error_Examples.md`

**Example 1: Critical Error (ChatGPT Zero-shot)**
- **Essay**: Student 3, Question 5 (Critical thinking)
- **Expert Grade**: C (2.85/4.00)
- **AI Grade**: A (3.75/4.00)
- **Error**: +0.90 points (32% overestimate)
- **AI Justification**: "Comprehensive analysis with strong evidence..."
- **Expert Comment**: "Surface-level discussion, lacks depth, missing counterarguments"
- **Root Cause**: AI misinterpreted verbosity for quality

**Example 2: Systematic Undergrading (Gemini Few-shot)**
- **Pattern**: Question 2 (Argumentation) consistently -0.15 to -0.25 points
- **Affected**: 8 out of 10 students
- **Dimension**: Arguments & Evidence (20% weight)
- **Hypothesis**: Few-shot examples set high standard, AI became conservative

**Example 3: Adjacent Error (ChatGPT Lenient)**
- **Essay**: Student 7, Question 4
- **Expert Grade**: B (3.15/4.00)
- **AI Grade**: C (2.95/4.00)
- **Error**: -0.20 points (boundary case)
- **Analysis**: Both grades valid, essay at B/C boundary (3.00 cutoff)

---

## 🔍 Usage

### For Researchers
Use these materials to:
- Replicate the study with different models
- Adapt prompts for your language/context
- Compare results with your own experiments

### For Educators
Use these materials to:
- Design AI-assisted grading for your courses
- Understand prompt engineering for assessment
- Train faculty on AI limitations

### For Developers
Use these materials to:
- Build custom AES systems
- Benchmark new models
- Improve prompt design

---

## 📝 Notes

**File Formats**:
- All files provided in Markdown (.md) for easy viewing
- Can be converted to PDF using Pandoc:
  ```bash
  pandoc S1_Rubric_Complete.md -o S1_Rubric_Complete.pdf
  ```

**Ethical Considerations**:
- Student essay content **NOT included** (privacy protection)
- Only grades and metadata shared
- Anonymous IDs used throughout

**Future Additions**:
- Complete confusion matrices (all 6 conditions)
- Per-student performance profiles
- Dimension-level error analysis
- Prompt optimization experiments

---

## 📧 Contact

For access to additional materials (subject to ethical approval):
- Corresponding Author: [email]
- Ethics clearance: [IRB reference]

---

*Last updated: December 25, 2025*

*Note: Files S1-S4 are placeholders in this initial release. Complete supplementary materials will be added in OSF v1.1 (planned: January 2026).*
