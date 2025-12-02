import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from services.notification import NotificationService
from core.models import FormattedMessage, NotificationPriority, NotificationType


def setup_handlers(application, notification_service: NotificationService):
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html("""
👋 <b>Бот уведомлений</b>

<b>Команды:</b>
/start - Начало
/help - Справка
/notify [текст] - Отправить уведомление
/test - Тестовые уведомления

<b>Пример:</b>
<code>/notify Сервер перезагружен</code>
        """)

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html("""
📚 <b>Справка</b>

<b>Форматирование HTML:</b>
<b>жирный</b> - &lt;b&gt;текст&lt;/b&gt;
<i>курсив</i> - &lt;i&gt;текст&lt;/i&gt;
<code>код</code> - &lt;code&gt;текст&lt;/code&gt;
<a href="https://example.com">ссылка</a> - &lt;a href="url"&gt;текст&lt;/a&gt;
        """)

    async def notify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_html("❌ Укажите текст")
            return

        text = " ".join(context.args)
        message = FormattedMessage(
            text=text,
            priority=NotificationPriority.MEDIUM,
            notification_type=NotificationType.INFO
        )

        success = await notification_service.send_formatted_message(
            update.effective_chat.id,
            message
        )

        if success:
            await update.message.reply_html("✅ Отправлено")
        else:
            await update.message.reply_html("❌ Ошибка")

    async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        test_messages = [
            FormattedMessage(
                text="Тест <b>HTML</b> форматирования",
                priority=NotificationPriority.LOW,
                notification_type=NotificationType.INFO
            ),
            FormattedMessage(
                text="<b>Внимание!</b> Важное сообщение",
                priority=NotificationPriority.HIGH,
                notification_type=NotificationType.WARNING
            ),
            FormattedMessage(
                text='Ссылка: <a href="https://example.com">Пример</a>',
                priority=NotificationPriority.MEDIUM,
                notification_type=NotificationType.INFO
            )
        ]

        for i, message in enumerate(test_messages, 1):
            success = await notification_service.send_formatted_message(
                update.effective_chat.id,
                message
            )

            if success:
                await update.message.reply_html(f"✅ Тест {i} отправлен")
            await asyncio.sleep(1)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("notify", notify_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(CommandHandler("send", start_command))