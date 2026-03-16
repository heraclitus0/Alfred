from __future__ import annotations
from alfred.prompts.builder import PromptBuilder
from alfred.prompts.compressor import compress_context
from alfred.types import ConsultationType


_TEMPLATE_MAP = {
    ConsultationType.SELF_IMPROVEMENT: "self_improvement.jinja",
    ConsultationType.WORLD_AWARENESS: "world_awareness.jinja",
    ConsultationType.INTERACTION_REFINEMENT: "interaction_refinement.jinja",
    ConsultationType.MISSION_STRATEGY: "mission_strategy.jinja",
}


class PromptEngineer:
    def __init__(self) -> None:
        self.builder = PromptBuilder()

    def build_consultation_prompt(self, consultation_type: ConsultationType, topic: str, context: dict, previous_summary: str | None = None) -> str:
        compressed = compress_context(context)
        if previous_summary:
            return self.builder.render(
                "continuation_query.jinja",
                previous_summary=previous_summary,
                topic=topic,
            )
        template = _TEMPLATE_MAP[consultation_type]
        kwargs = {"context": compressed, "topic": topic, "weakness": topic, "goal": topic}
        return self.builder.render(template, **kwargs)
