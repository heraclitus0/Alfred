def classify_target(target: str) -> str:
    if target in {"kill_switch", "credential_guard", "approval_engine"}:
        return "critical"
    if target in {"prompts", "summarizers", "heuristics", "recommendation_logic"}:
        return "medium"
    return "low"
