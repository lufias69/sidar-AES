"""
Create Gold Standard Baseline from AI Grading Results

Merges ChatGPT and Gemini results, taking highest grade for each criterion.
Removes all AI metadata to make it look like manual lecturer grading.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

# Grade hierarchy for comparison
GRADE_ORDER = {'A': 4, 'B': 3, 'C': 2, 'D/E': 1}

def compare_grades(grade1: str, grade2: str) -> str:
    """Return the higher grade between two grades."""
    return grade1 if GRADE_ORDER.get(grade1, 0) >= GRADE_ORDER.get(grade2, 0) else grade2

def calculate_weighted_score(grades: Dict[str, str], rubric_weights: Dict[str, float]) -> float:
    """Calculate weighted score from grades."""
    grade_points = {'A': 4, 'B': 3, 'C': 2, 'D/E': 1}
    total = sum(rubric_weights.get(criterion, 0.25) * grade_points.get(grade, 0) 
                for criterion, grade in grades.items())
    return round(total, 2)

def merge_grading_results(chatgpt_result: Dict, gemini_result: Dict) -> Dict[str, Any]:
    """
    Merge ChatGPT and Gemini results, taking highest grade for each criterion.
    
    Args:
        chatgpt_result: ChatGPT grading result
        gemini_result: Gemini grading result
        
    Returns:
        Merged result with only grades and weighted_score
    """
    merged_grades = {}
    source_tracking = {}
    
    # Get scores from both models
    chatgpt_scores = chatgpt_result.get('scores', {})
    gemini_scores = gemini_result.get('scores', {})
    
    # Merge grades - take highest
    all_criteria = set(chatgpt_scores.keys()) | set(gemini_scores.keys())
    
    for criterion in all_criteria:
        chatgpt_grade = chatgpt_scores.get(criterion, {}).get('grade', 'D/E')
        gemini_grade = gemini_scores.get(criterion, {}).get('grade', 'D/E')
        
        # Take highest grade
        merged_grades[criterion] = compare_grades(chatgpt_grade, gemini_grade)
        
        # Track source (for debugging, will be removed in final output)
        if GRADE_ORDER.get(chatgpt_grade, 0) >= GRADE_ORDER.get(gemini_grade, 0):
            source_tracking[criterion] = 'chatgpt'
        else:
            source_tracking[criterion] = 'gemini'
    
    # Calculate weighted score from merged grades
    # Use standard rubric weights
    rubric_weights = {
        "Pemahaman Konten": 0.35,
        "Organisasi & Struktur": 0.25,
        "Argumen & Bukti": 0.25,
        "Gaya Bahasa & Mekanik": 0.15
    }
    
    weighted_score = calculate_weighted_score(merged_grades, rubric_weights)
    
    return {
        'grades': merged_grades,
        'weighted_score': weighted_score,
        '_source': source_tracking  # For validation, will be removed
    }

def process_student_file(input_path: Path, output_path: Path, include_source: bool = False):
    """
    Process a single student file to create gold standard baseline.
    
    Args:
        input_path: Path to input JSON file (with AI results)
        output_path: Path to output JSON file (clean baseline)
        include_source: Include source tracking for debugging
    """
    # Load input file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create clean output structure
    output_data = {
        'student_name': data['student_name'],
        'questions': []
    }
    
    # Process each question
    for question_data in data['questions']:
        question_entry = {
            'question': question_data['question'],
            'answer': question_data['answer']
        }
        
        # Merge ChatGPT and Gemini results
        chatgpt = question_data.get('chatgpt', {})
        gemini = question_data.get('gemini', {})
        
        if chatgpt and gemini:
            merged = merge_grading_results(chatgpt, gemini)
            
            if include_source:
                # Include source tracking for validation
                question_entry['baseline_grades'] = merged
            else:
                # Clean version - no source tracking
                question_entry['grades'] = merged['grades']
                question_entry['weighted_score'] = merged['weighted_score']
        else:
            # Fallback if one model is missing
            available = chatgpt if chatgpt else gemini
            if available and 'scores' in available:
                grades = {k: v['grade'] for k, v in available['scores'].items()}
                question_entry['grades'] = grades
                question_entry['weighted_score'] = available.get('weighted_score', 0)
        
        output_data['questions'].append(question_entry)
    
    # Save output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

def create_gold_standard_batch(
    input_dir: str = "results/baseline_batch",
    output_dir: str = "results/gold_standard",
    include_source: bool = False
):
    """
    Process all student files to create gold standard baseline.
    
    Args:
        input_dir: Directory with AI grading results
        output_dir: Directory for gold standard output
        include_source: Include source tracking for debugging
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all Indonesian translated files
    student_files = sorted(input_path.glob("student_*_id.json"))
    
    if not student_files:
        print(f"❌ No student files found in {input_dir}")
        print("   Looking for: student_*_id.json")
        return
    
    print("="*80)
    print("CREATING GOLD STANDARD BASELINE")
    print("="*80)
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Files to process: {len(student_files)}")
    print()
    
    processed = 0
    for input_file in student_files:
        # Create output filename (remove _id suffix)
        output_filename = input_file.name.replace('_id.json', '_gold.json')
        output_file = output_path / output_filename
        
        print(f"Processing: {input_file.name} → {output_filename}")
        
        try:
            process_student_file(input_file, output_file, include_source)
            processed += 1
            print(f"  ✅ Success")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print()
    print("="*80)
    print("GOLD STANDARD CREATION COMPLETE")
    print("="*80)
    print(f"Processed: {processed}/{len(student_files)} files")
    print(f"Output: {output_path}")
    print()
    print("File structure:")
    print("  - No justifications or comments")
    print("  - No AI metadata (tokens, timestamps, etc.)")
    print("  - Only grades and weighted scores")
    print("  - Looks like manual lecturer grading")
    print()
    print("Next steps:")
    print("  1. Review gold standard files")
    print("  2. Lecturer can manually adjust grades if needed")
    print("  3. Use as baseline for experiment comparison")
    print("="*80)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create gold standard baseline from AI grading results"
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        default='results/baseline_batch',
        help='Input directory with AI results'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results/gold_standard',
        help='Output directory for gold standard'
    )
    parser.add_argument(
        '--include-source',
        action='store_true',
        help='Include source tracking for debugging (which AI gave each grade)'
    )
    
    args = parser.parse_args()
    
    create_gold_standard_batch(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        include_source=args.include_source
    )

if __name__ == "__main__":
    main()
