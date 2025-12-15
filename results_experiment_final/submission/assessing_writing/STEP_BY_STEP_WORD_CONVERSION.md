# Step-by-Step: Convert Manuscript to Word Format

**Goal:** Convert COMPREHENSIVE_ANALYSIS_REPORT.md to properly formatted manuscript_blinded.docx  
**Time Required:** 2-3 hours  
**Difficulty:** Medium

---

## OPTION 1: Using Pandoc (Recommended - Faster)

### Step 1: Install Pandoc (10 minutes)

**Check if already installed:**
```powershell
pandoc --version
```

**If not installed, install via Chocolatey:**
```powershell
# Install Chocolatey if needed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Pandoc
choco install pandoc -y

# Verify
pandoc --version
```

**Alternative: Download installer:**
- Go to: https://pandoc.org/installing.html
- Download Windows installer (.msi)
- Run installer
- Restart PowerShell

---

### Step 2: Create Word Template with Proper Formatting (15 minutes)

**Manual creation in Microsoft Word:**

1. **Open Word → Blank Document**

2. **Set Page Layout:**
   - Layout → Margins → Custom Margins
   - Top: 1 inch (2.54 cm)
   - Bottom: 1 inch (2.54 cm)
   - Left: 1 inch (2.54 cm)
   - Right: 1 inch (2.54 cm)
   - Click OK

3. **Set Font:**
   - Home → Font dropdown → Times New Roman
   - Home → Font Size → 12

4. **Set Spacing:**
   - Home → Paragraph → Line and Paragraph Spacing
   - Select "2.0" (double spacing)
   - Or: Home → Paragraph → Paragraph Settings
     * Line spacing: Double
     * Before: 0 pt
     * After: 0 pt

5. **Set Alignment:**
   - Home → Paragraph → Align Left (not Justify)

6. **Add Page Numbers:**
   - Insert → Page Number → Bottom of Page → Plain Number 2 (centered)

7. **Add Line Numbers:**
   - Layout → Line Numbers → Continuous

8. **Define Styles:**
   - Home → Styles → Create a Style → "Heading 1"
     * Font: Times New Roman, 12pt, Bold
     * Format: Title Case
   - Create "Heading 2"
     * Font: Times New Roman, 12pt, Bold
     * Format: Sentence case
   - Create "Heading 3"
     * Font: Times New Roman, 12pt, Italic
     * Format: Sentence case

9. **Save as Template:**
   - File → Save As
   - File name: `manuscript_template.docx`
   - Location: `E:\project\AES\results_experiment_final\submission\assessing_writing\`

---

### Step 3: Convert Markdown to Word (5 minutes)

```powershell
# Navigate to reports folder
cd E:\project\AES\results_experiment_final\reports

# Convert using template
pandoc COMPREHENSIVE_ANALYSIS_REPORT.md -o manuscript_draft.docx --reference-doc=E:\project\AES\results_experiment_final\submission\assessing_writing\manuscript_template.docx

# Or basic conversion without template
pandoc COMPREHENSIVE_ANALYSIS_REPORT.md -o manuscript_draft.docx
```

**Output:** `manuscript_draft.docx` created in reports/ folder

---

### Step 4: Post-Conversion Cleanup in Word (1 hour)

**Open manuscript_draft.docx in Microsoft Word:**

#### A. Fix Title and Header (5 min)
- [ ] Remove any extra blank pages at top
- [ ] Ensure title is centered
- [ ] Add blank line after title
- [ ] Add "Date: December 15, 2024" below title

#### B. Fix Headings (15 min)
- [ ] Apply "Heading 1" style to: Executive Summary, Introduction, Methodology, Results, Discussion, Limitations, Conclusions
- [ ] Apply "Heading 2" style to subsections (e.g., "1.1 Research Context")
- [ ] Apply "Heading 3" style to sub-subsections
- [ ] Use Find & Replace to standardize:
  * Find: `## ` → Replace with: Apply Heading 1 style
  * Find: `### ` → Replace with: Apply Heading 2 style

#### C. Fix Tables (20 min)
- [ ] Check each table (should be 5 tables total)
- [ ] Ensure tables are editable (not images)
- [ ] Add caption above each table:
  * Format: **Table 1.** Caption text
  * Font: Times New Roman, 12pt, Bold for "Table 1"
- [ ] Add notes below tables if needed
- [ ] Simple table format (remove heavy gridlines)
  * Table Tools → Design → Table Styles → Plain Table 1

#### D. Fix Figures (10 min)
- [ ] Insert graphical_abstract.png
  * Insert → Pictures → Browse
  * Select: `E:\project\AES\results_experiment_final\submission\graphical_abstract.png`
- [ ] Add caption below figure:
  * **Figure 1.** Graphical abstract showing study design and key findings
- [ ] Ensure figure is 300 DPI (check Properties)

#### E. Fix References (15 min)
- [ ] Scroll to References section
- [ ] Check APA 7th format:
  * Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Volume*(Issue), pages. https://doi.org/xxx
- [ ] Add DOIs where missing (search on Crossref.org or Google Scholar)
- [ ] Ensure hanging indent (1.27 cm):
  * Select all references
  * Home → Paragraph → Indentation → Special → Hanging → 1.27 cm

#### F. Fix Abstract (5 min)
- [ ] Copy trimmed abstract from ABSTRACT_TRIMMED.md (246 words)
- [ ] Replace abstract in manuscript
- [ ] Ensure single paragraph, no citations
- [ ] Add "Keywords:" line below with 6 keywords

#### G. Fix Lists (5 min)
- [ ] Convert bullet points to proper Word bullets
- [ ] Ensure consistent formatting (• or - )
- [ ] Numbered lists (1, 2, 3 not 1., 2., 3.)

#### H. Final Formatting Check (10 min)
- [ ] Select All (Ctrl+A)
- [ ] Verify: Times New Roman, 12pt, Double-spacing, Left-aligned
- [ ] Check page numbers (bottom center, all pages)
- [ ] Check line numbers (continuous, left margin)
- [ ] Remove any markdown artifacts (**, ##, etc.)

---

### Step 5: Save Versions (5 min)

**Save two versions:**

1. **manuscript_with_authors.docx** (Original - keep for reference)
   - File → Save As
   - Name: `manuscript_with_authors.docx`
   - Location: `E:\project\AES\results_experiment_final\submission\assessing_writing\`

2. **manuscript_draft.docx** (Working copy - will blind next)
   - Keep in reports/ folder for now
   - Will create blinded version in next step

---

## OPTION 2: Manual Copy-Paste (If Pandoc Fails)

### Step 1: Create New Word Document (5 min)

1. Open Microsoft Word
2. Blank Document
3. Set up formatting (see Option 1, Step 2 above)
4. Save as: `manuscript_draft.docx`

---

### Step 2: Copy Content from Markdown (1.5 hours)

**Open two windows side-by-side:**
- Left: COMPREHENSIVE_ANALYSIS_REPORT.md in VS Code
- Right: manuscript_draft.docx in Microsoft Word

**Copy section by section:**

1. **Title and Metadata (5 min)**
   - Copy title: "Comprehensive Analysis Report: LLM-Based Automated Essay Scoring"
   - Simplify to: "Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring: A Multi-Strategy Analysis of Reliability, Validity, and Practical Implications"
   - Paste in Word, center, bold
   - Add date below

2. **Abstract (5 min)**
   - Copy from ABSTRACT_TRIMMED.md (246 words)
   - Paste in Word
   - Heading: **Abstract** (not bold)
   - Below abstract: **Keywords:** [6 keywords]

3. **Main Body (45 min)**
   - Copy from "## Executive Summary" onwards
   - Paste in Word
   - Remove markdown formatting:
     * ## → Apply Heading 1 style
     * ### → Apply Heading 2 style
     * #### → Apply Heading 3 style
     * **text** → Bold (Ctrl+B)
     * *text* → Italic (Ctrl+I)

4. **Tables (20 min)**
   - For each table in markdown:
     * Copy table content
     * Word → Insert → Table → Convert Text to Table
     * Adjust column widths
     * Add caption above: **Table X.** Caption

5. **References (15 min)**
   - Copy references section
   - Apply hanging indent (1.27 cm)
   - Verify APA 7th format

6. **Clean Up (10 min)**
   - Find & Replace:
     * Find: `  ` (double space) → Replace: ` ` (single space)
     * Find: `##` → Replace: nothing
     * Find: `**` → Replace: nothing
   - Apply formatting throughout

---

## Post-Conversion Verification Checklist

**Before proceeding to blinding, verify:**

- [ ] Word count: ~7,959 words (check: Review → Word Count)
- [ ] Font: Times New Roman, 12pt (entire document)
- [ ] Spacing: Double-spaced (entire document)
- [ ] Margins: 1 inch all sides
- [ ] Page numbers: Bottom center, all pages
- [ ] Line numbers: Continuous, left margin
- [ ] Alignment: Left (not justified)
- [ ] Abstract: 246 words, no citations
- [ ] Keywords: 6 keywords listed
- [ ] Tables: 5 tables, all editable, captions above
- [ ] Figures: 1 figure (graphical abstract), caption below
- [ ] References: Hanging indent, APA 7th format
- [ ] No markdown artifacts (##, **, etc.)
- [ ] All sections present: Abstract, Intro, Method, Results, Discussion, Limitations, Conclusions, References

---

## Troubleshooting

### Problem: Pandoc not found
**Solution:**
```powershell
# Add Pandoc to PATH manually
$env:Path += ";C:\Program Files\Pandoc\"
pandoc --version
```

### Problem: Conversion has weird formatting
**Solution:** Use template:
```powershell
pandoc input.md -o output.docx --reference-doc=template.docx
```

### Problem: Tables look bad
**Solution:** Manually recreate tables in Word:
1. Insert → Table → Select rows/columns
2. Copy data from markdown cell by cell
3. Format: Table Tools → Design → Plain Table 1

### Problem: Spacing is inconsistent
**Solution:**
1. Select All (Ctrl+A)
2. Home → Paragraph → Line Spacing → 2.0
3. Home → Paragraph → Paragraph Settings
   - Before: 0 pt
   - After: 0 pt

### Problem: References not formatted correctly
**Solution:** Use citation manager:
1. Export from Zotero/Mendeley
2. Or use online APA formatter: https://www.scribbr.com/apa-citation-generator/
3. Or manually fix most critical ones

---

## Quick Commands Reference

```powershell
# Navigate to project
cd E:\project\AES\results_experiment_final

# Convert markdown to docx
pandoc reports/COMPREHENSIVE_ANALYSIS_REPORT.md -o submission/assessing_writing/manuscript_draft.docx

# With template
pandoc reports/COMPREHENSIVE_ANALYSIS_REPORT.md -o submission/assessing_writing/manuscript_draft.docx --reference-doc=submission/assessing_writing/manuscript_template.docx

# Check word count in PowerShell (approximate)
(Get-Content reports/COMPREHENSIVE_ANALYSIS_REPORT.md | Measure-Object -Word).Words

# Open in Word (from PowerShell)
Start-Process "submission/assessing_writing/manuscript_draft.docx"
```

---

## Estimated Timeline

| Task | Time | Cumulative |
|------|------|------------|
| Install Pandoc | 10 min | 10 min |
| Create template | 15 min | 25 min |
| Convert markdown | 5 min | 30 min |
| Fix headings | 15 min | 45 min |
| Fix tables | 20 min | 65 min |
| Fix figures | 10 min | 75 min |
| Fix references | 15 min | 90 min |
| Fix abstract | 5 min | 95 min |
| Final cleanup | 15 min | **110 min (1.8 hours)** |

**Total: ~2 hours with Pandoc, ~3 hours manual**

---

## Next Step After This

After manuscript_draft.docx is properly formatted:
→ Go to [BLINDING_GUIDE.md](BLINDING_GUIDE.md) to create blinded version

---

**Last Updated:** December 15, 2025  
**Status:** Ready to use  
**Difficulty:** Medium (with Pandoc) / Hard (manual)
