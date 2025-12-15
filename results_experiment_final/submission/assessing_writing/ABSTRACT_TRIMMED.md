# Abstract (Trimmed for Assessing Writing - 250 words max)

**Title:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring: A Multi-Strategy Analysis of Reliability, Validity, and Practical Implications

**Keywords:** Automated Essay Scoring, Large Language Models, Educational Assessment, Reliability, Validity, Hybrid Grading

---

## Abstract (246 words)

Large language models (LLMs) have emerged as promising tools for automated essay scoring (AES), yet comprehensive empirical validation of their reliability, validity, and practical utility remains limited. This study presents a systematic comparison of ChatGPT-4o and Gemini-2.5-Flash across three prompting strategies using 4,473 grading instances from 10 students and 7 essay questions with 10 trials per configuration.

ChatGPT zero-shot achieves the highest validity (QWK=0.600 [substantial], 62.4% exact agreement, 92.8% adjacent agreement) and demonstrates excellent consistency (ICC=0.969, Cronbach's α=0.997, Fleiss' κ=0.838). Classification metrics show 62.4% accuracy with balanced precision (0.635) and recall (0.432), though performance for high grades (4-5) approaches zero (F1≈0.000) due to severe class imbalance, necessitating mandatory human review. Gemini-2.5-Flash achieves moderate validity (QWK=0.457-0.469) at 34× lower cost but with critical reliability concerns: Few-shot strategy exhibits unacceptable consistency (κ=0.346) and must be avoided; only Zero-shot is reliable (ICC=0.832, κ=0.530).

Confusion matrix analysis reveals lenient prompting introduces systematic over-grading bias (45-55% of predictions inflated), rendering it wholly inappropriate for high-stakes summative assessment. Error analysis identifies 436 critical errors (±2 grades) with ChatGPT zero-shot showing lowest error rate (MAE=0.442, 7.3% major errors). A hybrid grading protocol—automated scoring for grades 1-3 with human verification for grades 4-5—reduces costs by 77% while maintaining quality standards.

These findings provide empirical evidence for strategic LLM deployment: ChatGPT zero-shot for high-stakes summative grading where validity is paramount, and Gemini zero-shot for formative feedback at scale where cost-effectiveness is prioritized.

---

**Word Count:** 246 words ✓ (within 150-250 limit)
