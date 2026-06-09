async def get_service_health(service_name: str) -> dict:
    return {
        "service": service_name,
        "status": "degraded",
        "healthy_instances": 2,
        "total_instances": 3
    }