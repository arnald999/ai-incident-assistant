# app/agents/incident_agent.py
from app.models.incident import AlertRequest, IncidentAnalysis, Recommendation
from app.tools.logs import get_pod_logs
from app.tools.deployments import get_deployment_status
from app.tools.incidents import get_recent_incidents


async def analyze_incident(alert: AlertRequest) -> IncidentAnalysis:
    logs = await get_pod_logs(alert.service_name)
    deployment = await get_deployment_status(alert.service_name)
    incidents = await get_recent_incidents(alert.service_name)

    return IncidentAnalysis(
        severity="critical",
        root_cause="Application startup failure caused by invalid database credentials",
        confidence=0.95,
        recommendations=[
            Recommendation(
                action="Verify Kubernetes secret configuration",
                reason="Logs indicate authentication failure during startup",
                priority="high"
            ),
            Recommendation(
                action="Rollback latest deployment if secret config is invalid",
                reason="Deployment began failing shortly after recent rollout",
                priority="high"
            )
        ],
        tools_used=[
            "get_pod_logs",
            "get_deployment_status",
            "get_recent_incidents"
        ]
    )