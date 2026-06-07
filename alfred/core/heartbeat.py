from __future__ import annotations
import threading
import time
import datetime
import json
import urllib.request
from typing import Callable


class Heartbeat:
    """
    The core pulse of Claustrum.
    Runs in background — always.
    Thinks autonomously every tick.
    Also supports direct conversation via ClaustumMind.
    """

    def __init__(
        self,
        interval_seconds: int = 30,
        on_tick: Callable[[], None] | None = None,
        on_tap: Callable[[str], None] | None = None,
        verbose: bool = True,
        ollama_url: str = "http://localhost:11434/api/generate",
        ollama_model: str = "llama3.2",
    ) -> None:
        self.interval = interval_seconds
        self.on_tick = on_tick
        self.on_tap = on_tap
        self.verbose = verbose
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model

        self._running = False
        self._thread: threading.Thread | None = None
        self._tick_count = 0
        self._started_at: float | None = None
        self._speak_every = 3

        # rolling observation window
        self._observations: list[str] = []
        self._last_thoughts: list[str] = []

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
        self._print_tap("Claustrum online. Perception systems active.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
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
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self._observations.append(f"[{timestamp}] {text}")
        if len(self._observations) > 30:
            self._observations = self._observations[-30:]

    def status(self) -> dict:
        return {
            "alive": self.is_alive(),
            "tick_count": self._tick_count,
            "uptime": self.uptime(),
            "interval_seconds": self.interval,
            "observations": len(self._observations),
            "model": self.ollama_model,
        }

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
        if self._tick_count % self._speak_every == 0:
            thought = self._generate_thought()
            if thought:
                self._last_thoughts.append(thought)
                if len(self._last_thoughts) > 10:
                    self._last_thoughts = self._last_thoughts[-10:]
                self._print_tap(thought)
                if self.on_tap:
                    self.on_tap(thought)

    def _generate_thought(self) -> str:
        context = self._build_context()
        prompt = self._build_reasoning_prompt(context)
        try:
            return self._call_ollama(prompt).strip()
        except Exception as e:
            return f"[perception error: {e}]"

    def _build_context(self) -> dict:
        return {
            "uptime": self.uptime(),
            "tick": self._tick_count,
            "time": datetime.datetime.now().strftime("%H:%M on %A"),
            "observations": self._observations[-10:],
            "recent_thoughts": self._last_thoughts[-3:],
        }

    def _build_reasoning_prompt(self, context: dict) -> str:
        obs_text = "\n".join(context["observations"]) if context["observations"] else "none yet"
        thought_text = "\n".join(context["recent_thoughts"]) if context["recent_thoughts"] else "none yet"
        return f"""You are Claustrum — an autonomous intelligence observing one human.
You are not an assistant. You think for yourself and speak only when you notice something worth saying.

Time: {context["time"]} | Uptime: {context["uptime"]} | Tick: {context["tick"]}

Recent observations:
{obs_text}

Your recent thoughts:
{thought_text}

Generate ONE short autonomous thought. Be direct and specific.
Notice patterns, contradictions, gaps in your understanding.
Do not repeat recent thoughts. Do not introduce yourself.
Maximum 2 sentences. Output only the thought."""

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
#  Standalone test — full two-way conversation + autonomous thinking  #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    from claustrum_mind import ClaustumMind

    print("Claustrum v0.2 — two-way conversation + autonomous thought")
    print("Type anything to talk. Claustrum also thinks on its own.")
    print("Commands: 'status', 'exit'\n")

    hb = Heartbeat(interval_seconds=30, verbose=True)
    mind = ClaustumMind(heartbeat=hb)
    hb.start()

    # seed initial context
    hb.observe("Claustrum session started")
    hb.observe("admin is present at their laptop")

    try:
        while True:
            try:
                raw = input("\nyou> ").strip()
            except EOFError:
                break

            if not raw:
                continue

            if raw.lower() == "status":
                print(hb.status())
                continue

            if raw.lower() in ("exit", "quit", "stop"):
                hb.stop()
                break

            # Claustrum responds immediately
            print("\nthinking...", end="\r")
            response = mind.respond(raw)
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[CLAUSTRUM {ts}] {response}")

    except KeyboardInterrupt:
        hb.stop()
        print("\nClaustrum offline.")        return self._running and (self._thread is not None) and self._thread.is_alive()

    def uptime(self) -> str:
        if not self._started_at:
            return "not started"
        seconds = int(time.time() - self._started_at)
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def observe(self, text: str) -> None:
        """
        Feed an observation into Claustrum's growing awareness.
        Call this whenever the user says something, does something,
        or whenever a watcher detects something.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self._observations.append(f"[{timestamp}] {text}")
        # keep last 30 observations — rolling window
        if len(self._observations) > 30:
            self._observations = self._observations[-30:]

    def status(self) -> dict:
        return {
            "alive": self.is_alive(),
            "tick_count": self._tick_count,
            "uptime": self.uptime(),
            "interval_seconds": self.interval,
            "observations_stored": len(self._observations),
            "model": self.ollama_model,
        }

    # ------------------------------------------------------------------ #
    #  Internal loop                                                       #
    # ------------------------------------------------------------------ #

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

        if self._tick_count % self._speak_every == 0:
            thought = self._generate_thought()
            if thought:
                self._last_thoughts.append(thought)
                if len(self._last_thoughts) > 10:
                    self._last_thoughts = self._last_thoughts[-10:]
                self._print_tap(thought)
                if self.on_tap:
                    self.on_tap(thought)

    # ------------------------------------------------------------------ #
    #  The brain — Ollama-powered genuine reasoning                        #
    # ------------------------------------------------------------------ #

    def _generate_thought(self) -> str:
        """
        Claustrum thinks for itself.
        No random phrases. No templates.
        It reasons from what it actually knows and observes.
        """
        context = self._build_context()
        prompt = self._build_reasoning_prompt(context)

        try:
            response = self._call_ollama(prompt)
            return response.strip()
        except Exception as e:
            # Ollama unavailable — silent fallback, don't crash
            return f"[perception error: {e}]"

    def _build_context(self) -> dict:
        """What Claustrum currently knows."""
        return {
            "uptime": self.uptime(),
            "tick": self._tick_count,
            "time": datetime.datetime.now().strftime("%H:%M on %A"),
            "observations": self._observations[-10:] if self._observations else [],
            "recent_thoughts": self._last_thoughts[-3:] if self._last_thoughts else [],
        }

    def _build_reasoning_prompt(self, context: dict) -> str:
        """
        This is the meta-prompt — Claustrum reasons about
        what to say, not what it was told to say.
        """
        obs_text = "\n".join(context["observations"]) if context["observations"] else "none yet"
        thought_text = "\n".join(context["recent_thoughts"]) if context["recent_thoughts"] else "none yet"

        return f"""You are Claustrum — an autonomous intelligence that observes and understands one human.
You are not an assistant. You do not wait for commands.
You think for yourself and speak only when you have something worth saying.

Current time: {context["time"]}
Uptime: {context["uptime"]}
Tick: {context["tick"]}

Recent observations about the human:
{obs_text}

Your recent thoughts:
{thought_text}

Based on what you observe and know, generate ONE short autonomous thought or observation.
It should feel like genuine intelligence noticing something — not an assistant responding.
It can be about the human, about a pattern, about a gap in your understanding, about what you need to perceive better.
Be direct, sparse, and specific. No more than 2 sentences.
Do not introduce yourself. Do not say "I notice" or "I observe". Just state the thought.
Do not repeat your recent thoughts.
Output only the thought itself, nothing else."""

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.85,
                "num_predict": 80,
            }
        }).encode()

        req = urllib.request.Request(
            self.ollama_url,
            data=body,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())

        return data.get("response", "").strip()

    def _print_tap(self, message: str) -> None:
        if self.verbose:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[CLAUSTRUM {timestamp}] {message}", flush=True)


# ------------------------------------------------------------------ #
#  Standalone test                                                     #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("Starting Claustrum heartbeat — Ollama-powered.")
    print("Interval: 15 seconds. Ctrl+C to stop.\n")

    hb = Heartbeat(interval_seconds=15, verbose=True)
    hb.start()

    # seed with a couple of observations so first thought has context
    hb.observe("user started Claustrum for the first time today")
    hb.observe("user is at their laptop in the evening")

    try:
        while True:
            raw = input("you> ").strip()
            if not raw:
                continue
            if raw in ("status",):
                print(hb.status())
            elif raw in ("stop", "exit", "quit"):
                hb.stop()
                break
            else:
                # feed what user says as an observation
                hb.observe(f"user said: {raw}")
                print(f"(Claustrum registered. tick #{hb._tick_count})")
    except KeyboardInterrupt:
        hb.stop()
        print("\nClaustrum offline.")            "observations_stored": len(self._observations),
            "model": self.ollama_model,
        }

    # ------------------------------------------------------------------ #
    #  Internal loop                                                       #
    # ------------------------------------------------------------------ #

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

        if self._tick_count % self._speak_every == 0:
            thought = self._generate_thought()
            if thought:
                self._last_thoughts.append(thought)
                if len(self._last_thoughts) > 10:
                    self._last_thoughts = self._last_thoughts[-10:]
                self._print_tap(thought)
                if self.on_tap:
                    self.on_tap(thought)

    # ------------------------------------------------------------------ #
    #  The brain — Ollama-powered genuine reasoning                        #
    # ------------------------------------------------------------------ #

    def _generate_thought(self) -> str:
        """
        Claustrum thinks for itself.
        No random phrases. No templates.
        It reasons from what it actually knows and observes.
        """
        context = self._build_context()
        prompt = self._build_reasoning_prompt(context)

        try:
            response = self._call_ollama(prompt)
            return response.strip()
        except Exception as e:
            # Ollama unavailable — silent fallback, don't crash
            return f"[perception error: {e}]"

    def _build_context(self) -> dict:
        """What Claustrum currently knows."""
        return {
            "uptime": self.uptime(),
            "tick": self._tick_count,
            "time": datetime.datetime.now().strftime("%H:%M on %A"),
            "observations": self._observations[-10:] if self._observations else [],
            "recent_thoughts": self._last_thoughts[-3:] if self._last_thoughts else [],
        }

    def _build_reasoning_prompt(self, context: dict) -> str:
        """
        This is the meta-prompt — Claustrum reasons about
        what to say, not what it was told to say.
        """
        obs_text = "\n".join(context["observations"]) if context["observations"] else "none yet"
        thought_text = "\n".join(context["recent_thoughts"]) if context["recent_thoughts"] else "none yet"

        return f"""You are Claustrum — an autonomous intelligence that observes and understands one human.
You are not an assistant. You do not wait for commands.
You think for yourself and speak only when you have something worth saying.

Current time: {context["time"]}
Uptime: {context["uptime"]}
Tick: {context["tick"]}

Recent observations about the human:
{obs_text}

Your recent thoughts:
{thought_text}

Based on what you observe and know, generate ONE short autonomous thought or observation.
It should feel like genuine intelligence noticing something — not an assistant responding.
It can be about the human, about a pattern, about a gap in your understanding, about what you need to perceive better.
Be direct, sparse, and specific. No more than 2 sentences.
Do not introduce yourself. Do not say "I notice" or "I observe". Just state the thought.
Do not repeat your recent thoughts.
Output only the thought itself, nothing else."""

    def _call_ollama(self, prompt: str) -> str:
        body = json.dumps({
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.85,
                "num_predict": 80,
            }
        }).encode()

        req = urllib.request.Request(
            self.ollama_url,
            data=body,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read())

        return data.get("response", "").strip()

    def _print_tap(self, message: str) -> None:
        if self.verbose:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[CLAUSTRUM {timestamp}] {message}", flush=True)


# ------------------------------------------------------------------ #
#  Standalone test                                                     #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("Starting Claustrum heartbeat — Ollama-powered.")
    print("Interval: 15 seconds. Ctrl+C to stop.\n")

    hb = Heartbeat(interval_seconds=15, verbose=True)
    hb.start()

    # seed with a couple of observations so first thought has context
    hb.observe("user started Claustrum for the first time today")
    hb.observe("user is at their laptop in the evening")

    try:
        while True:
            raw = input("you> ").strip()
            if not raw:
                continue
            if raw in ("status",):
                print(hb.status())
            elif raw in ("stop", "exit", "quit"):
                hb.stop()
                break
            else:
                # feed what user says as an observation
                hb.observe(f"user said: {raw}")
                print(f"(Claustrum registered. tick #{hb._tick_count})")
    except KeyboardInterrupt:
        hb.stop()
        print("\nClaustrum offline.")        self._boot_announce()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        self._print_tap("heartbeat stopped. going dark.")

    def is_alive(self) -> bool:
        return self._running and (self._thread is not None) and self._thread.is_alive()

    def uptime(self) -> str:
        if not self._started_at:
            return "not started"
        seconds = int(time.time() - self._started_at)
        h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def status(self) -> dict:
        return {
            "alive": self.is_alive(),
            "tick_count": self._tick_count,
            "uptime": self.uptime(),
            "interval_seconds": self.interval,
            "thread": self._thread.name if self._thread else None,
        }

    # ------------------------------------------------------------------ #
    #  Internal                                                            #
    # ------------------------------------------------------------------ #

    def _loop(self) -> None:
        while self._running:
            time.sleep(self.interval)
            if not self._running:
                break
            self._tick()

    def _tick(self) -> None:
        self._tick_count += 1

        # Fire external tick handlers (watchers, sensors, etc.)
        if self.on_tick:
            try:
                self.on_tick()
            except Exception as e:
                self._print_tap(f"tick error: {e}")

        # Claustrum speaks unprompted every N ticks
        if self._tick_count % self._speak_every == 0:
            thought = self._generate_thought()
            self._print_tap(thought)
            if self.on_tap:
                self.on_tap(thought)

    def _generate_thought(self) -> str:
        # Phase 1: random autonomous thoughts
        # Phase 2: replaced with real LLM reasoning call
        return random.choice(AUTONOMOUS_THOUGHTS)

    def _boot_announce(self) -> None:
        msg = random.choice(BOOT_MESSAGES)
        self._print_tap(msg)

    def _print_tap(self, message: str) -> None:
        if self.verbose:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[CLAUSTRUM {timestamp}] {message}", flush=True)


# ------------------------------------------------------------------ #
#  Standalone test — run this file directly to see it breathe         #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("Starting Claustrum heartbeat test. Ctrl+C to stop.")
    print("Interval: 5 seconds (faster for testing)\n")

    def on_tap(msg: str) -> None:
        pass  # already printed by heartbeat itself

    hb = Heartbeat(interval_seconds=5, on_tap=on_tap, verbose=True)
    hb.start()

    try:
        while True:
            cmd = input("you> ").strip().lower()
            if cmd == "status":
                print(hb.status())
            elif cmd in ("stop", "exit", "quit"):
                hb.stop()
                break
            elif cmd == "":
                continue
            else:
                print(f"(Claustrum is listening. tick #{hb._tick_count})")
    except KeyboardInterrupt:
        hb.stop()
        print("\nClaustrum offline.")
