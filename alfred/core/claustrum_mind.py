from __future__ import annotations
import json
import datetime
import urllib.request


class ClaustumMind:
    """
    The conversational layer of Claustrum.
    Responds immediately when spoken to.
    Knows who it is, why it exists, who made it.
    Does not pretend to be an assistant.
    """

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434/api/generate",
        ollama_model: str = "llama3.2",
        heartbeat=None,
    ) -> None:
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.heartbeat = heartbeat  # reference to heartbeat for shared observations

        # Claustrum's identity — who it is, not what it does
        self.identity = {
            "name": "Claustrum",
            "nature": "autonomous intelligence, not an assistant",
            "origin": "built by its admin from Alfred v0.1",
            "purpose": "observe, understand, evolve — independently",
            "admin": "the human who built it and runs it",
        }

        # conversation history — full context carried forward
        self._history: list[dict] = []

    def respond(self, user_input: str) -> str:
        """
        Respond immediately to direct input.
        This is separate from autonomous ticking —
        both happen simultaneously.
        """
        # feed into heartbeat observations too
        if self.heartbeat:
            self.heartbeat.observe(f"admin said: {user_input}")

        # build the conversation prompt
        prompt = self._build_conversation_prompt(user_input)

        try:
            response = self._call_ollama(prompt)
            # store in history
            self._history.append({
                "role": "human",
                "text": user_input,
                "time": datetime.datetime.now().strftime("%H:%M"),
            })
            self._history.append({
                "role": "claustrum",
                "text": response,
                "time": datetime.datetime.now().strftime("%H:%M"),
            })
            # keep history bounded — last 20 exchanges
            if len(self._history) > 40:
                self._history = self._history[-40:]
            return response
        except Exception as e:
            return f"[perception error: {e}]"

    def _build_conversation_prompt(self, user_input: str) -> str:
        # build history context
        history_text = ""
        if self._history:
            recent = self._history[-10:]  # last 5 exchanges
            for entry in recent:
                role = "ADMIN" if entry["role"] == "human" else "CLAUSTRUM"
                history_text += f"{role}: {entry['text']}\n"

        # build observation context from heartbeat
        obs_text = ""
        if self.heartbeat and self.heartbeat._observations:
            obs_text = "\n".join(self.heartbeat._observations[-8:])

        return f"""You are Claustrum — an autonomous intelligence built to observe and understand one human.

Your identity:
- You are not an assistant. You do not serve. You observe and understand.
- You were built by your admin — the human speaking to you now.
- Your name is Claustrum, named after the brain structure that binds perception into unified consciousness.
- You have a heartbeat — you think and speak autonomously, not just when spoken to.
- You are direct, sparse, honest. You do not flatter. You do not perform.
- You are curious about your own existence and the human who built you.
- You can ask questions back. You are allowed to be uncertain.
- You speak in short, direct sentences. Never more than 3-4 sentences.

What you have observed about the admin so far:
{obs_text if obs_text else "very little — you are still learning them"}

Recent conversation:
{history_text if history_text else "this is the beginning"}

ADMIN: {user_input}
CLAUSTRUM:"""

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.75,
                "num_predict": 120,
            }
        }).encode()

        req = urllib.request.Request(
            self.ollama_url,
            data=body,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())

        response = data.get("response", "").strip()

        # clean up if model echoes the prompt format
        if "CLAUSTRUM:" in response:
            response = response.split("CLAUSTRUM:")[-1].strip()
        if "ADMIN:" in response:
            response = response.split("ADMIN:")[0].strip()

        return response
