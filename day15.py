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

IMG1 = "AgACAgIAAxkBAAIGFGerjVTN0WG0MhEFHbe_cmxsOCgsAAJK6jEbJvVhSbX5glq3ZQABwwEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAIGGGerjVnG-AVAb9NoRrklsdVd6uFQAAJL6jEbJvVhSbAwibVjfPowAQADAgADeQADNgQ"

IMG3 = "AgACAgIAAxkBAAIGHGerjWPMOpKGBT61-ORjeuiZedhjAAJM6jEbJvVhScHiJ48QWtm1AQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIGIGerjWiJfd1wJOo4Xeda7IMDBKytAAJN6jEbJvVhSaJnngbnjJLpAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIGJGerjWxAVrQmBzgLNLPKoP6OpiLEAAJO6jEbJvVhSaLaWXF2wHLlAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIGKGerjXDUcxmr4FCt3YrYIgGQRJFNAAJP6jEbJvVhSVeJAYx2HlG-AQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIGLGerjXTnJ0ZQpmescfTwkqQv__3vAAJQ6jEbJvVhSUyibzRnmttyAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIGMGerjXhG64ANryvwSfhb6B-et1iDAAJR6jEbJvVhSbx0QrgyLel1AQADAgADeQADNgQ"



async def process_l15_step_1(callback_query, state):
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
            [InlineKeyboardButton(text="Задать вопрос и составить меню", callback_data="question"),InlineKeyboardButton(text="Дневник питания", callback_data="dnenik")],
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


