from alfred.app import build_runtime

runtime = build_runtime()
runtime.start_background_loops()
print("Worker started")
