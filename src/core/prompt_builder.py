"""
Prompt Builder for AI Agents
Generates dynamic prompts with rubric and essay information
"""

from typing import Dict, Optional
from src.core.rubric import Rubric


class PromptBuilder:
    """Builds prompts for AI essay grading"""
    
    def __init__(self, rubric: Rubric, system_prompt: Optional[str] = None, language: str = "indonesian", strategy: str = "zero-shot"):
        self.rubric = rubric
        self.language = language.lower()
        self.strategy = strategy.lower()
        self.system_prompt = system_prompt or self._default_system_prompt()
    
    def _default_system_prompt(self) -> str:
        """Default system prompt based on strategy"""
        base_prompt = self._get_base_system_prompt()
        strategy_addition = self._get_strategy_system_prompt()
        
        if strategy_addition:
            return f"{base_prompt}\n\n{strategy_addition}"
        return base_prompt
    
    def _get_base_system_prompt(self) -> str:
        """Get base system prompt without strategy modifications"""
        if self.language == "indonesian":
            return """Anda adalah penilai esai ahli dengan pengalaman bertahun-tahun dalam penilaian pendidikan.
Tugas Anda adalah mengevaluasi esai mahasiswa berdasarkan rubrik yang diberikan dengan beberapa kriteria.

Untuk setiap kriteria, Anda harus:
1. Memberikan nilai (A, B, C, atau D/E)
2. Memberikan justifikasi detail (2-4 kalimat) yang menjelaskan MENGAPA Anda memberikan nilai tersebut
3. Merujuk pada aspek spesifik dari esai dalam justifikasi Anda
4. Bersikap objektif, adil, dan konsisten

Respons Anda harus dalam format JSON yang valid. Semua justifikasi dan komentar harus dalam Bahasa Indonesia."""
        else:  # English
            return """You are an expert essay grader with years of experience in educational assessment.
Your task is to evaluate student essays based on a provided rubric with multiple criteria.

For each criterion, you must:
1. Assign a grade (A, B, C, or D/E)
2. Provide a detailed justification (2-4 sentences) explaining WHY you gave that grade
3. Reference specific aspects of the essay in your justification
4. Be objective, fair, and consistent

Your response must be in valid JSON format."""
    
    def _get_strategy_system_prompt(self) -> str:
        """Get additional system prompt based on strategy"""
        if self.strategy == "strict":
            if self.language == "indonesian":
                return """PENTING - MODE PENILAIAN KETAT:
- Terapkan standar penilaian yang SANGAT TINGGI
- Hanya berikan nilai A jika esai SEMPURNA tanpa cacat
- Berikan nilai lebih rendah jika ada kesalahan atau kelemahan SEKECIL APAPUN
- Fokus pada KELEMAHAN dan KEKURANGAN dalam esai
- Jangan terlalu murah hati dalam memberikan nilai"""
            else:
                return """IMPORTANT - STRICT GRADING MODE:
- Apply VERY HIGH grading standards
- Only give grade A if the essay is PERFECT without flaws
- Give lower grades for ANY mistakes or weaknesses
- Focus on WEAKNESSES and SHORTCOMINGS in the essay
- Do not be too generous with grades"""
        
        elif self.strategy == "lenient":
            if self.language == "indonesian":
                return """PENTING - MODE PENILAIAN LONGGAR:
- Fokus pada KEKUATAN dan usaha mahasiswa
- Berikan nilai lebih tinggi jika mahasiswa menunjukkan pemahaman dasar
- Hargai kreativitas dan usaha yang ditunjukkan
- Hanya berikan nilai D/E jika benar-benar tidak ada usaha
- Bersikap SUPPORTIF dan POSITIF dalam justifikasi"""
            else:
                return """IMPORTANT - LENIENT GRADING MODE:
- Focus on STRENGTHS and student effort
- Give higher grades if student shows basic understanding
- Appreciate creativity and demonstrated effort
- Only give D/E if there's truly no effort
- Be SUPPORTIVE and POSITIVE in justifications"""
        
        return ""
    
    def build_grading_prompt(
        self,
        question: str,
        student_answer: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Build complete grading prompt with strategy support
        
        Args:
            question: The essay question/prompt
            student_answer: Student's essay response
            additional_context: Optional additional instructions
            
        Returns:
            Complete prompt string
        """
        # Get strategy-specific additions
        strategy_instructions = self._get_strategy_instructions()
        strategy_examples = self._get_strategy_examples()
        
        if self.language == "indonesian":
            prompt_parts = [
                "# TUGAS PENILAIAN ESAI\n",
            ]
            
            # Add few-shot examples if applicable
            if strategy_examples:
                prompt_parts.extend(strategy_examples)
                prompt_parts.append("")
            
            prompt_parts.extend([
                "## Pertanyaan:",
                question,
                "",
                "## Jawaban Mahasiswa:",
                student_answer,
                "",
            ])
            
            # Add detailed rubric for detailed-rubric strategy
            if self.strategy == "detailed-rubric":
                prompt_parts.extend([
                    "## Rubrik Penilaian (Detail):",
                    self._get_detailed_rubric_indonesian(),
                    "",
                ])
            else:
                prompt_parts.extend([
                    "## Rubrik Penilaian:",
                    self.rubric.to_prompt_text(),
                    "",
                ])
            
            prompt_parts.extend([
                "## Instruksi:",
            ])
            
            # Add strategy-specific instructions
            if strategy_instructions:
                prompt_parts.extend(strategy_instructions)
                prompt_parts.append("")
            
            prompt_parts.extend([
                "Evaluasi jawaban mahasiswa sesuai dengan rubrik di atas.",
                "Untuk SETIAP kriteria, berikan:",
                "1. Nilai (A, B, C, atau D/E)",
                "2. Justifikasi detail (2-4 kalimat) yang:",
                "   - Menjelaskan MENGAPA Anda memberikan nilai tersebut",
                "   - Merujuk pada aspek spesifik dari jawaban mahasiswa",
                "   - Menyebutkan indikator rubrik mana yang terpenuhi atau tidak",
                "   - Bersifat konstruktif dan spesifik (bukan generik)",
                "",
            ])
        else:  # English
            prompt_parts = [
                "# ESSAY GRADING TASK\n",
            ]
            
            # Add few-shot examples if applicable
            if strategy_examples:
                prompt_parts.extend(strategy_examples)
                prompt_parts.append("")
            
            prompt_parts.extend([
                "## Question/Prompt:",
                question,
                "",
                "## Student's Answer:",
                student_answer,
                "",
            ])
            
            # Add detailed rubric for detailed-rubric strategy
            if self.strategy == "detailed-rubric":
                prompt_parts.extend([
                    "## Evaluation Rubric (Detailed):",
                    self._get_detailed_rubric_english(),
                    "",
                ])
            else:
                prompt_parts.extend([
                    "## Evaluation Rubric:",
                    self.rubric.to_prompt_text(),
                    "",
                ])
            
            prompt_parts.extend([
                "## Instructions:",
            ])
            
            # Add strategy-specific instructions
            if strategy_instructions:
                prompt_parts.extend(strategy_instructions)
                prompt_parts.append("")
            
            prompt_parts.extend([
                "Evaluate the student's answer according to the rubric above.",
                "For EACH criterion, provide:",
                "1. A grade (A, B, C, or D/E)",
                "2. A detailed justification (2-4 sentences) that:",
                "   - Explains WHY you assigned that grade",
                "   - References specific aspects from the student's answer",
                "   - Mentions which rubric indicators were met or not met",
                "   - Is constructive and specific (not generic)",
                "",
            ])
        
        if additional_context:
            if self.language == "indonesian":
                prompt_parts.extend([
                    "## Konteks Tambahan:",
                    additional_context,
                    ""
                ])
            else:
                prompt_parts.extend([
                    "## Additional Context:",
                    additional_context,
                    ""
                ])
        
        if self.language == "indonesian":
            prompt_parts.extend([
                "## Format Output yang Diperlukan:",
                "Responlah dengan HANYA JSON valid dalam struktur berikut:",
                "```json",
                "{",
                '  "scores": {',
            ])
        else:
            prompt_parts.extend([
                "## Required Output Format:",
                "Respond with ONLY valid JSON in this exact structure:",
                "```json",
                "{",
                '  "scores": {',
            ])
        
        # Add example structure for each criterion
        for i, criterion_name in enumerate(self.rubric.criteria.keys()):
            comma = "," if i < len(self.rubric.criteria) - 1 else ""
            prompt_parts.append(f'    "{criterion_name}": {{')
            prompt_parts.append('      "grade": "A|B|C|D/E",')
            prompt_parts.append('      "justification": "Detailed 2-4 sentence explanation here"')
            prompt_parts.append(f'    }}{comma}')
        
        if self.language == "indonesian":
            prompt_parts.extend([
                "  },",
                '  "overall_comment": "Komentar keseluruhan singkat opsional (1-2 kalimat)"',
                "}",
                "```",
                "",
                "PENTING:",
                "- Kembalikan HANYA JSON, tanpa teks lain",
                "- Pastikan semua nama kriteria sesuai persis seperti yang ditampilkan di atas",
                "- Justifikasi harus spesifik untuk esai INI, bukan generik",
                "- Nilai harus salah satu dari: A, B, C, D/E",
                "- Semua justifikasi dan overall_comment HARUS dalam Bahasa Indonesia",
            ])
        else:
            prompt_parts.extend([
                "  },",
                '  "overall_comment": "Optional brief overall assessment (1-2 sentences)"',
                "}",
                "```",
                "",
                "IMPORTANT:",
                "- Return ONLY the JSON, no other text",
                "- Ensure all criterion names match exactly as shown above",
                "- Justifications must be specific to THIS essay, not generic",
                "- Grade must be one of: A, B, C, D/E",
            ])
        
        return "\n".join(prompt_parts)
    
    def _get_strategy_instructions(self) -> list:
        """Get strategy-specific instructions"""
        if self.strategy == "cot" or self.strategy == "chain-of-thought":
            if self.language == "indonesian":
                return [
                    "PROSES BERPIKIR STEP-BY-STEP:",
                    "Sebelum memberikan nilai, lakukan analisis bertahap:",
                    "1. BACA: Identifikasi poin-poin utama dalam jawaban",
                    "2. BANDINGKAN: Cocokkan dengan indikator rubrik per kriteria",
                    "3. EVALUASI: Tentukan kekuatan dan kelemahan spesifik",
                    "4. PUTUSKAN: Berikan nilai berdasarkan analisis di atas",
                    "5. JUSTIFIKASI: Jelaskan reasoning Anda dengan jelas",
                ]
            else:
                return [
                    "STEP-BY-STEP THINKING PROCESS:",
                    "Before assigning grades, perform staged analysis:",
                    "1. READ: Identify key points in the answer",
                    "2. COMPARE: Match with rubric indicators per criterion",
                    "3. EVALUATE: Determine specific strengths and weaknesses",
                    "4. DECIDE: Assign grade based on analysis above",
                    "5. JUSTIFY: Explain your reasoning clearly",
                ]
        
        return []
    
    def _get_strategy_examples(self) -> list:
        """Get few-shot examples if applicable"""
        if self.strategy != "few-shot":
            return []
        
        if self.language == "indonesian":
            return [
                "## Contoh Penilaian:",
                "",
                "### Contoh 1:",
                "**Pertanyaan:** Jelaskan teknologi yang Anda gunakan dalam proyek",
                "**Jawaban:** Saya menggunakan Arduino Uno dengan sensor DHT22 untuk mengukur suhu dan kelembaban. Arduino dipilih karena mudah diprogram dan memiliki banyak library pendukung.",
                "**Penilaian:**",
                '- Pemahaman Konten: B ("Menjelaskan teknologi dengan cukup baik, menyebutkan nama spesifik (Arduino Uno, DHT22) dan fungsinya. Namun kurang detail tentang spesifikasi teknis atau alternatif yang dipertimbangkan.")',
                '- Argumen & Bukti: C ("Ada alasan pemilihan teknologi tapi masih sederhana. Perlu penjelasan lebih mendalam tentang trade-offs atau perbandingan dengan opsi lain.")',
                "",
                "### Contoh 2:",
                "**Pertanyaan:** Apa manfaat proyek Anda?",
                "**Jawaban:** Bermanfaat untuk masyarakat.",
                "**Penilaian:**",
                '- Pemahaman Konten: D/E ("Jawaban terlalu singkat dan tidak spesifik. Tidak menjelaskan manfaat konkret atau target pengguna yang jelas.")',
                '- Argumen & Bukti: D/E ("Tidak ada argumen atau bukti pendukung. Pernyataan terlalu umum dan tidak substantif.")',
                "",
                "Sekarang nilai jawaban berikut dengan standar yang sama:",
                ""
            ]
        else:
            return [
                "## Grading Examples:",
                "",
                "### Example 1:",
                "**Question:** Explain the technology you used in your project",
                "**Answer:** I used Arduino Uno with DHT22 sensor to measure temperature and humidity. Arduino was chosen because it's easy to program and has many supporting libraries.",
                "**Assessment:**",
                '- Content Understanding: B ("Explains technology fairly well, mentions specific names (Arduino Uno, DHT22) and their functions. However, lacks detail about technical specifications or alternatives considered.")',
                '- Arguments & Evidence: C ("There is reasoning for technology choice but still simple. Needs deeper explanation about trade-offs or comparison with other options.")',
                "",
                "### Example 2:",
                "**Question:** What are the benefits of your project?",
                "**Answer:** Beneficial for society.",
                "**Assessment:**",
                '- Content Understanding: D/E ("Answer too brief and not specific. Does not explain concrete benefits or clear target users.")',
                '- Arguments & Evidence: D/E ("No supporting arguments or evidence. Statement too general and not substantive.")',
                "",
                "Now grade the following answer with the same standards:",
                ""
            ]
    
    def _get_detailed_rubric_indonesian(self) -> str:
        """Get detailed rubric explanation in Indonesian"""
        lines = [
            "### RUBRIK DETAIL PER KRITERIA:",
            "",
            "**1. Pemahaman Konten (35% bobot)**",
            "",
            "A (Excellent - 4.0):",
            "  - Menunjukkan pemahaman mendalam dan komprehensif",
            "  - Menyebutkan detail teknis spesifik (nama alat, versi, spesifikasi)",
            "  - Menjelaskan konsep dengan akurat dan lengkap",
            "  - Jawaban minimal 5 kalimat substantif",
            "  - Menghubungkan teori dengan aplikasi praktis",
            "",
            "B (Good - 3.0):",
            "  - Menunjukkan pemahaman yang baik dan jelas",
            "  - Menyebutkan teknologi/konsep utama",
            "  - Penjelasan cukup detail tapi bisa lebih mendalam",
            "  - Jawaban minimal 3-4 kalimat",
            "  - Ada beberapa aspek yang kurang dibahas",
            "",
            "C (Fair - 2.0):",
            "  - Pemahaman dasar ada tapi kurang detail",
            "  - Menyebutkan teknologi secara umum tanpa spesifik",
            "  - Penjelasan masih superfisial",
            "  - Jawaban 2-3 kalimat pendek",
            "  - Banyak aspek penting yang terlewat",
            "",
            "D/E (Poor - 1.0):",
            "  - Pemahaman sangat terbatas atau tidak ada",
            "  - Tidak menyebutkan detail konkret",
            "  - Jawaban terlalu singkat (< 2 kalimat)",
            "  - Tidak relevan atau tidak menjawab pertanyaan",
            "",
            "**2. Organisasi & Struktur (25% bobot)**",
            "",
            "A: Struktur sangat jelas, logis, koheren, transisi smooth",
            "B: Struktur baik, cukup logis, transisi cukup jelas",
            "C: Struktur ada tapi agak berantakan, perlu perbaikan",
            "D/E: Tidak terstruktur, sulit diikuti, kacau",
            "",
            "**3. Argumen & Bukti (25% bobot)**",
            "",
            "A: Argumen kuat dengan bukti konkret, contoh spesifik, data jelas",
            "B: Argumen cukup baik, ada bukti tapi bisa lebih kuat",
            "C: Argumen lemah, bukti minim atau tidak relevan",
            "D/E: Tidak ada argumen yang jelas atau bukti",
            "",
            "**4. Gaya Bahasa & Mekanik (15% bobot)**",
            "",
            "A: Bahasa profesional, tata bahasa sempurna, tidak ada typo",
            "B: Bahasa baik, ada 1-2 kesalahan kecil",
            "C: Bahasa cukup tapi ada beberapa kesalahan",
            "D/E: Banyak kesalahan, sulit dipahami",
            "",
        ]
        return "\n".join(lines)
    
    def _get_detailed_rubric_english(self) -> str:
        """Get detailed rubric explanation in English"""
        lines = [
            "### DETAILED RUBRIC PER CRITERION:",
            "",
            "**1. Content Understanding (35% weight)**",
            "",
            "A (Excellent - 4.0):",
            "  - Shows deep and comprehensive understanding",
            "  - Mentions specific technical details (tool names, versions, specifications)",
            "  - Explains concepts accurately and completely",
            "  - Answer minimum 5 substantive sentences",
            "  - Connects theory with practical application",
            "",
            "B (Good - 3.0):",
            "  - Shows good and clear understanding",
            "  - Mentions main technologies/concepts",
            "  - Explanation quite detailed but could be deeper",
            "  - Answer minimum 3-4 sentences",
            "  - Some aspects not fully covered",
            "",
            "C (Fair - 2.0):",
            "  - Basic understanding present but lacking detail",
            "  - Mentions technology generally without specifics",
            "  - Explanation still superficial",
            "  - Answer 2-3 short sentences",
            "  - Many important aspects missed",
            "",
            "D/E (Poor - 1.0):",
            "  - Very limited or no understanding",
            "  - No concrete details mentioned",
            "  - Answer too brief (< 2 sentences)",
            "  - Not relevant or doesn't answer question",
            "",
            "**2. Organization & Structure (25% weight)**",
            "",
            "A: Very clear structure, logical, coherent, smooth transitions",
            "B: Good structure, quite logical, transitions fairly clear",
            "C: Structure exists but somewhat messy, needs improvement",
            "D/E: Unstructured, hard to follow, chaotic",
            "",
            "**3. Arguments & Evidence (25% weight)**",
            "",
            "A: Strong arguments with concrete evidence, specific examples, clear data",
            "B: Fairly good arguments, has evidence but could be stronger",
            "C: Weak arguments, minimal or irrelevant evidence",
            "D/E: No clear arguments or evidence",
            "",
            "**4. Language Style & Mechanics (15% weight)**",
            "",
            "A: Professional language, perfect grammar, no typos",
            "B: Good language, 1-2 minor errors",
            "C: Adequate language but several errors",
            "D/E: Many errors, hard to understand",
            "",
        ]
        return "\n".join(lines)
    
    def build_validation_prompt(self, essay: str) -> str:
        """Build prompt to validate essay quality before grading"""
        return f"""Analyze this essay and determine if it's suitable for grading:

{essay}

Check for:
1. Minimum length (at least 100 words)
2. Coherent text (not gibberish)
3. Relevant to academic writing

Respond with JSON:
{{
  "is_valid": true/false,
  "reason": "Brief explanation",
  "word_count": number
}}
"""
    
    def build_consistency_check_prompt(
        self,
        essay: str,
        previous_scores: Dict[str, Dict[str, str]]
    ) -> str:
        """
        Build prompt to explain consistency across trials
        
        Args:
            essay: The essay text
            previous_scores: Previous trial results
            
        Returns:
            Prompt for consistency analysis
        """
        return f"""You previously graded this essay multiple times.
Here are your previous scores:

{self._format_previous_scores(previous_scores)}

Essay:
{essay}

Explain any significant variations in your scoring across trials.
Respond in JSON:
{{
  "consistency_analysis": "Explanation of variations",
  "confidence": "high|medium|low"
}}
"""
    
    def _format_previous_scores(self, scores: Dict[str, Dict[str, str]]) -> str:
        """Format previous scores for display"""
        lines = []
        for trial, trial_scores in scores.items():
            lines.append(f"\n{trial}:")
            for criterion, data in trial_scores.items():
                lines.append(f"  - {criterion}: {data.get('grade', 'N/A')}")
        return "\n".join(lines)
    
    def get_system_prompt(self) -> str:
        """Get system prompt"""
        return self.system_prompt
    
    def get_rubric_summary(self) -> str:
        """Get brief rubric summary for context"""
        lines = [f"Rubric: {self.rubric.name}"]
        lines.append(f"Criteria ({len(self.rubric.criteria)}): {', '.join(self.rubric.criteria.keys())}")
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    from src.core.rubric import RubricManager
    
    manager = RubricManager()
    rubric = manager.get_rubric("default")
    
    builder = PromptBuilder(rubric)
    
    # Test prompt
    sample_question = "Explain the concept of Automated Essay Scoring (AES) and its implications for education."
    sample_answer = """Automated Essay Scoring (AES) adalah sistem yang menggunakan AI untuk menilai esai secara otomatis.
    Sistem ini dapat membantu mengurangi beban kerja guru dan memberikan feedback yang cepat kepada siswa.
    Namun, ada beberapa tantangan seperti bias dalam algoritma dan kurangnya penilaian aspek kreatif."""
    
    prompt = builder.build_grading_prompt(sample_question, sample_answer)
    
    print("="*80)
    print("GENERATED PROMPT:")
    print("="*80)
    print(prompt)
