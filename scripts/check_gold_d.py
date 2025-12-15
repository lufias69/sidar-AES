import os
import json

path = 'results/gold_standard'
files = [f for f in os.listdir(path) if f.endswith('.json')]
print(f'Found {len(files)} gold standard files (students)\n')

scores = []
for f in files:
    with open(os.path.join(path, f), 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Each file has multiple questions
        for q in data['questions']:
            scores.append(q['weighted_score'])

def to_grade(s):
    if s >= 3.5: return 'A'
    elif s >= 2.5: return 'B'
    elif s >= 1.5: return 'C'
    elif s >= 0.5: return 'D'
    else: return 'E'

grades = {}
for s in scores:
    g = to_grade(s)
    grades[g] = grades.get(g, 0) + 1

print('=' * 60)
print('GOLD STANDARD Grade Distribution')
print('=' * 60)
for g in sorted(grades.keys()):
    print(f'{g}: {grades[g]:2d} ({grades[g]/len(scores)*100:5.1f}%)')

print(f'\nTotal tasks: {len(scores)}')
print(f'Min score: {min(scores):.1f}')
print(f'Max score: {max(scores):.1f}')
print(f'Avg score: {sum(scores)/len(scores):.2f}')

# Count D grades
d_count = sum(1 for s in scores if 0.5 <= s < 1.5)
print(f'\n' + '=' * 60)
print(f'D grades in gold standard: {d_count} ({d_count/len(scores)*100:.1f}%)')
print('=' * 60)

if d_count == 0:
    print("\n✅ EXPLANATION:")
    print("Gold standard has NO D grades!")
    print("That's why confusion matrix shows no D in Gold Standard axis.")
    print("\nThe AI actually gave 4 D grades (0.6% of 700 tasks)")
    print("But since gold standard has no D, these appear in confusion matrix")
    print("as misclassifications where gold=C/B but AI predicted=D (very rare)")

