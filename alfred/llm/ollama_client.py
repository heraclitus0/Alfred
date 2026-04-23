from __future__ import annotations
import urllib.request
import json
from alfred.llm.base import BaseConsultClient

class OllamaConsultClient(BaseConsultClient):
    def __init__(self) -> None:
        self.model = "phi3:mini"
        self.url = "http://localhost:11434/api/generate"

    def ask(self, prompt: str, thread_id: str | None = None, consultation_type: str | None = None) -> str:
        try:
            body = json.dumps({
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }).encode()
            req = urllib.request.Request(self.url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as r:
                data = json.loads(r.read())
            return data["response"]
        except Exception as e:
            return f"[Ollama error: {e}]"

    def _stub(self, prompt: str, consultation_type: str | None) -> str:
        return "[Ollama not running — start with: ollama serve]"
