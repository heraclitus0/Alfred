from __future__ import annotations
from alfred.types import ConsultationType


class ProposalBuilder:
    def __init__(self, prompt_engineer, llm_client) -> None:
        self.prompt_engineer = prompt_engineer
        self.llm_client = llm_client

    def build_from_weakness(self, weakness: dict) -> dict:
        prompt = self.prompt_engineer.build_consultation_prompt(
            ConsultationType.SELF_IMPROVEMENT,
            topic=weakness["weakness"],
            context=weakness,
        )
        response = self.llm_client.ask(prompt, consultation_type=ConsultationType.SELF_IMPROVEMENT.value)
        return {
            "target": weakness["target"],
            "prompt": prompt,
            "response": response,
        }
