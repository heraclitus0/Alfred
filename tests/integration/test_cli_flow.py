from alfred.app import build_runtime


def test_runtime_boot_and_status():
    runtime = build_runtime()
    runtime.boot()
    assert runtime.status().mode.value == "PASSIVE"
