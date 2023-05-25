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
from authorization import send_welcome, web_app
from notifications import subscribe, unsubscribe
from schedule import today, tomorrow, week
from alert import send_alerts
from attendance import subject
import hashlib
import base64
import json


mydb = mysql.connector.connect(user='root',
                               password='2001441',
                               host='127.0.0.1',
                               port ='3305',
                               database='schedule')
mycursor = mydb.cursor()

scheduler = BackgroundScheduler()
scheduler.start()

bot = Bot("5831603956:AAH7UlCd1WADUXRqK17x3TIJUP6PojBSods")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


@dp.message_handler(commands=["start"])
async def start_command(message):
    await send_welcome(message)


@dp.message_handler(content_types=["web_app_data"])
async def web_app_command(message):
    await web_app(message)


@dp.message_handler(Text(equals="Расписание"))
async def view_schedule(message):
    await schedule_menu(message)


@dp.message_handler(Text(equals="Настроить уведомления"))
async def configure_notifications(message):
    await notifications_menu(message)


@dp.message_handler(Text(equals="Настройка"))
async def settings(message):
    await settings_menu(message)


@dp.message_handler(Text(equals="Личный кабинет"))
async def my(message):
    await my_menu(message)


@dp.message_handler(Text(equals="Вернуться в меню"))
async def back_to_main_menu(message):
    await main_menu(message)


@dp.message_handler(commands=["notifications_on"])
@dp.message_handler(Text(equals="Подписаться на уведомления"))
async def subscribe_command(message: Message):
    await subscribe(message)


@dp.message_handler(commands=["notifications_off"])
@dp.message_handler(Text(equals="Отписаться от уведомлений"))
async def unsubscribe_command(message: Message):
    await unsubscribe(message)


@dp.message_handler(commands=["unlink"])
@dp.message_handler(Text(equals="Отвязать аккаунт"))
async def unlink_account(message: Message):
    user_id = message.from_user.id
    mycursor.execute("DELETE FROM users WHERE telegram_id = %s", (user_id,))
    mycursor.execute("DELETE FROM students WHERE telegram_id = %s", (user_id,))
    mycursor.execute("DELETE FROM teachers WHERE telegram_id = %s", (user_id,))
    mydb.commit()
    await message.reply("Вы успешно отвязали аккаунт.")
    await send_welcome(message)

@dp.message_handler(commands=["menu"])
async def menu_command(message: Message):
    await main_menu(message)


def check_login(message1):
    query = "SELECT * FROM students WHERE login = %s"
    mycursor.execute(query, (message1,))
    result = mycursor.fetchone()
    if result:
        return True
    else:
        return False

def check_login2(user_id, message1):
    query = "SELECT * FROM users WHERE telegram_id = %s OR login = %s"
    mycursor.execute(query, (user_id, message1))
    result = mycursor.fetchone()
    if result:
        return False
    else:
        return True


@dp.message_handler(Text(equals="Отметиться на паре"))
async def schedule_today(message):
    schedule = subject(message)
    if schedule == "Сейчас у вас нет пар, чтобы отметиться!":
        await message.answer("Сейчас у вас нет пар, чтобы отметиться!")
    else:
        answer = schedule[0]
        id = schedule[1]
        subjectId = schedule[2]
        callback_data = json.dumps({"id": id, "subjectId": subjectId})
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Отметиться на этой паре", callback_data=callback_data))
        await message.answer(answer, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query_handler(lambda query: query.data.startswith('{"id":') and query.data.endswith('}'))
async def handle_attendance_callback(query: CallbackQuery):
    user_id = query.from_user.id
    callback_data = json.loads(query.data)
    id = callback_data["id"]
    subjectId = callback_data["subjectId"]

    mycursor.execute("SELECT id FROM students WHERE telegram_id = %s",
                     (user_id,))
    student_id = mycursor.fetchone()[0]

    url = 'https://api.example.com/endpoint'

    payload = {
        'id': id,
        'scheduleID': subjectId,
        'studentID': student_id,
        'willAttend': True
    }

    headers = {
        "Authorization": "Запросы"
    }

    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        answer = "Вы успешно отметились на паре"
        await query.answer(text=answer, show_alert=True)
    else:
        answer = "Произошла ошибка, попробуйте еще раз!"
        await query.answer(text=answer, show_alert=True)


@dp.message_handler(commands=["today"])
@dp.message_handler(Text(equals="Сегодня"))
async def today_commands(message: Message):
    await today(message)


@dp.message_handler(commands=["tomorrow"])
@dp.message_handler(Text(equals="Завтра"))
async def tomorrow_commands(message: Message):
    await tomorrow(message)


@dp.message_handler(commands=["week"])
@dp.message_handler(Text(equals='На неделю'))
async def week_commands(message: Message):
    await week(message)



@dp.message_handler()
async def check_message(message: Message):
    await message.reply("Извините, я вас не понимаю.")


scheduler = AsyncIOScheduler()

scheduler.add_job(send_alerts, 'cron', hour=8, minute=10, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=9, minute=50, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=11, minute=30, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=13, minute=35, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=15, minute=15, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=16, minute=55, timezone='Europe/Moscow')
scheduler.add_job(send_alerts, 'cron', hour=18, minute=35, timezone='Europe/Moscow')
scheduler.start()

start_polling(dp)