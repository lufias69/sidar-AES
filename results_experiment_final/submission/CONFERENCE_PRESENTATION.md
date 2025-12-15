# Conference Presentation Script
## Large Language Models for Automated Essay Scoring: A Comprehensive Study

**Duration:** 15-20 minutes  
**Target:** AERA, EDM, or AI in Education conferences  
**Format:** ~20 slides with presenter notes

---

## Slide 1: Title Slide

### Visual Elements
```
Large Language Models for Automated Essay Scoring:
A Comprehensive Validity, Reliability, and Error Analysis Study

[Visual: Split image showing essay on left, AI brain graphic on right]

Presenter Name¹, Co-author Name²
¹ Department of Education, University X
² Department of Computer Science, University Y

Conference Name | December 2024
```

### Presenter Notes
"Good morning/afternoon. Today I'll present our comprehensive evaluation of Large Language Models for automated essay scoring. This study addresses a critical question in educational technology: Can AI systems reliably grade student writing?"

**[Timing: 0:00-0:30]**

---

## Slide 2: Research Motivation

### Visual Elements
```
THE GRADING BOTTLENECK

📚 Challenge:
   • Teachers spend 30-40% of time grading
   • Feedback delayed by days or weeks
   • Limits formative assessment opportunities

🤖 Promise of AI:
   • Instant feedback for students
   • Scalable personalized learning
   • Free teacher time for instruction

❓ Research Gap:
   • Most studies: English-only, small samples
   • Limited reliability analysis
   • Unclear practical viability
```

### Presenter Notes
"Essay grading is time-intensive. A typical teacher might spend 15 minutes per essay—that's 7.5 hours for just 30 students. This limits how often students can practice writing and receive feedback.

AI systems promise instant feedback, but we need rigorous evaluation. Most existing studies focus on English essays with small samples and don't examine consistency. Our study fills this gap."

**[Timing: 0:30-2:00]**

---

## Slide 3: Research Questions

### Visual Elements
```
FIVE RESEARCH QUESTIONS

RQ1: VALIDITY
     How accurately do LLMs grade essays compared to expert humans?

RQ2: RELIABILITY  
     How consistently do LLMs grade the same essay across multiple trials?

RQ3: MODEL COMPARISON
     Does ChatGPT or Gemini perform better?

RQ4: ERROR ANALYSIS
     What types of grading errors do LLMs make?

RQ5: PRACTICAL IMPLICATIONS
     What are the cost-benefit trade-offs for real-world deployment?
```

### Presenter Notes
"Our study addresses five comprehensive questions. First, validity—do AI grades match expert human grades? Second, reliability—if we run the same essay twice, do we get consistent results? Third, we compare two leading LLMs: ChatGPT and Gemini. Fourth, we analyze error patterns—are mistakes random or systematic? Finally, we examine practical considerations: cost, speed, and deployment strategies."

**[Timing: 2:00-3:30]**

---

## Slide 4: Methodology Overview

### Visual Elements
```
COMPREHENSIVE EXPERIMENTAL DESIGN

📊 SCALE:
   • 4,473 automated gradings
   • 16 carefully selected students
   • 7 argumentative essay questions
   • 10 trials per essay × strategy

🤖 MODELS & STRATEGIES:
   Model              Strategy
   ────────────────  ──────────────
   ChatGPT-4o    →   Zero-shot
                 →   Few-shot (3 examples)
                 →   Lenient prompting
   
   Gemini-2.5-Flash → Zero-shot
                    → Few-shot (3 examples)
                    → Lenient prompting

✅ GOLD STANDARD:
   • 2 expert raters (10+ years experience)
   • ICC = 0.75 (good reliability)
   • 5-point × 5-dimension analytic rubric
```

### Presenter Notes
"We designed a large-scale experiment with over 4,400 gradings. We selected 10 students representing the full grade range, and each wrote essays for 7 different argumentative prompts.

Crucially, we tested each essay 10 times per strategy to measure consistency—something no prior study has done at this scale.

We evaluated two state-of-the-art LLMs with three prompting strategies: zero-shot with just the rubric, few-shot with example essays, and lenient prompting that encourages generosity.

Our gold standard: two expert teachers with over 10 years of experience, achieving good inter-rater reliability."

**[Timing: 3:30-5:30]**

---

## Slide 5: The Rubric

### Visual Elements
```
5-POINT ANALYTIC RUBRIC (5 DIMENSIONS)

Dimension                Weight    Criteria
───────────────────────  ──────   ────────────────────────────
1. Thesis Clarity         30%     Clear, specific position
2. Evidence Quality       25%     Relevant, credible support
3. Essay Structure        20%     Logical organization
4. Counterarguments       15%     Addresses opposing views
5. Language Mechanics     10%     Grammar, vocabulary

Final Grade = Σ (Dimension Score × Weight)

Scale: 1 (Inadequate) → 5 (Excellent)
```

### Presenter Notes
"The rubric evaluates five dimensions with specific weights. Thesis clarity is most important at 30%, followed by evidence at 25%. Structure, counterarguments, and language complete the assessment.

Each dimension is scored 1 to 5, then weighted to produce a final grade. This rubric is typical of university-level argumentative essay assessment."

**[Timing: 5:30-6:30]**

---

## Slide 6: RQ1 Results - Validity

### Visual Elements
```
VALIDITY: HOW ACCURATELY DO LLMs GRADE?

Best Performer: ChatGPT Zero-Shot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Quadratic Weighted Kappa (QWK)
   0.600 [95% CI: 0.562-0.639]
   
   Interpretation: MODERATE agreement

📊 Exact Agreement Rate
   62.42% of grades match exactly
   92.64% within ±1 grade
   
📊 Cohen's Kappa
   0.445 (moderate)

[Visual: Confusion matrix heatmap showing diagonal concentration]

⚠️ Performance varies by grade (see next slide)
```

### Presenter Notes
"For validity, ChatGPT's zero-shot approach performed best with a Quadratic Weighted Kappa of 0.600—indicating moderate agreement with expert humans.

To put this in perspective, 62% of AI grades matched expert grades exactly, and 93% were within one grade level.

This is comparable to having a second human rater, though not yet at expert-level consistency. Importantly, performance varies significantly by grade level, which I'll show next."

**[Timing: 6:30-8:00]**

---

## Slide 7: Confusion Matrix Insights

### Visual Elements
```
GRADE-DEPENDENT PERFORMANCE (ChatGPT Zero-Shot)

Predicted Grade Distribution
           E    D    C    B    A
Gold  E   212  74   10   0    0   Recall: 71.6%  ✓
      D    56  164  15   0    0   Recall: 69.8%  ✓
      C    28  100  144  1    0   Recall: 52.7%  ⚠️
      B     0   2   17   0    1   Recall:  0.0%  ❌
      A     0   0   0    0    0   Recall:  N/A   ❌

         Prec: Prec: Prec: Prec: Prec:
         71.6% 62.4% 77.4%  0%   100%

KEY INSIGHT: Conservative Bias
• High specificity (0.88-1.00): Rarely over-grades
• Variable recall (0.00-0.72): Grade-dependent accuracy
• Class imbalance: Only 20 grade-B essays (2%), zero grade-A
```

### Presenter Notes
"This confusion matrix reveals critical insights. The AI performs well for lower grades—E and D—with 70% recall. It correctly identifies struggling students.

But for grade C, recall drops to 53%, and for grades B and A, it performs very poorly.

Crucially, the AI shows conservative bias: high specificity means it rarely over-grades, but variable recall means it under-grades high performers.

This pattern has practical implications: the AI is safer for identifying low performers than for recognizing excellence."

**[Timing: 8:00-9:30]**

---

## Slide 8: RQ2 Results - Reliability

### Visual Elements
```
RELIABILITY: HOW CONSISTENT ARE LLMs?

10 trials per essay → Measure consistency

📊 Intraclass Correlation (ICC)
   
   ChatGPT Zero:  ICC(2,1) = 0.969  ✓✓✓ (Excellent)
   ChatGPT Few:   ICC(2,1) = 0.953  ✓✓✓ (Excellent)
   Gemini Zero:   ICC(2,1) = 0.832  ✓✓  (Good)
   Gemini Few:    ICC = N/A ❌ (Unstable)
   Gemini Lenient: ICC = N/A ❌ (Unstable)

📊 Fleiss' Kappa (Multi-Rater Agreement)
   ChatGPT Zero: κ = 0.838 (Almost Perfect)
   ChatGPT Few:  κ = 0.793 (Substantial)
   Gemini Zero:  κ = 0.530 (Moderate)
   Gemini Few:   κ = 0.346 ⚠️ (Fair - Unreliable!)
   Gemini Lenient: κ = 0.790 (Substantial)

📊 Cronbach's Alpha
   ChatGPT strategies: α > 0.99 (EXCELLENT)
   Gemini Zero: α = 0.982 (EXCELLENT)

[Visual: Box plot showing tight distributions]

✅ LLMs are HIGHLY consistent (even when wrong)
```

### Presenter Notes
"Reliability reveals critical differences between models. ChatGPT maintained excellent consistency with ICC of 0.969 and Fleiss' kappa of 0.838—exceeding typical human rater reliability of 0.70 to 0.80.

However, Gemini shows concerning variability: zero-shot achieves good reliability (ICC=0.832, κ=0.530), but **few-shot exhibits only fair agreement (κ=0.346)**, indicating unreliable predictions unsuitable for assessment.

This is a crucial finding: Gemini few-shot may achieve competitive accuracy on single trials, but lacks the consistency needed for trustworthy assessment. Students could receive drastically different grades for the same essay across trials.

Important caveat: High reliability doesn't mean high accuracy. But reliability is necessary for trust—unpredictable feedback is pedagogically harmful."

**[Timing: 9:30-11:00]**

---

## Slide 9: RQ3 Results - Model Comparison

### Visual Elements
```
CHATGPT vs. GEMINI: WHO WINS?

STATISTICAL TESTS:

Test                 Result              Winner
─────────────────   ─────────────────   ──────────
Paired t-test       t=2.11, p=0.037*    ChatGPT ✓
Effect size         d=0.199 (small)     
Mean difference     0.04 grades         

McNemar's test      χ²=131, p<0.0001*** ChatGPT ✓
Discordant pairs    206 vs 30           (87% win)

Win-Loss-Tie        236-140-534         ChatGPT ✓
                    (62.8% win rate)    

PRACTICAL TAKEAWAY:
━━━━━━━━━━━━━━━━━
ChatGPT: +0.04 grades higher on average
         Statistically significant but practically small

💰 Cost:  ChatGPT $0.0064  vs  Gemini $0.00021  (34× cheaper)
⚡ Speed: ChatGPT 704/hr    vs  Gemini 193/hr    (3.6× faster)

Choice depends on priority: Accuracy vs. Cost
```

### Presenter Notes
"When we pit ChatGPT against Gemini, ChatGPT shows statistically significant superiority across three tests.

However, the effect size is small—just 0.04 grades difference on average. That's about 4% of a grade level.

The more interesting comparison is cost and speed: Gemini is 34 times cheaper at a fraction of a cent per essay, but ChatGPT is 3.6 times faster.

For formative assessment where cost matters, Gemini is attractive. For high-volume grading where speed matters, ChatGPT wins. Both are viable depending on your priorities."

**[Timing: 11:00-12:30]**

---

## Slide 10: RQ4 Results - Error Analysis

### Visual Elements
```
ERROR PATTERNS: WHAT MISTAKES DO LLMs MAKE?

📊 MEAN ABSOLUTE ERROR (MAE)
   
   ChatGPT Zero:    0.442 grades  ✓ (Best)
   ChatGPT Few:     0.509 grades
   Gemini Zero:     0.527 grades
   ChatGPT Lenient: 0.842 grades  ❌ (Worst)

📊 BIAS (Systematic Over/Under-Grading)
   
   Zero-shot:  -0.009 (balanced)     ✓
   Few-shot:   +0.012 (balanced)     ✓
   Lenient:    +0.472 (over-grades)  ⚠️

📊 CRITICAL ERRORS (2+ grades off)
   
   ChatGPT Zero:  6/910  (0.7%)  ✓✓
   ChatGPT Few:   11/905 (1.2%)  ✓
   Gemini Zero:   14/903 (1.5%)  ✓
   Lenient:       110/936 (11.8%) ❌

[Visual: Error distribution histogram]
```

### Presenter Notes
"Error analysis reveals key patterns. ChatGPT's zero-shot approach has the lowest mean absolute error—less than half a grade level on average.

Crucially, zero-shot and few-shot strategies show minimal bias, meaning they're balanced in errors. Lenient prompting, however, systematically over-grades by nearly half a grade.

Critical errors—where the AI is off by 2 or more grades—occur in less than 1% of cases for zero-shot strategies. But lenient prompting has a 12% critical error rate, making it unsuitable for summative assessment.

This confirms that simpler prompting strategies work better than attempts to make the AI more 'generous.'"

**[Timing: 12:30-14:00]**

---

## Slide 11: RQ5 Results - Cost-Benefit

### Visual Elements
```
PRACTICAL IMPLICATIONS: COST & SPEED

💰 COST PER ESSAY
   
   Human Expert:  $1.50     (baseline)
   ChatGPT:       $0.0064   (234× cheaper)  ⬇ 99.6%
   Gemini:        $0.00021  (7,143× cheaper) ⬇ 99.99%

⚡ GRADING SPEED
   
   Human:    5 essays/hour    (baseline)
   ChatGPT:  704 essays/hour  (141× faster)   ⬆
   Gemini:   193 essays/hour  (39× faster)    ⬆

📈 SCALABILITY EXAMPLE (1,000 essays)
   
   Human:     200 hours, $1,500
   ChatGPT:   1.4 hours, $6.40
   Gemini:    5.2 hours, $0.21

⚠️ BUT: Moderate validity (QWK=0.60) requires human oversight
```

### Presenter Notes
"The cost and speed advantages are transformative. At less than a penny per essay, ChatGPT is 234 times cheaper than human grading. Gemini is even more economical at a fraction of a cent.

Speed is equally dramatic: ChatGPT can grade 704 essays per hour versus 5 for a human teacher.

For a class of 1,000 essays, ChatGPT reduces time from 200 hours to 1.4 hours and cost from $1,500 to $6.40.

However—and this is critical—moderate validity means we can't simply replace human grading. The question becomes: How do we combine AI efficiency with human expertise?"

**[Timing: 14:00-15:30]**

---

## Slide 12: Hybrid Protocol Recommendation

### Visual Elements
```
RECOMMENDED: HYBRID HUMAN-AI GRADING PROTOCOL

┌──────────────────────────────────────────┐
│ TIER 1: AUTO-GRADE (50% of essays)      │
│ AI predicts grade 1 or 2                 │
│ → Accept AI grade directly               │
│ → High specificity, low risk             │
│ → Cost: $0.0064/essay                    │
└──────────────────────────────────────────┘
             ↓
┌──────────────────────────────────────────┐
│ TIER 2: SPOT-CHECK (30% of essays)      │
│ AI predicts grade 3                      │
│ → 30% random sample for human review    │
│ → 70% accept AI grade                   │
│ → Cost: $0.45/essay (weighted)          │
└──────────────────────────────────────────┘
             ↓
┌──────────────────────────────────────────┐
│ TIER 3: HUMAN VERIFY (20% of essays)    │
│ AI predicts grade 4 or 5                 │
│ → Mandatory expert verification          │
│ → High stakes require human judgment    │
│ → Cost: $1.50/essay                      │
└──────────────────────────────────────────┘

📊 OVERALL:
   • Average cost: $0.33/essay (77.9% savings)
   • Maintains quality assurance
   • Scales teacher expertise
```

### Presenter Notes
"Based on our confusion matrix analysis, we propose a tiered hybrid protocol.

Tier 1: For grades 1-2, the AI's high specificity means low risk of over-grading. Accept these automatically—covers 50% of essays.

Tier 2: For grade 3, moderate confidence suggests spot-checking. Randomly review 30% by humans. This catches systematic errors without reviewing everything.

Tier 3: For grades 4-5, the AI's poor recall requires mandatory human verification. These are high-stakes grades for students.

Result: 78% cost savings while maintaining quality assurance. The AI handles routine cases; humans focus on complex judgments. This is the realistic path forward—augmentation, not replacement."

**[Timing: 15:30-17:00]**

---

## Slide 13: Key Contributions

### Visual Elements
```
WHAT THIS STUDY ADDS TO THE FIELD

1️⃣ LARGEST RELIABILITY STUDY
   • First to assess LLM consistency with 10 trials
   • ICC > 0.96: LLMs more reliable than humans
   • Critical for practical trust

2️⃣ COMPREHENSIVE ERROR ANALYSIS
   • Confusion matrix reveals grade-dependent performance
   • Conservative bias pattern (safe for low grades)
   • 436 errors categorized by severity

3️⃣ PRACTICAL DEPLOYMENT FRAMEWORK
   • Hybrid protocol with cost-benefit modeling
   • Tier-based strategy leverages AI strengths
   • Realistic pathway for educational adoption

4️⃣ NON-ENGLISH CONTEXT
   • First large-scale Indonesian AES study
   • Demonstrates LLM multilingual capability
   • Expands AES access beyond English dominance

5️⃣ OPEN METHODOLOGY
   • Reproducible protocols and code published
   • De-identified dataset available
   • Supports research community
```

### Presenter Notes
"Our study makes five key contributions. First, this is the largest reliability analysis of LLM grading, demonstrating consistency exceeds human raters.

Second, our comprehensive error analysis provides actionable insights—not just 'it works' or 'it doesn't,' but specifically where and how it performs.

Third, we move beyond accuracy metrics to propose a practical deployment framework that balances cost, quality, and trust.

Fourth, by studying Indonesian essays, we demonstrate LLMs can serve non-English contexts underserved by commercial systems.

Finally, we've made our methodology, code, and data openly available to accelerate research in this space."

**[Timing: 17:00-18:30]**

---

## Slide 14: Limitations

### Visual Elements
```
STUDY LIMITATIONS (Honestly Acknowledged)

⚠️ SAMPLE SIZE
   • 10 students → external validity limited
   • But: 4,473 gradings → internal validity strong
   • Replication needed with larger populations

⚠️ SINGLE LANGUAGE
   • Indonesian only → English generalization unclear
   • Multilingual replication underway

⚠️ ARGUMENTATIVE GENRE
   • Findings may not extend to narrative/creative writing
   • Structured rubrics favor AI performance

⚠️ CLASS IMBALANCE
   • 83% of essays grades 1-3
   • Limited data for grades 4-5 (esp. grade A: n=0)
   • Grade-dependent metrics less reliable at extremes

⚠️ GOLD STANDARD
   • Human ICC = 0.75 (good but not perfect)
   • AI performance ceiling constrained by benchmark

✅ All limitations disclosed in manuscript (Section 6.1)
```

### Presenter Notes
"Research has limitations, and ours are no exception. With 10 students, we prioritize internal validity over population generalization. The large number of gradings supports our conclusions, but replication with diverse samples is needed.

Our Indonesian context limits direct generalization to English, though emerging evidence suggests similar patterns.

The argumentative genre with structured rubrics likely favors AI. Performance may decline for creative writing where subjective judgment dominates.

Class imbalance means we have limited data for high grades, affecting precision of those estimates.

Finally, our human benchmark itself isn't perfect. The AI is compared to realistic, not idealized, human grading.

Importantly, these limitations don't invalidate our findings—they define their scope. We're transparent about what we can and cannot conclude."

**[Timing: 18:30-20:00]**

---

## Slide 15: Implications for Practice

### Visual Elements
```
RECOMMENDATIONS FOR EDUCATORS & POLICYMAKERS

FOR TEACHERS:
✅ Use LLMs for formative assessment and practice
✅ Provide instant feedback on multiple drafts
✅ Focus human time on high-stakes evaluation
❌ Don't use AI alone for summative grades
❌ Don't trust AI for creative/subjective writing

FOR INSTITUTIONS:
✅ Pilot hybrid protocols in low-stakes courses
✅ Invest in teacher training on AI limitations
✅ Establish clear policies on AI grading use
✅ Monitor for bias and fairness regularly
❌ Don't mandate AI to replace human graders
❌ Don't reduce instructional budgets based on AI "savings"

FOR POLICYMAKERS:
✅ Fund research on AI assessment systems
✅ Develop standards for transparency and validation
✅ Ensure student rights to human review
❌ Don't regulate AI grading out of existence
❌ Don't allow unvalidated systems in high-stakes contexts

🎯 CORE PRINCIPLE: Augment, don't automate education
```

### Presenter Notes
"What does this mean for practice? For teachers, LLMs are tools for formative learning—use them to provide instant feedback on practice essays so students can revise multiple times. But maintain human judgment for summative grades.

For institutions, pilot carefully. Train teachers to understand AI limitations, and don't use purported cost savings to reduce instructional budgets. The hybrid protocol requires human oversight.

For policymakers, support research and standards development, but avoid knee-jerk prohibition or blind adoption. Students should have the right to human review, especially for high-stakes decisions.

The core principle: augment human teaching, don't automate it. AI can handle routine feedback, freeing teachers for the complex pedagogical work only humans can do."

**[Timing: 20:00-22:00]**

---

## Slide 16: Future Research Directions

### Visual Elements
```
WHAT'S NEXT?

🔬 PLANNED STUDIES:

1. MULTI-LANGUAGE REPLICATION
   • English, Spanish, Chinese essays
   • Test cross-language validity patterns
   • Timeline: 6 months

2. GENRE COMPARISON
   • Narrative vs. argumentative within-subjects
   • Quantify genre effects on LLM performance
   • Timeline: 4 months

3. REAL-WORLD PILOT
   • Deploy hybrid protocol in 2 courses (n=200 students)
   • Measure student satisfaction, teacher workload, appeals
   • Timeline: 1 semester

4. BIAS AUDIT
   • Large sample (n=200) with demographics
   • Test for gender, SES, language background bias
   • Fairness metrics and mitigation strategies
   • Timeline: 5 months

5. LONGITUDINAL RELIABILITY
   • Re-grade same essays 6 months later
   • Assess model drift and temporal stability
   • Timeline: 7 months

🤝 Collaboration welcome! Contact: [email]
```

### Presenter Notes
"Our study opens several research directions. We're planning multi-language replication to establish generalizability. Genre comparison will quantify how LLMs perform on different writing types.

Most importantly, we're deploying a real-world pilot of the hybrid protocol to assess practical viability—not just accuracy in a lab, but teacher workload, student satisfaction, and system acceptance.

We're also planning a comprehensive bias audit with a larger, diverse sample.

And we'll test temporal reliability—do LLMs remain consistent as models are updated over time?

We welcome collaborators. If your institution is interested in piloting the hybrid protocol or contributing to the multi-language study, please contact us."

**[Timing: 22:00-23:30]**

---

## Slide 17: Conclusion

### Visual Elements
```
KEY TAKEAWAYS

✅ LLMs achieve MODERATE VALIDITY (QWK = 0.600)
   → Comparable to second human rater
   → Not yet expert-level

✅ LLMs demonstrate EXCELLENT RELIABILITY (ICC = 0.969)
   → More consistent than human raters
   → Critical for trust and fairness

✅ Performance is GRADE-DEPENDENT
   → High specificity (safe for low grades)
   → Variable recall (challenges with high grades)
   → Conservative bias overall

✅ HYBRID PROTOCOL is the path forward
   → 77.9% cost savings with quality assurance
   → Leverages AI efficiency + human expertise
   → Realistic deployment strategy

⚖️ AI should AUGMENT, not REPLACE, human judgment
   → Formative assessment: High potential
   → Summative assessment: Human oversight required
   → Teacher training essential

🚀 Future: Scalable, personalized formative assessment
```

### Presenter Notes
"In conclusion, LLMs show promise for automated essay scoring, achieving moderate validity comparable to a second human rater and excellent reliability exceeding typical human consistency.

However, performance varies by grade level, with a conservative bias that's safer for identifying struggling students than recognizing excellence.

The practical path forward is not full automation but a hybrid protocol that saves 78% of costs while maintaining human oversight for high-stakes decisions.

AI should augment human teaching—enabling more frequent practice and feedback—not replace the complex pedagogical judgments only expert teachers can make.

The future isn't AI grading instead of teachers. It's AI empowering teachers to provide better, more personalized formative assessment at scale."

**[Timing: 23:30-25:00]**

---

## Slide 18: Thank You / Q&A

### Visual Elements
```
THANK YOU!

Questions?

────────────────────────────────────────

📧 Contact: researcher@university.edu
🌐 Paper: [DOI link when published]
💾 Data & Code: github.com/username/aes-llm-study
📊 Supplementary Materials: osf.io/xxxxx

────────────────────────────────────────

Scan for full manuscript: [QR code]

Acknowledgments:
• Research participants
• Funding: [Grant name if applicable]
• Co-authors and collaborators

────────────────────────────────────────

Let's discuss:
1. Deployment experiences at your institution
2. Collaboration on future studies
3. Ethical considerations in your context
```

### Presenter Notes
"Thank you for your attention. I'm happy to take questions.

Our full manuscript, supplementary materials, and de-identified dataset are available online. We've also published all our code for complete reproducibility.

I'm especially interested in hearing about deployment experiences from this audience—what works, what doesn't—and potential collaborations.

Let's open it up for questions."

**[Timing: 25:00+]**

---

## Q&A: Anticipated Questions & Responses

### Q1: "Why Indonesian? Your findings might not generalize to English."

**Response:**
"Great question. Indonesian represents an underserved context—commercial AES systems don't support it. While direct generalization requires replication, emerging English-language studies show similar patterns. QWK of 0.60 in Indonesian vs. 0.58-0.76 in recent English studies suggests cross-language consistency. We're planning multi-language replication to formally test this."

---

### Q2: "Your gold standard ICC is only 0.75. Isn't that problematic?"

**Response:**
"Actually, 0.75 is considered 'good reliability' by psychometric standards and typical for essay grading. Unlike multiple-choice items with perfect reliability, essay grading involves subjective judgment. Using a realistic benchmark reflects real-world conditions. The AI is evaluated against the same imperfect standard human graders face in practice—which is the relevant comparison."

---

### Q3: "62% accuracy seems low. When will it be good enough for real use?"

**Response:**
"Context matters. For high-stakes summative assessment, you're right—62% alone isn't sufficient, which is why our hybrid protocol maintains human oversight. But for formative assessment—practice essays where students get multiple chances to revise—62% accuracy with instant feedback is transformative. The question isn't 'is it perfect?' but 'is it useful?' For the right applications, yes."

---

### Q4: "Won't this lead to teacher layoffs?"

**Response:**
"Our research explicitly advocates against replacement. The hybrid protocol requires 20% full human review and 30% spot-checking—that's 50% human involvement. Rather than eliminating teachers, this frees their time for higher-order instruction: small-group conferences, personalized feedback on complex thinking. The goal is to reduce mechanical grading time, not teaching positions."

---

### Q5: "How do you address bias in LLMs?"

**Response:**
"Excellent concern. Our current study didn't detect grade-level bias, but our small sample (n=16) limited subgroup analysis. We're planning a comprehensive bias audit with 200 students and demographic data to test for gender, SES, and language background effects. Ongoing monitoring is essential—which is another reason human oversight remains critical."

---

### Q6: "What about student learning? Does AI feedback help them improve?"

**Response:**
"That's the million-dollar question—and one we haven't answered yet. This study establishes that AI can grade with moderate accuracy and high consistency. The next step is a pedagogical study: Do students who receive instant AI feedback show greater improvement than those with delayed human feedback? That's what our real-world pilot will measure."

---

### Q7: "Why did lenient prompting perform so poorly?"

**Response:**
"Counterintuitive, right? We hypothesized that encouraging the AI to be generous might improve student experience. Instead, it caused systematic over-grading—elevating grades by nearly half a level on average with 12% critical errors. This suggests simpler prompts work better. The AI 'trying to be nice' undermines validity. Lesson learned: Don't anthropomorphize the system."

---

## Presentation Delivery Tips

### Timing Management
- **Total time budget:** 20-25 minutes
- **Core content:** 18-20 minutes (Slides 1-17)
- **Q&A:** 5-10 minutes
- **Buffer:** 2 minutes for technical issues

### Pacing Guidance
- **Slides 1-3:** Slow (setup, motivation)
- **Slides 4-6:** Moderate (methodology, establish credibility)
- **Slides 7-11:** Slow (key results, allow absorption)
- **Slides 12-13:** Moderate (recommendations)
- **Slides 14-17:** Fast (limitations, future work, conclusion)

### Audience Engagement
- **After Slide 6:** "Show of hands—who's tried AI grading in their courses?"
- **After Slide 11:** "I see some surprised faces about the cost numbers—questions so far?"
- **After Slide 12:** "Would this hybrid approach work in your context?"

### Backup Slides (If Time/Questions)
Prepare additional slides for:
1. Detailed statistical tests (RQ3)
2. Per-rubric dimension analysis
3. Example essay with AI vs. human grades
4. Implementation pseudocode for hybrid protocol
5. Budget breakdown for 1,000/10,000/100,000 essays

---

## Conference-Specific Adaptations

### AERA (American Educational Research Association)
- Emphasize: Psychometric rigor, reliability analysis, pedagogical implications
- Audience: Education researchers, measurement specialists
- Tone: Formal, statistical, theory-driven

### EDM (Educational Data Mining)
- Emphasize: Machine learning methods, error analysis, predictive modeling
- Audience: Computer scientists, learning analytics experts
- Tone: Technical, algorithmic, data-driven

### AI in Education (AIED)
- Emphasize: System design, practical deployment, human-AI collaboration
- Audience: Mixed (educators, technologists, designers)
- Tone: Balanced, accessible, innovation-focused

### L@S (Learning at Scale)
- Emphasize: Scalability, cost-benefit, hybrid protocols, infrastructure
- Audience: MOOCs, online learning, ed-tech practitioners
- Tone: Applied, practical, systems-thinking

---

## Visual Design Recommendations

### Color Scheme
- **Primary:** Deep Blue (#1E3A8A) for headers and key points
- **Success:** Green (#10B981) for positive findings (✓)
- **Warning:** Amber (#F59E0B) for cautions (⚠️)
- **Error:** Red (#DC2626) for critical issues (❌)
- **Neutral:** Gray (#6B7280) for supporting text

### Typography
- **Title:** Sans-serif, bold, 32-36pt
- **Headers:** Sans-serif, semibold, 24-28pt
- **Body:** Sans-serif, regular, 18-20pt (legible from back)
- **Code/Data:** Monospace, 16-18pt

### Charts/Graphs
- Confusion matrix: Heatmap with annotations
- Reliability: Box plots showing consistency
- Cost comparison: Bar chart with savings percentage
- Error distribution: Histogram with severity zones
- Performance by strategy: Grouped bar chart

---

## Post-Presentation Actions

### Immediate (Same Day)
- [ ] Share slide deck with interested attendees
- [ ] Collect contact info for collaboration inquiries
- [ ] Note all Q&A questions for manuscript FAQ

### Short-Term (1 Week)
- [ ] Send follow-up emails to potential collaborators
- [ ] Post slides on OSF/ResearchGate
- [ ] Tweet key findings with #AES #EdTech #AI

### Medium-Term (1 Month)
- [ ] Incorporate feedback into manuscript revision
- [ ] Schedule follow-up meetings with pilot institutions
- [ ] Update supplementary materials based on Q&A

---

**Presentation prepared by:** Research Team  
**Version:** 1.0  
**Last updated:** December 15, 2024  
**Status:** Ready for conference delivery
