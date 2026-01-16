import pandas as pd
import numpy as np
from pathlib import Path

from mappings import (
    COLUMN_ALIASES,
    WORK_ARRANGEMENT_MAP,
    YES_NO_MAP,
)

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "survey_raw.xlsx"
CLEAN_DATA_PATH = BASE_DIR / "data" / "processed" / "survey_clean.csv"

# =========================
# CONFIG
# =========================

# wartości traktowane jako brak danych
MISSING_VALUES = [
    "idk", "i dont know", "i don't know", ".", "-", "—", "nan", "none", ""
]

# kolumny tekstowe do normalizacji (PRZED mapowaniem)
TEXT_COLUMNS = [
    "What is your work arrangement?",
    "Is your educational background related to STEM (Science, Technology, Engineering, Mathematics)?",
    "Do you use any techniques to reduce interruptions (e.g., focus time, “do not disturb” status)?",
]

# kolumny Likerta (po aliasowaniu!)
LIKERT_COLUMNS = [
    "disruptiveness",
    "productivity",
    "job_satisfaction",
]

# =========================
# FUNCTIONS
# =========================

def load_raw_data(path: Path) -> pd.DataFrame:
    """Load raw survey data from Excel."""
    return pd.read_excel(path)


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace pseudo-missing values with NaN."""
    return df.replace(MISSING_VALUES, np.nan)


def normalize_text(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Lowercase and trim selected text columns."""
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )
    return df


def apply_column_aliases(df: pd.DataFrame) -> pd.DataFrame:
    """Rename verbose questionnaire columns to short aliases."""
    return df.rename(columns=COLUMN_ALIASES)


def map_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize categorical values using shared mappings."""

    if "work_arrangement" in df.columns:
        df["work_arrangement"] = (
            df["work_arrangement"]
            .map(WORK_ARRANGEMENT_MAP)
            .fillna(df["work_arrangement"])
        )

    if "do_you_use_any_techniques" in df.columns:
        df["do_you_use_any_techniques"] = (
            df["do_you_use_any_techniques"]
            .map(YES_NO_MAP)
            .fillna(df["do_you_use_any_techniques"])
        )

    if "educational_background_related_to_stem" in df.columns:
        df["educational_background_related_to_stem"] = (
            df["educational_background_related_to_stem"]
            .map(YES_NO_MAP)
            .fillna(df["educational_background_related_to_stem"])
        )

    return df


def convert_likert_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Likert scale columns (1–5) to numeric."""
    for col in LIKERT_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def save_clean_data(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned dataset."""
    df.to_csv(path, index=False)


# =========================
# PIPELINE
# =========================

def preprocess() -> pd.DataFrame:
    df = load_raw_data(RAW_DATA_PATH)

    df = clean_missing_values(df)
    df = normalize_text(df, TEXT_COLUMNS)

    # aliasowanie nazw kolumn (KANONICZNE)
    df = apply_column_aliases(df)

    # mapowanie kategorii po aliasowaniu
    df = map_categories(df)

    # konwersja skal Likerta
    df = convert_likert_to_numeric(df)

    # sanity check (możesz później usunąć)
    print(df.head())
    print(df.info())

    save_clean_data(df, CLEAN_DATA_PATH)
    return df


if __name__ == "__main__":
    preprocess()
