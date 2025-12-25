import re

# Read manuscript
with open('E:/project/AES/journal_submission/manuscript/MANUSCRIPT_DRAFT_v1.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Split sections
parts = content.split('## REFERENCES')
text_content = parts[0]

# Extract ALL citation patterns more carefully
all_citations = []

# Pattern 1: (Author, Year) or (Author & Author, Year)
pattern1 = re.finditer(r'\(([^()]+?),\s*(\d{4}[a-b]?)\)', text_content)
for match in pattern1:
    authors_raw = match.group(1).strip()
    year = match.group(2).strip()
    # Split by semicolon for multiple citations
    if ';' in authors_raw:
        parts = authors_raw.split(';')
        for part in parts:
            if ',' in part:
                auth = part.split(',')[0].strip()
                all_citations.append(f"{auth}, {year}")
    else:
        all_citations.append(f"{authors_raw}, {year}")

# Get unique citations
unique_cites = sorted(set(all_citations))

print("\n" + "="*70)
print("COMPLETE CITATION LIST FROM MANUSCRIPT")
print("="*70)
for i, cite in enumerate(unique_cites, 1):
    print(f"{i:3}. {cite}")

print(f"\nTotal unique citation instances: {len(unique_cites)}")
print("="*70)

# Now check which ones exist in References
print("\n" + "="*70)
print("CHECKING EACH CITATION AGAINST REFERENCES")
print("="*70)

references_text = parts[1] if len(parts) > 1 else ""

missing = []
found = []

for cite in unique_cites:
    # Extract first author and year
    parts = cite.split(',')
    if len(parts) >= 2:
        author = parts[0].strip().replace('et al.', '').replace('&', '').strip()
        year = parts[1].strip()
        
        # Check if author+year appears in references
        # Look for patterns like "Author, X. (Year)" or "Author. (Year)"
        if re.search(rf'{re.escape(author)}[^(]*?\({year}\)', references_text, re.IGNORECASE):
            found.append(cite)
            print(f"✅ {cite}")
        else:
            missing.append(cite)
            print(f"❌ {cite} - NOT FOUND IN REFERENCES")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"✅ Citations with matching references: {len(found)}")
print(f"❌ HALLUCINATED citations: {len(missing)}")

if missing:
    print("\n⚠️  HALLUCINATED CITATIONS TO FIX:")
    for cite in missing:
        print(f"  - {cite}")

print("="*70 + "\n")
