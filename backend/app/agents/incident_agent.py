from typing import Any

from app.models.incident import AlertRequest, IncidentAnalysis, Recommendation
from app.services.langfuse_service import langfuse
from app.services.llm_service import generate_structured_incident_analysis
from app.tools.registry import TOOL_REGISTRY


def classify_incident(alert: AlertRequest) -> str:
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

    return investigation_map.get(incident_type, ["get_deployment_status"])


async def execute_tools(
    tool_names: list[str],
    service_name: str,
) -> dict[str, Any]:
    results: dict[str, Any] = {}

    for tool_name in tool_names:
        with langfuse.start_as_current_observation(
            name=f"tool-{tool_name}",
            as_type="span",
            input={"service_name": service_name},
        ) as span:
            tool = TOOL_REGISTRY.get(tool_name)

            if not tool:
                error_result = {"error": "Tool not found"}
                results[tool_name] = error_result
                span.update(output=error_result)
                continue

            try:
                result = await tool(service_name)
                results[tool_name] = result
                span.update(output=result)
            except Exception as exc:
                error_result = {"error": str(exc)}
                results[tool_name] = error_result
                span.update(output=error_result)

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
    investigation_steps = build_investigation_steps(alert, tool_results)

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
                investigation_steps=investigation_steps,
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
                investigation_steps=investigation_steps,
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
                        reason=(
                            f"P95 latency is {p95_latency}ms and deployment occurred "
                            f"{deployed_minutes_ago} minutes ago"
                        ),
                        priority="high",
                    ),
                    Recommendation(
                        action="Inspect downstream dependencies and slow queries",
                        reason=f"Service health is {health_status} and error rate is {error_rate}",
                        priority="medium",
                    ),
                ],
                tools_used=list(tool_results.keys()),
                investigation_steps=investigation_steps,
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
                investigation_steps=investigation_steps,
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
                        reason=(
                            "Restarting may temporarily stabilize the service while "
                            "root cause is investigated"
                        ),
                        priority="medium",
                    ),
                ],
                tools_used=list(tool_results.keys()),
                investigation_steps=investigation_steps,
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
        investigation_steps=investigation_steps,
    )


async def analyze_incident(alert: AlertRequest) -> IncidentAnalysis:
    with langfuse.start_as_current_observation(
        name="incident-analysis",
        as_type="span",
        input=alert.model_dump(),
    ) as root_span:
        with langfuse.start_as_current_observation(
            name="classify-incident",
            as_type="span",
            input=alert.model_dump(),
        ) as span:
            incident_type = classify_incident(alert)
            span.update(output={"incident_type": incident_type})

        print(f"[Agent] Incident Type: {incident_type}")

        with langfuse.start_as_current_observation(
            name="plan-tools",
            as_type="span",
            input={"incident_type": incident_type},
        ) as span:
            planned_tools = plan_tools(alert)
            span.update(output={"planned_tools": planned_tools})

        print(f"[Agent] Planned Tools: {planned_tools}")

        with langfuse.start_as_current_observation(
            name="execute-tools",
            as_type="span",
            input={
                "planned_tools": planned_tools,
                "service_name": alert.service_name,
            },
        ) as span:
            tool_results = await execute_tools(
                tool_names=planned_tools,
                service_name=alert.service_name,
            )
            span.update(output=tool_results)

        with langfuse.start_as_current_observation(
            name="build-investigation-steps",
            as_type="span",
            input={"tool_names": list(tool_results.keys())},
        ) as span:
            investigation_steps = build_investigation_steps(
                alert=alert,
                tool_results=tool_results,
            )
            span.update(output={"steps": investigation_steps})

        try:
            with langfuse.start_as_current_observation(
                name="generate-llm-analysis",
                as_type="span",
                input={
                    "alert": alert.model_dump(),
                    "tool_results": tool_results,
                    "investigation_steps": investigation_steps,
                },
            ) as span:
                analysis = generate_structured_incident_analysis(
                    alert=alert.model_dump(),
                    tool_results=tool_results,
                    investigation_steps=investigation_steps,
                )
                span.update(output=analysis.model_dump())

            root_span.update(
                output={
                    "analysis_source": "llm",
                    "analysis": analysis.model_dump(),
                }
            )

            langfuse.flush()
            return analysis

        except Exception as exc:
            print(f"[Agent] LLM analysis failed: {exc}")

            fallback_analysis = synthesize_analysis(
                alert=alert,
                tool_results=tool_results,
            )

            root_span.update(
                output={
                    "analysis_source": "fallback",
                    "error": str(exc),
                    "analysis": fallback_analysis.model_dump(),
                }
            )

            langfuse.flush()
            return fallback_analysis