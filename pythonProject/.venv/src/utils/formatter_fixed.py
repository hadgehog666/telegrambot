from typing import Dict, List, Optional, Union
from datetime import datetime
from core.models import NotificationPriority, NotificationType


class FixedMessageFormatter:
    """Форматтер сообщений без неподдерживаемых тегов"""

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

    def format_with_priority(
            self,
            text: str,
            priority: NotificationPriority,
            include_timestamp: bool = True
    ) -> str:
        """Форматирование БЕЗ тега small"""
        templates = {
            NotificationPriority.LOW: "ℹ️ <b>Информация</b>\n\n{}",
            NotificationPriority.MEDIUM: "📢 <b>Уведомление</b>\n\n{}",
            NotificationPriority.HIGH: "⚠️ <b>Важно!</b>\n\n{}",
            NotificationPriority.CRITICAL: "🚨 <b>КРИТИЧЕСКО!</b>\n\n{}"
        }

        template = templates.get(priority, "{}")
        formatted = template.format(text)

        if include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # БЕЗ ТЕГА small - просто текст с эмодзи
            formatted += f"\n\n🕒 {timestamp}"

        return formatted

    def add_notification_type(self, text: str, notification_type: NotificationType) -> str:
        """Добавление типа уведомления"""
        icon = self.TYPE_EMOJIS.get(notification_type, "📝")
        return f"{icon} {text}"

    def get_timestamp(self) -> str:
        """Получение временной метки"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")