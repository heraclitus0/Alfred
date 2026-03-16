from __future__ import annotations
import os
import webbrowser
from alfred.constants import DEFAULT_CHATGPT_URL, DATA_DIR


class BrowserOperator:
    def __init__(self) -> None:
        self.chatgpt_url = os.getenv("ALFRED_OPEN_CHATGPT_URL", DEFAULT_CHATGPT_URL)
        (DATA_DIR / "exports" / "consultation_exports").mkdir(parents=True, exist_ok=True)

    def open_chatgpt(self, topic: str | None = None, thread_hint: str | None = None) -> None:
        url = self.chatgpt_url
        webbrowser.open(url)
        if topic:
            prompt_path = DATA_DIR / "exports" / "consultation_exports" / "last_browser_topic.txt"
            prompt_path.write_text(
                f"topic={topic}\nthread_hint={thread_hint or ''}\n",
                encoding="utf-8",
            )

    def open_url(self, url: str) -> None:
        webbrowser.open(url)
