import pandas as pd

df = pd.read_excel('data/Jawaban/jawaban UTS  Capstone Project.xlsx')
print(f'✅ Total mahasiswa: {len(df)}')
print(f'✅ Total pertanyaan: {len(df.columns)-1}')
print(f'\n📋 Daftar Mahasiswa:')
for i, name in enumerate(df['Nama']):
    print(f'  {i}. {name}')
