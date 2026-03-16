from pathlib import Path
from alfred.memory.summarizers.chat_summarizer import summarize_chat


def import_chat_file(path: str | Path) -> dict:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return {"path": str(path), "summary": summarize_chat(text), "raw": text}
