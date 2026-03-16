from alfred.types import ConsultationType


def infer_consultation_type(text: str) -> ConsultationType:
    t = text.lower()
    if any(k in t for k in ["world", "war", "news", "market"]):
        return ConsultationType.WORLD_AWARENESS
    if any(k in t for k in ["talk", "speak", "communication", "phrase"]):
        return ConsultationType.INTERACTION_REFINEMENT
    if any(k in t for k in ["mission", "strategy", "priority", "direction"]):
        return ConsultationType.MISSION_STRATEGY
    return ConsultationType.SELF_IMPROVEMENT
