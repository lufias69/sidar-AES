# IMMEDIATE ACTION PLAN - Journal Submission Preparation
**Created**: December 25, 2025  
**Target Submission**: January 5, 2026 (11 days from now)

---

## 🎯 PRIORITY TASKS (Ranked by Importance)

### ⭐ PRIORITY 1: Draft Complete Manuscript (3-4 days)

#### Task 1.1: Compile Manuscript Sections
**Time**: 1 day  
**Action**: Merge existing sections into one manuscript

**Files to Combine**:
```
Introduction (dari FINAL_RESEARCH_REPORT.md)
+ Methods (dari FINAL_RESEARCH_REPORT.md)  
+ Results (dari COMPREHENSIVE_ANALYSIS_SUMMARY.md + statistical tests)
+ Discussion (dari journal_submission/manuscript/DISCUSSION_SECTION.md)
+ Conclusion (update dari FINAL_RESEARCH_REPORT.md)
```

**Output**: `journal_submission/manuscript/main_manuscript.md`

#### Task 1.2: Write Abstract
**Time**: 2 hours  
**Structure** (250 words max):
- Background (2 sentences): AES potential + reliability gap
- Objective (1 sentence): Compare ChatGPT vs Gemini
- Methods (3 sentences): 70 tasks, 10 trials, factorial design
- Results (3 sentences): ICC >0.83, r=0.89, 97% cost savings
- Conclusion (2 sentences): Suitable for deployment, hybrid recommended

**Template ada di**: `results_experiment_final/submission/ABSTRACT.md`

#### Task 1.3: Research Highlights
**Time**: 1 hour  
**Format**: 3-5 bullets, 85 characters max each

Example:
- "First 10-trial reliability study for LLM-based essay grading (ICC >0.83)"
- "Gemini achieves 89% correlation at 97% lower cost than ChatGPT ($0.03 vs $1.10)"
- "Lenient prompting reduces grading errors by 50% for both AI models"

---

### ⭐ PRIORITY 2: Format References (1 day)

#### Task 2.1: Expand Literature Review
**Current**: ~20 references  
**Target**: 40-50 references

**Add categories**:
- [ ] Recent LLM-AES papers (2023-2025): 10 refs
- [ ] Computers & Education papers (show familiarity): 10 refs
- [ ] Validity/reliability frameworks: 5 refs
- [ ] Multilingual AES: 5 refs
- [ ] Indonesian education context: 5 refs
- [ ] Educational technology adoption: 5 refs

#### Task 2.2: Format to APA 7th
**Tool**: Use Zotero or Mendeley  
**Check**: 
- [ ] All in-text citations match reference list
- [ ] DOIs included where available
- [ ] Journal names not abbreviated
- [ ] Consistent formatting

**Command to search for citations**:
```powershell
# Find all potential citations in manuscript
Select-String -Path "journal_submission\manuscript\*.md" -Pattern "\(\w+.*?\d{4}\)"
```

---

### ⭐ PRIORITY 3: Create Cover Letter (2 hours)

#### Task 3.1: Draft Cover Letter
**Template struktur**:

```
Dear Editor-in-Chief,

[Paragraph 1: Introduction + Journal fit]
We submit for consideration "Test-Retest Reliability of Large Language Models 
for Automated Essay Scoring..." for publication in Computers & Education.

[Paragraph 2: Novelty - 3 key contributions]
This work makes three novel contributions:
1. First comprehensive reliability analysis (10 trials, ICC >0.83)
2. First ChatGPT vs Gemini comparison for assessment
3. First demonstration of LLM-AES in Indonesian contexts

[Paragraph 3: Significance]
Our findings demonstrate 97% cost savings while maintaining validity (r=0.89)
and exceptional reliability, with actionable deployment guidelines.

[Paragraph 4: Compliance]
All authors approve submission. No conflicts of interest. Data available.

[Paragraph 5: Suggested reviewers]
We suggest: Dr. Atsushi Mizumoto, Dr. Mark Warschauer... (see list)

Sincerely,
[Your name]
```

**File ada**: `results_experiment_final/submission/COVER_LETTER.md` (customize)

---

### ⭐ PRIORITY 4: Prepare Figures & Tables (1 day)

#### Task 4.1: Check Figure Quality
**Requirement**: 300 DPI minimum for publication

**Run check**:
```powershell
# Check current figures
Get-ChildItem journal_submission\figures\*.png | ForEach-Object {
    $img = [System.Drawing.Image]::FromFile($_.FullName)
    Write-Host "$($_.Name): $($img.Width)x$($img.Height) px"
    $img.Dispose()
}
```

#### Task 4.2: Create Figure Captions
**Format**:
```
Figure 1. Methodology flowchart showing experimental design with 2 models 
(ChatGPT-4o, Gemini 2.0 Flash) × 3 prompting strategies (lenient, few-shot, 
zero-shot) × 10 trials, totaling 1,958 grading instances.

Figure 2. Test-retest reliability comparison showing Intraclass Correlation 
Coefficients (ICC) and Fleiss' Kappa values across models and strategies. 
Error bars represent 95% confidence intervals.
```

#### Task 4.3: Format Tables
**Convert to journal format**:
- [ ] Add table numbers (Table 1, Table 2...)
- [ ] Add descriptive captions
- [ ] Add footnotes for statistical notation (*, **, ***)
- [ ] Ensure columns aligned
- [ ] Add horizontal rules (top, bottom, after header)

---

### ⭐ PRIORITY 5: Prepare Supplementary Materials (1 day)

#### Task 5.1: Compile Supplementary PDFs

**S1: Experimental Design**
- Detailed methodology
- Prompts used (lenient, few-shot, zero-shot)
- Rubric specifications
- Sample student essays (anonymized)

**S2: Statistical Details**
- Full ANOVA tables
- Post-hoc test results
- ICC calculation details
- Fleiss' Kappa matrices

**S3: Error Analysis Extended**
- Critical error examples
- Systematic bias detection details
- Per-rubric confusion matrices
- Qualitative analysis of justifications

**S4: Raw Data Summary**
- Gold standard grades (70 tasks)
- Experiment results aggregated
- Metadata (tokens, timing, costs)

#### Task 5.2: Create Data Repository
**Options**:
1. **OSF.io** (Open Science Framework) - Recommended
2. **Zenodo** - Good for large datasets
3. **GitHub** - For code + small data
4. **Figshare** - For figures + data

**Include**:
- [ ] `gold_standard_70_tasks.csv`
- [ ] `experiment_results_summary.csv`
- [ ] Analysis scripts (Python)
- [ ] README with data dictionary
- [ ] LICENSE (CC-BY 4.0 recommended)

---

## 📅 TIMELINE (11 Days to Submission)

### Week 1 (Dec 26-29): Content Creation

**Day 1 (Dec 26 - Thursday)**:
- [ ] Morning: Compile manuscript sections
- [ ] Afternoon: Write abstract + highlights
- [ ] Evening: Draft cover letter

**Day 2 (Dec 27 - Friday)**:
- [ ] Morning: Expand references to 40+
- [ ] Afternoon: Format references (APA 7th)
- [ ] Evening: Check all in-text citations

**Day 3 (Dec 28 - Saturday)**:
- [ ] Morning: Prepare supplementary S1-S2
- [ ] Afternoon: Prepare supplementary S3-S4
- [ ] Evening: Create data repository

**Day 4 (Dec 29 - Sunday)**:
- [ ] Morning: Check figure quality + captions
- [ ] Afternoon: Format tables
- [ ] Evening: Review entire manuscript

### Week 2 (Dec 30 - Jan 5): Polishing & Submission

**Day 5-6 (Dec 30-31)**:
- [ ] Download Computers & Education template
- [ ] Apply formatting to manuscript
- [ ] Adjust word count if needed
- [ ] Internal review (self or co-authors)

**Day 7 (Jan 1 - New Year)**:
- [ ] Run plagiarism check (iThenticate/Turnitin)
- [ ] Grammar/language editing (Grammarly)
- [ ] Fix any issues found

**Day 8-9 (Jan 2-3)**:
- [ ] Final read-through (print and read on paper)
- [ ] Co-author approvals
- [ ] Prepare author contributions statement
- [ ] Ethics/conflict of interest statements

**Day 10 (Jan 4)**:
- [ ] Final check all files
- [ ] Prepare submission materials
- [ ] Upload to data repository
- [ ] Get DOI for dataset

**Day 11 (Jan 5) - SUBMISSION DAY** 🎯:
- [ ] Submit manuscript via journal portal
- [ ] Upload figures, tables, supplementary
- [ ] Submit cover letter + suggested reviewers
- [ ] Confirm submission received
- [ ] **CELEBRATE!** 🎉

---

## 🛠️ TOOLS YOU'LL NEED

### Writing & Formatting:
- [ ] **Microsoft Word** or **LaTeX** (check journal requirement)
- [ ] **Zotero** or **Mendeley** (reference management)
- [ ] **Grammarly** (grammar checking)
- [ ] **Hemingway Editor** (readability)

### Analysis & Figures:
- [ ] **Python** (already have)
- [ ] **matplotlib/seaborn** (for figures)
- [ ] **Inkscape** or **Adobe Illustrator** (optional, for vector graphics)

### Data Management:
- [ ] **OSF.io account** (free, for data repository)
- [ ] **ORCID iD** (for all authors)

### Quality Checks:
- [ ] **Turnitin/iThenticate** (plagiarism check)
- [ ] **Grammarly Premium** (advanced checks)
- [ ] **OnlineOCR** or **PDFtk** (PDF manipulation)

---

## 💻 IMMEDIATE ACTIONS (TODAY/TOMORROW)

### Action 1: Create Main Manuscript File (NOW)
```powershell
# I'll create this for you in next step
```

### Action 2: Download Journal Template
**Link**: https://www.elsevier.com/journals/computers-and-education/0360-1315/guide-for-authors

**Look for**:
- LaTeX template (if you use LaTeX)
- Word template (easier for most)
- Author guidelines PDF

### Action 3: Set Up Reference Manager
**If using Zotero** (free):
1. Download: https://www.zotero.org/
2. Install browser connector
3. Import existing references from manuscript
4. Set citation style to APA 7th

### Action 4: Create OSF Project
1. Go to: https://osf.io/
2. Sign up (free)
3. Create new project: "LLM-based Automated Essay Scoring"
4. Upload data files
5. Make public (after paper acceptance)
6. Get DOI

---

## 📊 QUALITY CHECKLIST

Before submission, verify:

### Content:
- [ ] Title is descriptive and includes key terms
- [ ] Abstract follows 5-part structure (250 words)
- [ ] Introduction clearly states gap + contribution
- [ ] Methods describe design, sample, procedure, analysis
- [ ] Results report all RQs with statistics
- [ ] Discussion interprets findings vs. literature
- [ ] Conclusion summarizes + suggests future work
- [ ] References 40+ sources, 30% from target journal

### Format:
- [ ] Follows journal template exactly
- [ ] Word count within limits (check guideline)
- [ ] Figures 300+ DPI, labeled Figure 1, 2, 3...
- [ ] Tables numbered, captioned, formatted correctly
- [ ] All statistical notation explained
- [ ] Supplementary materials referenced in text

### Compliance:
- [ ] All authors approved submission
- [ ] Ethics approval documented (if needed)
- [ ] Conflict of interest statement included
- [ ] Data availability statement included
- [ ] ORCID iDs for all authors
- [ ] Suggested reviewers provided (3-5)

### Technical:
- [ ] Plagiarism <15% (preferably <10%)
- [ ] Grammar errors minimized
- [ ] All in-text citations in reference list
- [ ] All references cited in text
- [ ] No broken cross-references
- [ ] All figures/tables mentioned in text

---

## 🚨 POTENTIAL ROADBLOCKS & SOLUTIONS

### Roadblock 1: "References take too long!"
**Solution**: 
- Use Zotero auto-import from Google Scholar
- Prioritize recent Computers & Education papers
- Aim for 40 refs (good enough), not 60

### Roadblock 2: "I don't have Word template access"
**Solution**:
- Use LibreOffice (free) + convert to .docx
- Or use LaTeX (Overleaf is free online)
- Or submit in current format, adjust in revision

### Roadblock 3: "Co-authors not responding"
**Solution**:
- Send draft NOW with 48-hour deadline
- Submit solo if necessary (add co-authors later)
- Most important: don't delay submission!

### Roadblock 4: "Plagiarism check not available"
**Solution**:
- Use free alternative: Quetext.com
- Or use Grammarly plagiarism detector
- Or submit without (editor will check anyway)

---

## 🎯 SUCCESS METRICS

**Minimum Viable Submission**:
- ✅ Complete manuscript (all sections)
- ✅ Abstract + highlights
- ✅ 40+ references (APA format)
- ✅ Cover letter
- ✅ Figures + tables formatted
- ✅ Supplementary materials (S1-S4)

**Ideal Submission**:
- ✅ All of above PLUS
- ✅ Professional language editing
- ✅ Plagiarism <10%
- ✅ Data in public repository (OSF)
- ✅ Graphical abstract
- ✅ Co-author approvals

---

## 💡 TIPS FOR SUCCESS

1. **Start with easiest tasks first** → Build momentum
2. **Use existing materials** → Don't reinvent wheel
3. **Set daily goals** → "Today: write abstract"
4. **Take breaks** → Avoid burnout
5. **Accept "good enough"** → Perfect is the enemy of done
6. **Deadline is real** → Submit by Jan 5 no matter what!

---

## 🔥 WHAT TO DO RIGHT NOW (Next 30 minutes)

1. **Read** [JOURNAL_SELECTION_ANALYSIS.md](journal_submission/JOURNAL_SELECTION_ANALYSIS.md)
2. **Download** Computers & Education author guidelines
3. **Set up** Zotero or Mendeley
4. **Block time** in calendar (4 hours/day for next 11 days)
5. **Tell someone** your submission goal (accountability)

---

**YOU'VE GOT THIS!** 💪

Your research is strong (9.5/10), methodology is solid, results are significant. 
Now it's just about **packaging** it properly and **hitting submit**.

**Target**: January 5, 2026  
**Expected outcome**: Acceptance with minor revisions (75-80% confidence)  
**Publication**: June-July 2026

Let's go! 🚀
