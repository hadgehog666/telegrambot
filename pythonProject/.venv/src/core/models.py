from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
import re


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @classmethod
    def get_emoji(cls, priority: 'NotificationPriority') -> str:
        emoji_map = {
            cls.LOW: "ℹ️",
            cls.MEDIUM: "📢",
            cls.HIGH: "⚠️",
            cls.CRITICAL: "🚨"
        }
        return emoji_map.get(priority, "📝")


class NotificationType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    ALERT = "alert"

    @classmethod
    def get_emoji(cls, n_type: 'NotificationType') -> str:
        emoji_map = {
            cls.INFO: "ℹ️",
            cls.WARNING: "⚠️",
            cls.ERROR: "❌",
            cls.SUCCESS: "✅",
            cls.ALERT: "🚨"
        }
        return emoji_map.get(n_type, "📝")


class FormattedMessage(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    parse_mode: str = Field(default="HTML")
    disable_web_page_preview: bool = Field(default=True)
    priority: NotificationPriority = Field(default=NotificationPriority.MEDIUM)
    notification_type: NotificationType = Field(default=NotificationType.INFO)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

    @validator('parse_mode')
    def validate_parse_mode(cls, v):
        allowed_modes = ["HTML", "Markdown", "MarkdownV2"]
        if v not in allowed_modes:
            raise ValueError(f"Parse mode must be one of: {allowed_modes}")
        return v

    @validator('text')
    def validate_html_tags(cls, v, values):
        if values.get('parse_mode') == 'HTML':
            tags = re.findall(r'<(\w+)[^>]*>', v)
            closing_tags = re.findall(r'</(\w+)>', v)
            self_closing = ['br', 'hr', 'img', 'input', 'meta', 'link']

            for tag in tags:
                if tag not in self_closing:
                    if tag not in closing_tags:
                        raise ValueError(f"Незакрытый тег: <{tag}>")
        return v


class ScheduledNotification(BaseModel):
    message: FormattedMessage
    chat_id: int
    scheduled_time: datetime
    repeat_interval: Optional[int] = None
    enabled: bool = Field(default=True)

    @validator('scheduled_time')
    def validate_scheduled_time(cls, v):
        if v < datetime.now():
            raise ValueError("Scheduled time must be in the future")
        return v