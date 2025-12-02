from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional


class BotConfig(BaseSettings):
    """Конфигурация Telegram бота"""

    token: str = Field(
        default="",  # Добавьте значение по умолчанию
        env="BOT_TOKEN",
        description="Токен бота от @BotFather"
    )

    admin_ids: List[int] = Field(
        default=[],
        env="ADMIN_IDS",
        description="ID администраторов"
    )

    debug: bool = Field(
        default=False,
        env="DEBUG",
        description="Режим отладки"
    )

    default_parse_mode: str = Field(
        default="HTML",
        env="DEFAULT_PARSE_MODE"
    )

    max_message_length: int = Field(
        default=4096,
        env="MAX_MESSAGE_LENGTH"
    )

    enable_scheduling: bool = Field(
        default=True,
        env="ENABLE_SCHEDULING"
    )

    max_retries: int = Field(
        default=3,
        env="MAX_RETRIES"
    )

    retry_delay: int = Field(
        default=5,
        env="RETRY_DELAY"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Игнорировать лишние поля


# Создаем конфиг с обработкой ошибок
try:
    config = BotConfig()
except Exception as e:
    print(f"⚠️ Внимание: Ошибка загрузки конфигурации: {e}")
    print("📝 Использую значения по умолчанию")
    config = BotConfig(_env_file=None)  # Создаем без .env файла