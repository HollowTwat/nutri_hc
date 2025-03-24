import asyncio
import aiogram
import random
import os
import logging
from aiogram import Bot, Dispatcher, types
import openai
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, Router, BaseMiddleware, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo
from openai import AsyncOpenAI, OpenAI

import shelve
import json

from functions import *
from functions2 import *

from all_states import *

# IMG1 = "AgACAgIAAxkBAAIK5me1DteT3rVopG4uXNndnOfXCcjbAALm9TEb2NCpSTDjtoCdWbfcAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIK6me1DtsU_4ZUv1UVO9-mXzXeF-Q-AAIR8zEb41ioSSmqsOx9oV_9AQADAgADeQADNgQ"

# IMG3 = "AgACAgIAAxkBAAIK7me1Du2AKwN4OIy0FY-in6nXB0NnAALn9TEb2NCpSS5ry02-ZOdyAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIK8me1DvRKk7rGE4ZTOz9prFsI8dSYAALo9TEb2NCpSRro-211FrAYAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIK9me1Dvht9W9yJWPlfELtfOYD9lruAALp9TEb2NCpSdCXwPSFCM-2AQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIK-me1DvwyZ_iAyHgnOzlSSEYGwiMfAALq9TEb2NCpScqAJYMerHZ4AQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIK_me1DwABHhAWWHP8SkiH1j-aTcvXvQAC6_UxG9jQqUngfp3b3MbmmAEAAwIAA3kAAzYE"
# IMG8 = "AgACAgIAAxkBAAILAme1DwS6NFC7-KYIGOYYbJUZdab5AALs9TEb2NCpSafTGAxvM0RFAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEXH5n2fOdwMIWGN3cg6AyHA7p9H_5wQACXO4xG1ap0Ur_A-CCXtS7XQEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEXIFn2fOkLOgCqGh5AAFBJaA0hq1XyL4AAl3uMRtWqdFKWvNIsVm4CtgBAAMCAAN5AAM2BA"

IMG3 = "AgACAgIAAxkBAAEEXIRn2fPKslH6ZHmd87bgYpwYDgQdtAACXu4xG1ap0UqljNyiXYynpgEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEXIdn2fPT6VQp0GcMEEWiFwJ1kaclHgACX-4xG1ap0Ur2kV3qQEreRQEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEEXIpn2fPZ9YGJa5uvavZXFN9xxR-WBAACYO4xG1ap0UoYgDZlmV-rYQEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEXI1n2fPh0kHLfD9TnyipNXjPi7w5lwACYe4xG1ap0UqIEDtulU_8gAEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEXJBn2fPn0gw3ve5xJELEwzaGY0hLPwACYu4xG1ap0Uo8JedBBU2IYQEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEXJNn2fPvs5eao6yNgFCVWosj6ZtzCAACY-4xG1ap0Ur3pA30KszS7QEAAwIAA3kAAzYE"



async def process_l15_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 14:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates15.step_2)

    media_files = [
        InputMediaPhoto(media=IMG1),
        InputMediaPhoto(media=IMG2)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "<b>А есть ли осознанное питание без Нутри?</b> \n\nПривет! Это третий и заключительный этап обучения с Нутри! \n\nУ меня нет мании величия, так что осознанное питание без меня есть. Ты уже достаточно знаешь, чтобы питаться по-новому. Осталось закрепить эти знания и научиться применять их в реальной жизни. \n\nНа этой неделе будем учиться ориентироваться во внешнем мире и отвечать на вопросы: \n\n🍏 Как перейти от хаотичного сметания продуктов с полок супермаркета к рациональным покупкам? \n🍏 Как разобраться в хитрых надписях на этикетках? \n🍏 Какую из пяти видов пасты выбрать в кафе?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l15_step_2(callback_query, state):
    await state.set_state(LessonStates15.step_3)
    link = "https://telegra.ph/Kak-sostavit-racion-i-sdelat-zakupki-v-magazine-istochniki-informacii-07-16"
    text = f"<b>Урок 1 \nКак составить рацион и сделать закупки в магазине</b> \n\nВроде идёшь за яйцами, а возвращаешься с целым пакетом еды. В итоге съедаешь лишнего — не пропадать же. Бывало такое? Наверняка хотя бы разочек! \n\nТак происходит, когда нет чёткого списка покупок и составленного рациона. Как составить рацион и список, не потратив часы? Будем разбираться сегодня. Листай карточки. \n\nИсточники, по которым мы написали этот урок — <a href=\'{link}\'>по ссылке</a>."
    media_files = [
        InputMediaPhoto(media=IMG3, caption=text),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    
    text = "✍️<b>Задание на день:</b> \n\n🍎Составить рацион на ближайшую неделю \n\nЛайфхак \n\nЕсли хочешь облегчить задачу, попроси это сделать меня. \n\nДля этого нажми кнопку «Задать вопрос» и попроси с помощью текста или голосового сообщения: «Нутри, составь мне разнообразное меню на неделю». \n\nМожешь указать продукты, которые есть у тебя в холодильнике. Я предложу свой вариант, исходя из твоей нормы КБЖУ, а ты сможешь скорректировать его под себя."
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Задать вопрос и составить меню", callback_data="menu_nutri_yapp"),InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")],
        ])
    )
    await callback_query.answer()

async def process_l15_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Выходной от учёбы, но не от осознанного питания! \n\nНе забывай заполнять дневник и рассказывать мне о своих завтраках, обедах и ужинах. На этой неделе я буду обращать особенно пристальное внимание на твой рацион 🍽",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l15_step_11(callback_query, state):
    await callback_query.message.answer(
        "Нутри не терпится заглянуть в твоё меню на неделю! 👀 \n\nНадеюсь, я увижу там фрукты, овощи, крупы, рыбу и курицу! Или не увижу? \n\nПолучилось ли у тебя составить рацион на неделю?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Получилось!", callback_data="next"),InlineKeyboardButton(text="Сегодня никак...", callback_data="stop")],
        ])
        )
    await callback_query.answer()

async def process_l15_step_12(callback_query, state):
    await callback_query.message.answer(
        "Отлично! \nЕсли ты уже сделал(а) закупки, то уже скоро присмотримся к ним повнимательнее, а если нет — завтра вместе отправимся в магазин и будем учиться читать этикетки, чтобы выбрать в магазине лучшие продукты для твоего недельного меню.",
        )
    await callback_query.answer()

async def process_l15_step_12_2(callback_query, state):
    await callback_query.message.answer(
        "Понимаю! \nДавай составим меню завтра, чтобы сразу отправиться по магазинам! \n\nБудем учиться читать этикетки, чтобы выбрать в магазине лучшие продукты для твоего недельного меню.",
        )
    await callback_query.answer()


