def risk_class(value: float) -> str: return "critical" if value>0.9 else "high" if value>0.7 else "medium" if value>0.4 else "low"
