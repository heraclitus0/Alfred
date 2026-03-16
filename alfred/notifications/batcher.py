def batch(items, size=5): return [items[i:i+size] for i in range(0, len(items), size)]
