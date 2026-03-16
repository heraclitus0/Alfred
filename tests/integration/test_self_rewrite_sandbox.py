from alfred.app import build_runtime


def test_self_improvement_creates_sandbox_artifact():
    runtime = build_runtime()
    runtime.boot()
    result = runtime.run_self_improvement("prompts")
    assert result["validated"] is True
