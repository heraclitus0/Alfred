from alfred.app import build_runtime

runtime = build_runtime()
runtime.scheduler.run_once_due_jobs()
print("Scheduler tick complete")
