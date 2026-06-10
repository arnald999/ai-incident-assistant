from app.services.llm_service import generate_structured_incident_analysis

result = generate_structured_incident_analysis(
    alert={
        "service_name": "search-service",
        "alert_type": "ServiceDegradation",
        "message": "P95 latency increased from 150ms to 2.5s",
        "environment": "production",
    },
    tool_results={
        "get_service_metrics": {
            "service": "search-service",
            "p95_latency_ms": 2500,
            "cpu_percent": 45,
            "memory_percent": 60,
            "error_rate": 0.15,
        },
        "get_recent_deployments": {
            "service": "search-service",
            "version": "v2.3.1",
            "deployed_minutes_ago": 20,
        },
        "get_service_health": {
            "service": "search-service",
            "status": "degraded",
            "healthy_instances": 2,
            "total_instances": 3,
        },
    },
    investigation_steps=[
        "Classified incident as latency",
        "Selected investigation tools: get_service_metrics, get_recent_deployments, get_service_health",
        "Executed tool: get_service_metrics",
        "Executed tool: get_recent_deployments",
        "Executed tool: get_service_health",
        "Correlated tool outputs with alert context",
        "Generated structured incident diagnosis",
    ],
)

print(result.model_dump_json(indent=2))