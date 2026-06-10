import os

from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY", "")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY", "")
os.environ["LANGFUSE_BASE_URL"] = os.getenv(
    "LANGFUSE_HOST",
    "https://cloud.langfuse.com",
)

langfuse = get_client()