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


async def subscribe(message: Message):
    user_id = message.from_user.id
    sql = "SELECT * FROM users WHERE telegram_id = %s"
    val = (user_id, )
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if user:
        subscription = user[2]
        if subscription == 1:
            await message.reply("Вы уже подписаны на уведомления.")
        else:
            sql = "UPDATE users SET subs = 1 WHERE telegram_id = %s"
            val = (user_id, )
            mycursor.execute(sql, val)
            mydb.commit()
            await message.reply("Отлично! Теперь вы будете получать уведомления о начале пар.")
    else:
        await message.reply("Вы не авторизованы в боте. Пожалуйста, напишите команду /start и авторизуйтесь!")



async def unsubscribe(message: Message):
    user_id = message.from_user.id
    sql = "SELECT * FROM users WHERE telegram_id = %s"
    val = (user_id, )
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if user:
        subscription = user[2]
        if subscription == 0:
            await message.reply("Вы не были подписаны на уведомления.")
        else:
            sql = "UPDATE users SET subs = 0 WHERE telegram_id = %s"
            val = (user_id, )
            mycursor.execute(sql, val)
            mydb.commit()
            await message.reply("Я больше не буду присылать вам уведомления. Чтобы подписаться обратно, "
                                "нажмите на Подписаться на уведомления или используйте команду /notifications_on")
    else:
        await message.reply("Вы не авторизованы в боте. Пожалуйста, напишите команду /start и авторизуйтесь!")