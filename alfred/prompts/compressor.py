def compress_context(data: dict, max_chars: int = 2400) -> str:
    text = str(data)
    return text[:max_chars]
