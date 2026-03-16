def score_prompt(prompt: str) -> float: return min(1.0, max(0.1, len(prompt)/1000))
