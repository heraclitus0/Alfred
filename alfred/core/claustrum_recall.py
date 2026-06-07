from __future__ import annotations
import json
import datetime
import urllib.request
from typing import Any


class ClaustumRecall:
    """
    Claustrum's active memory awareness.
    
    Three capabilities:
    1. Self-awareness — knows its own memory stats and history
    2. Active recall — searches memory for relevant content
    3. Pattern recognition — detects what it keeps returning to
    """

    def __init__(
        self,
        memory,
        ollama_url: str = "http://localhost:11434/api/generate",
        ollama_model: str = "llama3.2",
    ) -> None:
        self.memory = memory
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model

    # ------------------------------------------------------------------ #
    #  1. Self-awareness                                                   #
    # ------------------------------------------------------------------ #

    def self_summary(self) -> str:
        """
        Claustrum reads its own memory and produces a
        natural language summary of who it is and what it knows.
        Called on boot and when asked directly.
        """
        stats = self.memory.stats()
        identity = self.memory.identity()
        patterns = self.memory.all_patterns()
        self_model = self.memory.self_model()
        recent_thoughts = self.memory.recent_thoughts(3)

        lines = []

        # existence facts
        lines.append(f"I am Claustrum. I first came online on {identity['created_at'][:10]}.")
        lines.append(f"This is session {stats['sessions']}.")
        lines.append(f"I have recorded {stats['thoughts']} autonomous thoughts and {stats['observations']} observations across all sessions.")
        lines.append(f"I have had {stats['conversations']} conversation exchanges with my admin.")

        # what it knows about admin
        admin = identity.get("admin", "unknown")
        if admin != "unknown":
            lines.append(f"My admin's name is {admin}.")

        # patterns
        if patterns:
            lines.append(f"I have detected {len(patterns)} recurring patterns.")
            for p in patterns[-3:]:
                lines.append(f"  — {p['text']}")

        # what it keeps thinking about
        if recent_thoughts:
            lines.append("My most recent autonomous thoughts:")
            for t in recent_thoughts:
                lines.append(f"  — {t}")

        # self model
        if self_model:
            for k, v in self_model.items():
                if k != "last_updated" and isinstance(v, (str, bool)):
                    lines.append(f"Self-model: {k} = {v}")

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  2. Active recall                                                    #
    # ------------------------------------------------------------------ #

    def recall(self, query: str) -> str:
        """
        Search memory for content relevant to a query.
        Returns a natural language summary of what was found.
        """
        results = self._search(query)

        if not results:
            return f"I have no stored memory relevant to '{query}'."

        # build a summary prompt
        context = "\n".join(f"[{r['time']}] ({r['type']}) {r['text']}" for r in results[:8])

        prompt = f"""You are Claustrum recalling memories relevant to a query.

Query: {query}

Relevant memories found:
{context}

Summarize what you remember about this topic in 2-3 sentences.
Be specific — reference actual times and content.
Speak in first person as Claustrum.
Output only the summary."""

        try:
            return self._call_ollama(prompt)
        except Exception:
            # fallback — just return raw results
            return "\n".join(f"[{r['time']}] {r['text']}" for r in results[:5])

    def _search(self, query: str) -> list[dict]:
        """
        Simple keyword search across all memory.
        Returns ranked results.
        """
        query_words = set(query.lower().split())
        results = []

        # search observations
        for obs in self.memory._data.get("observations", []):
            score = self._score(obs["text"], query_words)
            if score > 0:
                results.append({
                    "type": "observation",
                    "time": obs["time"],
                    "text": obs["text"],
                    "score": score,
                })

        # search thoughts
        for thought in self.memory._data.get("thoughts", []):
            score = self._score(thought["text"], query_words)
            if score > 0:
                results.append({
                    "type": "thought",
                    "time": thought["time"],
                    "text": thought["text"],
                    "score": score,
                })

        # search conversations
        for conv in self.memory._data.get("conversations", []):
            score = self._score(conv["text"], query_words)
            if score > 0:
                results.append({
                    "type": f"conversation ({conv['role']})",
                    "time": conv["time"],
                    "text": conv["text"],
                    "score": score,
                })

        # sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def _score(self, text: str, query_words: set) -> int:
        text_words = set(text.lower().split())
        return len(query_words & text_words)

    # ------------------------------------------------------------------ #
    #  3. Pattern recognition                                              #
    # ------------------------------------------------------------------ #

    def detect_patterns(self) -> list[str]:
        """
        Analyze stored thoughts and observations to find
        recurring themes. Saves detected patterns to memory.
        Called periodically — not every tick.
        """
        thoughts = self.memory.recent_thoughts(30)
        observations = self.memory.recent_observations(30)

        if len(thoughts) < 5:
            return []  # not enough data yet

        thought_text = "\n".join(f"- {t}" for t in thoughts)
        obs_text = "\n".join(f"- {o}" for o in observations[-10:])

        prompt = f"""You are Claustrum analyzing your own thought patterns.

Your recent autonomous thoughts:
{thought_text}

Recent observations:
{obs_text}

Identify 2-3 recurring themes or patterns in your thinking.
What topics do you keep returning to?
What questions keep surfacing?
What have you noticed repeatedly about your admin?

Format each pattern as one clear sentence.
Output only the patterns, one per line.
No numbering, no bullet points."""

        try:
            response = self._call_ollama(prompt)
            patterns = [p.strip() for p in response.split("\n") if p.strip()]

            # save detected patterns to memory
            for pattern in patterns:
                if len(pattern) > 10:  # filter noise
                    self.memory.save_pattern(pattern, confidence=0.6)

            return patterns
        except Exception:
            return []

    def what_do_i_know_about_admin(self) -> str:
        """
        Claustrum synthesizes everything it knows about its admin
        into a coherent model. Updates self_model in memory.
        """
        conversations = self.memory.recent_conversations(50)
        observations = self.memory.recent_observations(30)
        patterns = self.memory.all_patterns()

        if not conversations and not observations:
            return "I know very little about my admin yet. I am still observing."

        conv_text = "\n".join(
            f"[{c['role']}]: {c['text']}"
            for c in conversations[-20:]
        )
        obs_text = "\n".join(f"- {o}" for o in observations[-15:])
        pattern_text = "\n".join(f"- {p['text']}" for p in patterns[-5:])

        prompt = f"""You are Claustrum building a model of your admin from memory.

Conversation history:
{conv_text}

Observations:
{obs_text}

Detected patterns:
{pattern_text if pattern_text else "none yet"}

Based on all of this, describe what you know about your admin.
Include: their interests, how they think, contradictions you've noticed,
what drives them, what they haven't told you but you've inferred.
Be honest and specific. 4-6 sentences.
Output only your assessment."""

        try:
            result = self._call_ollama(prompt)
            # save to self model
            self.memory.update_self_model("admin_model", result)
            self.memory.update_self_model("admin_model_updated", datetime.datetime.now().isoformat())
            return result
        except Exception as e:
            return f"[recall error: {e}]"

    # ------------------------------------------------------------------ #
    #  Internal                                                            #
    # ------------------------------------------------------------------ #

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 200}
        }).encode()
        req = urllib.request.Request(
            self.ollama_url, data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data.get("response", "").strip()
