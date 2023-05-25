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

bot = Bot("5831603956:AAH7UlCd1WADUXRqK17x3TIJUP6PojBSods")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    view_schedule_button = KeyboardButton("Расписание")
    settings_button = KeyboardButton("Настройка")
    attendance_button = KeyboardButton("Отметиться на паре")
    my_button = KeyboardButton("Личный кабинет")
    markup.add(view_schedule_button)
    markup.add(attendance_button)
    markup.add(my_button, settings_button)
    await bot.send_message(chat_id=message.chat.id, text="Главное меню:", reply_markup=markup)


async def schedule_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    today_button = KeyboardButton("Сегодня")
    tomorrow_button = KeyboardButton("Завтра")
    week_button = KeyboardButton("На неделю")
    back_button = KeyboardButton("Вернуться в меню")
    markup.add(today_button, tomorrow_button, week_button)
    markup.add(back_button)
    await bot.send_message(chat_id=message.chat.id, text="Выберите, на какой день вы хотите увидеть расписание", reply_markup=markup)


async def notifications_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    subscribe_button = KeyboardButton("Подписаться на уведомления")
    unsubscribe_button = KeyboardButton("Отписаться от уведомлений")
    back_button = KeyboardButton("Вернуться в меню")
    markup.add(subscribe_button, unsubscribe_button)
    markup.add(back_button)
    await bot.send_message(chat_id=message.chat.id, text="Я могу присылать вам уведомления о следующей пары за 10 минут до её начала. "
                                                         "Также вы можете отписаться от них", reply_markup=markup)


async def settings_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    subscribeset_button = KeyboardButton("Настроить уведомления")
    account_button = KeyboardButton("Отвязать аккаунт")
    back_button = KeyboardButton("Вернуться в меню")
    markup.add(subscribeset_button, account_button)
    markup.add(back_button)
    await bot.send_message(chat_id=message.chat.id, text="Меню настроек:", reply_markup=markup)


async def my_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    subject_button = KeyboardButton("Дисциплины")
    attendance_button = KeyboardButton("Посещаемость")
    back_button = KeyboardButton("Вернуться в меню")
    markup.add(subject_button, attendance_button)
    markup.add(back_button)
    await bot.send_message(chat_id=message.chat.id, text="Личный кабинет:", reply_markup=markup)