import mysql.connector
import datetime
import locale
import requests
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils.executor import start_polling
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.json import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from menu import main_menu, schedule_menu, my_menu, settings_menu, notifications_menu
import hashlib
import base64
import json

bot = Bot("5831603956:AAH7UlCd1WADUXRqK17x3TIJUP6PojBSods")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['post_request'])
async def send_post_request(message: Message):
    url = 'https://api.example.com/endpoint'  # URL вашего API-эндпоинта

    # Параметры запроса, если необходимо
    payload = {
        'param1': 'value1',
        'param2': 'value2'
    }

    response = requests.post(url, json=payload)  # Выполняем POST-запрос

    if response.status_code == 200:
        await message.reply('Запрос успешно выполнен')
    else:
        await message.reply('Произошла ошибка при выполнении запроса')

@dp.message_handler(commands=['get_request'])
async def send_get_request(message: Message):
    url = 'https://api.example.com/endpoint'  # URL вашего API-эндпоинта

    # Параметры запроса, если необходимо
    params = {
        'param1': 'value1',
        'param2': 'value2'
    }

    response = requests.get(url, params=params)  # Выполняем GET-запрос

    if response.status_code == 200:
        await message.reply('Запрос успешно выполнен')
    else:
        await message.reply('Произошла ошибка при выполнении запроса')

@dp.message_handler(commands=['put_request'])
async def send_put_request(message: Message):
    url = 'https://api.example.com/endpoint'  # URL вашего API-эндпоинта

    # Параметры запроса, если необходимо
    payload = {
        'param1': 'value1',
        'param2': 'value2'
    }

    response = requests.put(url, json=payload)  # Выполняем PUT-запрос

    if response.status_code == 200:
        await message.reply('Запрос успешно выполнен')
    else:
        await message.reply('Произошла ошибка при выполнении запроса')