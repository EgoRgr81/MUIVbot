import mysql.connector
import datetime
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


def get_time():
    lesson_times = [
        "8:20", "10:00", "11:40", "13:45", "15:25", "17:05", "18:35"
    ]

    now = datetime.datetime.now().time()
    current_time = datetime.time(now.hour, now.minute)

    for lesson_time in lesson_times:
        start_time = datetime.datetime.strptime(lesson_time, "%H:%M").time()
        difference = datetime.datetime.combine(datetime.date.today(), start_time) - datetime.datetime.combine(datetime.date.today(), current_time)

        if difference.total_seconds() >= -900 and difference.total_seconds() <= 600:
            return start_time.strftime("%H:%M")
    return None


def subject(message: Message):
    time = get_time()
    user_id = message.from_user.id
    if time:
        current_date = datetime.datetime.now().date()
        date = current_date.strftime("%d.%m.%Y")

        mycursor.execute("SELECT groupName FROM students WHERE telegram_id = %s",
                         (user_id,))
        groupName = mycursor.fetchone()[0]
        url = '{{base_url}}/{{publication_name}}/{{http_service}}/schedule'

        params = {
            'group': groupName,
            'date': date,
            'timeStart': time,
        }

        headers = {
            "Authorization": "Запросы"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data:
                data = []
                lesson = response_data[0]
                id = lesson["id"]
                subjectID = lesson["subjectID"]
                time_start = lesson["timeStart"]
                time_end = lesson["timeEnd"]
                subject_name = lesson["subjectName"]
                lesson_type = lesson["type"]
                teacher_surname = lesson["teacherSurname"]
                teacher_name = lesson["teacherName"]
                teacher_patronymic = lesson["teacherPatronymic"]
                room_num = lesson["roomNum"]

                subject = "<b><u>Пара, на которой вы хотите отметиться:</u></b>\n\n"
                subject += f"{time_start}-{time_end}\n<b><i>{subject_name}</i></b> <i>({lesson_type})</i>\nПрепод. <b><i>{teacher_surname} {teacher_name}. {teacher_patronymic}. </i></b>/ Ауд. <b><i>{room_num}</i></b>\n\n"
                data.append(subject)
                data.append(id)
                data.append(subjectID)
                return data

            else:
                subject = "Сейчас у вас нет пар, чтобы отметиться!"
                return subject

        else:
            subject = "Сейчас у вас нет пар, чтобы отметиться!"
            return subject
    else:
        subject = "Сейчас у вас нет пар, чтобы отметиться!"
        return subject



