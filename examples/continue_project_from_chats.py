from pathlib import Path
from alfred.memory.ingestion.chat_importer import import_chat_file

path = Path("data/exports/chat_exports/sample.txt")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text("Project thoughts about Alfred, missions, and consultation loops.")
print(import_chat_file(path))
