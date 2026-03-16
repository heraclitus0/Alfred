from alfred.app import build_runtime
from alfred.types import ConsultationType

runtime = build_runtime()
runtime.boot()
out = runtime.consult(
    ConsultationType.SELF_IMPROVEMENT,
    "How should Alfred become more concrete, nuanced, and self-furthering in its prompt engineering?",
    {"scope": "prompt engineering", "constraint": "do not change authority boundaries"},
)
print(out)
print(runtime.run_self_improvement("prompts"))
