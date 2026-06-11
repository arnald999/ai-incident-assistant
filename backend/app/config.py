import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TOOL_MODE: str = os.getenv("TOOL_MODE", "mock")

    ENABLE_REAL_K8S: bool = (
        os.getenv("ENABLE_REAL_K8S", "false").lower() == "true"
    )

    ENABLE_REAL_PROMETHEUS: bool = (
        os.getenv("ENABLE_REAL_PROMETHEUS", "false").lower() == "true"
    )


settings = Settings()