from __future__ import annotations
import os
import time
import urllib.request
import json
from alfred.llm.base import BaseConsultClient

class GeminiConsultClient(BaseConsultClient):
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-2.0-flash-lite"

    def ask(self, prompt: str, thread_id: str | None = None, consultation_type: str | None = None) -> str:
        if not self.api_key:
            return self._stub(prompt, consultation_type)
        for attempt in range(3):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
                body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
                req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req) as r:
                    data = json.loads(r.read())
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait = 30 * (attempt + 1)
                    print(f"[Alfred] Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    return f"[Gemini error: {e}]"

    def _stub(self, prompt: str, consultation_type: str | None) -> str:
        header = f"[stubbed {consultation_type or 'consultation'} response]"
        return (
            f"{header}\n"
            "No GEMINI_API_KEY set.\n"
            f"Prompt excerpt: {prompt[:500]}"
        )
