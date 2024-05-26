import asyncio
import os

import audioread
import requests
import soundfile as sf
import json
from asgiref.sync import sync_to_async
from celery import shared_task
from django.utils import timezone
from openai import OpenAI
from pydub import AudioSegment
from telegram import Bot

from config.settings.base import TELEGRAM_BOT_TOKEN
from financial_advisor.telegram.models import LastUpdate
from financial_advisor.telegram.models import TelegramMessage

client = OpenAI()


@shared_task
def poll_telegram():
    asyncio.run(poll_telegram_async())


async def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    with open(filename, "wb") as file:
        file.write(response.content)
    return filename


async def classify_text(text=None, image_url=None):
    messages = [
        {
            "role": "system",
            "content": """You are my smart financial assistant that helps me track my expenses and incomes. 
            I want you to detect whether the following text or image are considered as expense or income. 
            You should return the answer in the form of json list of objects with keys: 
                - type (income/expense), 
                - amount (in Kazakhstani tenge), 
                - category (in English)
                - description of income/expense (in Russian)
            """,
        },
    ]
    if text:
        messages.append(
            {"role": "user", "content": text},
        )
    if image_url:
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    classification = response.choices[0].message.content
    print(classification)
    return classification


async def get_last_update_id():
    try:
        last_update = await sync_to_async(LastUpdate.objects.latest)("id")
        return last_update.update_id
    except LastUpdate.DoesNotExist:
        return None


async def convert_ogg_to_wav(ogg_path, wav_path):
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio.export(wav_path, format="wav")


async def set_last_update_id(update_id):
    last_update, created = await sync_to_async(LastUpdate.objects.get_or_create)(id=1)
    last_update.update_id = update_id
    await sync_to_async(last_update.save)()


async def poll_telegram_async():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    last_update_id = await get_last_update_id()

    updates = await bot.get_updates(offset=last_update_id + 1 if last_update_id else 0)

    for update in updates:
        if update.update_id:
            await set_last_update_id(update.update_id)

        if not update.message:
            return

        chat_id = update.message.chat.id
        message_id = update.message.message_id
        date = update.message.date

        if timezone.is_naive(date):
            date = timezone.make_aware(date, timezone.get_current_timezone())
        else:
            date = date.astimezone(timezone.get_current_timezone())

        image_url = None
        voice_url = None
        classification = None

        if update.message.photo:
            photo = update.message.photo[-1]
            file_info = await bot.get_file(photo.file_id)
            print(file_info.file_path)
            image_url = file_info.file_path
            classification = await classify_text(
                update.message.text
                if update.message.text
                else "Determine by following photo",
                image_url,
            )
        elif update.message.voice:
            voice = update.message.voice
            file_info = await bot.get_file(voice.file_id)
            voice_url = file_info.file_path

            file_extension = os.path.splitext(voice_url)[-1]
            file_name = f"voice_{message_id}{file_extension}"
            local_ogg_path = await download_file(voice_url, file_name)
            local_wav_path = file_name.replace(file_extension, ".wav")

            try:
                await convert_ogg_to_wav(local_ogg_path, local_wav_path)
                with open(local_wav_path, "rb") as audio_file:
                    resp = client.audio.transcriptions.create(
                        model="whisper-1", file=audio_file
                    )
                    transcription = resp.text
                    classification = await classify_text(transcription)
            except Exception as e:
                print(f"Error processing voice message: {e}")
            finally:
                # Clean up local files
                os.remove(local_ogg_path)
                os.remove(local_wav_path)

        else:
            classification = await classify_text(update.message.text)

        await bot.send_message(chat_id=chat_id, text=classification)

        await sync_to_async(TelegramMessage.objects.create)(
            chat_id=chat_id,
            message_id=message_id,
            text=update.message.text,
            image_url=image_url,
            voice_url=voice_url,
            date=date,
        )
