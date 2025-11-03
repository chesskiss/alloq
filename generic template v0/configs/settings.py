from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    # Index settings
    index_path: str = "domains/default/domain_kb"
    max_chunk_chars: int = 1200
    min_chunk_chars: int = 300

    class Config:
        extra = "ignore"

settings = Settings()
