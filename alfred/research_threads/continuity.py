def continue_summary(previous: str, new: str) -> str:
    if not previous:
        return new[:1200]
    return (previous + "\n\n" + new)[:1200]
