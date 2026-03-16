def render_status(status) -> str:
    return f"mode={status.mode.value} loops={status.loops_running} started_at={status.started_at:.0f}"
