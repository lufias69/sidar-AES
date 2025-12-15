"""
Batch Baseline Analysis - Process 10 Selected Students

Process 10 mahasiswa terbaik untuk baseline:
- Grade semua dengan ChatGPT + Gemini
- Generate hasil untuk review dosen
- Batch processing untuk efisiensi
"""

import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
from tqdm import tqdm

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


class BatchBaselineAnalyzer:
    """
    Batch analyzer untuk 10 mahasiswa terbaik sebagai baseline.
    """
    
    def __init__(self, excel_path: str = "data/Jawaban/jawaban UTS  Capstone Project.xlsx"):
        """Initialize batch baseline analyzer."""
        self.excel_path = Path(excel_path)
        self.rubric_manager = RubricManager()
        self.rubric = self.rubric_manager.get_rubric("default")
        self.prompt_builder = PromptBuilder(self.rubric)
        
        # Initialize agents
        self.chatgpt_agent = ChatGPTAgent()
        self.gemini_agent = GeminiAgent()
        
        # Load selected students
        self.selected_indices = self.load_selected_students()
    
    def load_selected_students(self) -> list:
        """Load indices of selected students from file."""
        selected_file = Path('selected_students.txt')
        if not selected_file.exists():
            logger.warning("selected_students.txt not found, using top 10")
            return list(range(10))
        
        indices = []
        with open(selected_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    idx = int(line.split(',')[0])
                    indices.append(idx)
        
        logger.info(f"Loaded {len(indices)} selected students")
        return indices
    
    def run_batch_baseline(
        self,
        use_chatgpt: bool = True,
        use_gemini: bool = True,
        output_dir: str = "results/baseline_batch",
        language: str = "indonesian"
    ):
        """
        Run baseline analysis for all 10 selected students.
        
        Args:
            use_chatgpt: Use ChatGPT?
            use_gemini: Use Gemini?
            output_dir: Output directory
            language: Language for justifications ("indonesian" or "english")
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n" + "="*80)
        logger.info("BATCH BASELINE ANALYSIS - 10 MAHASISWA TERBAIK")
        logger.info(f"Language: {language.upper()}")
        logger.info("="*80)
        
        # Load Excel
        logger.info("\n[1/3] Loading Excel data...")
        df = pd.read_excel(self.excel_path)
        
        # Process each selected student
        logger.info(f"\n[2/3] Processing {len(self.selected_indices)} students...")
        
        all_students_results = []
        
        for i, student_idx in enumerate(self.selected_indices, 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"STUDENT {i}/{len(self.selected_indices)}: {df.iloc[student_idx]['Nama']}")
            logger.info(f"{'='*80}")
            
            student_row = df.iloc[student_idx]
            student_name = student_row['Nama']
            
            # Extract questions
            questions = []
            for col in df.columns[1:]:
                questions.append({
                    'question': col,
                    'answer': str(student_row[col]) if pd.notna(student_row[col]) else ""
                })
            
            # Grade all questions
            student_results = {
                'student_index': student_idx,
                'student_name': student_name,
                'questions': []
            }
            
            for q_idx, q_data in enumerate(questions, 1):
                logger.info(f"\n  Question {q_idx}/7...")
                q_result = {'question': q_data['question'], 'answer': q_data['answer']}
                
                # ChatGPT
                if use_chatgpt:
                    try:
                        chatgpt_res = self.chatgpt_agent.grade_essay(
                            student_id=student_name,
                            question_id=f"Q{q_idx}",
                            question=q_data['question'],
                            answer=q_data['answer'],
                            rubric=self.rubric,
                            trial=1,
                            language=language
                        )
                        q_result['chatgpt'] = chatgpt_res.to_dict()
                        logger.info(f"    ✅ ChatGPT: {chatgpt_res.weighted_score:.2f}")
                    except Exception as e:
                        logger.error(f"    ❌ ChatGPT failed: {e}")
                        q_result['chatgpt'] = {'error': str(e)}
                
                # Gemini
                if use_gemini:
                    try:
                        gemini_res = self.gemini_agent.grade_essay(
                            student_id=student_name,
                            question_id=f"Q{q_idx}",
                            question=q_data['question'],
                            answer=q_data['answer'],
                            rubric=self.rubric,
                            trial=1,
                            language=language
                        )
                        q_result['gemini'] = gemini_res.to_dict()
                        logger.info(f"    ✅ Gemini: {gemini_res.weighted_score:.2f}")
                    except Exception as e:
                        logger.error(f"    ❌ Gemini failed: {e}")
                        q_result['gemini'] = {'error': str(e)}
                
                student_results['questions'].append(q_result)
            
            all_students_results.append(student_results)
            
            # Save individual student
            student_file = output_path / f"student_{student_idx:02d}_{student_name.replace(' ', '_')}.json"
            with open(student_file, 'w', encoding='utf-8') as f:
                json.dump(student_results, f, indent=2, ensure_ascii=False)
            logger.info(f"\n  ✅ Saved: {student_file}")
        
        # Save combined results
        logger.info(f"\n[3/3] Saving combined results...")
        
        combined_file = output_path / "baseline_all_students.json"
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_students': len(all_students_results),
                    'total_questions': 7,
                    'used_chatgpt': use_chatgpt,
                    'used_gemini': use_gemini,
                    'rubric': self.rubric.to_dict()
                },
                'students': all_students_results
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Combined results: {combined_file}")
        
        # Generate summary report
        self.generate_summary_report(all_students_results, output_path)
        
        logger.info("\n" + "="*80)
        logger.info("BATCH BASELINE COMPLETE!")
        logger.info("="*80)
        logger.info(f"Processed: {len(all_students_results)} students")
        logger.info(f"Total questions: {len(all_students_results) * 7}")
        logger.info(f"\nOutput directory: {output_path}")
        logger.info("\nNext steps:")
        logger.info("  1. Review hasil di folder results/baseline_batch/")
        logger.info("  2. Dosen review dan koreksi")
        logger.info("  3. Finalisasi baseline → Gold Standard")
        logger.info("="*80)
        
        return all_students_results
    
    def generate_summary_report(self, results: list, output_dir: Path):
        """Generate summary report for all students."""
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("BASELINE BATCH ANALYSIS - SUMMARY REPORT")
        report_lines.append("="*80)
        report_lines.append(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total Students: {len(results)}")
        report_lines.append(f"Questions per Student: 7")
        report_lines.append(f"Total Graded: {len(results) * 7} essays\n")
        
        report_lines.append("="*80)
        report_lines.append("STUDENTS SUMMARY")
        report_lines.append("="*80)
        
        for i, student in enumerate(results, 1):
            report_lines.append(f"\n{i}. {student['student_name']} (Index: {student['student_index']})")
            
            # Calculate average scores
            chatgpt_scores = []
            gemini_scores = []
            
            for q in student['questions']:
                if 'chatgpt' in q and 'weighted_score' in q['chatgpt']:
                    chatgpt_scores.append(q['chatgpt']['weighted_score'])
                if 'gemini' in q and 'weighted_score' in q['gemini']:
                    gemini_scores.append(q['gemini']['weighted_score'])
            
            if chatgpt_scores:
                report_lines.append(f"   ChatGPT Avg: {sum(chatgpt_scores)/len(chatgpt_scores):.2f}")
            if gemini_scores:
                report_lines.append(f"   Gemini Avg: {sum(gemini_scores)/len(gemini_scores):.2f}")
        
        report_lines.append("\n" + "="*80)
        report_lines.append("UNTUK DOSEN:")
        report_lines.append("="*80)
        report_lines.append("""
1. Review file individual per mahasiswa di folder ini
2. Untuk setiap mahasiswa, check 7 pertanyaan
3. Koreksi penilaian AI jika perlu
4. Hasil koreksi → BASELINE (Gold Standard)
5. File individual: student_XX_NamaMahasiswa.json
6. Buka dengan text editor atau JSON viewer
""")
        
        # Save report
        report_file = output_dir / "00_SUMMARY_REPORT.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"✅ Summary report: {report_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch baseline analysis - Process 10 mahasiswa terbaik"
    )
    parser.add_argument(
        '--no-chatgpt',
        action='store_true',
        help='Skip ChatGPT (save cost)'
    )
    parser.add_argument(
        '--no-gemini',
        action='store_true',
        help='Skip Gemini'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='indonesian',
        choices=['indonesian', 'english'],
        help='Language for justifications (default: indonesian)'
    )
    
    args = parser.parse_args()
    
    # Check API keys
    if not args.no_chatgpt and not os.getenv('OPENAI_API_KEY'):
        logger.error("❌ OPENAI_API_KEY not found!")
        return 1
    
    if not args.no_gemini and not os.getenv('GEMINI_API_KEY'):
        logger.error("❌ GEMINI_API_KEY not found!")
        return 1
    
    # Run analysis
    analyzer = BatchBaselineAnalyzer()
    
    try:
        analyzer.run_batch_baseline(
            use_chatgpt=not args.no_chatgpt,
            use_gemini=not args.no_gemini,
            language=args.language
        )
        return 0
    except Exception as e:
        logger.error(f"❌ Batch analysis failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
