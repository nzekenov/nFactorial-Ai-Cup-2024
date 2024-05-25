import asyncio

from asgiref.sync import sync_to_async
from celery import shared_task
from django.utils import timezone
from telegram import Bot

from config.settings.base import TELEGRAM_BOT_TOKEN
from financial_advisor.telegram.models import TelegramMessage


@shared_task
def poll_telegram():
    asyncio.run(poll_telegram_async())


async def poll_telegram_async():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updates = await bot.get_updates()

    for update in updates:
        if update.message:
            chat_id = update.message.chat.id
            message_id = update.message.message_id
            text = update.message.text
            date = update.message.date
            date = date.astimezone(timezone.get_current_timezone())
            print(text)
            # Save message to database
            await sync_to_async(TelegramMessage.objects.create)(
                chat_id=chat_id, message_id=message_id, text=text, date=date
            )
