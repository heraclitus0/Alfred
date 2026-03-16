from __future__ import annotations


def choose_thread(thread_manager, topic: str, consultation_type: str):
    return thread_manager.get_or_create(topic, consultation_type)
