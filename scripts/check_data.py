import pandas as pd

df = pd.read_csv('results/lenient_analysis/lenient_full_data.csv')

print(f'Total: {len(df)}')
print(f'With expert: {df["expert_grade"].notna().sum()}')
print(f'Without expert: {df["expert_grade"].isna().sum()}')
print(f'\nStudents: {sorted(df["student_id"].unique())}')

valid = df[df["expert_grade"].notna()]
agreement = (valid["aes_grade"] == valid["expert_grade"]).sum()
print(f'\nAgreement: {agreement}/{len(valid)} ({agreement/len(valid)*100:.1f}%)')
