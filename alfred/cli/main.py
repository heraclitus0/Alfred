from __future__ import annotations
from alfred.app import build_runtime
from alfred.cli.interactive_shell import AlfredShell


def main() -> None:
    runtime = build_runtime()
    runtime.boot()

    heartbeat = runtime.registry.get("heartbeat")
    heartbeat.start()

    try:
        shell = AlfredShell(runtime)
        shell.run()
    finally:
        heartbeat.stop()
