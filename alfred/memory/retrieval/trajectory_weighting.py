def trajectory_weight(base: float, recurrence: int, recency_score: float) -> float:
    return base + (0.2 * recurrence) + (0.3 * recency_score)
