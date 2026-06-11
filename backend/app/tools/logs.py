from app.config import settings


async def mock_pod_logs(service_name: str) -> str:
    if service_name == "payment-service":
        return """
        ERROR: payment-service failed to start
        Reason: invalid database credentials
        Exit code: 1
        """

    if service_name == "inventory-service":
        return """
        WARN: inventory-service memory usage increasing rapidly
        ERROR: container terminated with OOMKilled
        Reason: Java heap space exhausted
        Exit code: 137
        """

    return f"""
    INFO: {service_name} is running
    No critical errors found in recent pod logs
    """


async def get_pod_logs(service_name: str) -> str:
    if settings.TOOL_MODE == "real":
        raise NotImplementedError(
            "Real Kubernetes log integration not implemented yet"
        )

    return await mock_pod_logs(service_name)