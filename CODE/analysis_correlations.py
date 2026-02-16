import pandas as pd
from scipy.stats import spearmanr
from mappings import (
    COLUMN_ALIASES,
    INTERRUPTION_FREQUENCY_MAP,
    REGAIN_FOCUS_TIME_MAP,
)

DATA_PATH = "data/processed/survey_clean.csv"


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


# =========================
# MAP ORDINAL VARIABLES
# =========================

df["interruption_frequency_num"] = (
    df["interruption_frequency"]
    .map(INTERRUPTION_FREQUENCY_MAP)
)

df["time_to_regain_focus_num"] = (
    df["time_to_regain_focus"]
    .map(REGAIN_FOCUS_TIME_MAP)
)


# =========================
# CORRELATIONS
# =========================

def spearman(x, y, label):
    rho, p = spearmanr(x, y, nan_policy="omit")
    print(f"{label}: rho={rho:.3f}, p={p:.4f}")


print("\nExploratory correlations (Spearman)")
print("----------------------------------")

spearman(
    df["disruptiveness"],
    df["productivity"],
    "Disruptiveness vs Productivity",
)

spearman(
    df["interruption_frequency_num"],
    df["disruptiveness"],
    "Interruption frequency vs Disruptiveness",
)

spearman(
    df["time_to_regain_focus_num"],
    df["disruptiveness"],
    "Time to regain focus vs Disruptiveness",
)
