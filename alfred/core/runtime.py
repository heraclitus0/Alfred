from __future__ import annotations
import time
from typing import Any
from alfred.types import Event, Mode, RuntimeStatus, ConsultationType
from alfred.core.state_manager import StateManager
from alfred.core.mode_manager import ModeManager
from alfred.core.event_bus import EventBus
from alfred.core.loop_controller import LoopController
from alfred.core.scheduler import Scheduler
from alfred.core.registry import ComponentRegistry
from alfred.core.checkpoints import CheckpointManager
from alfred.core.health import HealthMonitor
from alfred.core.versioning import VersionStamp


class AlfredRuntime:
    def __init__(self, **components: Any):
        self.registry = ComponentRegistry()
        for name, component in components.items():
            self.registry.register(name, component)
        self.state = StateManager()
        self.modes = ModeManager(self.state)
        self.events = EventBus()
        self.loops = LoopController(self.events)
        self.scheduler = Scheduler(self.events)
        self.checkpoints = CheckpointManager(self.state)
        self.health = HealthMonitor(self.registry)
        self.version = VersionStamp.current()
        self.started_at = time.time()
        self._wire_default_handlers()

    def _wire_default_handlers(self) -> None:
        self.events.subscribe("notify", lambda e: self.registry.get("notification_manager").emit(e.payload))
        self.events.subscribe("audit", lambda e: self.registry.get("audit").record(e.payload.get("kind", "event"), e.payload))

    def boot(self) -> None:
        self.modes.set_mode(Mode.PASSIVE)
        self.events.publish(Event("audit", {"kind": "boot", "version": self.version.version}))

    def shutdown(self) -> None:
        self.loops.stop_all()
        self.checkpoints.save()
        self.events.publish(Event("audit", {"kind": "shutdown"}))
        self.modes.set_mode(Mode.OFF)

    def halt(self) -> None:
        self.registry.get("kill_switch").trigger("manual halt")
        self.modes.set_mode(Mode.HALT)
        self.loops.stop_all()

    def status(self) -> RuntimeStatus:
        return RuntimeStatus(
            mode=self.state.mode,
            started_at=self.started_at,
            loops_running=self.loops.running_loops(),
            last_checkpoint=self.state.last_checkpoint,
        )

    def start_background_loops(self) -> None:
        self.loops.start("watchers", self.registry.get("watcher_manager").tick)
        self.loops.start("health", self.health.tick)

    def open_chatgpt(self, topic: str | None = None) -> None:
        self.registry.get("browser").open_chatgpt(topic=topic)

    def consult(self, consultation_type: ConsultationType, topic: str, context: dict[str, Any]) -> dict[str, Any]:
        return self.registry.get("consultation").run_consultation(consultation_type, topic, context)

    def run_self_improvement(self, target: str) -> dict[str, Any]:
        weakness = self.registry.get("weakness_detector").detect(target)
        proposal = self.registry.get("proposal_builder").build_from_weakness(weakness)
        result = self.registry.get("rewrite_sandbox").run(proposal)
        if result.get("validated"):
            self.registry.get("promoter").promote(result)
        return result
