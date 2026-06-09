from typing import Any

from app.models.incident import AlertRequest, IncidentAnalysis, Recommendation
from app.tools.registry import TOOL_REGISTRY


def plan_tools(alert: AlertRequest) -> list[str]:
    alert_text = f"{alert.alert_type} {alert.message}".lower()

    tools = ["get_deployment_status"]

    if "crashloopbackoff" in alert_text or "pod" in alert_text:
        tools.append("get_pod_logs")

    if "payment" in alert.service_name.lower():
        tools.append("get_recent_incidents")

    return tools


async def execute_tools(
    tool_names: list[str],
    service_name: str,
) -> dict[str, Any]:
    results: dict[str, Any] = {}

    for tool_name in tool_names:
        tool = TOOL_REGISTRY.get(tool_name)

        if not tool:
            results[tool_name] = {"error": "Tool not found"}
            continue

        results[tool_name] = await tool(service_name)

    return results


def synthesize_analysis(
    alert: AlertRequest,
    tool_results: dict[str, Any],
) -> IncidentAnalysis:
    logs = str(tool_results.get("get_pod_logs", "")).lower()
    deployment = tool_results.get("get_deployment_status", {})
    incidents = tool_results.get("get_recent_incidents", [])

    if "invalid database credentials" in logs:
        return IncidentAnalysis(
            severity="critical",
            root_cause="Application startup failure caused by invalid database credentials",
            confidence=0.95,
            recommendations=[
                Recommendation(
                    action="Verify Kubernetes secret configuration",
                    reason="Pod logs indicate authentication failure during startup",
                    priority="high",
                ),
                Recommendation(
                    action="Rollback latest deployment if secret configuration changed recently",
                    reason="Deployment is unhealthy and may be related to a recent rollout",
                    priority="high",
                ),
            ],
            tools_used=list(tool_results.keys()),
        )

    if deployment.get("status") == "CrashLoopBackOff":
        return IncidentAnalysis(
            severity="high",
            root_cause="Service pods are repeatedly crashing after startup",
            confidence=0.8,
            recommendations=[
                Recommendation(
                    action="Inspect pod logs and recent deployment changes",
                    reason="CrashLoopBackOff usually indicates startup failure or runtime crash",
                    priority="high",
                )
            ],
            tools_used=list(tool_results.keys()),
        )

    return IncidentAnalysis(
        severity="medium",
        root_cause="Insufficient evidence to determine a precise root cause",
        confidence=0.55,
        recommendations=[
            Recommendation(
                action="Collect additional logs, metrics, and Kubernetes events",
                reason="Current tool results do not provide enough diagnostic evidence",
                priority="medium",
            )
        ],
        tools_used=list(tool_results.keys()),
    )


async def analyze_incident(alert: AlertRequest) -> IncidentAnalysis:
    planned_tools = plan_tools(alert)

    tool_results = await execute_tools(
        tool_names=planned_tools,
        service_name=alert.service_name,
    )

    return synthesize_analysis(
        alert=alert,
        tool_results=tool_results,
    )