import asyncio
from loguru import logger
from core.config import BotConfig
from bot.bot import TelegramNotificationBot


async def main():
    logger.add(
        "logs/bot.log",
        rotation="1 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    try:
        config = BotConfig()
    except Exception as e:
        logger.error(f"Ошибка конфигурации: {e}")
        print("❌ Создайте .env файл из .env.example")
        return

    if not config.token:
        logger.error("Токен не указан")
        print("❌ Укажите BOT_TOKEN в .env")
        print("📝 Как получить токен:")
        print("1. Откройте Telegram")
        print("2. Найдите @BotFather")
        print("3. Создайте бота /newbot")
        print("4. Скопируйте токен")
        print("5. Вставьте в .env: BOT_TOKEN=ваш_токен")
        return

    bot = TelegramNotificationBot(config)

    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())