from pydantic import BaseModel, Field
from typing import Optional


class PromptTemplate(BaseModel):
    """Internal representation of a YAML prompt file with structured format"""
    name: str = Field(description="Unique name of the prompt")
    version: str = Field(description="Version of the prompt")
    description: str = Field(default="", description="Description of what the prompt does")
    
    # Support both old format (prompt) and new structured format
    prompt: Optional[str] = Field(default=None, description="Jinja2 template content (legacy)")
    
    # Structured prompt sections
    identity: Optional[str] = Field(default=None, description="What role/identity the AI should assume")
    context: Optional[str] = Field(default=None, description="Background information and scenario setup")
    instructions: Optional[str] = Field(default=None, description="What the AI should do")
    constraints: Optional[str] = Field(default=None, description="Limitations and rules to follow")
    format_output: Optional[str] = Field(default=None, description="How the output should be formatted")
