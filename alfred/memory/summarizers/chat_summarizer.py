def summarize_chat(text: str, max_chars: int = 1200) -> str:
    text = " ".join(text.split())
    return text[:max_chars]
