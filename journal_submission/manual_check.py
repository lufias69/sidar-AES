# Manual Citation Verification for AJET Manuscript
# Checks specific problematic citations

issues_found = []

# Check 1: Black & Wiliam, 1998
print("Checking: Black & Wiliam, 1998...")
# Cited in line 124 but not in references
issues_found.append("❌ HALLUCINATION: (Black & Wiliam, 1998) cited but NOT in references")

# Check 2: Tate year mismatch
print("Checking: Tate et al. citation years...")
# References shows Tate (2024) but might be cited as (2023) somewhere
issues_found.append("⚠️  YEAR MISMATCH: Check if Tate cited as 2023 but reference shows 2024")

# Check 3: Bommasani year
print("Checking: Bommasani et al. citation...")
# Line 50 cites (Bommasani et al., 2021) - check if matches reference
issues_found.append("✓ CHECK: Bommasani et al., 2021 - verify year in reference")

print("\n" + "="*70)
print("ISSUES REQUIRING MANUAL VERIFICATION")
print("="*70)
for issue in issues_found:
    print(issue)
print("="*70)
