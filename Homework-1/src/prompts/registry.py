import yaml
from pathlib import Path
from jinja2 import Template
from .prompt_template import PromptTemplate


class PromptRegistry:
    def __init__(self, folder: str):
        self._templates = self._load(folder)

    def _load(self, folder: str) -> dict[str, PromptTemplate]:
        # Load all .yaml files from folder → dict {name: PromptTemplate}
        templates = {}
        for path in Path(folder).rglob("*.yaml"):
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
            tpl = PromptTemplate(**data)
            templates[tpl.name] = tpl
        return templates

    def render(self, name: str, **variables) -> str:
        """Render a prompt with Jinja2 variable substitution"""
        template = self._templates[name]
        
        # Support both old format and new structured format
        if template.prompt:
            # Legacy format: single prompt field
            return Template(template.prompt).render(**variables)
        else:
            # New structured format: combine all sections
            identity = Template(template.identity or "").render(**variables)
            context = Template(template.context or "").render(**variables)
            instructions = Template(template.instructions or "").render(**variables)
            constraints = Template(template.constraints or "").render(**variables)
            format_output = Template(template.format_output or "").render(**variables)
            
            prompt = f"""## Identity
{identity}

## Context
{context}

## Instructions
{instructions}

## Constraints
{constraints}

## Format Output
{format_output}"""
            
            return prompt