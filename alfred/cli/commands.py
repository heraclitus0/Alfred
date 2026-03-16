from __future__ import annotations
from alfred.types import Mode, ConsultationType


def handle_command(runtime, raw: str) -> str:
    raw = raw.strip()
    if raw == "888":
        runtime.modes.set_mode(Mode.ACTIVE)
        return "Alfred set to ACTIVE"
    if raw == "999":
        runtime.modes.set_mode(Mode.PASSIVE)
        return "Alfred set to PASSIVE"
    if raw == "666":
        runtime.halt()
        return "Alfred halted"
    if raw == "status":
        from alfred.cli.renderers import render_status
        return render_status(runtime.status())
    if raw.startswith("open-chatgpt"):
        topic = raw.split(maxsplit=1)[1] if len(raw.split(maxsplit=1)) > 1 else None
        runtime.open_chatgpt(topic)
        return "Opened ChatGPT"
    if raw.startswith("consult "):
        topic = raw.split(" ", 1)[1]
        out = runtime.consult(ConsultationType.SELF_IMPROVEMENT, topic, {"user_input": topic})
        return out.get("response", "No response")
    if raw.startswith("world "):
        topic = raw.split(" ", 1)[1]
        out = runtime.consult(ConsultationType.WORLD_AWARENESS, topic, {"user_input": topic})
        return out.get("response", "No response")
    if raw.startswith("improve "):
        target = raw.split(" ", 1)[1]
        out = runtime.run_self_improvement(target)
        return str(out)
    if raw == "tick":
        runtime.loops.run_once()
        runtime.scheduler.run_once_due_jobs()
        return "Tick complete"
    if raw == "exit":
        runtime.shutdown()
        raise SystemExit(0)
    return "Unknown command"
