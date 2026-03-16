from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RUNTIME_DIR = DATA_DIR / "runtime"
CHECKPOINT_DIR = RUNTIME_DIR / "checkpoints"
LOG_DIR = RUNTIME_DIR / "logs"
DEFAULT_CHATGPT_URL = "https://chatgpt.com/"
