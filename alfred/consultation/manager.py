from __future__ import annotations
from alfred.consultation.thread_router import choose_thread
from alfred.consultation.extractor import extract_learning
from alfred.consultation.updater import update_memory
from alfred.consultation.validators import validate_consultation_response


class ConsultationManager:
    def __init__(self, memory, thread_manager, prompt_engineer, llm_client, browser, notifications, audit) -> None:
        self.memory = memory
        self.thread_manager = thread_manager
        self.prompt_engineer = prompt_engineer
        self.llm_client = llm_client
        self.browser = browser
        self.notifications = notifications
        self.audit = audit

    def run_consultation(self, consultation_type, topic: str, context: dict) -> dict:
        thread = choose_thread(self.thread_manager, topic, consultation_type.value)
        prompt = self.prompt_engineer.build_consultation_prompt(
            consultation_type=consultation_type,
            topic=topic,
            context=context,
            previous_summary=thread.get("summary"),
        )
        response = self.llm_client.ask(prompt, thread_id=thread["thread_id"], consultation_type=consultation_type.value)
        if not validate_consultation_response(response):
            raise ValueError("Invalid consultation response")
        extracted = extract_learning(response)
        self.memory.save_consultation(thread["thread_id"], consultation_type.value, topic, prompt, response)
        self.thread_manager.update_summary(thread["thread_id"], topic, consultation_type.value, extracted["response"][:800])
        update_memory(self.memory, consultation_type.value, topic, extracted)
        self.audit.record("consultation", {"consultation_type": consultation_type.value, "topic": topic})
        return extracted

    def open_chatgpt_for_thread(self, topic: str, consultation_type: str) -> None:
        thread = choose_thread(self.thread_manager, topic, consultation_type)
        self.browser.open_chatgpt(topic=topic, thread_hint=thread["thread_id"])
