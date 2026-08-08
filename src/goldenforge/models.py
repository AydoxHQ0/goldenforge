from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Trace(BaseModel):
    """Normalized representation of a production AI interaction."""

    id: str
    input: str
    output: str

    timestamp: datetime | None = None
    model: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
    feedback: str | None = None
    tools: list[dict[str, Any]] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    evaluation: dict[str, Any] = Field(default_factory=dict)
