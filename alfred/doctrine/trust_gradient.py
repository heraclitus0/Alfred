def trust_score(successes: int, failures: int) -> float: return successes / max(1, successes + failures)
