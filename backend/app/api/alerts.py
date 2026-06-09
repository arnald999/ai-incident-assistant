# app/api/alerts.py
from fastapi import APIRouter
from app.models.incident import AlertRequest, IncidentAnalysis
from app.agents.incident_agent import analyze_incident

router = APIRouter()


@router.post("/alerts/analyze", response_model=IncidentAnalysis)
async def analyze_alert(payload: AlertRequest):
    return await analyze_incident(payload)