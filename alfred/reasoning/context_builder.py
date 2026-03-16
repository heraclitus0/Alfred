def build_context(primary_state: dict, thread_summary: str | None, extra: dict) -> dict:
    return {
        "primary_state": primary_state,
        "thread_summary": thread_summary,
        "extra": extra,
    }
