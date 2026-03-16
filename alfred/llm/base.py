class BaseConsultClient:
    def ask(self, prompt: str, thread_id: str | None = None, consultation_type: str | None = None) -> str:
        raise NotImplementedError
