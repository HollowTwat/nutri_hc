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

IMG1 = "AgACAgIAAxkBAAILSme1ELj3a15R1V1WuRIOxYI7sZ3lAAIX8zEb41ioSaT3QXsLdlsbAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAILTme1ELyNlcAaHnQLNz5nCBBtGDyjAAID9jEb2NCpSTbiHIjG0eJ0AQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAILUme1EMC13ao-Ks8FzB4PhdQrArZBAAIE9jEb2NCpSQqgHDdic8kgAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAILVme1EMNocZZUtZWZQUDc9RUnCegJAAIY8zEb41ioSaf2HO1qmtw_AQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAILWme1EMeZ8NEiIOJH4yfxeQ5grs1CAAIZ8zEb41ioSaxDknsp-8AmAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAILXme1EMsnOkYaNbjKqwRxZYHzLPSsAAIF9jEb2NCpSRWP28_At3L7AQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAILYme1ENDWVOv8b42-r2kJZ0O5YERqAAIG9jEb2NCpSW-Z7UAEIISyAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAILZme1ENQ4URgnk6snYgGzNvRcY7_cAAIH9jEb2NCpScVe-D4P5bDGAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAILame1ENnkZxAlFEmIZQTk3gAB3n_KBAACCPYxG9jQqUl0B4LYY_-D_wEAAwIAA3kAAzYE"

# IMG1 = "AgACAgIAAxkBAAIGeGerxKjyv3-d-sH91EPlal_5xsSWAAJ86zEbJvVhSWaXMIrBRmxRAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIGfGerxK4t-khVteqQfgRj1xZmINb6AAJ96zEbJvVhSd3E8dBPrIi0AQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIGgGerxLNwXpGUB5gKK9ySJqqvmXLaAAJ-6zEbJvVhSaCQOgY9BKAFAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIGhGerxLgJnDnoQQxQY_tq7tz8vBGfAAJ_6zEbJvVhSd3IZOIMwy0NAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIGiGerxL20cHkuFVz1uSuPg8llP593AAKA6zEbJvVhSW3ESyVpSCtQAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIGjGerxMKVJMA4sMmgnT4okuNlDjguAAKB6zEbJvVhSc7Oo-XXoQuXAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIGkGerxMdpQ8QBXDe1bSpqij2ZzJ75AAKC6zEbJvVhSRqDQYvM6lu0AQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIGlGerxMxlA-GwWMEkB3cdrAxB9hOVAAKD6zEbJvVhSYC6-V_YRy8PAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIGmGerxNCjisoKVj0DaEDUODIhxaP2AAKE6zEbJvVhScpH2mRMDmcwAQADAgADeQADNgQ"



async def process_l21_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 20:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return

    
    await callback_query.message.answer(
        "Привет! \nВчера был твой выпускной, и я его праздновала! \nСейчас, признаться, болит голова 🫠 \n\nПосле трёхнедельного курса осознанного питания так и хочется пойти в фастфуд и съесть бургер с картошечкой, правда? \n\nТеперь ты знаешь, что даже такое иногда можно себе позволить! Главное, чтобы фастфуд был редким гостем в твоей тарелке и не превращался в её постоянного обитателя. \n\nКак это сделать и как сохранить достигнутые за время курсы результаты? \n\nРассказываю в бонусном уроке!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_l21_step_2(callback_query, state):
    await state.set_state(LessonStates21.step_2)
    link = "https://telegra.ph/9-sovetov-o-tom-kak-sohranit-dostignutye-rezultaty-istochniki-informacii-07-16"
    text = f"<b>Бонусный урок для самых целеустремлённых! \n9 советов о том, как сохранить достигнутые результаты</b> \n\nВ США с 1994 года 30 лет существует Национальный реестр контроля веса. Он собирает данные о людях, которые потеряли не меньше 13,6 кг (30 фунтов) и удерживали этот вес не меньше года. Их в реестре около 5 тысяч. \n\nЧто помогло им не откатиться назад? Рассказываю в карточках о результатах этого и нескольких других больших исследований. Надеюсь, они помогут тебе сохранить результаты и продолжить получать радость и пользу от еды! \n\nИсточники, по которым мы написали этот урок — <a href=\'{link}\'>по ссылке</a>."
    media_files = [
        InputMediaPhoto(media=IMG3, caption=text),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    
    text = "Первый шаг к тому, чтобы сохранить результаты и улучшить их — продолжать следовать уже приобретённой привычке. \n\nЗаполняй дневник питания, а я продолжу давать советы о том, как прийти к твоим целям."
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ])
    )
    await callback_query.answer()






