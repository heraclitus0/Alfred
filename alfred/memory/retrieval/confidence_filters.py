def filter_by_confidence(items, minimum=0.0): return [i for i in items if i.get("confidence", 1.0) >= minimum]
