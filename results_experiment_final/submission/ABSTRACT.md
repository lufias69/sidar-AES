# Abstract

**Title:** Comparative Evaluation of ChatGPT-4o and Gemini-2.5-Flash for Automated Essay Scoring: A Multi-Strategy Analysis of Reliability, Validity, and Practical Implications

**Authors:** [To be added]

**Keywords:** Automated Essay Scoring, Large Language Models, ChatGPT, Gemini, Educational Assessment, Reliability, Validity, Prompting Strategies

---

## Abstract (250-300 words)

Large language models (LLMs) have emerged as promising tools for automated essay scoring (AES), yet comprehensive empirical validation of their reliability, validity, and practical utility remains limited. This study presents a systematic comparison of ChatGPT-4o and Gemini-2.5-Flash across three prompting strategies (zero-shot, few-shot, and lenient) using 4,473 grading instances from 10 students and 7 essay questions with 10 trials per configuration.

Our findings reveal that ChatGPT zero-shot achieves the highest validity (QWK=0.600 [substantial], 62.4% exact agreement, 92.8% adjacent agreement with expert human grading) and demonstrates excellent consistency (ICC=0.969, Cronbach's \u03b1=0.997, Fleiss' \u03ba=0.838). Classification metrics show ChatGPT maintaining 62.4% accuracy with balanced precision (0.635) and recall (0.432), though performance for high grades (4-5) approaches zero (F1\u22480.000) due to severe class imbalance, necessitating mandatory human review for top-performing essays. Gemini-2.5-Flash achieves moderate validity (QWK=0.457-0.469) at 34\u00d7 lower cost but with critical reliability concerns: Few-shot strategy exhibits unacceptable consistency (\u03ba=0.346, \"fair agreement\") and must be avoided; only Zero-shot is reliable (ICC=0.832, \u03ba=0.530).

Detailed confusion matrix analysis reveals that lenient prompting introduces systematic over-grading bias (45-55% of predictions inflated), rendering it wholly inappropriate for high-stakes summative assessment. Error analysis identifies 436 critical errors (±2 grades), predominantly in boundary cases, with ChatGPT zero-shot showing the lowest error rate (MAE=0.442, 7.3% major errors). Cost-benefit analysis demonstrates that a hybrid grading protocol—automated scoring for grades 1-3 with human verification for grades 4-5—reduces costs by 77% while maintaining quality standards.

These findings provide empirical evidence for strategic LLM deployment in educational assessment: ChatGPT zero-shot for high-stakes summative grading where validity is paramount, and Gemini zero-shot for formative feedback at scale where cost-effectiveness is prioritized. Our confusion matrix insights and tiered grading protocols offer practical frameworks for responsible implementation.

**Word Count:** 289 words
