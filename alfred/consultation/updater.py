def update_memory(memory, consultation_type: str, topic: str, extracted: dict) -> None:
    memory.put("consultation_learning", f"{consultation_type}:{topic}", extracted)
