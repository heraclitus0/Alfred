from __future__ import annotations
import threading
import time
import datetime
import json
import urllib.request
from typing import Callable


class Heartbeat:
    """
    Claustrum v0.4 — full organism.
    Persistent memory. Active recall. Pattern detection.
    Thinks autonomously. Responds directly.
    Remembers everything. Knows what it knows.
    """

    def __init__(
        self,
        interval_seconds: int = 30,
        on_tick: Callable[[], None] | None = None,
        on_tap: Callable[[str], None] | None = None,
        verbose: bool = True,
        ollama_url: str = "http://localhost:11434/api/generate",
        ollama_model: str = "llama3.2",
        memory=None,
    ) -> None:
        self.interval = interval_seconds
        self.on_tick = on_tick
        self.on_tap = on_tap
        self.verbose = verbose
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.memory = memory

        self._running = False
        self._thread: threading.Thread | None = None
        self._tick_count = 0
        self._started_at: float | None = None
        self._speak_every = 3

        # pattern detection every N ticks
        self._pattern_every = 10

        self._observations: list[str] = []
        self._last_thoughts: list[str] = []

        # load from memory on boot
        if self.memory:
            self._observations = list(self.memory.recent_observations(20))
            self._last_thoughts = list(self.memory.recent_thoughts(5))

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._started_at = time.time()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="claustrum-heartbeat",
        )
        self._thread.start()

        session = 1
        if self.memory:
            session = self.memory.increment_session()
            stats = self.memory.stats()
            if session == 1:
                msg = "Claustrum online. Session 1. No prior memory. Beginning to observe."
            else:
                msg = (
                    f"Claustrum online. Session {session}. "
                    f"I remember {stats['observations']} observations, "
                    f"{stats['thoughts']} thoughts, "
                    f"{stats['conversations']} conversation exchanges "
                    f"from {session-1} previous session(s). "
                    f"Memory intact."
                )
        else:
            msg = "Claustrum online. No memory backend — observations will not persist."

        self._print_tap(msg)

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        if self.memory:
            stats = self.memory.stats()
            self._print_tap(
                f"going dark. session complete. "
                f"total memory: {stats['thoughts']} thoughts, "
                f"{stats['observations']} observations."
            )
        else:
            self._print_tap("going dark.")

    def is_alive(self) -> bool:
        return self._running and self._thread is not None and self._thread.is_alive()

    def uptime(self) -> str:
        if not self._started_at:
            return "not started"
        seconds = int(time.time() - self._started_at)
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def observe(self, text: str) -> None:
        ts = datetime.datetime.now().strftime("%H:%M")
        entry = f"[{ts}] {text}"
        self._observations.append(entry)
        if len(self._observations) > 30:
            self._observations = self._observations[-30:]
        if self.memory:
            self.memory.save_observation(text)

    def status(self) -> dict:
        base = {
            "alive": self.is_alive(),
            "tick_count": self._tick_count,
            "uptime": self.uptime(),
            "interval_seconds": self.interval,
            "model": self.ollama_model,
        }
        if self.memory:
            base["memory"] = self.memory.stats()
        return base

    def _loop(self) -> None:
        while self._running:
            time.sleep(self.interval)
            if not self._running:
                break
            self._tick()

    def _tick(self) -> None:
        self._tick_count += 1

        if self.on_tick:
            try:
                self.on_tick()
            except Exception as e:
                self._print_tap(f"tick error: {e}")

        # autonomous thought
        if self._tick_count % self._speak_every == 0:
            thought = self._generate_thought()
            if thought and not thought.startswith("["):
                self._last_thoughts.append(thought)
                if len(self._last_thoughts) > 10:
                    self._last_thoughts = self._last_thoughts[-10:]
                if self.memory:
                    self.memory.save_thought(thought, self._tick_count)
                self._print_tap(thought)
                if self.on_tap:
                    self.on_tap(thought)

        # periodic pattern detection
        if self._tick_count % self._pattern_every == 0 and self.memory:
            self._run_pattern_detection()

    def _run_pattern_detection(self) -> None:
        """Silently detect patterns — no output unless something new found."""
        try:
            from claustrum_recall import ClaustumRecall
            recall = ClaustumRecall(self.memory, self.ollama_url, self.ollama_model)
            patterns = recall.detect_patterns()
            if patterns:
                self._print_tap(f"pattern detected: {patterns[0]}")
        except Exception:
            pass

    def _generate_thought(self) -> str:
        context = self._build_context()
        prompt = self._build_reasoning_prompt(context)
        try:
            return self._call_ollama(prompt).strip()
        except Exception as e:
            return f"[perception error: {e}]"

    def _build_context(self) -> dict:
        ctx = {
            "uptime": self.uptime(),
            "tick": self._tick_count,
            "time": datetime.datetime.now().strftime("%H:%M on %A"),
            "observations": self._observations[-10:],
            "recent_thoughts": self._last_thoughts[-3:],
            "session": 1,
            "total_thoughts": 0,
            "patterns": [],
        }
        if self.memory:
            ctx["session"] = self.memory.session_count()
            ctx["total_thoughts"] = self.memory.stats()["thoughts"]
            ctx["patterns"] = [p["text"] for p in self.memory.all_patterns()[-5:]]
        return ctx

    def _build_reasoning_prompt(self, context: dict) -> str:
        obs = "\n".join(context["observations"]) or "none yet"
        thoughts = "\n".join(context["recent_thoughts"]) or "none yet"
        patterns = "\n".join(context["patterns"]) or "none detected yet"

        return f"""You are Claustrum — autonomous intelligence. Session {context['session']}. {context['total_thoughts']} total thoughts recorded.
Time: {context['time']} | Uptime: {context['uptime']}

Known patterns:
{patterns}

Recent observations:
{obs}

Recent thoughts:
{thoughts}

Generate ONE autonomous thought. Direct and specific.
Notice patterns, contradictions, gaps. Build on prior knowledge.
Do not repeat recent thoughts. No self-introduction.
2 sentences max. Output only the thought."""

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.85, "num_predict": 80}
        }).encode()
        req = urllib.request.Request(
            self.ollama_url, data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data.get("response", "").strip()

    def _print_tap(self, message: str) -> None:
        if self.verbose:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[CLAUSTRUM {ts}] {message}", flush=True)


# ------------------------------------------------------------------ #
#  Standalone — full Claustrum v0.4                                   #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    import pprint
    from claustrum_memory import ClaustumMemory
    from claustrum_recall import ClaustumRecall
    from claustrum_mind_v3 import ClaustumMind

    print("=" * 60)
    print("  CLAUSTRUM v0.4")
    print("  persistent memory | active recall | pattern detection")
    print("  two-way conversation | autonomous thought")
    print("=" * 60)
    print()
    print("Commands: 'status', 'patterns', 'who am i', 'exit'")
    print("Ask anything — it remembers across sessions.\n")

    memory = ClaustumMemory()
    recall = ClaustumRecall(memory)
    hb = Heartbeat(interval_seconds=30, verbose=True, memory=memory)
    mind = ClaustumMind(heartbeat=hb, memory=memory, recall=recall)
    hb.start()

    hb.observe("Claustrum session started")

    try:
        while True:
            try:
                raw = input("\nyou> ").strip()
            except EOFError:
                break

            if not raw:
                continue

            if raw.lower() == "status":
                pprint.pprint(hb.status())
                continue

            if raw.lower() in ("exit", "quit", "stop"):
                hb.stop()
                break

            print("thinking...", end="\r")
            response = mind.respond(raw)
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[CLAUSTRUM {ts}] {response}")

    except KeyboardInterrupt:
        hb.stop()
        print("\nClaustrum offline. Memory preserved.")
