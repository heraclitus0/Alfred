from alfred.app import build_runtime
runtime = build_runtime()
runtime.boot()
runtime.start_background_loops()
runtime.loops.run_once()
print(runtime.registry.get("notification_manager").buffer)
