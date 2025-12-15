import pandas as pd

# Load Excel
df = pd.read_excel('data/Jawaban/jawaban UTS  Capstone Project.xlsx')
print(f"Total mahasiswa di Excel: {len(df)}")

# Parse selected_students.txt
with open('selected_students.txt', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

selected_names = [line.split(',')[1] for line in lines if ',' in line]
print(f"\nNama terpilih dari file ({len(selected_names)}):")
for name in selected_names:
    print(f"  - {name}")

# Filter
filtered_df = df[df['Nama'].isin(selected_names)]
print(f"\nHasil filtering: {len(filtered_df)} mahasiswa")
print("Mahasiswa yang ter-filter:")
for name in filtered_df['Nama'].tolist():
    print(f"  - {name}")
