# Research Highlights

**Maximum 3-5 bullet points, 85 characters each (including spaces)**

---

## Highlights

1. **ChatGPT zero-shot achieves 62% accuracy with excellent consistency (ICC=0.969)**

2. **Gemini few-shot shows poor reliability (κ=0.346), unsuitable despite competitive accuracy**

3. **Lenient prompting causes 45-55% over-grading, unsuitable for summative assessment**

4. **Hybrid grading reduces costs 77% while maintaining quality for critical decisions**

5. **Gemini offers 34× cost savings but requires zero-shot strategy for reliability**

---

## Alternative Highlights (Choose Best 3-5)

### Validity Focus
- ChatGPT zero-shot matches human inter-rater reliability (62% vs 40-60% typical)
- Adjacent agreement (93%) exceeds human graders, with most errors within ±1 grade
- Classification metrics show precision 0.635, recall 0.432, F1 0.377 for ChatGPT

### Reliability Focus
- ChatGPT demonstrates excellent consistency (ICC 0.942-0.969, κ=0.793-0.838)
- Gemini shows variable reliability: zero-shot good (ICC=0.832), few-shot poor (κ=0.346)
- Critical finding: Gemini few-shot unsuitable for assessment despite competitive accuracy
- Cronbach's alpha >0.99 for ChatGPT indicates near-perfect internal consistency

### Error Analysis Focus
- 436 critical errors identified, 93% preventable with confidence thresholds >0.6
- Zero-shot strategies show balanced errors (25% over, 25% under), lenient skews 55%
- Grade 4-5 performance poor (F1<0.05) due to class imbalance requiring human review

### Practical Implications
- Cost per essay: ChatGPT $0.011, Gemini $0.0003; speed: 704 vs 193 essays/hour
- Three-tier protocol: auto-grade 1-2, spot-check 3, human-verify 4-5 saves 77%
- Scalability: 100K essays/semester saves $116,700 annually with hybrid approach

### Methodological Contribution
- First comprehensive confusion matrix analysis of LLM grading with per-grade metrics
- Multi-model, multi-strategy, multi-trial (4,473 gradings) design ensures robustness
- Provides practical decision matrix and protocols for responsible LLM deployment
