from alfred.app import build_runtime
from alfred.types import ConsultationType


def test_consultation_thread_persists():
    runtime = build_runtime()
    runtime.boot()
    a = runtime.consult(ConsultationType.SELF_IMPROVEMENT, "prompt quality", {"x": 1})
    b = runtime.consult(ConsultationType.SELF_IMPROVEMENT, "prompt quality", {"x": 2})
    assert a["response"]
    assert b["response"]
