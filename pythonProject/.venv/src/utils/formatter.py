from typing import Dict, List, Optional, Union
from datetime import datetime
from core.models import NotificationPriority, NotificationType


class MessageFormatter:
    PRIORITY_EMOJIS = {
        NotificationPriority.LOW: "ℹ️",
        NotificationPriority.MEDIUM: "📢",
        NotificationPriority.HIGH: "⚠️",
        NotificationPriority.CRITICAL: "🚨"
    }

    TYPE_EMOJIS = {
        NotificationType.INFO: "ℹ️",
        NotificationType.WARNING: "⚠️",
        NotificationType.ERROR: "❌",
        NotificationType.SUCCESS: "✅",
        NotificationType.ALERT: "🚨"
    }

    HTML_FORMATTING = {
        "bold": lambda x: f"<b>{x}</b>",
        "italic": lambda x: f"<i>{x}</i>",
        "underline": lambda x: f"<u>{x}</u>",
        "strikethrough": lambda x: f"<s>{x}</s>",
        "code": lambda x: f"<code>{x}</code>",
        "pre": lambda x: f"<pre>{x}</pre>",
        "link": lambda text, url: f'<a href="{url}">{text}</a>'
    }

    def format_with_priority(self, text: str, priority: NotificationPriority) -> str:
        templates = {
            NotificationPriority.LOW: "ℹ️ <b>Информация</b>\n\n{}",
            NotificationPriority.MEDIUM: "📢 <b>Уведомление</b>\n\n{}",
            NotificationPriority.HIGH: "⚠️ <b>Важно!</b>\n\n{}",
            NotificationPriority.CRITICAL: "🚨 <b>КРИТИЧЕСКО!</b>\n\n{}"
        }
        template = templates.get(priority, "{}")
        return template.format(text)

    def add_notification_type(self, text: str, notification_type: NotificationType) -> str:
        icon = self.TYPE_EMOJIS.get(notification_type, "📝")
        return f"{icon} {text}"

    def apply_html_formatting(self, text: str, formats: Dict[str, Union[bool, str]] = None) -> str:
        if not formats:
            return text

        formatted_text = text

        if "bold" in formats and formats["bold"]:
            formatted_text = self.HTML_FORMATTING["bold"](formatted_text)

        if "italic" in formats and formats["italic"]:
            formatted_text = self.HTML_FORMATTING["italic"](formatted_text)

        if "underline" in formats and formats["underline"]:
            formatted_text = self.HTML_FORMATTING["underline"](formatted_text)

        if "strikethrough" in formats and formats["strikethrough"]:
            formatted_text = self.HTML_FORMATTING["strikethrough"](formatted_text)

        if "code" in formats and formats["code"]:
            formatted_text = self.HTML_FORMATTING["code"](formatted_text)

        if "pre" in formats and formats["pre"]:
            formatted_text = self.HTML_FORMATTING["pre"](formatted_text)

        if "link" in formats and formats["link"]:
            url = formats["link"]
            formatted_text = self.HTML_FORMATTING["link"](formatted_text, url)

        return formatted_text

    def create_table(self, data: Dict[str, str]) -> str:
        table_rows = []
        for key, value in data.items():
            table_rows.append(f"<b>{key}:</b> {value}")
        return "\n".join(table_rows)

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")