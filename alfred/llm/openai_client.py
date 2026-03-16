from __future__ import annotations
import os
from alfred.llm.base import BaseConsultClient


class OpenAIConsultClient(BaseConsultClient):
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.4")

    def ask(self, prompt: str, thread_id: str | None = None, consultation_type: str | None = None) -> str:
        if not self.api_key:
            return self._stub(prompt, consultation_type)
        try:
            from openai import OpenAI  # type: ignore
        except Exception:
            return self._stub(prompt, consultation_type)
        client = OpenAI(api_key=self.api_key)
        resp = client.responses.create(model=self.model, input=prompt)
        try:
            return getattr(resp, "output_text")
        except Exception:
            return str(resp)

    def _stub(self, prompt: str, consultation_type: str | None) -> str:
        header = f"[stubbed {consultation_type or 'consultation'} response]"
        return (
            f"{header}\n"
            "I received the prompt and recommend a bounded, testable next step.\n"
            f"Prompt excerpt: {prompt[:500]}"
        )
