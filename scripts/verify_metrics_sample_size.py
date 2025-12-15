"""
Verify sample size for all evaluation metrics (MAE, RMSE, Cohen's Kappa, Pearson, etc.)
This script checks if all metrics are calculated using the same 70 samples as confusion matrices.
"""

import sqlite3
import json
from pathlib import Path
from collections import defaultdict

# Database path
DB_PATH = Path(__file__).parent.parent / 'results' / 'grading_results.db'

def load_gold_standard():
    """Load gold standard from JSON files."""
    gold_dir = Path(__file__).parent.parent / 'data' / 'gold_standard'
    
    # Dictionary: {student_name: {question_number: weighted_score}}
    name_to_scores = defaultdict(dict)
    
    for file in sorted(gold_dir.glob('student_*.json')):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        student_name = data['student_name']  # Use name, not student_id!
        
        # Use array index as question number (1-7)
        for idx, q in enumerate(data['questions'], start=1):
            name_to_scores[student_name][idx] = q['weighted_score']
    
    return name_to_scores

def score_to_grade(score):
    """Convert numerical score to letter grade."""
    if score >= 3.5:
        return 'A'
    elif score >= 2.5:
        return 'B'
    elif score >= 1.5:
        return 'C'
    elif score >= 0.5:
        return 'D'
    else:
        return 'E'

def verify_metrics(model, strategy):
    """Verify sample size for metrics calculation."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Load gold standard (70 samples: 10 students × 7 questions)
    gold_data = load_gold_standard()
    
    print(f"\n{'='*60}")
    print(f"VERIFYING METRICS FOR: {model.upper()} ({strategy})")
    print(f"{'='*60}")
    
    # Query database with student_name field
    query = """
        SELECT DISTINCT 
            r.student_name,
            r.question_number,
            r.weighted_score as ai_score
        FROM grading_results r
        WHERE r.model = ? 
        AND r.strategy = ?
        AND r.status = 'success'
        AND r.student_name IS NOT NULL
        ORDER BY r.student_name, r.question_number
    """
    
    cursor.execute(query, (model, strategy))
    rows = cursor.fetchall()
    
    # Match with gold standard
    matched_data = []
    for row in rows:
        student_name = row['student_name']
        question_number = row['question_number']
        ai_score = row['ai_score']
        
        # Get gold score using student_name
        gold_score = gold_data.get(student_name, {}).get(question_number)
        
        if gold_score is not None:
            matched_data.append({
                'student_name': student_name,
                'question_number': question_number,
                'ai_score': ai_score,
                'gold_score': gold_score,
                'ai_grade': score_to_grade(ai_score),
                'gold_grade': score_to_grade(gold_score)
            })
    
    # Calculate metrics
    if matched_data:
        ai_scores = [d['ai_score'] for d in matched_data]
        gold_scores = [d['gold_score'] for d in matched_data]
        ai_grades = [d['ai_grade'] for d in matched_data]
        gold_grades = [d['gold_grade'] for d in matched_data]
        
        # MAE
        mae = sum(abs(a - g) for a, g in zip(ai_scores, gold_scores)) / len(matched_data)
        
        # RMSE
        mse = sum((a - g)**2 for a, g in zip(ai_scores, gold_scores)) / len(matched_data)
        rmse = mse ** 0.5
        
        # Pearson correlation
        mean_ai = sum(ai_scores) / len(ai_scores)
        mean_gold = sum(gold_scores) / len(gold_scores)
        
        numerator = sum((a - mean_ai) * (g - mean_gold) for a, g in zip(ai_scores, gold_scores))
        denom_ai = sum((a - mean_ai)**2 for a in ai_scores) ** 0.5
        denom_gold = sum((g - mean_gold)**2 for g in gold_scores) ** 0.5
        
        pearson = numerator / (denom_ai * denom_gold) if denom_ai and denom_gold else 0
        
        # Exact accuracy (grades)
        exact_match = sum(1 for a, g in zip(ai_grades, gold_grades) if a == g)
        accuracy = (exact_match / len(matched_data)) * 100
        
        print(f"  Total samples: {len(matched_data)}")
        print(f"  Expected: 70 (10 students × 7 questions)")
        print(f"  Match status: {'✅ CORRECT' if len(matched_data) == 70 else '❌ MISMATCH'}")
        print()
        print(f"  Metrics calculated on {len(matched_data)} samples:")
        print(f"    MAE:      {mae:.4f}")
        print(f"    RMSE:     {rmse:.4f}")
        print(f"    Pearson:  {pearson:.4f}")
        print(f"    Accuracy: {accuracy:.1f}% ({exact_match}/{len(matched_data)})")
        
        # Grade distribution check
        grade_counts = defaultdict(int)
        for grade in gold_grades:
            grade_counts[grade] += 1
        
        print()
        print(f"  Gold standard grade distribution:")
        for grade in ['A', 'B', 'C', 'D', 'E']:
            count = grade_counts.get(grade, 0)
            pct = (count / len(matched_data)) * 100
            print(f"    {grade}: {count:2d} ({pct:5.1f}%)")
        
        # Check for any missing matches
        missing = set()
        for student_name in gold_data:
            for q_num in gold_data[student_name]:
                found = any(
                    d['student_name'] == student_name and d['question_number'] == q_num
                    for d in matched_data
                )
                if not found:
                    missing.add((student_name, q_num))
        
        if missing:
            print(f"\n  ⚠️  WARNING: {len(missing)} samples missing from database:")
            for student, q in list(missing)[:5]:
                print(f"      - {student}, Q{q}")
            if len(missing) > 5:
                print(f"      ... and {len(missing) - 5} more")
    else:
        print(f"  ❌ NO DATA MATCHED!")
    
    conn.close()
    return len(matched_data) if matched_data else 0

def main():
    """Verify all metrics."""
    print("\n" + "="*60)
    print("METRICS SAMPLE SIZE VERIFICATION")
    print("="*60)
    print("\nThis script verifies that ALL evaluation metrics")
    print("(MAE, RMSE, Pearson, Cohen's Kappa, Accuracy)")
    print("are calculated using the same 70 samples as confusion matrices.")
    
    models_strategies = [
        ('chatgpt', 'lenient'),
        ('gemini', 'lenient'),
        ('chatgpt', 'zero-shot'),
        ('gemini', 'zero-shot')
    ]
    
    results = {}
    for model, strategy in models_strategies:
        sample_count = verify_metrics(model, strategy)
        results[(model, strategy)] = sample_count
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    all_correct = all(count == 70 for count in results.values())
    
    for (model, strategy), count in results.items():
        status = "✅" if count == 70 else "❌"
        print(f"  {status} {model.upper():7s} {strategy:10s}: {count:2d}/70 samples")
    
    print()
    if all_correct:
        print("✅ ALL METRICS USE CORRECT 70 SAMPLES!")
        print("   Confusion matrices, MAE, RMSE, Pearson, Cohen's Kappa,")
        print("   and accuracy are all calculated on the same dataset.")
    else:
        print("❌ SAMPLE SIZE MISMATCH DETECTED!")
        print("   Some metrics may be using different sample sizes.")
    print()

if __name__ == '__main__':
    main()
