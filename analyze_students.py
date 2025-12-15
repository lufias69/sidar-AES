"""
Analyze students and select best 10 for baseline
"""
import pandas as pd
import numpy as np

df = pd.read_excel('data/Jawaban/jawaban UTS  Capstone Project.xlsx')

# Analyze each student
student_stats = []

for idx, row in df.iterrows():
    name = row['Nama']
    
    # Calculate total length of all answers
    total_length = 0
    total_words = 0
    answer_count = 0
    
    for col in df.columns[1:]:  # Skip 'Nama'
        answer = str(row[col])
        if pd.notna(row[col]) and answer.strip():
            total_length += len(answer)
            total_words += len(answer.split())
            answer_count += 1
    
    avg_length = total_length / answer_count if answer_count > 0 else 0
    avg_words = total_words / answer_count if answer_count > 0 else 0
    
    student_stats.append({
        'index': idx,
        'name': name,
        'total_length': total_length,
        'total_words': total_words,
        'avg_length': avg_length,
        'avg_words': avg_words,
        'answer_count': answer_count
    })

# Sort by total length (longest first)
student_stats.sort(key=lambda x: x['total_length'], reverse=True)

print("="*80)
print("ANALISIS MAHASISWA - Ranking berdasarkan panjang jawaban")
print("="*80)
print(f"\nTotal mahasiswa: {len(student_stats)}")
print(f"Pertanyaan per mahasiswa: 7\n")

for i, stat in enumerate(student_stats, 1):
    print(f"{i:2d}. {stat['name']:15s} | "
          f"Total chars: {stat['total_length']:5d} | "
          f"Total words: {stat['total_words']:4d} | "
          f"Avg words/answer: {stat['avg_words']:5.1f}")

print("\n" + "="*80)
print("REKOMENDASI: 10 MAHASISWA TERBAIK untuk BASELINE")
print("="*80)
print("\nMahasiswa dengan jawaban terlengkap/terpanjang:\n")

top_10 = student_stats[:10]
for i, stat in enumerate(top_10, 1):
    print(f"{i}. {stat['name']} (Index: {stat['index']})")
    print(f"   - Total karakter: {stat['total_length']}")
    print(f"   - Total kata: {stat['total_words']}")
    print(f"   - Rata-rata kata per jawaban: {stat['avg_words']:.1f}\n")

print("="*80)
print("MAHASISWA YANG TIDAK DIPILIH (Jawaban terlalu pendek):")
print("="*80)
excluded = student_stats[10:]
for i, stat in enumerate(excluded, 1):
    print(f"{i}. {stat['name']} - Total kata: {stat['total_words']} (terlalu pendek)")

# Save indices to file
with open('selected_students.txt', 'w') as f:
    f.write("# 10 Mahasiswa Terpilih untuk Baseline\n")
    f.write("# Format: index,nama,total_words\n\n")
    for stat in top_10:
        f.write(f"{stat['index']},{stat['name']},{stat['total_words']}\n")

print(f"\n✅ Indeks mahasiswa terpilih disimpan di: selected_students.txt")
