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

async def today(message: Message):
    user_id = message.from_user.id
    current_date = datetime.datetime.now().date()
    date = current_date.strftime("%d.%m.%Y")

    mycursor.execute("SELECT groupName FROM students WHERE telegram_id = %s",
                     (user_id,))
    groupName = mycursor.fetchone()[0]
    url = '{{base_url}}/{{publication_name}}/{{http_service}}/schedule'

    params = {
        'group': groupName,
        'date': date,
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            schedule_message = "<b><u>Расписание на сегодня:</u></b>\n\n"

            for item in response_data:
                time_start = item["timeStart"]
                time_end = item["timeEnd"]
                subject_name = item["subjectName"]
                subject_type = item["type"]
                teacher_surname = item["teacherSurname"]
                teacher_name_initial = item["teacherName"][0]
                teacher_patronymic_initial = item["teacherPatronymic"][0]
                room_num = item["roomNum"]

                schedule_message += f"⏰{time_start}-{time_end}\n<b><i>{subject_name}</i></b> <i>({subject_type})</i>\n"
                schedule_message += f"Препод. <b><i>{teacher_surname} {teacher_name_initial}. {teacher_patronymic_initial}.  </i></b> / Ауд. <b><i>{room_num}</i></b>\n\n"

            await bot.send_message(chat_id=user_id, text=schedule_message, parse_mode="HTML")

        else:
            await bot.send_message(chat_id=user_id, text='У тебя сегодня нет пар. Отдыхаем)', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка, попробуйте заново.', parse_mode="HTML")


async def tomorrow(message: Message):
    user_id = message.from_user.id
    current_date = datetime.datetime.now().date()
    tomorrow_date = current_date + datetime.timedelta(days=1)
    date = tomorrow_date.strftime("%d.%m.%Y")

    mycursor.execute("SELECT groupName FROM students WHERE telegram_id = %s",
                     (user_id,))
    groupName = mycursor.fetchone()[0]
    url = '{{base_url}}/{{publication_name}}/{{http_service}}/schedule'

    params = {
        'group': groupName,
        'date': date,
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            schedule_message = "<b><u>Расписание на завтра:</u></b>\n\n"

            for item in response_data:
                time_start = item["timeStart"]
                time_end = item["timeEnd"]
                subject_name = item["subjectName"]
                subject_type = item["type"]
                teacher_surname = item["teacherSurname"]
                teacher_name_initial = item["teacherName"][0]
                teacher_patronymic_initial = item["teacherPatronymic"][0]
                room_num = item["roomNum"]

                schedule_message += f"⏰{time_start}-{time_end}\n<b><i>{subject_name}</i></b> <i>({subject_type})</i>\n"
                schedule_message += f"Препод. <b><i>{teacher_surname} {teacher_name_initial}. {teacher_patronymic_initial}.  </i></b> / Ауд. <b><i>{room_num}</i></b>\n\n"

            await bot.send_message(chat_id=user_id, text=schedule_message, parse_mode="HTML")

        else:
            await bot.send_message(chat_id=user_id, text='У тебя завтра нет пар. Отдыхаем)', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка, попробуйте заново.', parse_mode="HTML")


async def week(message: Message):
    user_id = message.from_user.id

    today = datetime.date.today()
    current_week_start = today - datetime.timedelta(days=today.weekday())
    current_week_end = current_week_start + datetime.timedelta(days=6)

    mycursor.execute("SELECT groupName FROM students WHERE telegram_id = %s",
                     (user_id,))
    groupName = mycursor.fetchone()[0]
    url = '{{base_url}}/{{publication_name}}/{{http_service}}/schedule'

    params = {
        'group': groupName,
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            for single_date in (current_week_start + datetime.timedelta(n) for n in range(7)):
                schedule_text = ""
                for item in response_data:
                    date = datetime.datetime.strptime(item["date"], "%d.%m.%Y").date()
                    if current_week_start <= date <= current_week_end:
                        if date == single_date:
                            time_start = item["timeStart"]
                            time_end = item["timeEnd"]
                            subject_name = item["subjectName"]
                            subject_type = item["type"]
                            teacher_surname = item["teacherSurname"]
                            teacher_name = item["teacherName"]
                            teacher_patronymic = item["teacherPatronymic"]
                            room_num = item["roomNum"]

                            schedule_text += f"{date.strftime('%d.%m.%Y')} - ({single_date.strftime('%A').capitalize()})\n"
                            schedule_text += f"{time_start}-{time_end}\n"
                            schedule_text += f"<b><i>{subject_name}</i></b> <i>({subject_type})</i>\n"
                            schedule_text += f"Препод. <b><i>{teacher_surname} {teacher_name[0]}. {teacher_patronymic[0]}.  </i></b> / Ауд. <b><i>{room_num}</i></b>\n\n"

                await bot.send_message(chat_id=user_id, text=schedule_text, parse_mode="HTML")

        else:
            await bot.send_message(chat_id=user_id, text='У тебя пар на этой неделе! Отдыхаем)', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка, попробуйте заново.', parse_mode="HTML")
