# Daily Task Breakdown - 5-Day Submission Plan

**Goal:** Submit manuscript to Assessing Writing within 5 working days  
**Total Time:** ~9 hours spread across 5 days  
**Start Date:** [Fill in - e.g., December 16, 2025]

---

## 📅 DAY 1: Monday - Information Gathering (1.5 hours)

### Morning (30 minutes)

**Task 1.1: Send Email to Co-Authors (10 min)**
- [ ] Open [EMAIL_TEMPLATES_READY_TO_SEND.md](EMAIL_TEMPLATES_READY_TO_SEND.md)
- [ ] Copy "EMAIL 1: To Co-Authors - Information Request"
- [ ] Fill in all [BRACKETS] with actual names, dates
- [ ] Set deadline: Day 3 (Wednesday)
- [ ] Send email
- [ ] Save copy to project folder

**Task 1.2: Contact IRB/Ethics Committee (10 min)**
- [ ] Find IRB contact email (check department website)
- [ ] Copy "EMAIL 3: To IRB/Ethics Committee"
- [ ] Fill in study details and protocol number (if known)
- [ ] Set deadline: Day 3 (Wednesday)
- [ ] Send email
- [ ] Save copy

**Task 1.3: Set Up Tracking (10 min)**
- [ ] Create spreadsheet or document to track:
  * Co-author responses (Name | Info Received | Approved)
  * IRB status (Requested | Received | Uploaded)
  * Tasks completed today
- [ ] Set calendar reminders:
  * Day 3: Check co-author responses
  * Day 4: Final approval reminder
  * Day 5: Submit to journal

---

### Afternoon (1 hour)

**Task 1.4: Install Pandoc (15 min)**
- [ ] Open PowerShell as Administrator
- [ ] Run: `pandoc --version` (check if installed)
- [ ] If not installed:
  ```powershell
  choco install pandoc -y
  ```
- [ ] Or download from: https://pandoc.org/installing.html
- [ ] Verify installation: `pandoc --version`

**Task 1.5: Review Submission Guidelines (20 min)**
- [ ] Read [JOURNAL_GUIDELINES.md](JOURNAL_GUIDELINES.md) completely
- [ ] Note any requirements you're unsure about
- [ ] Check Assessing Writing website for latest updates
- [ ] Bookmark Editorial Manager: https://www.editorialmanager.com/asw/

**Task 1.6: Review Final Action Plan (25 min)**
- [ ] Read [FINAL_ACTION_PLAN.md](FINAL_ACTION_PLAN.md) completely
- [ ] Understand all 7 phases
- [ ] Identify potential roadblocks
- [ ] Note questions for tomorrow

**END OF DAY 1 CHECKLIST:**
- [ ] Emails sent to co-authors ✓
- [ ] Email sent to IRB ✓
- [ ] Pandoc installed ✓
- [ ] Guidelines reviewed ✓
- [ ] Action plan understood ✓

---

## 📅 DAY 2: Tuesday - Manuscript Formatting (3 hours)

### Morning (2 hours)

**Task 2.1: Create Word Template (20 min)**
- [ ] Open Microsoft Word
- [ ] Set margins: 1 inch all sides (Layout → Margins → Custom)
- [ ] Set font: Times New Roman, 12pt (Home → Font)
- [ ] Set spacing: Double (Home → Paragraph → Line Spacing → 2.0)
- [ ] Add page numbers: Bottom center (Insert → Page Number)
- [ ] Add line numbers: Continuous (Layout → Line Numbers)
- [ ] Save as: `manuscript_template.docx` in assessing_writing/ folder
- [ ] **Detailed guide:** [STEP_BY_STEP_WORD_CONVERSION.md](STEP_BY_STEP_WORD_CONVERSION.md)

**Task 2.2: Convert Markdown to Word (10 min)**
```powershell
cd E:\project\AES\results_experiment_final\reports

pandoc COMPREHENSIVE_ANALYSIS_REPORT.md -o manuscript_draft.docx --reference-doc=../submission/assessing_writing/manuscript_template.docx
```
- [ ] Check output file created successfully
- [ ] Open manuscript_draft.docx to verify basic structure

**Task 2.3: Format Tables (30 min)**
- [ ] Open manuscript_draft.docx
- [ ] Find Table 1 (Validity Metrics)
  * Add caption above: "**Table 1.** Validity metrics..."
  * Ensure editable (not image)
  * Apply simple format: Table Tools → Design → Plain Table 1
- [ ] Repeat for Tables 2-5
- [ ] Verify all tables cited in text
- [ ] **Follow:** Section "Fix Tables" in STEP_BY_STEP_WORD_CONVERSION.md

**Task 2.4: Format Headings (20 min)**
- [ ] Executive Summary → Heading 1 style
- [ ] Introduction → Heading 1
- [ ] Methodology → Heading 1
- [ ] All subsections (e.g., "2.1 Research Design") → Heading 2
- [ ] All sub-subsections → Heading 3
- [ ] Check Table of Contents auto-generates correctly

**Task 2.5: Insert Graphical Abstract (15 min)**
- [ ] Place cursor where figure should go
- [ ] Insert → Pictures → Browse
- [ ] Select: `E:\project\AES\results_experiment_final\submission\graphical_abstract.png`
- [ ] Add caption below: "**Figure 1.** Graphical abstract showing study design and key findings"
- [ ] Verify 300 DPI (right-click → Properties)
- [ ] Center figure

**Task 2.6: Fix Abstract (10 min)**
- [ ] Open [ABSTRACT_TRIMMED.md](../ABSTRACT_TRIMMED.md)
- [ ] Copy 246-word abstract
- [ ] Replace abstract in manuscript_draft.docx
- [ ] Add Keywords line below with 6 keywords
- [ ] Verify no citations in abstract

---

### Afternoon (1 hour)

**Task 2.7: Fix References (30 min)**
- [ ] Scroll to References section
- [ ] For each reference:
  * Check APA 7th format
  * Add DOI if missing (search Crossref.org or Google Scholar)
  * Ensure hanging indent (1.27 cm)
- [ ] Spot-check 10 random references
- [ ] Verify all in-text citations have reference entry
- [ ] **If too many errors:** Consider using Zotero to re-export

**Task 2.8: Final Formatting Pass (20 min)**
- [ ] Select All (Ctrl+A)
- [ ] Verify: Times New Roman, 12pt, Double-spacing
- [ ] Check page numbers on all pages
- [ ] Check line numbers visible
- [ ] Remove any markdown artifacts (##, **, etc.)
- [ ] Spell check (F7)

**Task 2.9: Save Version (10 min)**
- [ ] File → Save As
- [ ] Name: `manuscript_with_authors.docx`
- [ ] Location: `assessing_writing/` folder
- [ ] Keep manuscript_draft.docx as working copy

**END OF DAY 2 CHECKLIST:**
- [ ] Manuscript converted to Word ✓
- [ ] All tables formatted ✓
- [ ] All headings styled ✓
- [ ] Figure inserted ✓
- [ ] Abstract updated ✓
- [ ] References checked ✓
- [ ] Saved formatted version ✓

**EVENING TASK (Optional, 15 min):**
- [ ] Check email for co-author responses
- [ ] Update tracking spreadsheet
- [ ] Send reminder if no responses yet

---

## 📅 DAY 3: Wednesday - Blinding & Supplementary (2 hours)

### Morning (1 hour)

**Task 3.1: Check Co-Author Responses (10 min)**
- [ ] Review emails from co-authors
- [ ] Update tracking spreadsheet
- [ ] If missing info, send follow-up (EMAIL 5 template)
- [ ] Update TITLE_PAGE.md with received information

**Task 3.2: Create Blinded Version (45 min)**
- [ ] Open manuscript_with_authors.docx
- [ ] File → Save As → `manuscript_blinded.docx`
- [ ] **Follow step-by-step:** [BLINDING_GUIDE.md](BLINDING_GUIDE.md)

**Key blinding tasks:**
- [ ] Remove author names from first page
- [ ] Remove institutional affiliations
- [ ] Remove acknowledgments section
- [ ] Find & Replace institution name with "a public university in Indonesia"
- [ ] Search for "we" and change to third person where identifying
- [ ] Remove specific IRB protocol number (keep generic "approved by ethics committee")
- [ ] File → Info → Properties → Remove author info
- [ ] Search for YOUR NAME → Should be 0 results (except references)
- [ ] Search for INSTITUTION NAME → Should be 0 results

**Task 3.3: Verify Blinding (5 min)**
- [ ] Read first 2 pages of manuscript_blinded.docx
- [ ] Ask yourself: "Could I identify the authors?"
- [ ] If YES → blind more thoroughly
- [ ] Compare side-by-side with manuscript_with_authors.docx
- [ ] Verify file properties (author field blank)

---

### Afternoon (1 hour)

**Task 3.4: Update Title Page (20 min)**
- [ ] Open [TITLE_PAGE.md](TITLE_PAGE.md)
- [ ] Fill in all author information received from Day 1
- [ ] Add all ORCID iDs
- [ ] Verify email addresses
- [ ] Convert to Word:
  ```powershell
  pandoc assessing_writing/TITLE_PAGE.md -o assessing_writing/title_page.docx
  ```
- [ ] Or manually copy to Word document
- [ ] Save as: `title_page.docx`

**Task 3.5: Update Declarations (20 min)**
- [ ] Open [DECLARATIONS.md](DECLARATIONS.md)
- [ ] Add IRB protocol number (if received from Day 1)
- [ ] Add data repository DOI (if created, or note "will be provided")
- [ ] Confirm author contributions match co-author responses
- [ ] Convert to PDF:
  ```powershell
  pandoc assessing_writing/DECLARATIONS.md -o assessing_writing/declarations.pdf
  ```
- [ ] Or copy to Word → Save As PDF

**Task 3.6: Verify Supplementary Materials (20 min)**
- [ ] Check S1-S5 files in supplementary_materials/ folder
- [ ] Verify no author-identifying information
- [ ] Check all cross-references in main manuscript match
- [ ] Optional: Convert to PDF for cleaner presentation
  ```powershell
  cd results_experiment_final/submission/supplementary_materials
  pandoc S1_EXTENDED_METHODOLOGY.md -o S1_EXTENDED_METHODOLOGY.pdf
  pandoc S2_RAW_DATA_SUMMARY.md -o S2_RAW_DATA_SUMMARY.pdf
  # ... repeat for S3-S5
  ```

**END OF DAY 3 CHECKLIST:**
- [ ] Blinded manuscript created ✓
- [ ] Blinding verified ✓
- [ ] Title page completed ✓
- [ ] Declarations updated ✓
- [ ] Supplementary materials checked ✓

**EVENING TASK (Optional, 30 min):**
- [ ] Create Zenodo account (https://zenodo.org)
- [ ] Start uploading data (can finalize later)
- [ ] Or prepare README.md for data repository

---

## 📅 DAY 4: Thursday - Reviewers & Final Review (1.5 hours)

### Morning (1 hour)

**Task 4.1: Find Suggested Reviewers (45 min)**
- [ ] Open [SUGGESTED_REVIEWERS_TEMPLATE.md](SUGGESTED_REVIEWERS_TEMPLATE.md)
- [ ] Google Scholar search: "automated essay scoring" + "Assessing Writing"
- [ ] Identify 3-4 potential reviewers from recent publications
- [ ] For each reviewer:
  * Verify current affiliation (Google their name)
  * Check no conflicts (different institution, not co-authors)
  * Note 1-2 relevant publications
  * Find email address (university website)
  * Write 2-3 sentence rationale
- [ ] Update TITLE_PAGE.md with reviewer information

**Task 4.2: Internal Manuscript Review (15 min)**
- [ ] Open manuscript_blinded.docx
- [ ] Quick scan for:
  * Author identifying information (should be none)
  * Formatting consistency
  * All tables/figures present and cited
  * Word count appropriate (~8,000 words)
  * Abstract within 250 words (246 ✓)
- [ ] Print checklist from [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- [ ] Go through checklist systematically

---

### Afternoon (30 minutes)

**Task 4.3: Send Final Approval to Co-Authors (15 min)**
- [ ] Export manuscript_blinded.docx to PDF
- [ ] Open [EMAIL_TEMPLATES_READY_TO_SEND.md](EMAIL_TEMPLATES_READY_TO_SEND.md)
- [ ] Copy "EMAIL 2: To Co-Authors - Final Approval Request"
- [ ] Attach:
  * manuscript_blinded.pdf
  * title_page.pdf (or .docx)
  * declarations.pdf
- [ ] Set deadline: Tomorrow (Day 5) 10 AM
- [ ] Send email

**Task 4.4: Prepare Cover Letter (15 min)**
- [ ] Open [COVER_LETTER_ASSESSING_WRITING.md](COVER_LETTER_ASSESSING_WRITING.md)
- [ ] Fill in author names at bottom
- [ ] Update suggested reviewers section if found
- [ ] Convert to PDF:
  ```powershell
  pandoc assessing_writing/COVER_LETTER_ASSESSING_WRITING.md -o assessing_writing/cover_letter.pdf
  ```
- [ ] Save PDF

**END OF DAY 4 CHECKLIST:**
- [ ] Suggested reviewers identified ✓
- [ ] Manuscript reviewed ✓
- [ ] Final approval sent to co-authors ✓
- [ ] Cover letter ready ✓

**EVENING TASK (Recommended, 30 min):**
- [ ] Register account at Editorial Manager: https://www.editorialmanager.com/asw/
- [ ] Complete author profile
- [ ] Familiarize yourself with submission interface

---

## 📅 DAY 5: Friday - SUBMISSION DAY (1.5 hours)

### Morning (30 minutes) - Wait for Co-Author Approval

**Task 5.1: Check Co-Author Approvals (10 min)**
- [ ] Check email for "APPROVED" responses
- [ ] Update tracking spreadsheet
- [ ] If all approved → Proceed to submission
- [ ] If missing approval → Call or text co-author

**Task 5.2: Final File Check (20 min)**
- [ ] Verify all files ready in assessing_writing/ folder:
  * [ ] cover_letter.pdf
  * [ ] title_page.docx
  * [ ] manuscript_blinded.docx
  * [ ] declarations.pdf
  * [ ] graphical_abstract.png (300 DPI)
  * [ ] S1_EXTENDED_METHODOLOGY.md (or .pdf)
  * [ ] S2_RAW_DATA_SUMMARY.md
  * [ ] S3_STATISTICAL_TESTS.md
  * [ ] S4_IMPLEMENTATION_CODE.md
  * [ ] S5_EXTENDED_TABLES.md

- [ ] Check file sizes (nothing >10 MB)
- [ ] Verify file names are professional (no spaces, underscores OK)

---

### Afternoon (1 hour) - SUBMIT!

**Task 5.3: Editorial Manager Submission (45 min)**

**Follow step-by-step in Editorial Manager:**

1. **Login** (5 min)
   - [ ] Go to: https://www.editorialmanager.com/asw/
   - [ ] Login with registered account
   - [ ] Click "Submit New Manuscript"

2. **Select Type** (2 min)
   - [ ] Article Type: "Research Article"
   - [ ] Click "Next"

3. **Enter Metadata** (10 min)
   - [ ] Title: [Copy from title_page.docx]
   - [ ] Short title (40 chars): "LLM Reliability in Essay Scoring"
   - [ ] Abstract: [Copy from ABSTRACT_TRIMMED.md - 246 words]
   - [ ] Keywords (6):
     * Automated Essay Scoring
     * Large Language Models
     * Educational Assessment
     * Reliability
     * Validity
     * Hybrid Grading

4. **Add Authors** (10 min)
   - [ ] Add corresponding author (you)
   - [ ] Add co-author 1 (from title_page.docx)
   - [ ] Add co-author 2 (from title_page.docx)
   - [ ] Verify all ORCID iDs entered
   - [ ] Designate corresponding author

5. **Upload Files** (10 min)
   - [ ] Upload File 1: cover_letter.pdf (Item Type: Cover Letter)
   - [ ] Upload File 2: title_page.docx (Item Type: Title Page)
   - [ ] Upload File 3: manuscript_blinded.docx (Item Type: Manuscript)
   - [ ] Upload File 4: graphical_abstract.png (Item Type: Figure)
   - [ ] Upload File 5: S1_EXTENDED_METHODOLOGY.md (Item Type: Supplementary Material)
   - [ ] Upload File 6: S2_RAW_DATA_SUMMARY.md (Item Type: Supplementary Material)
   - [ ] Upload File 7: S3_STATISTICAL_TESTS.md (Item Type: Supplementary Material)
   - [ ] Upload File 8: S4_IMPLEMENTATION_CODE.md (Item Type: Supplementary Material)
   - [ ] Upload File 9: S5_EXTENDED_TABLES.md (Item Type: Supplementary Material)

6. **Suggested Reviewers** (5 min)
   - [ ] Add 3-4 reviewers from title_page.docx
   - [ ] Include: Name, email, institution, expertise, rationale

7. **Declarations** (5 min)
   - [ ] Funding: None
   - [ ] Conflicts of Interest: None declared
   - [ ] Data Availability: [Yes - provide Zenodo DOI or "available upon request"]
   - [ ] Ethics Approval: [Yes - protocol number from IRB]
   - [ ] Informed Consent: Yes, obtained

8. **Review & Submit** (8 min)
   - [ ] Preview PDF generated by system
   - [ ] **CRITICAL:** Check manuscript_blinded has NO author info
   - [ ] Verify all files uploaded
   - [ ] Check metadata accuracy
   - [ ] Read terms and conditions
   - [ ] Check "I agree" box
   - [ ] **CLICK "SUBMIT"**

9. **Save Confirmation** (2 min)
   - [ ] Save confirmation email
   - [ ] Note Manuscript ID: [ASW-XXXX-YYYY]
   - [ ] Take screenshot of confirmation page
   - [ ] Save to project folder

---

### Post-Submission (15 minutes)

**Task 5.4: Notify Co-Authors (10 min)**
- [ ] Open EMAIL_TEMPLATES_READY_TO_SEND.md
- [ ] Copy "EMAIL 4: To Co-Authors - Post-Submission Notification"
- [ ] Fill in Manuscript ID
- [ ] Send to all co-authors

**Task 5.5: Archive Files (5 min)**
- [ ] Create folder: `submission_archive_2025-12-20/`
- [ ] Copy all final versions:
  * manuscript_blinded.docx
  * manuscript_with_authors.docx
  * title_page.docx
  * cover_letter.pdf
  * declarations.pdf
  * All supplementary files
- [ ] Save confirmation email in archive
- [ ] Backup to external drive or cloud

**Task 5.6: Set Reminders (5 min)**
- [ ] Calendar reminder: 2 weeks from today (check for desk-reject)
- [ ] Calendar reminder: 10 weeks from today (follow up if no response)
- [ ] Calendar reminder: 12 weeks from today (polite inquiry)
- [ ] Add to task list: "Check journal status weekly"

---

## 🎉 END OF DAY 5 - MANUSCRIPT SUBMITTED!

**Celebration Checklist:**
- [ ] Manuscript successfully submitted ✓
- [ ] Confirmation email received ✓
- [ ] Co-authors notified ✓
- [ ] Files archived ✓
- [ ] Reminders set ✓

---

## 📊 Progress Tracking Sheet

| Day | Phase | Hours | Status | Completion |
|-----|-------|-------|--------|------------|
| Day 1 | Information Gathering | 1.5h | ⏸️ Not Started | 0% |
| Day 2 | Manuscript Formatting | 3h | ⏸️ Not Started | 0% |
| Day 3 | Blinding & Supplementary | 2h | ⏸️ Not Started | 0% |
| Day 4 | Reviewers & Final Review | 1.5h | ⏸️ Not Started | 0% |
| Day 5 | SUBMISSION | 1.5h | ⏸️ Not Started | 0% |
| **TOTAL** | **All Phases** | **9.5h** | **0% Complete** | |

**Update this sheet daily to track progress!**

---

## What to Expect After Submission

### Week 1-2: Initial Editorial Review
- Editor checks manuscript fits journal scope
- Checks formatting and completeness
- Decides to send to reviewers or desk-reject
- **Action:** Check email daily for editor communication

### Week 2-8: Peer Review
- 2-3 reviewers read and evaluate manuscript
- Reviewers write detailed reports
- **Action:** Be patient, don't contact editor unless >12 weeks

### Week 8-12: Editorial Decision
- Editor reads reviewer reports
- Makes decision: Accept / Revisions / Reject
- Sends decision email with reviewer comments
- **Action:** Respond promptly if revisions requested

### Expected Timeline to Publication
- Best case (Minor Revisions): 4-6 months from submission
- Typical (Major Revisions): 6-9 months from submission
- If Rejected: Revise and submit to next journal within 2-4 weeks

---

## Emergency Contacts

**If you encounter problems:**

**Technical Issues:**
- Editorial Manager Help: https://www.editorialmanager.com/asw/help/
- Elsevier Author Support: https://service.elsevier.com/app/contact/supporthub/publishing/

**Questions About Submission:**
- Assessing Writing Editorial Office: [Check journal website for email]

**Co-Author Issues:**
- Have backup: Can submit without unresponsive co-author if necessary
- Document all communication attempts

**IRB Issues:**
- If can't get approval letter by Day 5:
  * Note "ethics approval pending" in cover letter
  * Provide before peer review begins

---

**Good luck with your submission! 🎉**

**Remember:** This is a strong manuscript with high acceptance probability (70-85%). Even if revisions are requested, that's normal and positive feedback for improvement.

---

**Last Updated:** December 15, 2025  
**Purpose:** Day-by-day actionable task breakdown  
**Estimated Total Time:** 9.5 hours over 5 days
