# app/tools/logs.py
async def get_pod_logs(service_name: str) -> str:
    return f"""
    ERROR: {service_name} failed to start
    Reason: invalid database credentials
    Exit code: 1
    """