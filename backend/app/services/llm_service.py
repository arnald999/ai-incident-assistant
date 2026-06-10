import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = os.getenv("MODEL", "qwen/qwen3-30b-a3b:free")


def test_openrouter_connection() -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Reply with only: OpenRouter connected"}
        ],
    )

    return response.choices[0].message.content