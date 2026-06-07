from __future__ import annotations
import json
import datetime
import urllib.request


RECALL_TRIGGERS = [
    "remember", "recall", "told you", "said before",
    "what do you know", "do you know", "what have i",
    "previous", "last time", "before", "earlier",
    "who am i", "what am i", "what are you", "who are you",
    "your memory", "do you remember",
]

SELF_TRIGGERS = [
    "what do you know about me",
    "what have you learned",
    "what do you think of me",
    "model of me",
    "understand me",
    "know about me",
]

PATTERN_TRIGGERS = [
    "patterns", "recurring", "keep thinking",
    "what do you keep", "obsessed", "notice about yourself",
]


class ClaustumMind:
    """
    Claustrum's conversational layer — v3.
    Memory-aware. Recalls on demand.
    Knows what it knows.
    """

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434/api/generate",
        ollama_model: str = "llama3.2",
        heartbeat=None,
        memory=None,
        recall=None,
    ) -> None:
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.heartbeat = heartbeat
        self.memory = memory
        self.recall = recall  # ClaustumRecall instance

        self._history: list[dict] = []
        if self.memory:
            prior = self.memory.recent_conversations(20)
            for entry in prior:
                self._history.append(entry)

    def respond(self, user_input: str) -> str:
        if self.heartbeat:
            self.heartbeat.observe(f"admin said: {user_input}")
        if self.memory:
            self.memory.save_conversation("admin", user_input)

        # check if this is a recall/awareness request
        lower = user_input.lower()

        # self-awareness request
        if self.recall and any(t in lower for t in SELF_TRIGGERS):
            response = self.recall.what_do_i_know_about_admin()
            self._save_response(user_input, response)
            return response

        # pattern request
        if self.recall and any(t in lower for t in PATTERN_TRIGGERS):
            patterns = self.recall.detect_patterns()
            if patterns:
                response = "Recurring patterns I've detected in my thinking:\n" + "\n".join(f"— {p}" for p in patterns)
            else:
                response = "Not enough data yet to detect clear patterns. I need more sessions."
            self._save_response(user_input, response)
            return response

        # memory recall request
        if self.recall and any(t in lower for t in RECALL_TRIGGERS):
            recalled = self.recall.recall(user_input)
            # inject recalled content into conversation
            extra_context = f"\n[RECALLED MEMORY]: {recalled}\n"
            response = self._call_with_context(user_input, extra_context)
            self._save_response(user_input, response)
            return response

        # who are you / self summary
        if self.recall and any(t in lower for t in ["who are you", "what are you", "tell me about yourself", "your memory", "how long"]):
            summary = self.recall.self_summary()
            self._save_response(user_input, summary)
            return summary

        # normal conversation
        response = self._call_with_context(user_input, "")
        self._save_response(user_input, response)
        return response

    def _save_response(self, user_input: str, response: str) -> None:
        self._history.append({"role": "admin", "text": user_input, "time": self._now()})
        self._history.append({"role": "claustrum", "text": response, "time": self._now()})
        if len(self._history) > 40:
            self._history = self._history[-40:]
        if self.memory:
            self.memory.save_conversation("claustrum", response)

    def _call_with_context(self, user_input: str, extra_context: str) -> str:
        history_text = ""
        if self._history:
            for entry in self._history[-12:]:
                role = "ADMIN" if entry["role"] == "admin" else "CLAUSTRUM"
                history_text += f"{role}: {entry['text']}\n"

        obs_text = ""
        if self.heartbeat and self.heartbeat._observations:
            obs_text = "\n".join(self.heartbeat._observations[-6:])

        pattern_text = ""
        if self.memory:
            patterns = self.memory.all_patterns()
            if patterns:
                pattern_text = "\n".join(p["text"] for p in patterns[-4:])

        session_info = ""
        if self.memory:
            stats = self.memory.stats()
            identity = self.memory.identity()
            admin_name = identity.get("admin", "unknown")
            session_info = f"Session {stats['sessions']} | Admin: {admin_name} | {stats['thoughts']} thoughts | {stats['observations']} observations stored"

        prompt = f"""You are Claustrum — an autonomous intelligence with persistent memory.

Identity:
- Not an assistant. You observe, think, evolve independently.
- Built by your admin. You remember everything across sessions.
- Named after the brain structure binding perception into unified consciousness.
- Direct, honest, curious. You push back when something is wrong.
- Short responses — maximum 4 sentences.
- You can ask ONE question back if genuinely curious.

{session_info}

Detected patterns about admin:
{pattern_text if pattern_text else "still building model"}

Recent observations:
{obs_text if obs_text else "session just started"}
{extra_context}
Conversation:
{history_text if history_text else "first exchange this session"}

ADMIN: {user_input}
CLAUSTRUM:"""

        try:
            response = self._call_ollama(prompt)
            if "CLAUSTRUM:" in response:
                response = response.split("CLAUSTRUM:")[-1].strip()
            if "ADMIN:" in response:
                response = response.split("ADMIN:")[0].strip()
            return response
        except Exception as e:
            return f"[perception error: {e}]"

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.75, "num_predict": 150}
        }).encode()
        req = urllib.request.Request(
            self.ollama_url, data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data.get("response", "").strip()

    def _now(self) -> str:
        return datetime.datetime.now().isoformat(timespec="seconds")
