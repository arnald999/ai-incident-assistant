async def get_service_metrics(service_name: str) -> dict:
    if service_name == "search-service":
        return {
            "service": service_name,
            "p95_latency_ms": 2500,
            "cpu_percent": 45,
            "memory_percent": 60,
            "error_rate": 0.15,
        }

    if service_name == "analytics-service":
        return {
            "service": service_name,
            "p95_latency_ms": 320,
            "cpu_percent": 92,
            "memory_percent": 58,
            "error_rate": 0.04,
        }

    if service_name == "inventory-service":
        return {
            "service": service_name,
            "p95_latency_ms": 450,
            "cpu_percent": 65,
            "memory_percent": 94,
            "error_rate": 0.08,
        }

    return {
        "service": service_name,
        "p95_latency_ms": 300,
        "cpu_percent": 50,
        "memory_percent": 55,
        "error_rate": 0.01,
    }