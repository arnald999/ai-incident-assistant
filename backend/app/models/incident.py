from pydantic import BaseModel, Field
from typing import List, Literal


class AlertRequest(BaseModel):
    service_name: str
    alert_type: str
    message: str
    environment: str = "production"


class Recommendation(BaseModel):
    action: str
    reason: str
    priority: Literal["low", "medium", "high"]


class IncidentAnalysis(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    root_cause: str
    confidence: float = Field(ge=0, le=1)
    recommendations: List[Recommendation]
    tools_used: List[str]
    investigation_steps: List[str]