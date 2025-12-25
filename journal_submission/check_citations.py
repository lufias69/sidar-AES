import re
from collections import defaultdict

# Read manuscript
with open('E:/project/AES/journal_submission/manuscript/MANUSCRIPT_DRAFT_v1.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into text and references sections
parts = content.split('## REFERENCES')
text_content = parts[0]
references_content = parts[1] if len(parts) > 1 else ""

# Extract all citations from text (various formats)
citation_patterns = [
    r'\(([A-Z][A-Za-z\s&\.]+),?\s+(\d{4}[a-b]?)\)',  # (Author, 2023)
    r'\(([A-Z][A-Za-z\s&\.]+)\s+et\s+al\.,?\s+(\d{4}[a-b]?)\)',  # (Author et al., 2023)
]

citations_in_text = set()
for pattern in citation_patterns:
    matches = re.finditer(pattern, text_content)
    for match in matches:
        author = match.group(1).strip().replace(' et al.', '').replace('et al.', '')
        year = match.group(2).strip()
        # Clean author name
        author = author.replace(' &', '').replace(' and', '').strip()
        if author and year:
            citations_in_text.add((author, year))

# Extract all reference entries (first author + year)
reference_entries = set()
ref_lines = references_content.split('\n')
for line in ref_lines:
    # Match pattern: Author, X. (Year) or Author, X., & Author, Y. (Year)
    match = re.match(r'^([A-Za-z\s\-]+),\s+[A-Z]\..*?\((\d{4}[a-b]?)\)', line.strip())
    if match:
        author = match.group(1).strip()
        year = match.group(2).strip()
        reference_entries.add((author, year))
    # Also match corporate authors like "OpenAI. (2023)"
    match2 = re.match(r'^([A-Za-z\s]+)\.\s+\((\d{4}[a-b]?)\)', line.strip())
    if match2:
        author = match2.group(1).strip()
        year = match2.group(2).strip()
        reference_entries.add((author, year))

print("\n" + "="*60)
print("CITATION VERIFICATION REPORT")
print("="*60)

print(f"\n📚 Citations in text: {len(citations_in_text)}")
print(f"📖 Entries in References: {len(reference_entries)}")

# Find citations in text but not in references (HALLUCINATIONS)
hallucinations = []
for author, year in sorted(citations_in_text):
    # Check if this citation exists in references
    found = False
    for ref_author, ref_year in reference_entries:
        if year == ref_year and (author.lower() in ref_author.lower() or ref_author.lower() in author.lower()):
            found = True
            break
    if not found:
        hallucinations.append((author, year))

# Find references not cited in text (UNUSED)
unused = []
for ref_author, ref_year in sorted(reference_entries):
    found = False
    for author, year in citations_in_text:
        if ref_year == year and (author.lower() in ref_author.lower() or ref_author.lower() in author.lower()):
            found = True
            break
    if not found:
        unused.append((ref_author, ref_year))

print("\n" + "="*60)
if hallucinations:
    print("⚠️  HALLUCINATED CITATIONS (in text, NOT in references):")
    print("="*60)
    for author, year in hallucinations:
        print(f"  ❌ ({author}, {year})")
else:
    print("✅ NO HALLUCINATIONS - All citations have matching references")

print("\n" + "="*60)
if unused:
    print("📌 UNUSED REFERENCES (in references, NOT cited in text):")
    print("="*60)
    for author, year in unused:
        print(f"  ⚠️  {author} ({year})")
else:
    print("✅ ALL REFERENCES USED - No orphaned entries")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"  Citations in text: {len(citations_in_text)}")
print(f"  Reference entries: {len(reference_entries)}")
print(f"  Hallucinations: {len(hallucinations)}")
print(f"  Unused references: {len(unused)}")
print("="*60 + "\n")
