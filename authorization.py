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
from menu import main_menu
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


async def send_welcome(message: Message):
    markup_web = ReplyKeyboardMarkup()
    auth_button = KeyboardButton("Авторизация",
                                 web_app=WebAppInfo(url="https://egorgrashchenkov1.siteme.org/main.html"))
    markup_web.add(auth_button)

    await bot.send_message(message.chat.id, "Добро пожаловать в чат-бота <b><i>Расписание МУИВ</i></b>! Чтобы бот работал корректно, необходимо авторизоваться. "
                                            "Для этого нажмите ниже на кнопку <b>Авторизация.</b>", parse_mode="HTML", reply_markup=markup_web)


async def web_app(message: Message):
    user_id = message.from_user.id
    res = json.loads(message.web_app_data.data)

    encrypt_key = "NotObviousEncryptKey"
    login = res["login"]
    password = res["password"]

    input_str = login + ":" + password
    hash_value = hashlib.sha256(encrypt_key.encode()).hexdigest().upper()

    hash_char_pos = 0
    encrypted_string = ""

    for char in input_str:
        if hash_char_pos >= len(hash_value):
            hash_char_pos = 0

        hash_char = hash_value[hash_char_pos]
        encrypted_char_code = ord(char) + ord(hash_char)
        encrypted_char = chr(encrypted_char_code)
        encrypted_string += encrypted_char
        hash_char_pos += 1

    encoded_string = base64.b64encode(encrypted_string.encode()).decode()
    token = encoded_string

    url = "{{base_url}}/{{publication_name}}/{{http_service}}/login"
    data = {
        "token": token,
        "isTeacher": res["choice"]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Запросы"
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            id = response_data['id']
            name = response_data['name']
            surname = response_data['surname']
            patronymic = response_data['patronymic']
            group_name = response_data['groupName']
            course = response_data['course']
            semester = response_data['semester']

            query = "INSERT INTO users (telegram_id, subs) VALUES (%s, %s)"
            values = (user_id, '1')
            mycursor.execute(query, values)
            mydb.commit()

            if res["choice"] == 'false':
                query = "INSERT INTO students (telegram_id, id, name, surname, patronymic, group_name, course, semester) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                values = (user_id, id, name, surname, patronymic, group_name, course, semester)
                mycursor.execute(query, values)
                mydb.commit()
                await bot.send_message(chat_id=user_id, text=f'Здравствуйте,{name} {patronymic}!\nВы успешно авторизировались в чат-боте!',
                                       parse_mode="HTML")
                await main_menu(message)
            else:
                query = "INSERT INTO teachers (telegram_id, id, name, surname, patronymic " \
                        "VALUES (%s, %s, %s, %s, %s)"
                values = (user_id, id, name, surname, patronymic)
                mycursor.execute(query, values)
                mydb.commit()
                await bot.send_message(chat_id=user_id,
                                       text=f'Здравствуйте,{name} {patronymic}!\nВы успешно авторизировались в чат-боте!',
                                       parse_mode="HTML")
                await main_menu(message)

        else:
            await bot.send_message(chat_id=user_id, text='Неверный логин или пароль, попробуйте заново.', parse_mode="HTML")

    else:
        await bot.send_message(chat_id=user_id, text='Произошла ошибка, попробуйте заново.', parse_mode="HTML")