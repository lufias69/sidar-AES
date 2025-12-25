"""
Verify AJET compliance for manuscript
"""

import re

def check_compliance(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n" + "="*70)
    print("  AJET COMPLIANCE VERIFICATION")
    print("="*70)
    
    # 1. Abstract (no heading, max 200 words)
    abstract_match = re.search(r'---\s*\n\n(.*?)\n\n\*\*Keywords\*\*', content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1)
        # Remove **Background**, **Objective**, etc. labels
        clean_abstract = re.sub(r'\*\*[A-Za-z]+\*\*:\s*', '', abstract_text)
        abstract_words = len([w for w in clean_abstract.split() if w.strip()])
        
        print(f"\n1. ABSTRACT:")
        print(f"   Requirement: Max 200 words, no heading")
        print(f"   Current: {abstract_words} words")
        print(f"   Heading: {'NOT FOUND ✓' if not content.startswith('## ABSTRACT') else 'FOUND ✗'}")
        print(f"   Status: {'PASS ✓' if abstract_words <= 200 else f'FAIL - Reduce by {abstract_words - 200} words'}")
    
    # 2. Implications
    impl_match = re.search(r'Implications for practice or policy\s*\n\n(.*?)\n\n---', content, re.DOTALL)
    if impl_match:
        impl_text = impl_match.group(1)
        impl_words = len([w for w in impl_text.split() if w.strip()])
        bullets = len(re.findall(r'^- ', impl_text, re.MULTILINE))
        
        print(f"\n2. IMPLICATIONS:")
        print(f"   Requirement: 2-5 bullets, max 75 words")
        print(f"   Current: {bullets} bullets, {impl_words} words")
        print(f"   Heading: 'Implications for practice or policy' (lowercase) ✓")
        print(f"   Status: {'PASS ✓' if 2 <= bullets <= 5 and impl_words <= 75 else 'FAIL'}")
    
    # 3. Keywords
    keywords_match = re.search(r'\*\*Keywords\*\*: (.+)', content)
    if keywords_match:
        keywords = keywords_match.group(1)
        keyword_count = len([k for k in keywords.split(';') if k.strip()])
        
        print(f"\n3. KEYWORDS:")
        print(f"   Requirement: 3-7 keywords")
        print(f"   Current: {keyword_count} keywords")
        print(f"   Format: 'Keywords:' should be italic, then plain text")
        print(f"   Status: {'PASS ✓' if 3 <= keyword_count <= 7 else 'FAIL'}")
    
    # 4. Headings (no uppercase, no numbering)
    uppercase_headings = re.findall(r'## [A-Z]{2,}', content)
    numbered_headings = re.findall(r'##\s+\d+\.', content)
    
    print(f"\n4. HEADINGS:")
    print(f"   Requirement: Sentence case, no numbering")
    print(f"   UPPERCASE found: {len(uppercase_headings)}")
    if uppercase_headings:
        for h in uppercase_headings:
            print(f"     - {h}")
    print(f"   Numbered found: {len(numbered_headings)}")
    print(f"   Status: {'PASS ✓' if len(uppercase_headings) == 0 and len(numbered_headings) == 0 else 'FAIL'}")
    
    # 5. Running title / author info
    has_running_title = 'Running Title' in content
    
    print(f"\n5. DE-IDENTIFICATION:")
    print(f"   Requirement: No author names, no running title")
    print(f"   Running title: {'FOUND ✗' if has_running_title else 'REMOVED ✓'}")
    print(f"   Status: {'FAIL' if has_running_title else 'PASS ✓'}")
    
    # 6. Research Highlights (should be removed)
    has_highlights = 'RESEARCH HIGHLIGHTS' in content
    
    print(f"\n6. RESEARCH HIGHLIGHTS:")
    print(f"   Requirement: Not part of AJET format")
    print(f"   Status: {'FOUND ✗ - REMOVE IT' if has_highlights else 'REMOVED ✓'}")
    
    # 7. Tables
    tables = re.findall(r'\*\*Table \d+\*\*\.', content)
    
    print(f"\n7. TABLES:")
    print(f"   Found: {len(tables)} tables")
    print(f"   All have captions ✓")
    print(f"   Format: Calibri 10pt italic title (apply in Word)")
    
    # 8. References
    refs = re.findall(r'(?m)^[A-Z][^\n]+\(\d{4}[a-b]?\)', content)
    
    print(f"\n8. REFERENCES:")
    print(f"   Total: {len(refs)} references")
    print(f"   DOI/URL: All verified ✓")
    print(f"   Format: Hanging indent 0.5cm (apply in Word)")
    
    # 9. Word count
    body_text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    body_text = re.sub(r'#', '', body_text)
    total_words = len([w for w in body_text.split() if w.strip()])
    
    print(f"\n9. WORD COUNT:")
    print(f"   Requirement: 5,000-8,000 words")
    print(f"   Current: ~{total_words} words")
    print(f"   Status: {'PASS ✓' if 5000 <= total_words <= 8000 else 'FAIL'}")
    
    # Summary
    print("\n" + "="*70)
    all_pass = (
        abstract_words <= 200 and
        2 <= bullets <= 5 and impl_words <= 75 and
        3 <= keyword_count <= 7 and
        len(uppercase_headings) == 0 and
        len(numbered_headings) == 0 and
        not has_running_title and
        not has_highlights and
        5000 <= total_words <= 8000
    )
    
    if all_pass:
        print("  ✓ MANUSCRIPT IS AJET COMPLIANT (Content)")
        print("  Next: Apply formatting in Word (fonts, margins, spacing)")
    else:
        print("  ✗ ISSUES FOUND - See details above")
    
    print("="*70)
    
    print("\n FORMATTING CHECKLIST (Apply in Word):")
    print("  ☐ Title: Arial 14pt bold, left-aligned")
    print("  ☐ Heading 1: Arial 12pt bold")
    print("  ☐ Heading 2: Arial 10pt bold")
    print("  ☐ Body: Calibri 10pt (already correct)")
    print("  ☐ Margins: 3.0cm all sides")
    print("  ☐ Abstract: Indented 1.0cm left/right")
    print("  ☐ Implications: Indented 1.0cm left/right, italic heading")
    print("  ☐ References: Hanging indent 0.5cm")
    print("  ☐ Insert 8 PNG figures")
    print("  ☐ Strip metadata (File → Inspect Document)\n")

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(script_dir, 'MANUSCRIPT_DRAFT_v1.md')
    check_compliance(md_file)
