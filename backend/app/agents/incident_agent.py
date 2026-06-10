from typing import Any

from app.models.incident import AlertRequest, IncidentAnalysis, Recommendation
from app.tools.registry import TOOL_REGISTRY
from app.services.llm_service import generate_structured_incident_analysis


def classify_incident(alert: AlertRequest) -> str:
    """
    Determine the incident category from the alert type and message.
    """

    text = f"{alert.alert_type} {alert.message}".lower()

    if "crashloopbackoff" in text:
        return "startup_failure"

    if "latency" in text or "p95" in text or "p99" in text:
        return "latency"

    if "cpu" in text:
        return "cpu"

    if "memory" in text or "oom" in text:
        return "memory"

    return "unknown"


def plan_tools(alert: AlertRequest) -> list[str]:
    """
    Decide which tools to run based on incident type.
    """

    incident_type = classify_incident(alert)

    investigation_map = {
        "startup_failure": [
            "get_pod_logs",
            "get_deployment_status",
            "get_recent_incidents",
        ],

        "latency": [
            "get_service_metrics",
            "get_recent_deployments",
            "get_service_health",
        ],

        "cpu": [
            "get_service_metrics",
            "get_recent_deployments",
        ],

        "memory": [
            "get_service_metrics",
            "get_pod_logs",
        ],
    }

    return investigation_map.get(
        incident_type,
        ["get_deployment_status"],
    )


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


def build_investigation_steps(
    alert: AlertRequest,
    tool_results: dict[str, Any],
) -> list[str]:
    incident_type = classify_incident(alert)

    steps = [
        f"Classified incident as {incident_type}",
        f"Selected investigation tools: {', '.join(tool_results.keys())}",
    ]

    for tool_name in tool_results.keys():
        steps.append(f"Executed tool: {tool_name}")

    steps.append("Correlated tool outputs with alert context")
    steps.append("Generated structured incident diagnosis")

    return steps


def synthesize_analysis(
    alert: AlertRequest,
    tool_results: dict[str, Any],
) -> IncidentAnalysis:
    logs = str(tool_results.get("get_pod_logs", "")).lower()
    deployment = tool_results.get("get_deployment_status", {})
    metrics = tool_results.get("get_service_metrics", {})
    health = tool_results.get("get_service_health", {})
    recent_deployment = tool_results.get("get_recent_deployments", {})

    incident_type = classify_incident(alert)

    if incident_type == "startup_failure":
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
                investigation_steps=build_investigation_steps(
                    alert=alert,
                    tool_results=tool_results,
                ),
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
                investigation_steps=build_investigation_steps(
                    alert=alert,
                    tool_results=tool_results,
                ),
            )

    if incident_type == "latency":
        p95_latency = metrics.get("p95_latency_ms")
        error_rate = metrics.get("error_rate")
        health_status = health.get("status")
        deployed_minutes_ago = recent_deployment.get("deployed_minutes_ago")
        version = recent_deployment.get("version")

        if p95_latency and p95_latency >= 1000:
            return IncidentAnalysis(
                severity="high",
                root_cause=f"Latency degradation likely introduced by recent deployment {version}",
                confidence=0.87,
                recommendations=[
                    Recommendation(
                        action=f"Review or rollback deployment {version}",
                        reason=f"P95 latency is {p95_latency}ms and deployment occurred {deployed_minutes_ago} minutes ago",
                        priority="high",
                    ),
                    Recommendation(
                        action="Inspect downstream dependencies and slow queries",
                        reason=f"Service health is {health_status} and error rate is {error_rate}",
                        priority="medium",
                    ),
                ],
                tools_used=list(tool_results.keys()),
                investigation_steps=build_investigation_steps(
                    alert=alert,
                    tool_results=tool_results,
                ),
            )

    if incident_type == "cpu":
        cpu = metrics.get("cpu_percent")

        if cpu and cpu >= 80:
            return IncidentAnalysis(
                severity="high",
                root_cause="High CPU utilization is causing service instability",
                confidence=0.82,
                recommendations=[
                    Recommendation(
                        action="Scale the service horizontally",
                        reason=f"CPU utilization is {cpu}%",
                        priority="high",
                    ),
                    Recommendation(
                        action="Profile recent code paths for CPU-heavy operations",
                        reason="Recent deployment may have introduced inefficient processing",
                        priority="medium",
                    ),
                ],
                tools_used=list(tool_results.keys()),
                investigation_steps=build_investigation_steps(
                    alert=alert,
                    tool_results=tool_results,
                ),
            )

    if incident_type == "memory":
        memory = metrics.get("memory_percent")

        if memory and memory >= 80:
            return IncidentAnalysis(
                severity="high",
                root_cause="Memory pressure detected on service instances",
                confidence=0.82,
                recommendations=[
                    Recommendation(
                        action="Inspect memory usage and potential leaks",
                        reason=f"Memory utilization is {memory}%",
                        priority="high",
                    ),
                    Recommendation(
                        action="Restart affected pods if memory continues increasing",
                        reason="Restarting may temporarily stabilize the service while root cause is investigated",
                        priority="medium",
                    ),
                ],
                tools_used=list(tool_results.keys()),
                investigation_steps=build_investigation_steps(
                    alert=alert,
                    tool_results=tool_results,
                ),
            )

    return IncidentAnalysis(
        severity="medium",
        root_cause="Insufficient evidence to determine a precise root cause",
        confidence=0.55,
        recommendations=[
            Recommendation(
                action="Collect additional logs, metrics, Kubernetes events, and deployment metadata",
                reason="Current tool results do not provide enough diagnostic evidence",
                priority="medium",
            )
        ],
        tools_used=list(tool_results.keys()),
        investigation_steps=build_investigation_steps(
            alert=alert,
            tool_results=tool_results,
        ),
    )


async def analyze_incident(alert: AlertRequest) -> IncidentAnalysis:
    incident_type = classify_incident(alert)
    print(f"[Agent] Incident Type: {incident_type}")

    planned_tools = plan_tools(alert)
    print(f"[Agent] Planned Tools: {planned_tools}")

    tool_results = await execute_tools(
        tool_names=planned_tools,
        service_name=alert.service_name,
    )

    investigation_steps = build_investigation_steps(
        alert=alert,
        tool_results=tool_results,
    )

    return generate_structured_incident_analysis(
        alert=alert.model_dump(),
        tool_results=tool_results,
        investigation_steps=investigation_steps,
    )