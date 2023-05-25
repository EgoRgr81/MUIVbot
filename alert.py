import mysql.connector
from datetime import datetime, timedelta
import pytz
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
import hashlib
import base64
import json


mydb = mysql.connector.connect(user='root',
                               password='2001441',
                               host='127.0.0.1',
                               port ='3305',
                               database='schedule')
mycursor = mydb.cursor()


bot = Bot("5831603956:AAH7UlCd1WADUXRqK17x3TIJUP6PojBSods")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


async def send_alerts():
    current_date = datetime.now().date()
    date = current_date.strftime("%d.%m.%Y")
    tz_moscow = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(tz_moscow).time()
    new_time = (datetime.combine(datetime.min, current_time) + timedelta(minutes=10)).time()
    time_Start = new_time.strftime("%H:%M")

    url = '{{base_url}}/{{publication_name}}/{{http_service}}/schedule'

    params = {
        'date': date,
        'timeStart': time_Start
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            for item in response_data:
                group_name = item["groupName"]
                subject_name = item["subjectName"]
                subject_type = item["type"]
                teacher_surname = item["teacherSurname"]
                teacher_name = item["teacherName"]
                teacher_patronymic = item["teacherPatronymic"]
                room_num = item["roomNum"]

                query = "SELECT telegram_id FROM students WHERE groupName = %s"
                mycursor.execute(query, (group_name,))
                students = mycursor.fetchall()

                for student in students:
                    telegram_id = student[0]
                    message = (
                        f"<b>Через 10 минут у тебя пара!</b>\n"
                        f"<i>{subject_name} ({subject_type})</i>\n"
                        f"Препод. {teacher_surname} {teacher_name[0]}. {teacher_patronymic[0]}. / Ауд. {room_num}"
                    )

                    await bot.send_message(chat_id=telegram_id, text=message, parse_mode="HTML")
