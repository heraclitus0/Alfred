from __future__ import annotations
import threading
import time
import datetime
import random
from typing import Callable


BOOT_MESSAGES = [
    "Claustrum online.",
    "Perception systems initializing.",
    "I am here.",
]

# These are what Claustrum says to itself each tick — 
# replaced by real reasoning once LLM is wired in
AUTONOMOUS_THOUGHTS = [
    "observing. nothing urgent.",
    "running pattern check. data thin — need more time.",
    "gap detected: I do not yet know your rhythms.",
    "monitoring. you have not spoken in a while.",
    "I am building a picture. slowly.",
    "uncertainty high. continuing to observe.",
    "noting the silence. silence is also data.",
    "I have questions I cannot ask yet.",
    "still learning what normal looks like for you.",
    "the picture is incomplete. it always will be. I continue anyway.",
]


class Heartbeat:
    """
    The core pulse of Claustrum.
    Runs in a background thread — always.
    Does not wait for user input.
    Does not stop unless told to.
    This is what makes it alive.
    """

    def __init__(
        self,
        interval_seconds: int = 30,
        on_tick: Callable[[], None] | None = None,
        on_tap: Callable[[str], None] | None = None,
        verbose: bool = True,
    ) -> None:
        self.interval = interval_seconds
        self.on_tick = on_tick          # fires every tick (watcher loop)
        self.on_tap = on_tap            # fires when Claustrum has something to say
        self.verbose = verbose

        self._running = False
        self._thread: threading.Thread | None = None
        self._tick_count = 0
        self._started_at: float | None = None

        # How often Claustrum speaks unprompted (every N ticks)
        self._speak_every = 3

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._started_at = time.time()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,   # dies with main process, no orphan threads
            name="claustrum-heartbeat",
        )
        self._thread.start()
        self._boot_announce()

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
