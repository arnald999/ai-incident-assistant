import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.incident import IncidentAnalysis
from app.services.prompts import build_incident_prompt

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

    content = response.choices[0].message.content

    data = json.loads(content)

    return IncidentAnalysis.model_validate(data)