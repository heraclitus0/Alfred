from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PromptBuilder:
    def __init__(self) -> None:
        template_dir = Path(__file__).resolve().parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=False)

    def render(self, template_name: str, **kwargs) -> str:
        return self.env.get_template(template_name).render(**kwargs)
