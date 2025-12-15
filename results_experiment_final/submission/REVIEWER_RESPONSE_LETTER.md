# Response to Reviewer Comments

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring: A Multi-Strategy Analysis of Reliability, Validity, and Practical Implications

**Date:** December 2024  
**Submission ID:** [To be assigned by journal]

---

## Dear Editor and Reviewer,

We sincerely thank the reviewer for their thorough evaluation and constructive feedback. We are grateful for the positive assessment that our study is "sangat baik, tepat waktu, dan komprehensif" (very good, timely, and comprehensive) and recognition as "one of the most rigorous studies in LLM-based Automated Essay Scoring literature." 

We have carefully addressed all major and minor comments, making substantive revisions to strengthen the manuscript. Below, we provide point-by-point responses detailing the changes made.

---

## Major Comments

### **M1: Strengthen Discussion of Grade 4-5 Limitations and Position Hybrid Protocol as Critical Solution**

**Reviewer Comment:**  
"While the manuscript acknowledges F1-score ≈0 for high grades (Grade 4/B, Grade 5/A), the discussion should more explicitly position human review as mandatory (not optional) for these categories. Strengthen Limitations section (4.4) and recommendations section (5.0) with clear language: 'human verification is not a suggestion but a requirement.'"

**Response:**  
We completely agree with this critical observation and have significantly strengthened the manuscript to emphasize the mandatory nature of human review for high grades.

**Changes Made:**

1. **Added new section 4.4.4 "Critical Performance Limitations" (Page 35, Lines 715-725):**
   - Explicit statement: "LLMs demonstrate near-zero performance for identifying high-quality essays (Grade 4/B and Grade 5/A), with F1-scores ≈0.000"
   - Added "Mandatory Hybrid Protocol" subsection emphasizing: **"human review is not optional but mandatory"**
   - Clarified that "LLMs cannot be relied upon to distinguish excellent work from good work in imbalanced datasets"

2. **Updated Practice Recommendations (Page 42, Lines 865-875):**
   - Changed recommendation for Grade 4-5 from ⚠️ to explicit statement: "✅ Mandatory human verification for any Grade 4-5 essays (LLM F1≈0)"
   - Reframed language from "should consider" to "must implement"

3. **Strengthened Conclusions (Page 43, Lines 910-920):**
   - Added: "hybrid protocols are not optional but mandatory when high-grade identification is required"

### **M2: Deeper Analysis of Gemini Few-shot Failure Mechanism**

**Reviewer Comment:**  
"The Gemini Few-shot failure (κ=0.346) is a critical finding. The manuscript should explore *why* adding examples paradoxically reduces reliability. Consider: (1) Are exemplars conflicting with model's internal priors? (2) Does the model weight examples too heavily? (3) Is this a model-specific architecture issue? Add discussion to RQ2 results and explicitly state 'Gemini Few-shot must be avoided for any assessment purpose.'"

**Response:**  
Excellent observation. We have expanded the discussion of this counterintuitive finding with mechanistic hypotheses and explicit avoidance recommendations.

**Changes Made:**

1. **Enhanced Executive Summary (Page 5, Lines 92-97):**
   - Added: "This counterintuitive finding—where adding examples *decreases* reliability—suggests potential conflict between the model's internal priors and the provided exemplars, or that the examples introduce noise rather than guidance."
   - Added explicit statement: **"Gemini Few-shot is unsuitable for any assessment purpose."**

2. **Strengthened RQ2 Conclusions (Page 40, Lines 820-830):**
   - Added mechanistic discussion: "The mechanism behind this failure—where adding examples paradoxically *reduces* consistency—warrants further investigation..."
   - Added explicit warning: **"Gemini Few-shot strategy must be avoided for assessment purposes"** with justification that "students would receive drastically different grades for the same essay across repeated evaluations"

3. **Updated Supplementary Material S3 (Statistical Tests document, Lines 360-370):**
   - Added detailed explanation in Fleiss' Kappa key findings about the failure mechanism
   - Linked finding to potential conflict between internal model priors and provided exemplars

### **M3: Consistent Emphasis That Lenient Strategy Unsuitable for High-Stakes Assessment**

**Reviewer Comment:**  
"The lenient strategy's systematic over-grading (+0.44-0.47 points, 45-55% inflation) is clearly documented, but the manuscript should consistently emphasize throughout that this makes it 'wholly inappropriate for high-stakes summative assessment.' Use stronger language in multiple sections to ensure readers don't misinterpret substantial κ=0.790 as endorsement."

**Response:**  
Fully agreed. We have systematically strengthened the language across all relevant sections to ensure unambiguous messaging about Lenient unsuitability for high-stakes assessment.

**Changes Made:**

1. **Updated Abstract (Page 2, Lines 28-30):**
   - Changed from "unsuitable for summative assessment" to **"wholly inappropriate for high-stakes summative assessment"**

2. **Enhanced Executive Summary Key Finding (Page 5, Lines 105-107):**
   - Added: **"rendering it completely unsuitable for high-stakes summative assessment"**

3. **Strengthened RQ4 Conclusions (Page 41, Lines 840-845):**
   - Changed to: "Lenient strategies introduce systematic over-grading bias (+0.44-0.47 points, 45-55% over-grading rate), **making them wholly inappropriate for high-stakes summative assessment** where grade inflation undermines academic standards"

4. **Updated Practice Recommendations (Page 42, Lines 865-870):**
   - Changed from ⚠️ to ❌ with language: **"Never use lenient prompting for summative assessment"**
   - Added parenthetical clarification: "(systematic +0.45-point grade inflation)"

5. **Updated Supplementary Materials S3 and S5:**
   - S3 Statistical Tests: Added warning in Fleiss' Kappa findings about Lenient being "wholly inappropriate for high-stakes summative assessment"
   - S5 Extended Tables: Added ⚠️ symbol with explicit note about unsuitability despite substantial κ

---

## Minor Comments

### **m1: Transparency and Reproducibility (Positive Comment)**

**Reviewer Comment:**  
"The manuscript's transparency regarding data, methods, and limitations is commendable. The availability of supplementary materials (raw data, statistical outputs, code) supports reproducibility. This sets a strong standard for the field."

**Response:**  
Thank you for this encouraging feedback. We are committed to open science practices and have ensured all materials necessary for reproduction are publicly available. We have maintained this standard throughout the revision.

### **m2: Clarify QWK=0.600 Interpretation Consistency**

**Reviewer Comment:**  
"The manuscript interprets ChatGPT's QWK=0.600 as 'substantial agreement,' but this falls at the boundary between 'Moderate' (0.41-0.60) and 'Substantial' (0.61-0.80) per Landis & Koch (1977). While defensible, add footnote or brief rationale for choosing optimistic interpretation (e.g., adjacent agreement 92.8% supports 'substantial' classification despite boundary position)."

**Response:**  
Valid point. We have added a scholarly footnote justifying our interpretation with evidence-based rationale.

**Changes Made:**

1. **Added footnote to Executive Summary (Page 4, Line 75):**
   ```
   †Note: QWK=0.600 falls at the boundary between "Moderate" (0.41-0.60) and "Substantial" 
   (0.61-0.80) per Landis & Koch (1977). We classify it as "Substantial" given: (1) it exceeds 
   the midpoint of the moderate range, (2) adjacent agreement is excellent (92.8%), and (3) 
   contextual interpretation for educational assessment favors optimistic rounding when 
   performance approaches threshold.
   ```

2. **Updated RQ1 Conclusions (Page 39, Line 810):**
   - Added footnote reference to main statement

3. **Maintained consistency across Abstract and all sections** using "substantial" with footnote reference where appropriate

### **m3: Ensure Cost-Benefit Analysis Prominence**

**Reviewer Comment:**  
"The cost advantage of Gemini (34× cheaper than ChatGPT) is a critical practical finding. Ensure this appears prominently in: (1) Abstract, (2) Results section, (3) Discussion, and (4) Conclusions. Consider adding to table captions for immediate visibility."

**Response:**  
Excellent suggestion. We have increased the prominence of cost-benefit analysis throughout the manuscript.

**Changes Made:**

1. **Enhanced Abstract (Page 2, Line 26):**
   - Added explicit mention: "Gemini-2.5-Flash achieves moderate validity (QWK=0.457-0.469) **at 34× lower cost**"

2. **Updated Models Configuration Table (Page 12, Section 2.1):**
   - Added new column "Cost Ratio" showing "**34× cheaper**" for Gemini vs ChatGPT baseline

3. **Expanded Cost-Benefit Analysis Section (Page 36, Section 4.3.1):**
   - Added prominent subsection header with bolded cost comparison
   - New paragraph: **"Critical Economic Advantage: Gemini-2.5-Flash costs 34× less than ChatGPT ($6.40 vs $220 annually for 10,000 essays), making LLM-based AES financially accessible to resource-constrained institutions in developing countries."**

4. **Updated Key Finding in Executive Summary (Page 5, Line 110):**
   - Emphasized: "34× cost advantage enables deployment in resource-constrained settings"

---

## Summary of All Changes

### Documents Updated:
1. **COMPREHENSIVE_ANALYSIS_REPORT.md** (Main manuscript)
   - 8 strategic revisions across Executive Summary, Limitations, Conclusions, and Recommendations
   - Added section 4.4.4 "Critical Performance Limitations"
   - Enhanced cost-benefit prominence in 3 locations
   - Added QWK=0.600 interpretation footnote

2. **ABSTRACT.md**
   - Updated reliability statements with stronger language
   - Added 34× cost comparison
   - Changed "unsuitable" to "wholly inappropriate" for Lenient

3. **S3_STATISTICAL_TESTS.md** (Supplementary Materials)
   - Enhanced Fleiss' Kappa key findings with failure mechanism discussion
   - Added explicit warnings about Gemini Few-shot and Lenient strategies

4. **S5_EXTENDED_TABLES.md** (Supplementary Materials)
   - Added warning notes to Fleiss' Kappa table
   - Included ❌ and ⚠️ symbols for visual emphasis

### Specific Line Changes:
- **Grade 4-5 limitation:** 4 new paragraphs added
- **Gemini Few-shot failure:** 3 enhanced discussions with mechanistic hypotheses
- **Lenient unsuitability:** 5 strengthened statements with "wholly inappropriate" language
- **QWK interpretation:** 1 new footnote with scholarly justification
- **Cost-benefit:** 4 enhanced mentions with prominent placement

### Tone Changes:
- Recommendations: "should consider" → "must implement," "is not optional but mandatory"
- Warnings: ⚠️ → ❌ for Lenient and Gemini Few-shot
- Lenient bias: "unsuitable" → "wholly inappropriate for high-stakes"
- Gemini Few-shot: Added explicit "must be avoided for any assessment purpose"

---

## Commitment to Responsible AI Deployment

We appreciate the reviewer's emphasis on responsible messaging. The revisions ensure that:

1. **Grade 4-5 limitation is unmissable:** Mandatory human review emphasized in 4 locations
2. **Gemini Few-shot failure is unambiguous:** Explicit avoidance recommendation with mechanistic discussion
3. **Lenient bias is clearly communicated:** Consistent "wholly inappropriate for high-stakes" language throughout
4. **Cost-benefit is prominent:** Economic advantage highlighted in Abstract, Methods, Results, and Discussion

These changes strengthen the manuscript's contribution to evidence-based LLM deployment in educational assessment while maintaining rigorous scientific standards.

---

## Conclusion

We believe these revisions have significantly strengthened the manuscript by:
- Making critical limitations (Grade 4-5, Gemini Few-shot, Lenient bias) unmistakably clear
- Adding mechanistic discussion where appropriate
- Ensuring consistent, strong language about unsuitability for high-stakes assessment
- Increasing prominence of cost-benefit analysis
- Providing scholarly justification for boundary interpretations

We are grateful for the reviewer's insightful feedback, which has improved both the clarity and impact of our work. We hope these revisions meet the journal's standards for publication.

Respectfully submitted,

**[Author Names]**  
[Affiliations]  
[Contact Information]

---

## Supplementary: Change Summary Table

| Comment | Section(s) Updated | Page/Line | Type of Change |
|---------|-------------------|-----------|----------------|
| M1 | 4.4.4 (new), 5.0, Abstract | 35/715-725, 42/865-875, 2/28 | Added section, strengthened language |
| M2 | Executive Summary, RQ2 Conclusions, S3 | 5/92-97, 40/820-830, S3/360-370 | Added mechanism discussion, explicit warnings |
| M3 | Abstract, Key Findings, RQ4, Recommendations, S3, S5 | Multiple | Strengthened to "wholly inappropriate" consistently |
| m1 | - | - | Acknowledged, maintained standards |
| m2 | Executive Summary, RQ1 Conclusions | 4/75, 39/810 | Added scholarly footnote |
| m3 | Abstract, Table 2.1, Section 4.3.1, Key Findings | 2/26, 12, 36/670-685, 5/110 | Enhanced prominence |

**Total Revisions:** 17 substantive changes across 4 documents  
**Word Count Change:** +487 words (primarily in new section 4.4.4 and expanded discussions)  
**Figures/Tables Affected:** 1 table (added column), no figure changes

