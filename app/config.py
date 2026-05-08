import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "KeaBuilder Hybrid ML Lead Intelligence API"
    )

    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    USE_LLM: bool = os.getenv("USE_LLM", "false").lower() == "true"

    MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")

    MISTRAL_MODEL: str = os.getenv(
        "MISTRAL_MODEL",
        "mistral-small-latest"
    )

    SEMANTIC_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    RULE_WEIGHT: float = 0.40
    SEMANTIC_WEIGHT: float = 0.40
    LLM_WEIGHT: float = 0.20


settings = Settings()