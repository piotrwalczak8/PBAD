import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import numpy as np

# 1. Wczytanie danych
file_path = 'Z_Interruptions in Software Development_ Productivity & Focus Survey(kopia sheet 1 do wykresow).csv'
try:
    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
except Exception:
    df = pd.read_csv(file_path, sep=';', encoding='cp1252')

# 2. Mapowanie wartości tekstowych na skale
mappings = {
    'How\xa0old are you?': {'18 - 24': 1, '25 - 29': 2, '30 - 34': 3, '35-44': 4, '45 - 54': 5, '55 - 64': 6},
    'What is the size of your company?': {'Under 20 employees': 1, '21–100': 2, '101–500': 3, '501–5000': 4, 'More than 5000': 5},
    'How long have you been working in software development?': {'Less than 1 year': 1, '1–3 years': 2, '4–7 years': 3, '8–12 years': 4, 'More than 12 years': 5},
    'How big is your team?': {'1 person (solo)': 1, '2–3 people': 2, '4–7 people': 3, '8–12 people': 4, '13–20 people': 5, 'More than 20 people': 6},
    'How frequently do you experience interruptions in a typical workday?': {'Less than 3 times per day': 1, '3–6 times': 2, '7–10 times': 3, 'More than 10 times': 4},
    'How quickly do you switch to handling the new "interrupting " task?': {'Immediately': 1, '1 - 15 minutes': 2, '15 - 30 minutes': 3, '30 - 60 minutes': 4},
    'On average, how long does it take you to regain full focus after an interruption?': {'Immediately': 1, '1 - 15 minutes': 2, '15 - 30 minutes': 3, '30 - 60 minutes': 4, 'more than 60 minutes': 5}
}

df_corr = df.copy()
for col, mapping in mappings.items():
    if col in df_corr.columns:
        df_corr[col] = df_corr[col].map(mapping)

likert_cols = [
    'How much do interruptions disrupt your focus and workflow?\xa0(1 = not disruptive at all, 5 = very disruptive)',
    'How effective do you consider these methods to be?\xa0(1 = ineffective, 5 = very effective)',
    'How do you rate your productivity in a typical workday?\xa0(1 = very low, 5 = very high)',
    'How often do you feel that interruptions negatively affect the quality of your work? (1 = never, 5 - very often)',
    'How satisfied are you with your job overall (job satisfaction)?\xa0(1 = very dissatisfied, 5 = very satisfied)'
]

rename_map = {
    'How\xa0old are you?': 'Age',
    'What is the size of your company?': 'Company Size',
    'How long have you been working in software development?': 'Experience',
    'How big is your team?': 'Team Size',
    'How frequently do you experience interruptions in a typical workday?': 'Interruption Freq',
    'How quickly do you switch to handling the new "interrupting " task?': 'Switch Speed',
    'On average, how long does it take you to regain full focus after an interruption?': 'Regain Focus Time',
    'How much do interruptions disrupt your focus and workflow?\xa0(1 = not disruptive at all, 5 = very disruptive)': 'Disruption Level',
    'How effective do you consider these methods to be?\xa0(1 = ineffective, 5 = very effective)': 'Method Effectiveness',
    'How do you rate your productivity in a typical workday?\xa0(1 = very low, 5 = very high)': 'Productivity',
    'How often do you feel that interruptions negatively affect the quality of your work? (1 = never, 5 - very often)': 'Neg Quality Effect',
    'How satisfied are you with your job overall (job satisfaction)?\xa0(1 = very dissatisfied, 5 = very satisfied)': 'Job Satisfaction'
}

existing_cols = [c for c in list(mappings.keys()) + likert_cols if c in df_corr.columns]
df_final = df_corr[existing_cols].rename(columns=rename_map)

# 3. Obliczenia
corr_matrix = df_final.corr(method='spearman')

def get_p_values(df):
    cols = df.columns
    p_vals = pd.DataFrame(np.zeros((len(cols), len(cols))), columns=cols, index=cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            if i == j: continue
            mask = ~df.iloc[:, i].isna() & ~df.iloc[:, j].isna()
            _, p = spearmanr(df.iloc[:, i][mask], df.iloc[:, j][mask])
            p_vals.iloc[i, j] = p
    return p_vals

p_values = get_p_values(df_final)

# 4. Generowanie wykresów
# Heatmapa
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Spearman correlation matrix')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')

# Znalezienie najsilniejszych par (poza wiekiem i stażem)
pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        r, p = corr_matrix.iloc[i, j], p_values.iloc[i, j]
        if p < 0.05 and not (corr_matrix.columns[i] == 'Age' and corr_matrix.columns[j] == 'Experience'):
            pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], r))

top_pairs = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)[:3]

# Scatter plots dla Top 3
for idx, (v1, v2, r) in enumerate(top_pairs):
    plt.figure(figsize=(8, 6))
    sns.regplot(data=df_final, x=v1, y=v2, x_jitter=0.2, y_jitter=0.2, scatter_kws={'alpha':0.5})
    plt.title(f'Correlation: {v1} vs {v2}\nSpearman r = {r:.3f}')
    plt.tight_layout()
    plt.savefig(f'top_korelacja_{idx+1}.png')

print("pliki .png w folderze.")