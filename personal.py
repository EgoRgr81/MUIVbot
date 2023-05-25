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

async def pers_subject(message: Message):
    user_id = message.from_user.id
    mycursor.execute("SELECT groupName FROM students WHERE telegram_id = %s",
                     (user_id,))
    groupName = mycursor.fetchone()[0]
    url = 'https://api.example.com/endpoint'

    params = {
        'groupName': groupName,
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            subjects_message = "Список дисциплин в этом семестре:\n"

            for index, subject in enumerate(response_data, start=1):
                subject_name = subject['subjectName']
                subject_exam_type = subject['subjectExamType']
                teacher_surname = subject['teacherSurname']
                teacher_name = subject['teacherName']
                teacher_patronymic = subject['teacherPatronymic']
                teacher_initials = f"{teacher_surname} {teacher_name[0]}. {teacher_patronymic[0]}."
                subjects_message += f"{index}. {subject_name} ({subject_exam_type})\nПреподаватель: {teacher_initials}\n\n"

            await bot.send_message(chat_id=user_id, text=subjects_message, parse_mode="HTML")

        else:
            await bot.send_message(chat_id=user_id, text='Данные не найдены.', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка, попробуйте заново.', parse_mode="HTML")


async def perc_attend(message: Message):
    user_id = message.from_user.id
    mycursor.execute("SELECT id FROM students WHERE telegram_id = %s",
                     (user_id,))
    id = mycursor.fetchone()[0]
    url = 'https://api.example.com/endpoint'

    params = {
        'userId': id,
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            total_count = len(response_data)
            true_count = sum(subject['visited'] for subject in response_data)
            false_count = total_count - true_count

            true_percentage = (true_count / total_count) * 100

            result_message = f"Процент посещаемости пар в семестре: {true_percentage:.2f}%\n\n" \
                             f"Количество посещенных пар: {true_count}\n" \
                             f"Количество пропущенных пар: {false_count}"

            await bot.send_message(chat_id=user_id, text=result_message, parse_mode="HTML")

        else:
            await bot.send_message(chat_id=user_id, text='Данные не найдены.', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка', parse_mode="HTML")