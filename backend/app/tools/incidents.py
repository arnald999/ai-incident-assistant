# app/tools/incidents.py
async def get_recent_incidents(service_name: str) -> list[dict]:
    return [
        {
            "service": service_name,
            "root_cause": "Invalid DB credentials after secret rotation",
            "resolution": "Updated Kubernetes secret and restarted deployment"
        }
    ]