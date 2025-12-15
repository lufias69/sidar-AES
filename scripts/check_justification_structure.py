#!/usr/bin/env python3
"""
Check justification data structure in database
"""
import sqlite3
import json

def check_justification_structure():
    conn = sqlite3.connect('results/grading_results.db')
    cur = conn.cursor()
    
    # Get one sample from each model
    for model in ['chatgpt', 'gemini']:
        print(f"\n{'='*80}")
        print(f"Sample from {model.upper()}")
        print('='*80)
        
        cur.execute("""
            SELECT experiment_id, student_id, question_number, 
                   grades, justification, overall_comment
            FROM grading_results 
            WHERE model = ? AND status = 'completed'
            LIMIT 1
        """, (model,))
        
        result = cur.fetchone()
        if result:
            exp_id, student_id, q_num, grades_json, justification, overall_comment = result
            print(f"Experiment: {exp_id}")
            print(f"Student: {student_id}, Question: {q_num}")
            
            # Parse grades JSON
            print(f"\n{'='*40}")
            print("GRADES JSON Structure:")
            print('='*40)
            grades = json.loads(grades_json)
            print(f"Keys: {list(grades.keys())}")
            
            # Show sample of each rubric
            for rubric_name in list(grades.keys())[:2]:  # Show first 2 rubrics
                print(f"\n{rubric_name}:")
                if isinstance(grades[rubric_name], dict):
                    for key, val in grades[rubric_name].items():
                        if isinstance(val, str) and len(val) > 100:
                            print(f"  {key}: {val[:100]}...")
                        else:
                            print(f"  {key}: {val}")
            
            # Show justification
            print(f"\n{'='*40}")
            print("JUSTIFICATION Field:")
            print('='*40)
            if justification:
                print(f"Length: {len(justification)} chars")
                print(f"Preview:\n{justification[:300]}...")
            else:
                print("(Empty or NULL)")
            
            # Show overall comment
            print(f"\n{'='*40}")
            print("OVERALL_COMMENT Field:")
            print('='*40)
            if overall_comment:
                print(f"Length: {len(overall_comment)} chars")
                print(f"Preview:\n{overall_comment[:300]}...")
            else:
                print("(Empty or NULL)")
                
        else:
            print(f"No completed data found for {model}")
    
    # Statistics
    print(f"\n{'='*80}")
    print("JUSTIFICATION STATISTICS")
    print('='*80)
    
    for model in ['chatgpt', 'gemini']:
        cur.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN justification IS NOT NULL AND justification != '' THEN 1 ELSE 0 END) as has_justification,
                   SUM(CASE WHEN overall_comment IS NOT NULL AND overall_comment != '' THEN 1 ELSE 0 END) as has_comment
            FROM grading_results
            WHERE model = ? AND status = 'completed'
        """, (model,))
        
        total, has_just, has_comment = cur.fetchone()
        print(f"\n{model.upper()}:")
        print(f"  Total completed tasks: {total}")
        print(f"  Has justification: {has_just} ({has_just/total*100 if total > 0 else 0:.1f}%)")
        print(f"  Has overall_comment: {has_comment} ({has_comment/total*100 if total > 0 else 0:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    check_justification_structure()
