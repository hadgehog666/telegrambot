import asyncio
import os
from loguru import logger
from bot.bot import TelegramNotificationBot


async def main():
    """Основная функция запуска"""
    logger.add(
        "logs/bot.log",
        rotation="1 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    print("\n" + "=" * 50)
    print("TELEGRAM NOTIFICATION BOT")
    print("=" * 50)

    token = None

    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        print(f"📁 Найден .env файл: {env_path}")
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        if key.strip() == 'BOT_TOKEN':
                            token = value.strip()
                            print(f"✅ Токен найден в .env файле")
                            break
        except Exception as e:
            print(f"❌ Ошибка чтения .env: {e}")

    if not token:
        print("\n" + "=" * 50)
        print("📝 Токен не найден в .env файле")
        print("=" * 50)
        print("Как получить токен:")
        print("1. Откройте Telegram")
        print("2. Найдите @BotFather")
        print("3. Отправьте /newbot")
        print("4. Скопируйте токен (пример: 1234567890:ABCdefGHIJKLMNopqRSTUVwxyz)")
        print("=" * 50)

        token = input("\n✏️  Введите токен бота: ").strip()

        if not token:
            print("❌ Токен обязателен!")
            return

        save = input("💾 Сохранить токен в .env файл? (y/n): ").strip().lower()
        if save == 'y':
            try:
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.write(f"BOT_TOKEN={token}\n")
                    f.write("DEBUG=false\n")
                print(f"✅ Токен сохранен в {env_path}")
            except Exception as e:
                print(f"⚠️ Не удалось сохранить в .env: {e}")

    if not token:
        token = os.getenv("BOT_TOKEN")
        if token:
            print("✅ Токен найден в переменных окружения")

    if not token:
        print("❌ Токен не найден!")
        return

    print(f"\n✅ Используется токен: {token[:10]}...{token[-10:]}")

    class SimpleConfig:
        def __init__(self, token):
            self.token = token
            self.admin_ids = []
            self.debug = False
            self.default_parse_mode = "HTML"
            self.max_message_length = 4096
            self.enable_scheduling = True
            self.max_retries = 3
            self.retry_delay = 5

    config = SimpleConfig(token)

    try:
        bot = TelegramNotificationBot(config)

        print("\n" + "=" * 50)
        print("🚀 ЗАПУСК БОТА...")
        print("=" * 50)

        await bot.start()

    except KeyboardInterrupt:
        print("\n👋 Остановка по запросу пользователя")
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка: {e}")
        print("\nПроверьте:")
        print("1. Правильность токена")
        print("2. Интернет соединение")
        print("3. Что бот активирован в Telegram")
    finally:
        try:
            await bot.stop()
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
