from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Severity = Literal["info", "warn", "error"]

class Rule(BaseModel):
    id: str
    description: str
    weight: float = 1.0
    severity: Severity = "warn"
    # checker: how to evaluate the rule
    # - 'contains_any'/'contains_all' => simple lexical
    # - 'llm' => ask model to check
    checker: Literal["contains_any", "contains_all", "llm"] = "llm"
    params: dict = Field(default_factory=dict)

class Rubric(BaseModel):
    name: str
    version: str = "0.1"
    rules: List[Rule]
    passing_score: float = 0.6  # fraction of weighted points required
    notes: Optional[str] = None
