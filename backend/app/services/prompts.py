import json


def build_incident_prompt(
    alert: dict,
    tool_results: dict,
    investigation_steps: list[str],
) -> str:
    return f"""
You are an expert Site Reliability Engineer.

Analyze the incident using the alert, investigation steps, and tool results.

Return ONLY valid JSON. Do not include markdown. Do not include explanation outside JSON.

JSON schema:

{{
  "severity": "low | medium | high | critical",
  "root_cause": "string",
  "confidence": 0.0,
  "recommendations": [
    {{
      "action": "string",
      "reason": "string",
      "priority": "low | medium | high"
    }}
  ],
  "tools_used": ["string"],
  "investigation_steps": ["string"]
}}

ALERT:
{json.dumps(alert, indent=2)}

INVESTIGATION STEPS:
{json.dumps(investigation_steps, indent=2)}

TOOL RESULTS:
{json.dumps(tool_results, indent=2)}
"""