from app.services.llm_service import generate_incident_analysis

result = generate_incident_analysis(
    alert={
        "service_name": "search-service",
        "alert_type": "ServiceDegradation",
    },
    tool_results={
        "metrics": {
            "p95_latency_ms": 2500
        }
    },
    investigation_steps=[
        "Collected metrics"
    ]
)

print(result)