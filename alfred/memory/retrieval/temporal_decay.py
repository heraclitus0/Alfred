def decay_score(age_seconds: float, half_life: float = 86400.0) -> float:
    return 0.5 ** (age_seconds / half_life)
