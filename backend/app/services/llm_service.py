import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.incident import IncidentAnalysis
from app.services.prompts import build_incident_prompt
from app.services.langfuse_service import langfuse

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = os.getenv("MODEL", "openrouter/free")


def generate_structured_incident_analysis(
    alert: dict,
    tool_results: dict,
    investigation_steps: list[str],
) -> IncidentAnalysis:
    prompt = build_incident_prompt(
        alert=alert,
        tool_results=tool_results,
        investigation_steps=investigation_steps,
    )

    with langfuse.start_as_current_observation(
        name="incident-analysis",
        as_type="span",
        input={
            "alert": alert,
            "tool_results": tool_results,
            "investigation_steps": investigation_steps,
        },
    ) as trace_span:

        with langfuse.start_as_current_observation(
            name="openrouter-analysis",
            as_type="generation",
            input=prompt,
            model=MODEL,
        ) as generation:

            print("[LLM] Calling OpenRouter...")
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert SRE incident investigator. "
                            "You must return only valid JSON matching the requested schema."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
            )
            print("[LLM] OpenRouter response received")

            content = response.choices[0].message.content
            generation.update(output=content)

        data = json.loads(content)
        trace_span.update(output=data)

    langfuse.flush()
    return IncidentAnalysis.model_validate(data)