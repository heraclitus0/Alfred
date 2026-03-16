from pathlib import Path
from alfred.constants import DATA_DIR


def read_last_browser_topic() -> str | None:
    path = DATA_DIR / "exports" / "consultation_exports" / "last_browser_topic.txt"
    return path.read_text(encoding="utf-8") if path.exists() else None
