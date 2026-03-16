from pathlib import Path

DIRS = [
    "data/runtime/logs",
    "data/runtime/traces",
    "data/runtime/checkpoints",
    "data/runtime/notifications",
    "data/runtime/watcher_cache",
    "data/memory/identity",
    "data/memory/missions",
    "data/memory/episodic",
    "data/memory/trust",
    "data/memory/narrative",
    "data/memory/consultation",
    "data/memory/research_threads",
    "data/exports/chat_exports",
    "data/exports/consultation_exports",
    "data/sandboxes/code",
    "data/sandboxes/prompt_trials",
    "data/sandboxes/workflow_trials",
    "data/sandboxes/consultation_trials",
    "data/sandboxes/self_rewrites",
]

for d in DIRS:
    Path(d).mkdir(parents=True, exist_ok=True)
print("Bootstrap complete.")
