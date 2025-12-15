"""
Test Indonesian Language Support

Test grading dengan Bahasa Indonesia untuk validasi sistem.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.chatgpt_agent import ChatGPTAgent
from src.core.rubric import RubricManager
from dotenv import load_dotenv
import json

load_dotenv()

def test_indonesian_grading():
    """Test grading dengan Bahasa Indonesia."""
    
    # Load rubric
    rubric_manager = RubricManager()
    rubric = rubric_manager.get_rubric("default")
    
    # Initialize agent
    agent = ChatGPTAgent()
    
    # Sample essay
    question = "Jelaskan singkat tentang topik capstone project yang sedang kamu kerjakan. Apa masalah utama yang ingin kamu selesaikan dan apa tujuan dari proyek tersebut?"
    answer = "Membuat sistem pendeteksi hujan otomatis untuk jemuran. Masalah utama yang ingin saya selesaikan adalah pakaian yang basah karena hujan. Tujuan proyek ini adalah agar pakaian yang dijemur tetap kering meskipun hujan."
    
    print("="*80)
    print("TEST INDONESIAN LANGUAGE SUPPORT")
    print("="*80)
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer}")
    print("\n" + "="*80)
    print("TESTING WITH LANGUAGE='indonesian'...")
    print("="*80)
    
    # Grade with Indonesian
    result_id = agent.grade_essay(
        student_id="TEST_STUDENT",
        question_id="Q1",
        question=question,
        answer=answer,
        rubric=rubric,
        trial=1,
        language="indonesian"
    )
    
    print("\nRESULT (Indonesian):")
    print(json.dumps(result_id.to_dict(), indent=2, ensure_ascii=False))
    
    # Check if justifications are in Indonesian
    print("\n" + "="*80)
    print("VALIDATION:")
    print("="*80)
    
    scores = result_id.to_dict()['scores']
    all_indonesian = True
    
    for criterion, data in scores.items():
        justification = data.get('justification', '')
        # Simple check: Indonesian text should not have English indicators
        has_english_markers = any(word in justification.lower() for word in 
                                  ['the student', 'however', 'while', 'although', 'demonstrates'])
        
        if has_english_markers:
            print(f"⚠️  {criterion}: Might be in English")
            all_indonesian = False
        else:
            print(f"✅ {criterion}: Indonesian detected")
    
    overall = result_id.to_dict().get('overall_comment', '')
    has_english_markers = any(word in overall.lower() for word in 
                              ['the', 'response', 'provides', 'would', 'more'])
    
    if has_english_markers:
        print(f"⚠️  Overall comment: Might be in English")
        all_indonesian = False
    else:
        print(f"✅ Overall comment: Indonesian detected")
    
    print("\n" + "="*80)
    if all_indonesian:
        print("✅ SUCCESS: All justifications appear to be in Indonesian!")
    else:
        print("⚠️  WARNING: Some justifications might still be in English")
    print("="*80)
    
    return all_indonesian


if __name__ == "__main__":
    success = test_indonesian_grading()
    sys.exit(0 if success else 1)
