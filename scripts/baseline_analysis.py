"""
Baseline Analysis Script

Script untuk menjalankan analisis PERTAMA sebagai baseline:
1. Extract data 1 mahasiswa dari Excel
2. Grade dengan ChatGPT + Gemini (1 trial)
3. Generate hasil untuk review dosen
4. Dosen koreksi → jadi gold standard

Hasil baseline akan digunakan sebagai pembanding untuk 10 pengujian berikutnya.
"""

import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.chatgpt_agent import ChatGPTAgent
from src.agents.gemini_agent import GeminiAgent
from src.core.rubric import RubricManager
from src.core.prompt_builder import PromptBuilder
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Load environment variables
load_dotenv()


class BaselineAnalyzer:
    """
    Analyzer untuk membuat baseline pertama kali.
    """
    
    def __init__(self, excel_path: str = "data/Jawaban/jawaban UTS  Capstone Project.xlsx"):
        """Initialize baseline analyzer."""
        self.excel_path = Path(excel_path)
        self.rubric_manager = RubricManager()
        self.rubric = self.rubric_manager.load_default_rubric()
        self.prompt_builder = PromptBuilder(self.rubric)
        
        # Initialize agents
        self.chatgpt_agent = ChatGPTAgent()
        self.gemini_agent = GeminiAgent()
    
    def load_excel_data(self) -> pd.DataFrame:
        """Load data from Excel file."""
        logger.info(f"Loading Excel file: {self.excel_path}")
        df = pd.read_excel(self.excel_path)
        logger.info(f"Loaded {len(df)} students, {len(df.columns)-1} questions")
        return df
    
    def extract_student_data(self, df: pd.DataFrame, student_index: int = 0) -> dict:
        """
        Extract data untuk 1 mahasiswa.
        
        Args:
            df: DataFrame from Excel
            student_index: Index mahasiswa (default 0 = mahasiswa pertama)
        
        Returns:
            Dictionary dengan data mahasiswa dan jawabannya
        """
        student_row = df.iloc[student_index]
        student_name = student_row['Nama']
        
        # Extract questions and answers
        questions = []
        for col in df.columns[1:]:  # Skip 'Nama' column
            question_text = col
            answer_text = student_row[col]
            
            questions.append({
                'question': question_text,
                'answer': str(answer_text) if pd.notna(answer_text) else ""
            })
        
        return {
            'student_name': student_name,
            'student_index': student_index,
            'questions': questions,
            'total_questions': len(questions)
        }
    
    def grade_single_essay(
        self,
        question: str,
        answer: str,
        agent_name: str = "ChatGPT"
    ) -> dict:
        """
        Grade 1 esai dengan agent pilihan.
        
        Args:
            question: Pertanyaan essay
            answer: Jawaban mahasiswa
            agent_name: "ChatGPT" atau "Gemini"
        
        Returns:
            Hasil grading
        """
        agent = self.chatgpt_agent if agent_name == "ChatGPT" else self.gemini_agent
        
        logger.info(f"Grading with {agent_name}...")
        result = agent.grade_essay(question, answer, self.rubric)
        
        return result
    
    def format_for_review(self, student_data: dict, results: dict) -> str:
        """
        Format hasil untuk review dosen.
        
        Returns:
            String formatted untuk mudah dibaca dosen
        """
        output = []
        output.append("=" * 80)
        output.append("BASELINE ANALYSIS - HASIL UNTUK REVIEW DOSEN")
        output.append("=" * 80)
        output.append(f"\nMahasiswa: {student_data['student_name']}")
        output.append(f"Tanggal Analisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Total Pertanyaan: {student_data['total_questions']}")
        output.append("\n" + "=" * 80)
        
        for i, (question_data, question_results) in enumerate(zip(student_data['questions'], results), 1):
            output.append(f"\n\n{'='*80}")
            output.append(f"PERTANYAAN {i}")
            output.append("=" * 80)
            output.append(f"\n{question_data['question']}")
            output.append(f"\nJAWABAN MAHASISWA:")
            output.append(f"{question_data['answer']}")
            output.append("\n" + "-" * 80)
            
            # ChatGPT Results
            if 'chatgpt' in question_results:
                chatgpt_result = question_results['chatgpt']
                output.append(f"\n[HASIL CHATGPT GPT-4o]")
                output.append(f"Nilai Akhir: {chatgpt_result.get('weighted_score', 0):.2f}/100")
                output.append(f"\nPenilaian Per Kriteria:")
                
                for criterion, grade_info in chatgpt_result.get('grades', {}).items():
                    output.append(f"\n  • {criterion}: {grade_info['grade']}")
                    output.append(f"    Justifikasi: {grade_info['justification']}")
                
                output.append("\n" + "-" * 80)
            
            # Gemini Results
            if 'gemini' in question_results:
                gemini_result = question_results['gemini']
                output.append(f"\n[HASIL GEMINI 2.0 FLASH]")
                output.append(f"Nilai Akhir: {gemini_result.get('weighted_score', 0):.2f}/100")
                output.append(f"\nPenilaian Per Kriteria:")
                
                for criterion, grade_info in gemini_result.get('grades', {}).items():
                    output.append(f"\n  • {criterion}: {grade_info['grade']}")
                    output.append(f"    Justifikasi: {grade_info['justification']}")
        
        output.append("\n\n" + "=" * 80)
        output.append("INSTRUKSI UNTUK DOSEN:")
        output.append("=" * 80)
        output.append("""
1. Review setiap penilaian AI di atas
2. Koreksi jika ada yang tidak sesuai:
   - Ubah grade (A/B/C/D/E)
   - Edit justifikasi
   - Sesuaikan nilai akhir
3. Hasil koreksi Anda akan menjadi BASELINE (gold standard)
4. Baseline ini akan digunakan sebagai pembanding untuk 10 pengujian berikutnya

Format Koreksi (jika ada):
- Pertanyaan X, Kriteria Y: Grade [A/B/C/D/E] → Alasan
- Nilai akhir: [0-100]
""")
        
        return "\n".join(output)
    
    def run_baseline_analysis(
        self,
        student_index: int = 0,
        use_chatgpt: bool = True,
        use_gemini: bool = True,
        output_dir: str = "results/baseline"
    ):
        """
        Jalankan analisis baseline lengkap.
        
        Args:
            student_index: Index mahasiswa (0 = pertama)
            use_chatgpt: Gunakan ChatGPT?
            use_gemini: Gunakan Gemini?
            output_dir: Directory untuk menyimpan hasil
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n" + "="*80)
        logger.info("STARTING BASELINE ANALYSIS")
        logger.info("="*80)
        
        # Step 1: Load data
        logger.info("\n[1/4] Loading Excel data...")
        df = self.load_excel_data()
        
        # Step 2: Extract student
        logger.info(f"\n[2/4] Extracting student {student_index}...")
        student_data = self.extract_student_data(df, student_index)
        logger.info(f"Student: {student_data['student_name']}")
        logger.info(f"Questions: {student_data['total_questions']}")
        
        # Step 3: Grade all questions
        logger.info(f"\n[3/4] Grading {student_data['total_questions']} questions...")
        all_results = []
        
        for i, q_data in enumerate(student_data['questions'], 1):
            logger.info(f"\nProcessing Question {i}/{student_data['total_questions']}...")
            question_results = {}
            
            # ChatGPT
            if use_chatgpt:
                try:
                    chatgpt_result = self.grade_single_essay(
                        q_data['question'],
                        q_data['answer'],
                        "ChatGPT"
                    )
                    question_results['chatgpt'] = chatgpt_result
                    logger.info(f"  ✅ ChatGPT: {chatgpt_result.get('weighted_score', 0):.2f}/100")
                except Exception as e:
                    logger.error(f"  ❌ ChatGPT failed: {e}")
            
            # Gemini
            if use_gemini:
                try:
                    gemini_result = self.grade_single_essay(
                        q_data['question'],
                        q_data['answer'],
                        "Gemini"
                    )
                    question_results['gemini'] = gemini_result
                    logger.info(f"  ✅ Gemini: {gemini_result.get('weighted_score', 0):.2f}/100")
                except Exception as e:
                    logger.error(f"  ❌ Gemini failed: {e}")
            
            all_results.append(question_results)
        
        # Step 4: Format and save
        logger.info("\n[4/4] Formatting results for review...")
        
        # Save raw JSON
        json_file = output_path / f"baseline_raw_{student_data['student_name']}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'student_data': student_data,
                'results': all_results,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'used_chatgpt': use_chatgpt,
                    'used_gemini': use_gemini,
                    'rubric': self.rubric.to_dict()
                }
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved raw JSON: {json_file}")
        
        # Save formatted for review
        review_text = self.format_for_review(student_data, all_results)
        review_file = output_path / f"baseline_review_{student_data['student_name']}.txt"
        with open(review_file, 'w', encoding='utf-8') as f:
            f.write(review_text)
        logger.info(f"✅ Saved review file: {review_file}")
        
        # Print summary
        logger.info("\n" + "="*80)
        logger.info("BASELINE ANALYSIS COMPLETE!")
        logger.info("="*80)
        logger.info(f"Student: {student_data['student_name']}")
        logger.info(f"Questions graded: {student_data['total_questions']}")
        logger.info(f"\nOutput files:")
        logger.info(f"  1. Raw JSON: {json_file}")
        logger.info(f"  2. Review file: {review_file}")
        logger.info("\nNext steps:")
        logger.info("  1. Buka file review: baseline_review_*.txt")
        logger.info("  2. Dosen review dan koreksi hasil AI")
        logger.info("  3. Hasil koreksi jadi BASELINE/Gold Standard")
        logger.info("  4. Jalankan 10 pengujian penuh dengan baseline sebagai pembanding")
        logger.info("="*80)
        
        return {
            'student_data': student_data,
            'results': all_results,
            'output_files': {
                'json': str(json_file),
                'review': str(review_file)
            }
        }


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run baseline analysis - Grade 1 mahasiswa untuk review dosen"
    )
    parser.add_argument(
        '--student',
        type=int,
        default=0,
        help='Index mahasiswa (0=pertama, 1=kedua, dst)'
    )
    parser.add_argument(
        '--chatgpt',
        action='store_true',
        default=True,
        help='Gunakan ChatGPT (default: True)'
    )
    parser.add_argument(
        '--gemini',
        action='store_true',
        default=True,
        help='Gunakan Gemini (default: True)'
    )
    parser.add_argument(
        '--no-chatgpt',
        action='store_true',
        help='Jangan gunakan ChatGPT'
    )
    parser.add_argument(
        '--no-gemini',
        action='store_true',
        help='Jangan gunakan Gemini'
    )
    
    args = parser.parse_args()
    
    # Check API keys
    if not args.no_chatgpt and not os.getenv('OPENAI_API_KEY'):
        logger.error("❌ OPENAI_API_KEY not found in .env file!")
        logger.info("Please add: OPENAI_API_KEY=sk-... to your .env file")
        return 1
    
    if not args.no_gemini and not os.getenv('GEMINI_API_KEY'):
        logger.error("❌ GEMINI_API_KEY not found in .env file!")
        logger.info("Please add: GEMINI_API_KEY=... to your .env file")
        return 1
    
    # Run analysis
    analyzer = BaselineAnalyzer()
    
    try:
        result = analyzer.run_baseline_analysis(
            student_index=args.student,
            use_chatgpt=not args.no_chatgpt,
            use_gemini=not args.no_gemini
        )
        
        print("\n✅ BASELINE ANALYSIS SUCCESS!")
        print(f"\nReview file: {result['output_files']['review']}")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
