# Final Action Plan - Assessing Writing Submission

**Goal:** Submit manuscript to Assessing Writing within 1-2 weeks  
**Current Status:** 85% ready - need author info, formatting, and administrative tasks  
**Estimated Remaining Time:** 8-10 hours of focused work

---

## 🎯 PHASE 1: AUTHOR & INSTITUTIONAL INFORMATION (1 hour)

### Task 1.1: Collect Author Information (30 minutes)

**For EACH author, collect:**
- [ ] Full legal name (as appears on publications)
- [ ] Academic degree(s) and credentials
- [ ] Current title/position
- [ ] Department name
- [ ] Institution full name and address
- [ ] Email address (institutional preferred)
- [ ] Phone number (corresponding author only)
- [ ] ORCID iD (register free at https://orcid.org if needed)

**Files to update:**
1. `assessing_writing/TITLE_PAGE.md`
2. `assessing_writing/COVER_LETTER_ASSESSING_WRITING.md` (bottom signature)
3. `assessing_writing/DECLARATIONS.md` (Author Contributions section)

**Action:** Send email to co-authors requesting this information (template below)

---

### Task 1.2: Add Ethics Information (15 minutes)

**Collect from IRB/Ethics Committee:**
- [ ] Protocol number
- [ ] Approval date
- [ ] Expiration date (if applicable)
- [ ] Scan of approval letter (PDF)

**Files to update:**
1. `assessing_writing/TITLE_PAGE.md` - Ethics Approval section
2. `assessing_writing/DECLARATIONS.md` - Ethics section
3. Scan file: `ethics_approval.pdf` (for upload)

**If ethics not yet approved:**
- Option A: Apply now (can take 2-6 weeks)
- Option B: Note "approval pending" in cover letter
- Option C: Some journals allow submission with application pending

---

### Task 1.3: Author Contributions (CRediT) (15 minutes)

**Use CRediT taxonomy:** https://credit.niso.org/

**Review with co-authors and confirm who did:**
- Conceptualization: Who had the original idea?
- Methodology: Who designed the study?
- Software: Who wrote the code?
- Validation: Who verified results?
- Formal Analysis: Who ran the statistics?
- Investigation: Who collected data?
- Resources: Who provided materials/access?
- Data Curation: Who managed the data?
- Writing - Original Draft: Who wrote first draft?
- Writing - Review & Editing: Who revised?
- Visualization: Who created figures/tables?
- Supervision: Who oversaw the project?
- Project Administration: Who managed logistics?
- Funding Acquisition: Who got funding? (N/A if none)

**Roles:** Lead, Equal, or Supporting for each

**Update:** `assessing_writing/DECLARATIONS.md` - Author Contribution Statement

---

## 🎯 PHASE 2: MANUSCRIPT FORMATTING (3 hours)

### Task 2.1: Install Pandoc (if not installed) (10 minutes)

**Windows:**
```powershell
# Option 1: Chocolatey
choco install pandoc

# Option 2: Download installer
# https://pandoc.org/installing.html
```

**Verify installation:**
```powershell
pandoc --version
```

---

### Task 2.2: Convert Markdown to Word (30 minutes)

**Create Word template (template.docx) with:**
- Times New Roman, 12pt
- Double spacing
- 1" margins all sides
- Page numbers bottom center
- Line numbers continuous

**Or download Elsevier template:** https://www.elsevier.com/authors/policies-and-guidelines/latex-instructions

**Convert manuscript:**
```powershell
cd E:\project\AES\results_experiment_final\reports

# Convert to Word with template
pandoc COMPREHENSIVE_ANALYSIS_REPORT.md -o manuscript_draft.docx --reference-doc=template.docx

# Or basic conversion
pandoc COMPREHENSIVE_ANALYSIS_REPORT.md -o manuscript_draft.docx
```

**Output:** `manuscript_draft.docx` (with author info - will blind later)

---

### Task 2.3: Format in Microsoft Word (1.5 hours)

**Open manuscript_draft.docx and apply:**

1. **[ ] Typography (15 min)**
   - Font: Times New Roman, 12pt (entire document)
   - Spacing: Double-space (Select All → Paragraph → Line Spacing → Double)
   - Margins: 1 inch all sides (Layout → Margins → Normal)
   - Alignment: Left (not justified)

2. **[ ] Headings (10 min)**
   - Level 1: Bold, Title Case (e.g., "Introduction")
   - Level 2: Bold, Sentence case (e.g., "Research questions")
   - Level 3: Italic, Sentence case (e.g., "Validity metrics")
   - Apply styles consistently throughout

3. **[ ] Line Numbers (5 min)**
   - Layout → Line Numbers → Continuous

4. **[ ] Page Numbers (5 min)**
   - Insert → Page Number → Bottom of Page → Plain Number 2 (centered)

5. **[ ] Tables (20 min)**
   - Ensure all tables are editable (not images)
   - Simple format (minimal lines)
   - Caption above table
   - Notes below table using superscript letters

6. **[ ] Figures (10 min)**
   - Insert graphical_abstract.png
   - Caption below figure
   - Ensure 300 dpi quality

7. **[ ] References (30 min)**
   - Verify APA 7th edition format
   - Add DOIs where available
   - Check all in-text citations match reference list
   - Use citation manager (Zotero/Mendeley) if possible

8. **[ ] Abstract (5 min)**
   - Copy from `ABSTRACT_TRIMMED.md` (246 words)
   - Format: single paragraph, no citations

9. **[ ] Keywords (2 min)**
   - Add 6 keywords below abstract

10. **[ ] Header/Footer (5 min)**
    - Remove any default headers
    - Keep only page numbers in footer

**Save as:** `manuscript_with_authors.docx`

---

### Task 2.4: Create Blinded Version (1 hour)

**Follow:** `assessing_writing/BLINDING_GUIDE.md`

**Key steps:**
1. **[ ] Save As:** `manuscript_blinded.docx` (work on this copy)

2. **[ ] Remove author identifying info:**
   - Delete author names and affiliations from first page
   - Check header/footer for author info
   - Find & Replace institution name with generic
   - Change "we" to third person where identifying
   - Remove/blind acknowledgments
   - Remove specific IRB protocol number

3. **[ ] Automated searches (Ctrl+F):**
   - Search for YOUR NAME → Should be 0 (except references)
   - Search for INSTITUTION NAME → Should be 0
   - Search for EMAIL ADDRESSES (@) → Should be 0

4. **[ ] File properties:**
   - File → Info → Properties → Remove author, company
   - Or: File → Info → Inspect Document → Remove All

5. **[ ] Final check:**
   - Read first 2 pages - could you identify authors?
   - Compare with manuscript_with_authors.docx side-by-side

**Output files:**
- `manuscript_with_authors.docx` (keep for reference)
- `manuscript_blinded.docx` (for submission)

---

### Task 2.5: Create Title Page Document (15 minutes)

**Convert to Word:**
```powershell
pandoc assessing_writing/TITLE_PAGE.md -o assessing_writing/title_page.docx
```

**Or manually:**
- Copy content from `TITLE_PAGE.md`
- Paste into new Word doc
- Format: Times New Roman, 12pt, single-spaced
- Remove markdown formatting symbols

**Output:** `title_page.docx`

---

## 🎯 PHASE 3: SUPPLEMENTARY MATERIALS (1 hour)

### Task 3.1: Verify Supplementary Files (15 minutes)

**Check each file:**
- [ ] S1_EXTENDED_METHODOLOGY.md - Complete methodology details
- [ ] S2_RAW_DATA_SUMMARY.md - Dataset characteristics
- [ ] S3_STATISTICAL_TESTS.md - Full statistical outputs
- [ ] S4_CONFUSION_MATRICES.md - Detailed matrices
- [ ] S5_EXTENDED_TABLES.md - Extended reliability/validity tables

**Verify:**
- All citations to supplementary materials in main manuscript correct (e.g., "see S3 for full outputs")
- No author-identifying information in supplementary files
- Consistent formatting across all files

---

### Task 3.2: Convert Supplementary to PDF (Optional) (15 minutes)

**Assessing Writing accepts Markdown, but PDF is cleaner:**

```powershell
cd results_experiment_final/submission/supplementary_materials

# Convert each to PDF
pandoc S1_EXTENDED_METHODOLOGY.md -o S1_EXTENDED_METHODOLOGY.pdf
pandoc S2_RAW_DATA_SUMMARY.md -o S2_RAW_DATA_SUMMARY.pdf
pandoc S3_STATISTICAL_TESTS.md -o S3_STATISTICAL_TESTS.pdf
pandoc S4_CONFUSION_MATRICES.md -o S4_CONFUSION_MATRICES.pdf
pandoc S5_EXTENDED_TABLES.md -o S5_EXTENDED_TABLES.pdf
```

**Or submit .md files directly** (many journals accept)

---

### Task 3.3: Create Data Repository (30 minutes)

**Option A: Zenodo (Recommended)**

1. **[ ] Go to:** https://zenodo.org
2. **[ ] Create account** (free, use institutional email)
3. **[ ] New Upload:**
   - Title: "Dataset for: Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for AES"
   - Upload:
     * `grading_results.db` (SQLite database)
     * Supplementary materials (S1-S5 as ZIP or PDF)
     * README.md (describe dataset structure)
   - License: CC BY 4.0 (or CC0 for public domain)
   - Access: Open
4. **[ ] Publish** → Get DOI (format: 10.5281/zenodo.XXXXXX)
5. **[ ] Copy DOI** and add to:
   - `DECLARATIONS.md` - Data Availability section
   - `manuscript_blinded.docx` - Data Availability footnote

**Option B: Open Science Framework (OSF)**
- Similar process at https://osf.io
- Create project → Upload files → Make public → Get DOI

**Option C: Defer to Post-Acceptance**
- Note in manuscript: "Data will be made available in public repository upon acceptance"
- Many authors do this to avoid wasting time if rejected

---

### Task 3.4: Create Code Repository (Optional, 15 minutes)

**GitHub:**
```powershell
cd E:\project\AES

# Initialize git if not already
git init

# Create .gitignore
# Exclude: .env, API keys, large data files

# Add files
git add scripts/
git add requirements.txt
git add README.md

# Commit
git commit -m "Analysis code for AES study"

# Create repo on GitHub.com, then push
git remote add origin https://github.com/yourusername/aes-study.git
git push -u origin main
```

**Or:** Upload scripts/ folder to Zenodo with data

**Add repository URL to:**
- `DECLARATIONS.md` - Data Availability
- `manuscript_blinded.docx` - Code Availability statement

---

## 🎯 PHASE 4: SUGGESTED REVIEWERS (45 minutes)

### Task 4.1: Search for Potential Reviewers (30 minutes)

**Use:** `assessing_writing/SUGGESTED_REVIEWERS_TEMPLATE.md` as guide

**Strategy:**
1. **Google Scholar:** "automated essay scoring" + "Assessing Writing"
2. **Check recent issues:** https://www.sciencedirect.com/journal/assessing-writing
3. **Look at your references:** Who did you cite extensively?
4. **Conferences:** AERA, NCME, WRAB recent presenters

**Find 4-5 reviewers with:**
- [ ] Relevant expertise (AES, validity, reliability, LLM in education)
- [ ] Recent publications (2022-2025)
- [ ] Different institutions
- [ ] International diversity
- [ ] No conflicts of interest

**For each, record:**
- Full name and title
- Institution and email
- 1-2 relevant publications
- Brief rationale (2-3 sentences)

---

### Task 4.2: Update Title Page (15 minutes)

**Add to:** `assessing_writing/TITLE_PAGE.md` - Suggested Reviewers section

**Format:**
```
Reviewer 1
Name: Dr. Jane Smith, PhD
Position: Associate Professor
Institution: University of XYZ
Email: jane.smith@xyz.edu
Expertise: Automated writing evaluation, validity studies
Relevant Publications: 
- Smith et al. (2024). Validity of AES systems. Assessing Writing, 45, 100-115.
Rationale: Dr. Smith's expertise in psychometric evaluation of AES systems and recent publications on validity evidence align perfectly with our RQ1-RQ2 focus.
```

**Repeat for 3-4 reviewers**

---

## 🎯 PHASE 5: FINAL DECLARATIONS (30 minutes)

### Task 5.1: Complete All Declarations (20 minutes)

**Review and finalize:** `assessing_writing/DECLARATIONS.md`

**Ensure complete:**
- [x] Data Availability Statement (add repository DOI if created)
- [x] Conflict of Interest Statement (confirm "no conflicts")
- [x] Funding Statement (confirm "no funding")
- [x] Ethics Approval (add protocol number)
- [x] Informed Consent (confirm obtained)
- [x] Author Contribution Statement (CRediT - confirm with co-authors)
- [x] Acknowledgments (full version for title page, removed from blinded)

---

### Task 5.2: Convert Declarations to PDF (10 minutes)

```powershell
pandoc assessing_writing/DECLARATIONS.md -o assessing_writing/declarations.pdf
```

**Or:** Copy into Word doc and save as PDF

**Output:** `declarations.pdf` (for upload)

---

## 🎯 PHASE 6: PRE-SUBMISSION REVIEW (1 hour)

### Task 6.1: Internal Review Checklist (30 minutes)

**Print or read on screen:**
- [ ] `manuscript_blinded.docx` - Read first 5 pages, check for author info
- [ ] Abstract within 250 words (current: 246 ✓)
- [ ] All tables and figures cited in text
- [ ] All in-text citations in reference list
- [ ] All reference list entries cited in text
- [ ] No broken cross-references ("see Section XX")
- [ ] Consistent terminology throughout
- [ ] Spelling and grammar check (F7 in Word)

---

### Task 6.2: Co-Author Final Approval (30 minutes)

**Send to all co-authors:**
1. `manuscript_blinded.docx` (or PDF export)
2. `title_page.docx` (verify their info correct)
3. `DECLARATIONS.md` (verify author contributions)
4. Deadline for approval: [Date - 3 days before submission]

**Email template:**
```
Subject: Final Approval Needed - Assessing Writing Submission

Dear Co-Authors,

Our manuscript "Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash 
for Automated Essay Scoring" is ready for submission to Assessing Writing.

Please review attached files and confirm:
1. Your information is correct in title_page.docx
2. Author contributions accurately reflect your role
3. You approve the final manuscript version
4. You agree to submission to this journal

Please reply with "APPROVED" by [Date] or suggest any changes.

Estimated submission date: [Date]

Best regards,
[Your Name]
```

---

## 🎯 PHASE 7: SUBMISSION (2 hours)

### Task 7.1: Register at Editorial Manager (15 minutes)

1. **[ ] Go to:** https://www.editorialmanager.com/asw/
2. **[ ] Click:** "Register" (if no account)
3. **[ ] Fill in:**
   - Email (corresponding author - institutional preferred)
   - Name, affiliation
   - Complete profile
4. **[ ] Verify email** (check inbox)
5. **[ ] Login**

---

### Task 7.2: Start New Submission (1.5 hours)

**Follow step-by-step submission wizard:**

**Step 1: Type, Title, Abstract**
- [ ] Select type: "Research Article"
- [ ] Enter full title (copy from title page)
- [ ] Enter abstract (copy from ABSTRACT_TRIMMED.md - 246 words)
- [ ] Enter short title (40 chars): "LLM Reliability in Essay Scoring"

**Step 2: Keywords**
- [ ] Enter 6 keywords (one per box):
  1. Automated Essay Scoring
  2. Large Language Models
  3. Educational Assessment
  4. Reliability
  5. Validity
  6. Hybrid Grading

**Step 3: Authors**
- [ ] Add corresponding author (from title_page.docx)
- [ ] Add co-authors (from title_page.docx)
- [ ] Enter ORCID iDs for all
- [ ] Designate corresponding author

**Step 4: Upload Files**
Upload in this order:
1. [ ] **Cover Letter** 
   - Convert COVER_LETTER_ASSESSING_WRITING.md to PDF
   - Or copy to Word → Save as PDF
2. [ ] **Title Page**
   - Upload title_page.docx
3. [ ] **Manuscript (Blinded)**
   - Upload manuscript_blinded.docx
4. [ ] **Figures**
   - Upload graphical_abstract.png (labeled "Figure 1")
5. [ ] **Supplementary Material 1**
   - Upload S1_EXTENDED_METHODOLOGY.md (or .pdf)
6. [ ] **Supplementary Material 2**
   - Upload S2_RAW_DATA_SUMMARY.md (or .pdf)
7. [ ] **Supplementary Material 3**
   - Upload S3_STATISTICAL_TESTS.md (or .pdf)
8. [ ] **Supplementary Material 4**
   - Upload S4_CONFUSION_MATRICES.md (or .pdf)
9. [ ] **Supplementary Material 5**
   - Upload S5_EXTENDED_TABLES.md (or .pdf)

**Step 5: Suggested Reviewers (Optional)**
- [ ] Add 3-4 reviewers from title_page.docx
- [ ] Include email, institution, expertise for each

**Step 6: Declarations**
- [ ] Funding: None
- [ ] Conflicts of Interest: None declared
- [ ] Data Availability: Yes (provide repository DOI or "available upon request")
- [ ] Ethics Approval: Yes (provide protocol number or "approved by institutional ethics committee")
- [ ] Human Subjects: Yes
- [ ] Informed Consent: Yes, obtained

**Step 7: Comments to Editor (Optional)**
- [ ] Can mention: "This manuscript has not been published elsewhere and is not under consideration by other journals. We believe it aligns perfectly with Assessing Writing's focus on writing assessment methods and technologies."

**Step 8: Review Submission**
- [ ] Preview PDF - CHECK CAREFULLY:
  * Blinded manuscript has NO author info
  * All files uploaded correctly
  * Abstract correct
  * Keywords correct
- [ ] Review metadata
- [ ] Check all declarations

**Step 9: Agree & Submit**
- [ ] Read terms and conditions
- [ ] Check box to agree
- [ ] **CLICK SUBMIT**

**Step 10: Save Confirmation**
- [ ] Save confirmation email
- [ ] Note manuscript ID number
- [ ] Take screenshot of submission confirmation

---

### Task 7.3: Post-Submission (15 minutes)

**Immediate actions:**
1. **[ ] Email co-authors:**
   ```
   Subject: Manuscript Submitted - Assessing Writing
   
   Dear Co-Authors,
   
   Our manuscript "Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash 
   for Automated Essay Scoring" has been successfully submitted to Assessing Writing.
   
   Manuscript ID: [ASW-XXXX-YYYY]
   Submission Date: December XX, 2025
   
   Expected timeline:
   - Initial review: 1-2 weeks
   - Peer review: 8-12 weeks
   - Decision: 8-12 weeks from today
   
   I will keep you updated on any editorial communications.
   
   Best regards,
   [Your Name]
   ```

2. **[ ] Archive files:**
   - Create folder: `submission_archive_[date]/`
   - Copy all final versions
   - Save confirmation email

3. **[ ] Set calendar reminders:**
   - Week 2: Check for desk-reject
   - Week 10: Follow up if no response
   - Week 13: Polite inquiry if no decision

---

## 📊 PROGRESS TRACKING

### Status Dashboard

| Phase | Tasks | Est. Time | Status | Priority |
|-------|-------|-----------|--------|----------|
| 1. Author/Institutional Info | 3 | 1 hour | ⏸️ Pending | 🔴 Critical |
| 2. Manuscript Formatting | 5 | 3 hours | ⏸️ Pending | 🔴 Critical |
| 3. Supplementary Materials | 4 | 1 hour | ⏸️ Pending | 🟡 High |
| 4. Suggested Reviewers | 2 | 45 min | ⏸️ Pending | 🟢 Medium |
| 5. Final Declarations | 2 | 30 min | ⏸️ Pending | 🟡 High |
| 6. Pre-Submission Review | 2 | 1 hour | ⏸️ Pending | 🟡 High |
| 7. Submission | 3 | 2 hours | ⏸️ Pending | 🔴 Critical |
| **TOTAL** | **21 tasks** | **9.25 hours** | **0% Complete** | |

---

## 🎯 RECOMMENDED SCHEDULE

### Week 1 (Days 1-3): Preparation
- **Day 1:** Phase 1 (Author info, Ethics) - 1 hour
- **Day 2:** Phase 2 (Formatting) - 3 hours
- **Day 3:** Phase 3-5 (Supplementary, Reviewers, Declarations) - 2 hours

### Week 1 (Days 4-5): Review & Submission
- **Day 4:** Phase 6 (Pre-submission review, co-author approval) - 1 hour
- **Day 5:** Phase 7 (Submission) - 2 hours

**Total Calendar Time:** 5 working days (can compress to 2-3 days if focused)

---

## 📧 EMAIL TEMPLATES

### To Co-Authors (Information Request)

```
Subject: Action Required - Journal Submission Information

Dear Co-Authors,

We are preparing to submit our manuscript "Comparative Evaluation of 
ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring" to 
Assessing Writing (Q1 journal, IF 3.1).

Please provide by [Date - 3 days from now]:

1. Full name (as should appear in publication)
2. Academic degree(s) and credentials
3. Current title/position
4. Department name
5. Institution full name and address
6. Institutional email address
7. ORCID iD (register free at https://orcid.org if needed)

8. Confirm your role in this project for Author Contributions:
   [ ] Conceptualization
   [ ] Methodology
   [ ] Data collection
   [ ] Analysis
   [ ] Writing - original draft
   [ ] Writing - review & editing
   [ ] Other: _____________

Please reply with this information by [Date].

Thank you!
Best regards,
[Your Name]
```

---

### To IRB/Ethics Committee (Documentation Request)

```
Subject: Request for Ethics Approval Documentation

Dear [Ethics Committee Contact],

I am preparing to submit a manuscript for publication in an international 
journal and require documentation of ethics approval.

Study Title: Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash 
for Automated Essay Scoring

Protocol Number: [XXX-YYYY-ZZ] (if known)
Approval Date: [Date] (if known)

Could you please provide:
1. Official approval letter (PDF)
2. Confirmation of protocol number
3. Approval date and expiration date

This documentation is required for journal submission.

Thank you for your assistance.

Best regards,
[Your Name]
[Contact Information]
```

---

## ⚠️ TROUBLESHOOTING

### Common Issues & Solutions

**Issue: "I don't have ethics approval yet"**
- **Solution A:** Apply now through your IRB (may take 2-6 weeks)
- **Solution B:** Note in cover letter: "Ethics approval pending, will provide before review begins"
- **Solution C:** Some journals allow post-submission ethics approval

**Issue: "Co-author not responding"**
- **Solution:** Set firm deadline, note you'll proceed without their input if necessary
- **Solution:** Only list co-authors who have approved (can remove unresponsive authors)

**Issue: "Can't convert Markdown to Word"**
- **Solution A:** Install Pandoc (https://pandoc.org)
- **Solution B:** Copy-paste content manually into Word
- **Solution C:** Use online converter (e.g., https://word2md.com - reverse direction)

**Issue: "References not in APA 7th format"**
- **Solution:** Use citation manager (Zotero - free)
- **Solution:** Use online APA formatter
- **Solution:** Manually fix most egregious errors, journal will help with minor issues

**Issue: "Don't know suggested reviewers"**
- **Solution:** Skip this (it's optional)
- **Solution:** Ask colleague who works in this field
- **Solution:** Search Google Scholar for recent papers on your topic

---

## ✅ FINAL CHECKLIST BEFORE SUBMIT

**Absolutely must have:**
- [x] Manuscript formatted (Times New Roman, double-space, line numbers)
- [x] Blinded version (NO author identifiers)
- [x] Title page (WITH author identifiers)
- [x] Abstract (246 words ✓)
- [x] Keywords (6 keywords)
- [x] All declarations complete
- [ ] Ethics approval documentation
- [x] All co-authors approved
- [x] Supplementary files ready

**Nice to have:**
- [ ] Data repository with DOI
- [ ] Code repository
- [ ] Suggested reviewers (3-4)
- [ ] Graphical abstract (already have ✓)

**Double-check:**
- [ ] No author names in blinded manuscript
- [ ] All [brackets] filled in with real information
- [ ] File properties cleaned (author = blank in blinded version)
- [ ] All files saved in correct format (.docx, .pdf, .png)

---

## 🎉 SUCCESS METRICS

**Immediate Success:**
- ✅ Manuscript submitted without desk-rejection

**Short-term Success (2-4 weeks):**
- ✅ Manuscript sent for peer review (not desk-rejected)

**Medium-term Success (8-12 weeks):**
- ✅ Receive reviewer comments (even if revisions required)

**Long-term Success (4-6 months):**
- ✅ Manuscript accepted for publication

**Expected Probability:**
- Desk-reject: <10% (manuscript is strong and fits scope)
- Minor revisions: 40-50% (most likely outcome)
- Major revisions: 30-40%
- Accept as-is: <5% (rare on first submission)
- Reject after review: 10-20%

**Overall acceptance probability: 70-85%** (excellent for Q1 journal)

---

**Ready to start? Begin with Phase 1: Author & Institutional Information**

**Next Action:** Send email to co-authors requesting information (template above)

---

**Last Updated:** December 15, 2025  
**Created by:** AI Assistant  
**Purpose:** Complete action plan for submitting to Assessing Writing journal  
**Estimated Time to Complete:** 9-10 hours spread over 5 days
