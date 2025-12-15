# Research Highlights (Assessing Writing Submission)

**Manuscript:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring

---

## Highlights (3-5 bullet points, max 85 characters each)

• ChatGPT zero-shot achieves substantial validity (QWK=0.600, ICC=0.969)

• Gemini few-shot shows poor reliability (κ=0.346) and must be avoided

• LLMs fail at identifying high-quality essays (F1≈0 for Grades 4-5)

• Lenient prompting causes 45-55% over-grading, unsuitable for summative use

• Hybrid protocol reduces costs 77% while maintaining assessment quality

---

## Extended Research Highlights

### 1. Rigorous Multi-Trial Reliability Assessment
First comprehensive study with 10 independent trials (4,473 gradings total) revealing ChatGPT excellent consistency (ICC=0.969, Fleiss' κ=0.838) but Gemini few-shot poor reliability (κ=0.346), challenging assumptions about LLM consistency in writing assessment.

### 2. Critical Limitation for High-Quality Writing Detection
LLMs demonstrate near-zero performance (F1≈0.000) for identifying high-quality essays (Grades 4-5) due to class imbalance, necessitating mandatory human review—a critical finding for writing assessment validity.

### 3. Systematic Bias in Lenient Prompting
Lenient strategies introduce 45-55% over-grading bias (+0.44-0.47 points), rendering them wholly inappropriate for summative writing assessment despite substantial agreement metrics (κ=0.790), highlighting importance of error pattern analysis.

### 4. Evidence-Based Hybrid Assessment Protocol
Tiered grading framework combining automated scoring for common grades (1-3) with human verification for high grades (4-5) reduces costs 77% ($15,000→$3,000 annually) while maintaining quality standards.

### 5. Cost-Effectiveness Enables Equitable Access
Gemini-2.5-Flash costs 34× less than ChatGPT ($6.40 vs $220 per 10,000 essays), making automated formative feedback financially viable for resource-constrained writing programs in developing countries.

---

## Visual Abstract Summary

**Problem:** LLM reliability and validity for writing assessment unknown  
**Method:** 4,473 gradings, 2 models, 3 strategies, 10 trials  
**Finding:** ChatGPT reliable (ICC=0.969) but fails at high grades (F1≈0)  
**Solution:** Hybrid protocol: automate Grades 1-3, human review Grades 4-5  
**Impact:** 77% cost reduction, maintains validity, enables equitable access

---

## Significance Statement (250 words)

This study provides the most comprehensive psychometric evaluation of large language models for automated essay scoring to date, addressing critical gaps in understanding their reliability, validity, and practical utility for writing assessment. Through 4,473 grading instances across two state-of-the-art LLMs and three prompting strategies, we reveal both promising capabilities and critical limitations that must inform responsible deployment.

Our findings challenge common assumptions about LLM consistency, demonstrating that few-shot approaches—widely advocated in natural language processing—can paradoxically *reduce* reliability for certain models (Gemini κ=0.346 vs 0.530 for zero-shot). This counterintuitive result has important implications for writing assessment practitioners designing LLM-based systems.

We identify a critical validity limitation: LLMs achieve near-zero recall for high-quality writing (F1≈0 for Grades 4-5), meaning they systematically fail to identify excellent work. This finding necessitates mandatory human review for top-performing essays, fundamentally shaping how LLM-based assessment should be implemented.

Our detection of systematic over-grading bias in lenient prompting (45-55% inflation) provides empirical evidence that such strategies are wholly inappropriate for summative writing assessment, despite appearing reliable by conventional metrics. This highlights the importance of comprehensive error analysis beyond simple agreement statistics.

Finally, our evidence-based hybrid protocols demonstrate that strategic integration of automated and human grading can reduce costs by 77% while maintaining quality standards. With Gemini costing 34× less than ChatGPT, we show how automated formative feedback becomes financially viable even for resource-constrained institutions, potentially democratizing access to timely writing feedback.

These contributions provide actionable, evidence-based guidance for writing program administrators, assessment researchers, and policymakers navigating the integration of LLM technologies in writing assessment contexts.
