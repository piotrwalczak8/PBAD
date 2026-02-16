# =========================
# COLUMN ALIASES
# =========================

COLUMN_ALIASES = {
    "How much do interruptions disrupt your focus and workflow? (1 = not disruptive at all, 5 = very disruptive)": "disruptiveness",
    "How do you rate your productivity in a typical workday? (1 = very low, 5 = very high)": "productivity",
    "How satisfied are you with your job overall (job satisfaction)? (1 = very dissatisfied, 5 = very satisfied)": "job_satisfaction",
    "What is your work arrangement?": "work_arrangement",
    "How frequently do you experience interruptions in a typical workday?": "interruption_frequency",
    "On average, how long does it take you to regain full focus after an interruption?": "time_to_regain_focus",
}

# =========================
# ORDINAL MAPS (DO ANALYSIS)
# =========================

INTERRUPTION_FREQUENCY_MAP = {
    "Less than 3 times per day": 1,
    "3–6 times": 2,
    "7–10 times": 3,
    "More than 10 times": 4,
}

REGAIN_FOCUS_TIME_MAP = {
    "Immediately": 1,
    "1 - 15 minutes": 2,
    "15 - 30 minutes": 3,
    "30 - 60 minutes": 4,
    "more than 60 minutes": 5,
}
