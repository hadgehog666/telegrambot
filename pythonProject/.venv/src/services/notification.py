import asyncio
from typing import List, Optional, Dict, Any
from loguru import logger
from telegram import Bot
from telegram.error import TelegramError, RetryAfter

from core.config import BotConfig
from core.models import FormattedMessage
from utils.formatter import MessageFormatter


class NotificationService:
    def __init__(self, bot: Bot, config: BotConfig):
        self.bot = bot
        self.config = config
        self.formatter = MessageFormatter()

    async def send_formatted_message(
            self,
            chat_id: int,
            message: FormattedMessage,
            reply_to_message_id: Optional[int] = None
    ) -> bool:
        try:
            formatted_text = self.formatter.format_with_priority(
                message.text,
                message.priority
            )

            formatted_text = self.formatter.add_notification_type(
                formatted_text,
                message.notification_type
            )

            timestamp = self.formatter.get_timestamp()
            formatted_text += f"\n\n<small>🕒 {timestamp}</small>"

            await self.bot.send_message(
                chat_id=chat_id,
                text=formatted_text,
                parse_mode=message.parse_mode,
                disable_web_page_preview=message.disable_web_page_preview,
                reply_to_message_id=reply_to_message_id
            )

            logger.info(f"Сообщение отправлено в чат {chat_id}")
            return True

        except TelegramError as e:
            logger.error(f"Ошибка отправки в чат {chat_id}: {e}")
            return False

    async def send_bulk_notifications(
            self,
            chat_ids: List[int],
            message: FormattedMessage
    ) -> Dict[str, Any]:
        results = {
            "total": len(chat_ids),
            "success": 0,
            "failed": 0,
            "errors": []
        }

        for chat_id in chat_ids:
            success = await self.send_formatted_message(chat_id, message)

            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(chat_id)

            await asyncio.sleep(0.1)

        logger.info(f"Массовая отправка: {results['success']}/{results['total']}")
        return results