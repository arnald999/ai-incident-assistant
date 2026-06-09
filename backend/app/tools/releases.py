async def get_recent_deployments(service_name: str) -> dict:
    return {
        "service": service_name,
        "version": "v2.3.1",
        "deployed_minutes_ago": 20
    }