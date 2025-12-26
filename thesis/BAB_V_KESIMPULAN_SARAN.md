# BAB V
# KESIMPULAN DAN SARAN

## 5.1 Kesimpulan

Berdasarkan hasil penelitian terhadap 1,958 penilaian esai menggunakan factorial 2×3 experimental design dengan ChatGPT-4o dan Gemini-2.5-Flash pada strategi prompting Zero-shot, Few-shot, dan Lenient (Montgomery, 2017), dapat disimpulkan sebagai berikut:

### 5.1.1 Kesimpulan Utama Per Research Question

**RQ1 - Reliabilitas Sistem AES:**
ChatGPT-4o mendemonstrasikan **excellent reliability** dengan Intraclass Correlation Coefficient (ICC) values 0.942-0.969 dan Fleiss' kappa 0.793-0.838 untuk semua strategi (Koo & Li, 2016). Gemini shows mixed results: Zero-shot achieves good reliability (ICC 0.832, κ 0.530), **namun Few-shot demonstrates POOR reliability (κ 0.346)** dan tidak direkomendasikan untuk deployment. ChatGPT's superior consistency menjadikannya lebih suitable untuk high-stakes assessment applications. Variance decomposition analysis mengungkap bahwa >99.8% variance dalam scores berasal dari genuine essay quality differences, dengan measurement error <0.2%.

**RQ2 - Validitas Sistem AES:**
Sistem AES menunjukkan **strong criterion validity** dengan Pearson correlation values berkisar r=0.69-0.89 (Cohen, 1988). Gemini Lenient mencapai validity tertinggi (r=0.89, MAE=0.28), sementara ChatGPT menunjukkan moderate-to-strong validity (r=0.69-0.76). Semua konfigurasi melampaui minimum acceptable correlation (r≥0.60) untuk educational assessment applications. Classification accuracy analysis menunjukkan balanced performance across grade levels dengan critical errors <12%.

**RQ3 - Konsistensi Sistem AES:**
Analisis Coefficient of Variation (CV) mengkonfirmasi **good-to-moderate consistency** untuk sebagian besar kondisi. ChatGPT Lenient menunjukkan excellent consistency (CV 3.2%), sementara **Gemini Few-shot menunjukkan poor consistency** dan high trial-to-trial variability (κ=0.346). Lenient strategies menunjukkan acceptable variability namun require bias monitoring. Temporal analysis across 10 trials mengkonfirmasi no systematic learning effects untuk ChatGPT, ensuring stable performance over time.

**RQ4 - Perbandingan Model dan Strategi:**
Mixed-Effects ANOVA mengkonfirmasi **statistically significant differences** antar kondisi ($p<0.001$, $\eta^2=0.124$, large effect) (Montgomery, 2017; Field, 2018). Lenient strategies significantly outperform Zero-shot approaches dalam validity ($p<0.001$), namun dengan trade-offs dalam consistency dan bias. **CRITICAL FINDING**: Gemini Few-shot demonstrates POOR reliability (κ=0.346) dan unsuitable untuk assessment despite competitive single-trial accuracy. Post-hoc analysis mengidentifikasi **Gemini Lenient** (highest validity: r=0.89) dan **ChatGPT Lenient** (highest reliability: ICC=0.942) sebagai optimal configurations untuk different use cases.

**RQ5 - Pola Kesalahan Sistematis:**
Comprehensive error pattern analysis mengungkap **predictable dan manageable failure modes** (Ramesh & Sanampudi, 2022). Systematic bias analysis menunjukkan Gemini Zero-shot perfectly balanced (0% net bias, $\chi^2=0.14$, $p=0.708$), sementara Lenient strategies prone terhadap liberal bias (15-19% over-grading, $p<0.001$). Grade-specific error analysis mengkonfirmasi 98.9% predictions within $\pm 1.0$ grade range, dengan major errors (>1.0 grade) extremely rare (1.1%). Content-based analysis mengidentifikasi specific essay characteristics (e.g., argumentasi lemah, struktur tidak jelas) prone terhadap higher errors, enabling targeted quality assurance protocols (Wilson & Roscoe, 2020).

### 5.1.2 Temuan Signifikan

1. **Model Performance Hierarchy:** Gemini Lenient achieves highest validity (Pearson r=0.89, MAE=0.28), outperforming ChatGPT (r=0.69-0.76, MAE=0.38-0.65). However, ChatGPT demonstrates superior test-retest reliability (ICC 0.942-0.969) compared to Gemini's mixed results. **Critical caveat**: Gemini Few-shot unsuitable due to POOR reliability (κ=0.346).

2. **Strategy Effectiveness Ranking:** Lenient strategies achieve best validity (Gemini Lenient r=0.89, ChatGPT Lenient r=0.76) namun dengan systematic over-grading bias requiring monitoring. Zero-shot strategies offer balanced performance. **Few-shot results mixed**: ChatGPT Few-shot acceptable (ICC 0.953, κ 0.793), but **Gemini Few-shot UNSUITABLE** due to poor reliability (κ=0.346, fair agreement only).

3. **Deployment Readiness:** ChatGPT configurations exceed minimum reliability thresholds (ICC >0.90) untuk educational assessment tools (Koo & Li, 2016). **Recommended configurations**: 
   - **Gemini Lenient** untuk highest validity (r=0.89, MAE=0.28, low cost \$0.000/essay)
   - **ChatGPT Lenient** untuk highest reliability (ICC=0.942, κ=0.818, excellent consistency CV=3.2%)
   - **AVOID: Gemini Few-shot** (POOR reliability κ=0.346, unsuitable for assessment)

4. **Safety Profile:** Extremely low critical error rates (<1%) dengan no catastrophic failures (A↔E misclassifications) detected, ensuring student protection dan fairness.

5. **Economic Viability:** Compelling cost-benefit profiles dengan ROI timelines 1-8 months depending pada deployment scale, supporting investment decisions.

### 5.1.3 Kontribusi Teoretis

Penelitian ini memberikan **first comprehensive evaluation** of state-of-the-art Large Language Models (OpenAI, 2024; Google, 2024) untuk Indonesian automated essay scoring dengan rigorous multi-trial experimental design (Montgomery, 2017). Findings extend existing literature yang predominantly focuses pada high-resource languages (Ke & Ng, 2019; Ramesh & Sanampudi, 2022), demonstrating feasibility dan effectiveness of LLM-based AES dalam low-resource language contexts.

**Key theoretical contributions:**
- Evidence-based validation of LLM reliability dan validity untuk educational assessment
- Systematic characterization of prompting strategy effects pada assessment quality
- Comprehensive error pattern taxonomy untuk LLM-based grading systems
- Framework for multi-criteria evaluation of automated assessment tools

### 5.1.4 Kontribusi Praktis

Results provide **actionable deployment guidelines** untuk implementing LLM-based AES dalam Indonesian educational contexts (Dikli, 2006; Ke & Ng, 2019):

- **Optimal Configuration Recommendations:** 
  - **Gemini Lenient** untuk highest validity (r=0.89) OR **ChatGPT Lenient** untuk highest reliability (ICC=0.942)
  - **AVOID: Gemini Few-shot** (POOR reliability, κ=0.346)
- **Quality Assurance Frameworks:** Multi-layered protocols dengan confidence scoring dan human oversight (Wilson & Roscoe, 2020)
- **Risk Management Strategies:** Comprehensive error detection dan mitigation protocols (Ramesh & Sanampudi, 2022)
- **Economic Justification:** ROI analysis supporting investment dalam automated grading technology

**Practical significance untuk pendidikan Indonesia:**
- Potential reduction dalam teacher assessment workload (85-95% time savings)
- Improved grading consistency dan fairness melalui systematic evaluation protocols
- Enhanced feedback frequency enabling more writing practice untuk students
- Scalable solution untuk large-class contexts common dalam Indonesian higher education

---

## 5.2 Saran

### 5.2.1 Saran untuk Implementasi Praktis

**1. Deployment Strategy Recommendations:**
- **Pilot Implementation (Months 1-3):** Start dengan small-scale deployment (100-500 essays, minimum 3 essay topics) using **Gemini Lenient** (for validity) OR **ChatGPT Lenient** (for reliability) configuration untuk minimize risks sambil validating local performance (Creswell & Creswell, 2018). **AVOID Gemini Few-shot**. Target validation metrics: ICC >0.90, Pearson r >0.75, perfect match accuracy >70%.
- **Phased Rollout (Months 4-12):** Gradual expansion following 12-month timeline dengan clear validation checkpoints: Month 4 (500-1000 essays), Month 7 (1000-3000 essays), Month 10 (full deployment). Performance monitoring includes weekly bias audits dan monthly reliability checks (Rogers, 2003).
- **Hybrid Approach:** Maintain human oversight untuk boundary cases (confidence scores <0.8, approximately 15-20% of essays) dan systematic bias monitoring (monthly $\chi^2$ tests for grading distribution) sesuai dengan human-in-the-loop principles (Wilson & Roscoe, 2020).

**2. Quality Assurance Protocols:**
- **Pre-processing Filters:** Implement minimum length requirements ($\geq 100$ words, eliminates ~5-8% submissions) dan topic relevance screening (semantic similarity threshold >0.70) untuk eliminate low-quality inputs
- **Confidence Scoring:** Deploy confidence thresholds untuk automatic routing: high confidence (>0.8, ~65% of essays) direct processing, medium confidence (0.5-0.8, ~20% of essays) flagged review, low confidence (<0.5, ~15% of essays) mandatory human assessment. Monitor flag rates weekly untuk system calibration.
- **Bias Monitoring:** Regular systematic bias analysis (weekly during pilot, monthly post-deployment) dengan automated alerts untuk significant deviations from balanced grading (alert trigger: $|\text{bias}|>10\%$ atau $\chi^2$ dengan $p<0.05$)

**3. Technology Infrastructure:**
- **Redundant Systems:** Multiple model backends (primary: Gemini-2.5-Flash, backup: ChatGPT-4o) untuk reliability dengan automatic failover capabilities (target uptime >99.5%)
- **Load Balancing:** Distributed processing architecture dengan parallel API calls (recommended: 5-10 concurrent requests) untuk handling peak assessment periods (target throughput: 500-1000 essays/hour)
- **Data Security:** Comprehensive privacy protection protocols including encryption at rest (AES-256) dan in transit (TLS 1.3), data anonymization, dan compliance dengan educational data protection requirements (e.g., FERPA, GDPR where applicable)

**4. Change Management:**
- **Faculty Training (Pre-deployment):** Comprehensive training programs (minimum 8 hours, 2 sessions) untuk educators tentang AES capabilities, limitations, dan proper utilization. Include hands-on calibration exercises (target: faculty-AES agreement $\kappa$ >0.70). Provide ongoing support dengan monthly Q&A sessions.
- **Student Communication (Week 1):** Clear explanation tentang AES role dalam assessment process (written guidelines + FAQ), emphasizing hybrid approach dan human oversight availability. Conduct student surveys (baseline dan post-semester) untuk monitoring trust dan acceptance (target satisfaction >75%).
- **Gradual Transition (Months 1-6):** Parallel running dengan human grading untuk 100% of essays selama first 2 months, reducing to 30% random sampling by month 6 untuk building confidence. Document comparative statistics (target agreement $\kappa$ >0.75)

### 5.2.2 Saran untuk Penelitian Lanjutan

**1. Methodological Extensions:**
- **Longitudinal Studies:** Multi-semester evaluation (minimum 3 semesters, 6-12 months duration) untuk assessing long-term reliability, potential model drift, dan temporal validity degradation (Creswell & Creswell, 2018). Track performance metrics monthly (ICC, Fleiss' κ, Pearson r, bias statistics) untuk detecting systematic changes. Target sample: 200+ students, 1000+ unique essays.
- **Cross-Domain Validation:** Testing effectiveness across different subjects (science reports, humanities essays, technical documentation) dan writing genres (argumentative, narrative, expository, descriptive) untuk domain generalizability assessment. Conduct comparative analysis dengan domain-specific rubrics dan expert evaluations. Expected outcome: domain transfer coefficients quantifying cross-context validity.
- **Multi-Language Evaluation:** Extending analysis untuk regional Indonesian languages (Javanese, Sundanese, Balinese) atau bilingual contexts (Indonesian-English code-switching common dalam academic settings). Assess language-specific bias patterns dan cultural fairness across diverse linguistic backgrounds (Ke & Ng, 2019). Partner dengan multilingual education experts untuk rubric adaptation.

**2. Advanced Analytics:**
- **Explainable AI (XAI):** Developing interpretable models yang dapat provide detailed feedback reasoning menggunakan attention visualization, feature attribution techniques (SHAP, LIME), atau chain-of-thought prompting (Wei et al., 2022). Target: generate 3-5 specific, actionable feedback points per essay dengan evidence citations. Validate educational value through instructor surveys (target pedagogical usefulness rating >4.0/5.0).
- **Adaptive Assessment:** Dynamic adjustment of assessment criteria berdasarkan student proficiency levels (beginner, intermediate, advanced) atau learning progression trajectories using item response theory (IRT) frameworks. Implement multi-stage testing dengan difficulty adaptation based on initial performance. Expected outcome: improved measurement precision (standard error reduction 15-20%) across ability spectrum.
- **Personalized Feedback:** Tailored feedback generation berdasarkan individual student writing patterns (common error types, strength areas), learning history (improvement trends), dan target areas identified by instructors. Leverage student writing portfolios untuk contextualized recommendations. Implement A/B testing untuk comparing personalized vs. generic feedback effectiveness (target improvement in revision quality: 20-30% higher).

**3. Technological Improvements:**
- **Prompt Optimization:** Advanced prompt engineering techniques including automated prompt search (genetic algorithms, reinforcement learning), multi-turn prompting strategies, dan domain-specific instruction tuning untuk improving accuracy 5-10% dan reducing systematic bias >50% (Brown et al., 2020; Wei et al., 2022). Conduct systematic ablation studies identifying critical prompt components. Validate optimized prompts through cross-validation ($k=5$ folds).
- **Ensemble Methods:** Combining multiple models (Gemini + ChatGPT) atau strategies (weighted voting, confidence-based selection) untuk robust performance across diverse essay types. Implement stacking ensembles dengan meta-learner training on prediction patterns. Expected improvement: Pearson r increase 0.03-0.05 points, MAE reduction 0.05-0.10 points. Balance accuracy gains against computational costs (target: <2x processing time). **Note**: Exclude Gemini Few-shot from ensemble due to poor reliability.
- **Real-time Calibration:** Dynamic model adjustment berdasarkan continuous performance monitoring using online learning algorithms, periodic re-anchoring dengan expert ratings (monthly calibration sets, 50-100 essays), dan drift detection algorithms (ADWIN, DDM) triggering re-validation protocols (Ramesh & Sanampudi, 2022). Implement automatic alert systems untuk performance degradation (Δ ICC<-0.05 atau Δ Pearson r<-0.05).

**4. Educational Research:**
- **Learning Impact Studies:** Evaluating effects of AI-assisted assessment pada student writing development using quasi-experimental designs dengan control groups (traditional grading) dan treatment groups (AES-assisted). Measure outcomes: writing quality improvement (pre-post essay scores, rubric-based progression), revision effectiveness (draft-to-final improvement rates), dan learning engagement (writing frequency, revision iterations). Target sample: 200+ students across 2 semesters. Expected effect sizes: Cohen's $d=0.3{-}0.5$ untuk writing quality gains (Creswell & Creswell, 2018).
- **Teacher Workflow Analysis:** Studying AES integration effects pada teacher productivity (time savings: target 85-95% grading time reduction), assessment quality (inter-rater reliability improvement), workload redistribution (time reallocation toward feedback quality enhancement), dan pedagogical practices (formative vs. summative emphasis shifts) using mixed-methods approaches combining time-motion studies, surveys ($n>50$ instructors), dan interviews ($n=15{-}20$ in-depth cases).
- **Student Perception Research:** Understanding student attitudes toward automated assessment (trust, fairness perceptions, acceptance rates), impacts pada learning motivation (intrinsic vs. extrinsic motivation scales), writing anxiety levels, dan help-seeking behaviors using validated instruments (MSLQ, PANAS) dengan longitudinal tracking (baseline, mid-semester, end-semester, 3-month follow-up). Target: 300+ student participants dengan demographic stratification ensuring representative sampling. Analyze mediating factors (prior technology experience, academic self-efficacy) influencing acceptance patterns.

### 5.2.3 Saran untuk Institusi Pendidikan

**1. Strategic Planning:**
- **Investment Prioritization:** Consider AES implementation sebagai high-ROI technology investment dengan clear timeline dan milestones
- **Policy Development:** Establish institutional policies untuk ethical AI use dalam assessment, including transparency requirements dan student rights protection
- **Stakeholder Engagement:** Active involvement of faculty, students, dan administrators dalam implementation planning untuk ensuring buy-in dan successful adoption

**2. Capacity Building:**
- **Technical Expertise:** Develop internal technical capacity atau establish partnerships untuk ongoing system maintenance dan optimization
- **Assessment Literacy:** Enhance faculty understanding of assessment best practices dalam AI-augmented environments
- **Data Analytics:** Build institutional capabilities untuk continuous monitoring dan improvement of assessment systems

**3. Quality Standards:**
- **Validation Protocols:** Establish regular validation procedures untuk ensuring continued accuracy dan fairness
- **Ethical Guidelines:** Develop comprehensive ethical frameworks untuk AI use dalam educational assessment
- **Student Support:** Provide additional support mechanisms untuk students who may need accommodation dalam AI-assessed environments

### 5.2.4 Saran untuk Pengembangan Kebijakan

**1. National Education Policy:**
- **Regulatory Framework:** Develop national guidelines untuk AI use dalam educational assessment, ensuring consistency across institutions
- **Quality Standards:** Establish minimum performance requirements untuk automated assessment systems dalam Indonesian education
- **Research Support:** Prioritize funding untuk continued research dalam AI-assisted education untuk maintaining competitive advantage

**2. Ethical Considerations:**
- **Fairness Assurance:** Mandate regular bias auditing untuk all deployed automated assessment systems
- **Transparency Requirements:** Require institutions untuk clearly communicate AI involvement dalam assessment processes
- **Student Rights Protection:** Establish rights untuk human review dalam case of disputed automated assessments

**3. Professional Development:**
- **Educator Training:** National programs untuk training educators dalam effective AI-assisted assessment practices
- **Technical Standards:** Certification programs untuk technical personnel managing educational AI systems
- **Research Collaboration:** Facilitate collaboration antara institutions untuk sharing best practices dan research findings

---

## 5.3 Keterbatasan Penelitian

### 5.3.1 Keterbatasan Metodologis

1. **Sample Scope:** Penelitian terbatas pada 10 selected students dan 70 unique essays (total 2.369 assessments dengan repetisi), yang mungkin tidak fully representative dari broader population diversity dalam Indonesian higher education (Palinkas et al., 2015). Purposive sampling strategy, meskipun appropriate untuk exploratory research, membatasi statistical generalizability. Variasi dalam student proficiency levels (representasi tidak merata across grade levels) dan demographic characteristics tidak fully captured. **Mitigasi:** Future research requires probability sampling dengan minimum 100 students dan 500 unique essays untuk adequate population representation.

2. **Domain Specificity:** Focus pada specific essay types (argumentative essays) dan topics (pendidikan, teknologi, lingkungan) mungkin limit generalizability untuk different writing genres (narrative, descriptive, expository) atau subject areas (technical writing, creative writing, scientific reports). Essay characteristics (length 150-400 words, university level) tidak representative untuk K-12 contexts atau professional writing. **Mitigasi:** Cross-domain validation studies dengan diverse text types dan educational levels diperlukan.

3. **Temporal Constraints:** Evaluation period terbatas (single semester data collection), tidak capturing potential long-term performance trends, model updates, atau seasonal variations dalam essay quality. Rapid evolution dalam LLM technology (model versions updated quarterly) berarti findings potentially time-sensitive. Tidak ada longitudinal tracking untuk student writing development atau system performance degradation over extended periods. **Mitigasi:** Continuous monitoring protocols dengan quarterly re-validation recommended.

### 5.3.2 Keterbatasan Teknis

1. **Model Versions:** Rapid evolution dalam LLM technology (model updates every 3-6 months) berarti findings specific untuk ChatGPT-4o (version gpt-4o-2024-08-06) dan Gemini-2.5-Flash (version gemini-2.0-flash-exp) yang digunakan dalam penelitian ini (OpenAI, 2024; Google, 2024), requiring periodic re-evaluation. Model behavior dapat berubah significantly across versions, affecting reproducibility. Black-box nature dari commercial LLMs membatasi understanding tentang internal decision-making processes. **Mitigasi:** Version pinning dalam production systems dan quarterly performance validation dengan latest model versions.

2. **Infrastructure Dependency:** Performance results based pada specific API configurations (temperature 0.1, top_p 0.95, max_tokens 2000) dan may vary dengan different technical implementations. API latency variability (observed range: 2.5-8.3 seconds per request) affects scalability projections. Network reliability dan geographic API endpoint proximity influence real-world performance. Rate limiting constraints (ChatGPT: 10,000 TPM, Gemini: 2,000 RPM) impose throughput ceilings. **Mitigasi:** Load testing dengan production-equivalent infrastructure dan redundant API configurations.

3. **Language Nuances:** Potential limitations dalam capturing subtle Indonesian language nuances (idioms, colloquialisms, regional variations), cultural context (lokal references, indigenous concepts), atau code-switching behaviors (Indonesian-English mixing common dalam academic writing) yang may affect assessment accuracy (Ke & Ng, 2019). LLM training data predominantly English-centric dapat introduce systematic biases dalam non-English contexts. Rubric interpretations may reflect Western educational paradigms tidak fully aligned dengan Indonesian pedagogical traditions. **Mitigasi:** Cultural adaptation studies dan rubric localization dengan Indonesian education experts.

### 5.3.3 Keterbatasan Praktis

1. **Cost Considerations:** Economic analysis based pada current API pricing (ChatGPT-4o: \$5/\$15 per 1M tokens, Gemini-2.5-Flash: \$0.075/\$0.30 per 1M tokens) yang subject untuk significant changes, potentially affecting long-term viability projections. ROI calculations (1-8 months payback period) assume stable pricing dan tidak account untuk potential price increases, discount discontinuations, atau competitive market shifts. Hidden costs (infrastructure, training, maintenance) mungkin underestimated. Smaller institutions dengan limited budgets may face adoption barriers. **Mitigasi:** Flexible licensing agreements, cost-benefit re-analysis annually, dan exploring open-source alternatives untuk budget-constrained contexts.

2. **Regulatory Environment:** Recommendations developed dalam current regulatory context (Indonesian education regulations, data privacy laws) yang may evolve, requiring policy adaptations. Absence of national AI-in-education guidelines creates uncertainty untuk compliance requirements. International data transfer regulations (for cloud-based APIs) may impose legal constraints. Student data protection requirements (consent, storage, retention) require careful navigation. Accreditation bodies may develop new standards untuk AI-assisted assessment validation. **Mitigasi:** Proactive engagement dengan policymakers, flexible implementation designs accommodating regulatory changes.

3. **Institutional Variability:** Implementation challenges may vary significantly across different institutional contexts (university vs K-12, public vs private, urban vs rural), available resources (technical infrastructure, IT support, faculty training budgets), dan technical capabilities (API integration expertise, data analytics capacity). Cultural resistance terhadap AI adoption among faculty atau students dapat impede deployment success. Organizational readiness factors (change management capacity, leadership support, existing technology infrastructure) critically influence outcomes. Socioeconomic disparities dalam institutional resources may create unequal access patterns. **Mitigasi:** Context-specific implementation assessments, tiered deployment strategies accommodating diverse institutional capabilities, dan shared resource consortia untuk smaller institutions.

4. **Ethical and Social Implications:** Potential unintended consequences including over-reliance pada automated systems reducing human expertise development, algorithmic bias perpetuating existing educational inequalities, student gaming behaviors exploiting system weaknesses, dan psychological impacts of AI assessment pada student motivation dan self-efficacy. Transparency limitations dalam commercial LLMs raise accountability concerns. Long-term effects pada writing pedagogy dan assessment literacy remain uncertain. **Mitigasi:** Ongoing ethical monitoring, maintaining human expertise development pathways, bias auditing protocols, dan comprehensive impact assessment studies.

---

## 5.4 Penutup

Penelitian ini telah memberikan comprehensive evaluation terhadap feasibility dan effectiveness Large Language Models untuk automated essay scoring dalam konteks pendidikan Indonesia. Evidence-based findings mendukung optimistic outlook untuk practical deployment dengan appropriate safeguards dan quality assurance protocols.

**Key takeaway:** LLM-based automated essay scoring represents viable dan valuable technology untuk enhancing assessment efficiency dan consistency dalam Indonesian educational contexts, dengan empirical evidence supporting **ChatGPT reliability** (ICC 0.942-0.969) dan **Gemini Lenient validity** (r=0.89). Success deployment requires careful attention untuk model selection (**Gemini Lenient** for validity OR **ChatGPT Lenient** for reliability; **AVOID Gemini Few-shot** due to poor reliability κ=0.346), robust quality assurance frameworks (multi-layered validation dengan confidence thresholds dan human oversight untuk 15-20% flagged cases), dan thoughtful change management practices (phased 12-month rollout dengan comprehensive faculty training dan continuous monitoring).

**Future directions:** Continued research dan development dalam AI-assisted educational assessment akan enable more sophisticated, personalized, dan effective learning environments (Dikli, 2006; Ke & Ng, 2019). Priority research areas include: (1) longitudinal impact studies pada student writing development, (2) cross-cultural validity investigations untuk diverse Indonesian contexts, (3) advanced explainable AI untuk detailed feedback generation, dan (4) adaptive assessment systems responding to individual learning trajectories. Indonesian institutions positioned untuk leveraging this technology dengan proper planning (minimum 3-month pilot), strategic investment (estimated ROI 1-8 months depending on scale), dan sustained commitment untuk maintaining educational quality dan student welfare.

**Implikasi Kebijakan:** Findings mendukung development of national guidelines untuk AI-assisted educational assessment, including minimum performance standards (ICC >0.90 for reliability, Pearson r >0.75 for validity, Fleiss' κ >0.70 for consistency), mandatory bias auditing protocols (quarterly reviews), mandatory reliability testing (multi-trial evaluation), dan transparency requirements (clear disclosure of AI involvement dalam grading processes). **Critical requirement**: Exclude models/strategies with poor reliability (κ <0.40). Policymakers should consider incentive programs untuk institutional adoption, particularly for under-resourced institutions, while establishing oversight mechanisms ensuring ethical implementation dan student rights protection.

The journey toward AI-augmented education requires sustained collaboration antara researchers, educators, technologists, dan policymakers untuk ensuring that technological advances serve educational goals while maintaining fundamental values of fairness, transparency, dan student-centered development (Creswell & Creswell, 2018). This research provides empirical foundation dan practical frameworks untuk that important work, demonstrating that dengan appropriate safeguards dan evidence-based implementation, LLM-based AES dapat meaningfully contribute toward addressing assessment challenges dalam Indonesian higher education while preserving—and potentially enhancing—educational quality dan equity.

---

**AKHIR BAB V**