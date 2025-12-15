#!/usr/bin/env python3
"""
Analyze quality of AI-generated justifications in AES
"""
import sqlite3
import json
import pandas as pd
import numpy as np
from pathlib import Path
import re
from collections import Counter

def extract_justifications_chatgpt(justification_json):
    """Extract justifications from ChatGPT format"""
    try:
        if isinstance(justification_json, str):
            data = json.loads(justification_json)
        else:
            data = justification_json
        
        rubrics = []
        justifications = []
        
        for rubric, text in data.items():
            rubrics.append(rubric)
            # Handle both string and dict formats
            if isinstance(text, dict):
                justifications.append(str(text))
            else:
                justifications.append(str(text) if text else "")
        
        return rubrics, justifications
    except:
        return [], []

def extract_justifications_gemini(grades_json):
    """Extract justifications from Gemini format"""
    try:
        if isinstance(grades_json, str):
            data = json.loads(grades_json)
        else:
            data = grades_json
        
        rubrics = []
        justifications = []
        
        for rubric, info in data.items():
            if isinstance(info, dict) and 'justification' in info:
                rubrics.append(rubric)
                justifications.append(str(info['justification']) if info['justification'] else "")
        
        return rubrics, justifications
    except:
        return [], []

def score_to_grade(score):
    """Convert GPA score to letter grade"""
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

def analyze_completeness():
    """Analyze if justifications address all rubrics"""
    print("\n" + "="*80)
    print("1. COMPLETENESS ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades, overall_comment
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        rubric_coverage = []
        empty_justifications = 0
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            if not rubrics:
                empty_justifications += 1
                continue
            
            non_empty = sum(1 for j in justifs if j and len(j.strip()) > 0)
            coverage = (non_empty / len(rubrics)) * 100 if rubrics else 0
            rubric_coverage.append(coverage)
        
        print(f"  Average rubric coverage: {np.mean(rubric_coverage):.2f}%")
        print(f"  Tasks with 100% coverage: {sum(1 for c in rubric_coverage if c == 100)}/{len(rubric_coverage)} ({sum(1 for c in rubric_coverage if c == 100)/len(rubric_coverage)*100:.1f}%)")
        print(f"  Tasks with empty justifications: {empty_justifications}")
        print(f"  Overall comments present: {sum(1 for c in df['overall_comment'] if c and len(str(c).strip()) > 0)}/{len(df)} ({sum(1 for c in df['overall_comment'] if c and len(str(c).strip()) > 0)/len(df)*100:.1f}%)")
    
    conn.close()

def analyze_length():
    """Analyze justification length statistics"""
    print("\n" + "="*80)
    print("2. LENGTH ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades, overall_comment
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        justif_lengths = []
        comment_lengths = []
        word_counts = []
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            for j in justifs:
                if j:
                    justif_lengths.append(len(j))
                    word_counts.append(len(j.split()))
            
            if row['overall_comment']:
                comment_lengths.append(len(str(row['overall_comment'])))
        
        print(f"\n  Per-rubric justifications:")
        print(f"    Mean length: {np.mean(justif_lengths):.1f} characters")
        print(f"    Median length: {np.median(justif_lengths):.1f} characters")
        print(f"    Mean words: {np.mean(word_counts):.1f} words")
        print(f"    Range: {min(justif_lengths)}-{max(justif_lengths)} characters")
        
        print(f"\n  Overall comments:")
        print(f"    Mean length: {np.mean(comment_lengths):.1f} characters")
        print(f"    Median length: {np.median(comment_lengths):.1f} characters")
        print(f"    Range: {min(comment_lengths)}-{max(comment_lengths)} characters")
    
    conn.close()

def analyze_specificity():
    """Analyze specificity using generic vs specific phrases"""
    print("\n" + "="*80)
    print("3. SPECIFICITY ANALYSIS")
    print("="*80)
    
    # Generic phrases (Indonesian)
    generic_phrases = [
        'cukup baik', 'cukup jelas', 'sudah baik', 'sudah cukup', 
        'masih kurang', 'perlu ditingkatkan', 'perlu diperbaiki',
        'dapat ditingkatkan', 'bisa lebih', 'harus lebih',
        'kurang detail', 'kurang spesifik', 'kurang lengkap',
    ]
    
    # Specific indicators
    specific_indicators = [
        'menunjukkan', 'menjelaskan', 'menyebutkan', 'menguraikan',
        'memberikan contoh', 'mengilustrasikan', 'merinci',
        'menganalisis', 'mengevaluasi', 'membandingkan',
    ]
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        generic_count = 0
        specific_count = 0
        total_justifs = 0
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            for j in justifs:
                if not j:
                    continue
                total_justifs += 1
                
                j_lower = j.lower()
                
                # Check for generic phrases
                has_generic = any(phrase in j_lower for phrase in generic_phrases)
                if has_generic:
                    generic_count += 1
                
                # Check for specific indicators
                has_specific = any(indicator in j_lower for indicator in specific_indicators)
                if has_specific:
                    specific_count += 1
        
        print(f"  Total justifications: {total_justifs}")
        print(f"  Contains generic phrases: {generic_count} ({generic_count/total_justifs*100:.1f}%)")
        print(f"  Contains specific indicators: {specific_count} ({specific_count/total_justifs*100:.1f}%)")
        print(f"  Specificity ratio: {specific_count/generic_count:.2f}" if generic_count > 0 else "  Specificity ratio: N/A")
    
    conn.close()

def analyze_grade_alignment():
    """Analyze if justification sentiment aligns with assigned grade"""
    print("\n" + "="*80)
    print("4. GRADE-JUSTIFICATION ALIGNMENT ANALYSIS")
    print("="*80)
    
    # Keywords for sentiment
    positive_keywords = [
        'baik', 'jelas', 'lengkap', 'detail', 'spesifik', 'komprehensif',
        'mendalam', 'sistematis', 'terstruktur', 'koheren', 'relevan',
        'tepat', 'sesuai', 'akurat', 'kuat', 'solid', 'excellent',
    ]
    
    negative_keywords = [
        'kurang', 'tidak', 'belum', 'minim', 'lemah', 'tidak jelas',
        'tidak lengkap', 'tidak detail', 'tidak spesifik', 'tidak relevan',
        'tidak sesuai', 'tidak tepat', 'perlu', 'harus', 'sebaiknya',
    ]
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades, weighted_score
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        aligned = 0
        misaligned = 0
        neutral = 0
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
                grades_data = json.loads(row['grades']) if isinstance(row['grades'], str) else row['grades']
                # ChatGPT stores letter grades directly
                grade_list = [grades_data.get(rubric, 'C') for rubric in rubrics]
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
                grades_data = json.loads(row['grades']) if isinstance(row['grades'], str) else row['grades']
                grade_list = [grades_data[rubric]['grade'] if isinstance(grades_data[rubric], dict) 
                             else grades_data[rubric] for rubric in rubrics]
            
            for justif, grade in zip(justifs, grade_list):
                if not justif:
                    continue
                
                justif_lower = justif.lower()
                
                # Count keywords
                pos_count = sum(1 for kw in positive_keywords if kw in justif_lower)
                neg_count = sum(1 for kw in negative_keywords if kw in justif_lower)
                
                # Determine sentiment
                if pos_count > neg_count:
                    sentiment = 'positive'
                elif neg_count > pos_count:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                    neutral += 1
                    continue
                
                # Check alignment
                if sentiment == 'positive' and grade in ['A', 'B']:
                    aligned += 1
                elif sentiment == 'negative' and grade in ['D', 'E']:
                    aligned += 1
                elif sentiment == 'positive' and grade in ['D', 'E']:
                    misaligned += 1
                elif sentiment == 'negative' and grade in ['A', 'B']:
                    misaligned += 1
                else:
                    aligned += 1  # Neutral grades (C) are considered aligned
        
        total = aligned + misaligned + neutral
        print(f"  Total analyzed: {total}")
        print(f"  Aligned: {aligned} ({aligned/total*100:.1f}%)")
        print(f"  Misaligned: {misaligned} ({misaligned/total*100:.1f}%)")
        print(f"  Neutral: {neutral} ({neutral/total*100:.1f}%)")
    
    conn.close()

def analyze_actionability():
    """Analyze if justifications provide actionable feedback"""
    print("\n" + "="*80)
    print("5. ACTIONABILITY ANALYSIS")
    print("="*80)
    
    # Actionable phrases
    actionable_phrases = [
        'perlu', 'harus', 'sebaiknya', 'dapat', 'bisa',
        'disarankan', 'direkomendasikan', 'ditambahkan',
        'diperbaiki', 'ditingkatkan', 'dikembangkan',
        'lebih', 'tambahkan', 'perbaiki', 'tingkatkan',
        'jelaskan', 'uraikan', 'sebutkan', 'berikan',
    ]
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades, overall_comment
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        rubric_actionable = 0
        rubric_total = 0
        comment_actionable = 0
        comment_total = 0
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            # Per-rubric justifications
            for j in justifs:
                if not j:
                    continue
                rubric_total += 1
                
                j_lower = j.lower()
                has_actionable = any(phrase in j_lower for phrase in actionable_phrases)
                if has_actionable:
                    rubric_actionable += 1
            
            # Overall comments
            if row['overall_comment']:
                comment_total += 1
                c_lower = str(row['overall_comment']).lower()
                has_actionable = any(phrase in c_lower for phrase in actionable_phrases)
                if has_actionable:
                    comment_actionable += 1
        
        print(f"  Per-rubric justifications:")
        print(f"    Contains actionable phrases: {rubric_actionable}/{rubric_total} ({rubric_actionable/rubric_total*100:.1f}%)")
        
        print(f"\n  Overall comments:")
        print(f"    Contains actionable phrases: {comment_actionable}/{comment_total} ({comment_actionable/comment_total*100:.1f}%)")
    
    conn.close()

def analyze_common_themes():
    """Identify common themes in justifications"""
    print("\n" + "="*80)
    print("6. COMMON THEMES ANALYSIS")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    for model in ['chatgpt', 'gemini']:
        print(f"\n{model.upper()}:")
        
        df = pd.read_sql_query(f"""
            SELECT justification, grades
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
            LIMIT 100
        """, conn)
        
        # Extract key phrases (bigrams and trigrams)
        all_words = []
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            for j in justifs:
                if j:
                    # Remove punctuation and lowercase
                    j_clean = re.sub(r'[^\w\s]', '', j.lower())
                    words = j_clean.split()
                    all_words.extend(words)
        
        # Get most common words (excluding stopwords)
        stopwords = ['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 
                    'adalah', 'ini', 'itu', 'tidak', 'sudah', 'telah', 'dalam',
                    'juga', 'dapat', 'akan', 'atau', 'saya', 'anda']
        
        filtered_words = [w for w in all_words if w not in stopwords and len(w) > 3]
        word_freq = Counter(filtered_words)
        
        print(f"\n  Top 10 most common words:")
        for word, count in word_freq.most_common(10):
            print(f"    {word}: {count}")
    
    conn.close()

def generate_summary_report():
    """Generate summary statistics for paper"""
    print("\n" + "="*80)
    print("7. SUMMARY STATISTICS FOR PAPER")
    print("="*80)
    
    conn = sqlite3.connect('results/grading_results.db')
    
    summary = {}
    
    for model in ['chatgpt', 'gemini']:
        df = pd.read_sql_query(f"""
            SELECT justification, grades, overall_comment
            FROM grading_results
            WHERE model = '{model}' AND strategy = 'lenient' AND status = 'completed'
        """, conn)
        
        # Overall metrics
        total_tasks = len(df)
        justif_lengths = []
        comment_lengths = []
        
        for idx, row in df.iterrows():
            if model == 'chatgpt':
                rubrics, justifs = extract_justifications_chatgpt(row['justification'])
            else:
                rubrics, justifs = extract_justifications_gemini(row['grades'])
            
            for j in justifs:
                if j:
                    justif_lengths.append(len(j))
            
            if row['overall_comment']:
                comment_lengths.append(len(str(row['overall_comment'])))
        
        summary[model] = {
            'total_tasks': total_tasks,
            'total_justifications': len(justif_lengths),
            'avg_justif_length': np.mean(justif_lengths),
            'avg_comment_length': np.mean(comment_lengths),
            'min_justif_length': min(justif_lengths),
            'max_justif_length': max(justif_lengths),
        }
    
    print("\nSummary Table:")
    print("-" * 80)
    print(f"{'Metric':<40} {'ChatGPT':<20} {'Gemini':<20}")
    print("-" * 80)
    print(f"{'Total grading tasks':<40} {summary['chatgpt']['total_tasks']:<20} {summary['gemini']['total_tasks']:<20}")
    print(f"{'Total justifications':<40} {summary['chatgpt']['total_justifications']:<20} {summary['gemini']['total_justifications']:<20}")
    print(f"{'Avg justification length (chars)':<40} {summary['chatgpt']['avg_justif_length']:<20.1f} {summary['gemini']['avg_justif_length']:<20.1f}")
    print(f"{'Avg comment length (chars)':<40} {summary['chatgpt']['avg_comment_length']:<20.1f} {summary['gemini']['avg_comment_length']:<20.1f}")
    print(f"{'Min justification length':<40} {summary['chatgpt']['min_justif_length']:<20} {summary['gemini']['min_justif_length']:<20}")
    print(f"{'Max justification length':<40} {summary['chatgpt']['max_justif_length']:<20} {summary['gemini']['max_justif_length']:<20}")
    print("-" * 80)
    
    conn.close()

def main():
    print("\n" + "="*80)
    print("JUSTIFICATION QUALITY ANALYSIS")
    print("="*80)
    
    analyze_completeness()
    analyze_length()
    analyze_specificity()
    analyze_grade_alignment()
    analyze_actionability()
    analyze_common_themes()
    generate_summary_report()
    
    print("\n" + "="*80)
    print("✓ JUSTIFICATION ANALYSIS COMPLETED!")
    print("="*80)

if __name__ == "__main__":
    main()
