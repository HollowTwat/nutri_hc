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

IMG1 = "AgACAgIAAxkBAAID22emtcBQwY0wC_Uj9oJ7Y_sT32sVAAIP7zEbjtU5STaq5zrIV-5lAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAID32emtcWX4-7gl4hKd0r2k4NK43XjAAIQ7zEbjtU5SRnpDJpPn-ZLAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAID42emtdIUSvug1I9Zt67aCYaMOcitAAIR7zEbjtU5SSn0UUomMAMjAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAID52emtdnBismsA5CoPK-l9uwKuh8ZAAIS7zEbjtU5SRy4BBqUDcZ5AQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAID62emtd9w9rn6S3O-pC0NKUd88vfCAAIT7zEbjtU5SX4oWty96LyLAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAID72emteQ1oF8OUwQz6nV4nAE1H0rsAAIU7zEbjtU5SW6rQijujG4bAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAID82emtem3WG-nu_Yuaz-cJTgE-QABNwACFe8xG47VOUn_rPkka3goawEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAID92emte5fXca4lOpmc7QywDAMh0-7AAIW7zEbjtU5SVYdTiQjLfVGAQADAgADeQADNgQ"



async def process_l6_step_1(callback_query, state):
    await state.set_state(LessonStates6.step_2)
    await callback_query.message.answer(
        "Доброе утро! ☀️ \n\nТы наверняка заметил(а): на этой неделе мы не пытаемся кардинально изменить твой рацион. \n\nМы просто учимся наедаться, а не переедать, утолять голод, а не заедать эмоции. Это база. Чтобы изменить рацион, сначала нужно слышать сигналы тела. Но это, конечно, не всё. \n\nНа следующей неделе на этот фундамент будем укладывать кирпичики в виде нового подхода к рациону. \n\nСегодняшний урок поможет понять, насколько сильно стоит поменять рацион. Будем разбираться, как организм говорит нам о том, что с рационом что-то не так. \n\nПройдём урок?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройдём!", callback_data="next"), InlineKeyboardButton(text="Отложим до завтра", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l6_step_2(callback_query, state):
    await state.set_state(LessonStates6.step_3)
    link = "https://telegra.ph/Kaka-pont-chego-ne-hvataet-v-racione-istochniki-informacii-07-16"
    text = f"<b>Урок 6 \nКак понять, чего не хватает в рационе</b> \n\nНесбалансированный рацион часто даёт о себе знать. Он отражается на внешнем виде и самочувствии, посылая сигналы: «Пора что-то менять!». \n\nПо каким признакам понять, что рацион стоит менять, разбираемся в сегодняшнем уроке. \n\n🔴<b>Важный дисклеймер!</b> \n\nЕсли ты обнаружил(а) у себя проблемы, перечисленные в карточках, обязательно обратись к врачу. Причина может быть не только в еде. Да, Нутри помогает наладить питание, но не помогает лечить болезни. \n\nВ паре с терапевтом, гастроэнтерологом или эндокринологом я точно буду полезнее! \n\nИсточники информации — <a href=\'{link}\'>по ссылке</a>."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    text = "✍️<b>Задание на день:</b> \n\n🍎 Попроси помощи Нутри. \n\nДля этого нажми кнопку «Задать вопрос», а потом напиши текст или голосовое примерно со следующей просьбой, например: \n\n<i>«Нутри, подскажи как я могу разнообразить свое питание?»</i>"
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Задать вопрос", callback_data="next")],
            [InlineKeyboardButton(text="📖 Дневник питания", callback_data="stop")]
        ])
    )
    
    await callback_query.answer()

async def process_l6_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Не могу тебе отказать!  \n\nНо для дневника питания выходных не бывает. Заполняй его после каждого приёма пищи. Так я сама расскажу, чего не хватает в твоём рационе 🥦",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l6_step_11(callback_query, state):
    await callback_query.message.answer(
        "Вечер — время душевных разговоров. Если весь день было не до вопросов Нутри, то сейчас — самое время спросить всё, что ты хотел(а) узнать о питании, но боялся(лась) спросить!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Задать вопрос", callback_data="menu")]]))
    await callback_query.answer()