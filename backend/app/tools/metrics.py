async def get_service_metrics(service_name: str) -> dict:
    return {
        "service": service_name,
        "p95_latency_ms": 2500,
        "cpu_percent": 45,
        "memory_percent": 60,
        "error_rate": 0.15
    }