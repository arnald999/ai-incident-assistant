# app/tools/deployments.py
async def get_deployment_status(service_name: str) -> dict:
    return {
        "service": service_name,
        "status": "CrashLoopBackOff",
        "replicas": "0/3",
        "last_deploy": "15 minutes ago"
    }