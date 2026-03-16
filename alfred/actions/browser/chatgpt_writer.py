from pathlib import Path
from alfred.constants import DATA_DIR


def write_browser_prompt(prompt: str) -> str:
    path = DATA_DIR / "exports" / "consultation_exports" / "browser_prompt.txt"
    path.write_text(prompt, encoding="utf-8")
    return str(path)
