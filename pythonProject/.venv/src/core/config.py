from typing import List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):

    token: str = Field(..., env="BOT_TOKEN")
    admin_ids: List[int] = Field(default=[], env="ADMIN_IDS")
    debug: bool = Field(default=False, env="DEBUG")
    default_parse_mode: str = Field(default="HTML", env="DEFAULT_PARSE_MODE")
    max_message_length: int = Field(default=4096, env="MAX_MESSAGE_LENGTH")
    enable_scheduling: bool = Field(default=True, env="ENABLE_SCHEDULING")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    retry_delay: int = Field(default=5, env="RETRY_DELAY")

    @validator('admin_ids', pre=True)
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            if v.strip():
                return [int(id.strip()) for id in v.split(',') if id.strip().isdigit()]
            return []
        return v

    @validator('default_parse_mode')
    def validate_parse_mode(cls, v):
        allowed_modes = ["HTML", "Markdown", "MarkdownV2"]
        if v not in allowed_modes:
            raise ValueError(f"Parse mode must be one of: {allowed_modes}")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = BotConfig()