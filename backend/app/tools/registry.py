from typing import Any, Awaitable, Callable

from app.tools.logs import get_pod_logs
from app.tools.deployments import get_deployment_status
from app.tools.incidents import get_recent_incidents
from app.tools.metrics import get_service_metrics
from app.tools.health import get_service_health
from app.tools.releases import get_recent_deployments

ToolFn = Callable[..., Awaitable[Any]]


TOOL_REGISTRY: dict[str, ToolFn] = {
    "get_pod_logs": get_pod_logs,
    "get_deployment_status": get_deployment_status,
    "get_recent_incidents": get_recent_incidents,
    "get_service_metrics": get_service_metrics,
    "get_service_health": get_service_health,
    "get_recent_deployments": get_recent_deployments,
}


TOOL_SCHEMAS = [
    {
        "name": "get_pod_logs",
        "description": "Fetch recent pod logs for a Kubernetes service",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
    {
        "name": "get_deployment_status",
        "description": "Fetch Kubernetes deployment rollout and replica status",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
    {
        "name": "get_recent_incidents",
        "description": "Fetch recent historical incidents for a service",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
    {
        "name": "get_service_metrics",
        "description": "Fetch service-level metrics such as latency, CPU, memory, and error rate",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
    {
        "name": "get_service_health",
        "description": "Fetch current service health and instance availability",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
    {
        "name": "get_recent_deployments",
        "description": "Fetch recent deployments or releases for a service",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"}
            },
            "required": ["service_name"],
        },
    },
]