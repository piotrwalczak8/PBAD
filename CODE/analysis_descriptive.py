import pandas as pd
from scipy.stats import mannwhitneyu
from mappings import COLUMN_ALIASES

DATA_PATH = "data/processed/survey_clean.csv"

LIKERT_COLUMNS = [
    "disruptiveness",
    "productivity",
    "job_satisfaction",
]

WORK_MODE_COLUMN = "work_arrangement"


# =========================
# LOAD & PREPARE DATA
# =========================

df = pd.read_csv(DATA_PATH)

df.columns = (
    df.columns
    .str.replace("\xa0", " ", regex=False)
    .str.strip()
)

df = df.rename(columns=COLUMN_ALIASES)

print("Loaded data shape:", df.shape)


# =========================
# HELPERS
# =========================

def likert_summary(series: pd.Series) -> dict:
    return {
        "n": int(series.count()),
        "median": series.median(),
        "q1": series.quantile(0.25),
        "q3": series.quantile(0.75),
        "iqr": series.quantile(0.75) - series.quantile(0.25),
    }


def print_section(title: str):
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))


# =========================
# 1. DESCRIPTIVE STATISTICS
# =========================

print_section("Descriptive statistics (Likert scales)")

for col in LIKERT_COLUMNS:
    if col in df.columns:
        summary = likert_summary(df[col])
        print(f"\n{col}")
        for k, v in summary.items():
            print(f"  {k}: {v}")


# =========================
# 2. FREQUENCY DISTRIBUTIONS
# =========================

print_section("Frequency distributions")

for col in LIKERT_COLUMNS:
    if col in df.columns:
        freq = df[col].value_counts().sort_index()
        freq.index.name = None
        freq.name = None
        print(f"\n{col}")
        print(freq)


# =========================
# 3. GROUP COMPARISON
# =========================

print_section("Remote vs On-site (Disruptiveness)")

if WORK_MODE_COLUMN in df.columns:
    remote = df[df[WORK_MODE_COLUMN] == "Remote"]["disruptiveness"]
    onsite = df[df[WORK_MODE_COLUMN] == "On-site"]["disruptiveness"]

    if len(remote) > 0 and len(onsite) > 0:
        stat, p = mannwhitneyu(remote, onsite)
        print(f"p-value = {p:.4f}")
