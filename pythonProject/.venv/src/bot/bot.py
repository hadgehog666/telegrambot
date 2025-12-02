import asyncio
from loguru import logger
from telegram.ext import Application
from core.config import BotConfig
from services.notification import NotificationService
from .handlers import setup_handlers


class TelegramNotificationBot:
    def __init__(self, config: BotConfig):
        self.config = config
        self.application = Application.builder().token(config.token).build()
        self.notification_service = NotificationService(
            self.application.bot,
            config
        )

    async def start(self):
        logger.info("Запуск бота...")

        setup_handlers(self.application, self.notification_service)

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        logger.info("✅ Бот запущен")

        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Остановка...")
            await self.stop()

    async def stop(self):
        await self.application.stop()
        await self.application.shutdown()
        logger.info("Бот остановлен")