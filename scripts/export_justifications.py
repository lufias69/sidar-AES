#!/usr/bin/env python3
"""
Export all justifications from database to readable format
"""
import sqlite3
import json
from pathlib import Path

def export_justifications():
    conn = sqlite3.connect('results/grading_results.db')
    output_dir = Path('results/justifications_export')
    output_dir.mkdir(exist_ok=True)
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{'='*80}")
        print(f"Exporting {model.upper()} justifications...")
        print('='*80)
        
        cur = conn.cursor()
        cur.execute("""
            SELECT experiment_id, student_id, question_number,
                   answer_text, justification, overall_comment, weighted_score
            FROM grading_results
            WHERE model = ? AND strategy = 'lenient' AND status = 'completed'
            ORDER BY student_id, question_number
        """, (model,))
        
        results = cur.fetchall()
        
        # Write to file
        output_file = output_dir / f'{model}_justifications.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"{'='*80}\n")
            f.write(f"{model.upper()} JUSTIFICATIONS (Lenient Strategy)\n")
            f.write(f"Total: {len(results)} grading tasks\n")
            f.write(f"{'='*80}\n\n")
            
            for idx, row in enumerate(results, 1):
                exp_id, student_id, q_num, answer, justif_json, comment, score = row
                
                f.write(f"{'='*80}\n")
                f.write(f"Task #{idx}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Experiment: {exp_id}\n")
                f.write(f"Student: {student_id}, Question: {q_num}\n")
                f.write(f"Weighted Score: {score:.2f}\n")
                f.write(f"\n{'-'*80}\n")
                f.write(f"STUDENT ANSWER:\n")
                f.write(f"{'-'*80}\n")
                f.write(f"{answer[:500]}{'...' if len(answer) > 500 else ''}\n")
                
                # Parse and display justifications
                f.write(f"\n{'-'*80}\n")
                f.write(f"PER-RUBRIC JUSTIFICATIONS:\n")
                f.write(f"{'-'*80}\n")
                
                try:
                    justif_data = json.loads(justif_json)
                    
                    for rubric_name, content in justif_data.items():
                        f.write(f"\n[{rubric_name}]\n")
                        
                        if isinstance(content, dict):
                            # Gemini format
                            if 'justification' in content:
                                f.write(f"Grade: {content.get('grade', 'N/A')}\n")
                                f.write(f"Justification: {content['justification']}\n")
                            else:
                                f.write(f"{content}\n")
                        else:
                            # ChatGPT format (direct string)
                            f.write(f"{content}\n")
                
                except Exception as e:
                    f.write(f"Error parsing justification: {e}\n")
                
                # Overall comment
                f.write(f"\n{'-'*80}\n")
                f.write(f"OVERALL COMMENT:\n")
                f.write(f"{'-'*80}\n")
                f.write(f"{comment}\n")
                f.write(f"\n\n")
        
        print(f"✓ Exported {len(results)} justifications to {output_file}")
    
    # Create summary statistics
    print(f"\n{'='*80}")
    print("Creating summary statistics...")
    print('='*80)
    
    summary_file = output_dir / 'justification_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"{'='*80}\n")
        f.write("JUSTIFICATION SUMMARY STATISTICS\n")
        f.write(f"{'='*80}\n\n")
        
        for model in ['chatgpt', 'gemini']:
            cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(LENGTH(justification)) as avg_justif_len,
                    MIN(LENGTH(justification)) as min_justif_len,
                    MAX(LENGTH(justification)) as max_justif_len,
                    AVG(LENGTH(overall_comment)) as avg_comment_len
                FROM grading_results
                WHERE model = ? AND strategy = 'lenient' AND status = 'completed'
            """, (model,))
            
            stats = cur.fetchone()
            total, avg_just, min_just, max_just, avg_comm = stats
            
            f.write(f"{model.upper()}:\n")
            f.write(f"{'-'*80}\n")
            f.write(f"  Total tasks: {total}\n")
            f.write(f"  Avg justification length: {avg_just:.1f} characters\n")
            f.write(f"  Min justification length: {min_just} characters\n")
            f.write(f"  Max justification length: {max_just} characters\n")
            f.write(f"  Avg overall comment length: {avg_comm:.1f} characters\n")
            f.write(f"\n")
    
    print(f"✓ Summary statistics saved to {summary_file}")
    
    conn.close()
    
    print(f"\n{'='*80}")
    print("✓ EXPORT COMPLETED!")
    print(f"✓ Files saved to: {output_dir}")
    print('='*80)

if __name__ == "__main__":
    export_justifications()
