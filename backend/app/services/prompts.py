def build_incident_prompt(
    alert: dict,
    tool_results: dict,
    investigation_steps: list[str],
) -> str:
    return f"""
You are an expert Site Reliability Engineer.

Analyze the incident.

ALERT:
{alert}

INVESTIGATION STEPS:
{investigation_steps}

TOOL RESULTS:
{tool_results}

Return:

1. Severity
2. Root Cause
3. Confidence Score
4. Recommendations

Be concise and evidence-based.
"""