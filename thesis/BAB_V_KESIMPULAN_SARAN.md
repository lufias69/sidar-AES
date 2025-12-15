# BAB V
# KESIMPULAN DAN SARAN

## 5.1 Kesimpulan

Berdasarkan hasil penelitian comprehensive terhadap 2,369 essay assessments menggunakan factorial 2×3 experimental design dengan ChatGPT-4o dan Gemini-2.5-Flash across Zero-shot, Few-shot, dan Lenient prompting strategies, dapat disimpulkan sebagai berikut:

### 5.1.1 Kesimpulan Utama Per Research Question

**RQ1 - Reliabilitas Sistem AES:**
Kedua model Large Language Model mendemonstrasikan **excellent reliability** dengan Intraclass Correlation Coefficient (ICC) values >0.987 untuk semua kondisi eksperimen. Analisis Cronbach's Alpha mengkonfirmasi internal consistency yang outstanding (α >0.987), substantially melampaui standard reliability thresholds untuk educational assessment tools. Variance decomposition analysis mengungkap bahwa >99.8% variance dalam scores berasal dari genuine essay quality differences, dengan measurement error <0.2%, menunjukkan sistem yang highly dependable untuk practical deployment.

**RQ2 - Validitas Sistem AES:**
Sistem AES menunjukkan **strong criterion validity** dengan Quadratic Weighted Kappa (QWK) values berkisar 0.691-0.812. Gemini-2.5-Flash mencapai kategori "Almost Perfect Agreement" (QWK >0.80) untuk Zero-shot dan Few-shot conditions, sementara ChatGPT-4o consistent dalam kategori "Substantial Agreement" (0.60-0.80). Pearson correlations dengan human expert judgments strong (r >0.78), dan classification accuracy analysis menunjukkan balanced performance across grade levels dengan minimal critical errors (<1%).

**RQ3 - Konsistensi Sistem AES:**
Analisis Coefficient of Variation (CV) mengkonfirmasi **excellent-to-good consistency** untuk semua kondisi (mean CV 5.8%-12.4%). Gemini Few-shot menunjukkan consistency terbaik (CV 5.8%), diikuti Gemini Zero-shot (CV 6.2%). Lenient strategies menunjukkan higher variability namun remain within acceptable deployment thresholds. Temporal analysis across 10 trials mengkonfirmasi no systematic learning effects atau degradation, ensuring stable performance over time.

**RQ4 - Perbandingan Model dan Strategi:**
Mixed-Effects ANOVA mengkonfirmasi **statistically significant differences** dengan Gemini superior to ChatGPT (p<0.001, η²=0.124, large effect). Few-shot dan Lenient strategies significantly outperform Zero-shot approaches (p<0.001, η²=0.075, medium effect). Interaction effects antara model dan strategi significant namun small (η²=0.010), suggesting consistent strategy effects across both models. Post-hoc analysis mengidentifikasi Gemini Few-shot sebagai optimal configuration.

**RQ5 - Pola Kesalahan Sistematis:**
Comprehensive error pattern analysis mengungkap **predictable dan manageable failure modes**. Systematic bias analysis menunjukkan Gemini Zero-shot perfectly balanced (0% net bias), sementara Lenient strategies prone terhadap liberal bias (15-19% over-grading). Grade-specific error analysis mengkonfirmasi 98.9% predictions within ±1.0 grade range, dengan major errors (>1.0 grade) extremely rare (1.1%). Content-based analysis mengidentifikasi specific essay characteristics prone terhadap higher errors, enabling targeted quality assurance protocols.

### 5.1.2 Temuan Signifikan

1. **Model Performance Hierarchy:** Gemini-2.5-Flash > ChatGPT-4o across all evaluation metrics, dengan consistent margin 0.06-0.10 points dalam QWK values dan 2-3% higher accuracy rates.

2. **Strategy Effectiveness Ranking:** Few-shot > Zero-shot > Lenient dalam terms of balanced performance, reliability, dan consistency. Lenient strategies effective untuk supportive feedback namun require bias monitoring.

3. **Deployment Readiness:** All configurations exceed minimum reliability thresholds, dengan Gemini Few-shot optimal untuk most educational applications, achieving 84.1% perfect accuracy dan QWK 0.812.

4. **Safety Profile:** Extremely low critical error rates (<1%) dengan no catastrophic failures (A↔E misclassifications) detected, ensuring student protection dan fairness.

5. **Economic Viability:** Compelling cost-benefit profiles dengan ROI timelines 1-8 months depending pada deployment scale, supporting investment decisions.

### 5.1.3 Kontribusi Teoretis

Penelitian ini memberikan **first comprehensive evaluation** of state-of-the-art Large Language Models untuk Indonesian automated essay scoring dengan rigorous multi-trial experimental design. Findings extend existing literature yang predominantly focuses pada high-resource languages, demonstrating feasibility dan effectiveness of LLM-based AES dalam low-resource language contexts.

**Key theoretical contributions:**
- Evidence-based validation of LLM reliability dan validity untuk educational assessment
- Systematic characterization of prompting strategy effects pada assessment quality
- Comprehensive error pattern taxonomy untuk LLM-based grading systems
- Framework for multi-criteria evaluation of automated assessment tools

### 5.1.4 Kontribusi Praktis

Results provide **actionable deployment guidelines** untuk implementing LLM-based AES dalam Indonesian educational contexts:

- **Optimal Configuration Recommendations:** Gemini Few-shot untuk balanced performance
- **Quality Assurance Frameworks:** Multi-layered protocols dengan confidence scoring dan human oversight
- **Risk Management Strategies:** Comprehensive error detection dan mitigation protocols
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
- **Pilot Implementation:** Start dengan small-scale deployment (100-500 essays) using Gemini Few-shot configuration untuk minimize risks sambil validating local performance
- **Phased Rollout:** Gradual expansion following 12-month timeline dengan clear validation checkpoints dan performance monitoring
- **Hybrid Approach:** Maintain human oversight untuk boundary cases (confidence scores <0.8) dan systematic bias monitoring

**2. Quality Assurance Protocols:**
- **Pre-processing Filters:** Implement minimum length requirements (≥100 words) dan topic relevance screening untuk eliminate low-quality inputs
- **Confidence Scoring:** Deploy confidence thresholds untuk automatic routing: high confidence (>0.8) direct processing, medium confidence (0.5-0.8) flagged review, low confidence (<0.5) human assessment
- **Bias Monitoring:** Regular systematic bias analysis dengan automated alerts untuk significant deviations from balanced grading

**3. Technology Infrastructure:**
- **Redundant Systems:** Multiple model backends untuk reliability dan failover capabilities
- **Load Balancing:** Distributed processing architecture untuk handling peak assessment periods
- **Data Security:** Comprehensive privacy protection protocols sesuai dengan educational data protection requirements

**4. Change Management:**
- **Faculty Training:** Comprehensive training programs untuk educators tentang AES capabilities, limitations, dan proper utilization
- **Student Communication:** Clear explanation tentang AES role dalam assessment process untuk maintaining trust dan transparency
- **Gradual Transition:** Parallel running dengan human grading selama initial phases untuk building confidence

### 5.2.2 Saran untuk Penelitian Lanjutan

**1. Methodological Extensions:**
- **Longitudinal Studies:** Multi-semester evaluation untuk assessing long-term reliability dan potential model drift
- **Cross-Domain Validation:** Testing effectiveness across different subjects (science, humanities, technical writing) untuk domain generalizability
- **Multi-Language Evaluation:** Extending analysis untuk regional Indonesian languages atau bilingual contexts

**2. Advanced Analytics:**
- **Explanatory AI:** Developing interpretable models yang dapat provide detailed feedback reasoning untuk educational value
- **Adaptive Assessment:** Dynamic adjustment of assessment criteria berdasarkan student proficiency levels atau learning progression
- **Personalized Feedback:** Tailored feedback generation berdasarkan individual student writing patterns dan improvement areas

**3. Technological Improvements:**
- **Prompt Optimization:** Advanced prompt engineering techniques untuk further improving accuracy dan reducing bias
- **Ensemble Methods:** Combining multiple models atau strategies untuk robust performance across diverse essay types
- **Real-time Calibration:** Dynamic model adjustment berdasarkan continuous performance monitoring

**4. Educational Research:**
- **Learning Impact Studies:** Evaluating effects of AI-assisted assessment pada student writing development dan learning outcomes
- **Teacher Workflow Analysis:** Studying how AES integration affects teacher productivity dan pedagogical practices
- **Student Perception Research:** Understanding student attitudes towards automated assessment dan impacts pada learning motivation

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

1. **Sample Scope:** Penelitian terbatas pada 10 selected students dan 70 unique essays, yang mungkin tidak fully representative dari broader population diversity dalam Indonesian higher education.

2. **Domain Specificity:** Focus pada specific essay types dan topics mungkin limit generalizability untuk different writing genres atau subject areas.

3. **Temporal Constraints:** Evaluation period terbatas, tidak capturing potential long-term performance trends atau seasonal variations dalam essay quality.

### 5.3.2 Keterbatasan Teknis

1. **Model Versions:** Rapid evolution dalam LLM technology berarti findings specific untuk ChatGPT-4o dan Gemini-2.5-Flash versions yang digunakan, requiring periodic re-evaluation.

2. **Infrastructure Dependency:** Performance results based pada specific API configurations dan may vary dengan different technical implementations.

3. **Language Nuances:** Potential limitations dalam capturing subtle Indonesian language nuances atau cultural context yang may affect assessment accuracy.

### 5.3.3 Keterbatasan Praktis

1. **Cost Considerations:** Economic analysis based pada current API pricing yang subject untuk change, potentially affecting long-term viability projections.

2. **Regulatory Environment:** Recommendations developed dalam current regulatory context yang may evolve, requiring policy adaptations.

3. **Institutional Variability:** Implementation challenges may vary significantly across different institutional contexts, resources, dan technical capabilities.

---

## 5.4 Penutup

Penelitian ini telah memberikan comprehensive evaluation terhadap feasibility dan effectiveness Large Language Models untuk automated essay scoring dalam konteks pendidikan Indonesia. Evidence-based findings mendukung optimistic outlook untuk practical deployment dengan appropriate safeguards dan quality assurance protocols.

**Key takeaway:** LLM-based automated essay scoring represents viable dan valuable technology untuk enhancing assessment efficiency dan consistency dalam Indonesian educational contexts. Success deployment requires careful attention untuk model selection (Gemini Few-shot recommended), robust quality assurance frameworks, dan thoughtful change management practices.

**Future direction:** Continued research dan development dalam AI-assisted educational assessment akan enable more sophisticated, personalized, dan effective learning environments. Indonesian institutions positioned untuk leveraging this technology dengan proper planning, investment, dan commitment untuk maintaining educational quality dan student welfare.

The journey toward AI-augmented education requires collaboration antara researchers, educators, technologists, dan policymakers untuk ensuring that technological advances serve educational goals while maintaining fundamental values of fairness, transparency, dan student development. This research provides foundation untuk that important work.

---

**AKHIR BAB V**