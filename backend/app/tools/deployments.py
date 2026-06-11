from app.config import settings


async def mock_deployment_status(service_name: str) -> dict:
    if service_name == "payment-service":
        return {
            "service": service_name,
            "status": "CrashLoopBackOff",
            "replicas": 3,
            "available_replicas": 0,
        }

    return {
        "service": service_name,
        "status": "Healthy",
        "replicas": 3,
        "available_replicas": 3,
    }


async def get_deployment_status(service_name: str) -> dict:
    if settings.TOOL_MODE == "real":
        raise NotImplementedError(
            "Real Kubernetes deployment integration not implemented yet"
        )

    return await mock_deployment_status(service_name)