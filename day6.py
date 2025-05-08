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

# IMG1 = "AgACAgIAAxkBAAIJ3me1B0Wk_5o82LsiLHnaqfNZuC2dAAKG9TEb2NCpSY88liLmyimZAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIJ4me1B0pXWi3bsfO-yHhBdUbmimA5AAKH9TEb2NCpSZ1ZfeEhm4B7AQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIJ5me1B04LVXaTUsJXxAIuMKPE48emAAKI9TEb2NCpSc-ZjFfu_Um6AQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIJ6me1B1LH93OnG0kYztSl5o9A68xUAAKJ9TEb2NCpSberV3bKagIxAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIJ7me1B1aH1VvKTYlnkJVHvCwc3UKcAAKK9TEb2NCpSXYrGxXWsvGBAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIJ8me1B1r7aGB59eoo7TnaPAucBbTvAAKL9TEb2NCpSYVqHvJDB9ccAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIJ9me1B16jYLAEDjXDSzPXYFdjygABlgACjPUxG9jQqUkM7UaX3sSc9QEAAwIAA3kAAzYE"
# IMG8 = "AgACAgIAAxkBAAIJ-me1B2LB-3AyAAEKJtQ3fIjulDJD9wACjfUxG9jQqUmQOVYkmdK_PQEAAwIAA3kAAzYE"

IMG1 = "AgACAgIAAxkBAAEEXApn2e2W8Si4aVXTp2LTjj3yTmbbCAACsfAxG2W90Er1x-8QFd6lggEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEXA1n2e2e53kbAAHJ2gNUbl1Y7b6iiBsAArLwMRtlvdBKlTnGMw8QFyUBAAMCAAN5AAM2BA"
IMG3 = "AgACAgIAAxkBAAEHUj1oD1bMzbS_k_yB3f0cSIc9yLh7rQACzuwxGxLsgUgse4I1O7X2_wEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEXB5n2e3OYpGlz7eWCLY7od1ZTlGQHgACtPAxG2W90Er_Wet7LM8WNQEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEHUkFoD1cB9tVWTpT2GXNxeXtjxi1HHgAC0uwxGxLsgUhkTtgVYdSGSAEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEXCRn2e3n-asgwZHFZZaxss16_8J77gACtvAxG2W90EqWGOH8RhCTdAEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEXCdn2e3vxyRBVgn-09sFE6OstaN6CAACt_AxG2W90EqR78juDxlvQQEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEXCpn2e32NNx60_2COR0H4WIhKp22BQACuPAxG2W90EqopfeMS46agwEAAwIAA3kAAzYE"



async def process_l6_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 5:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        await state.set_state(UserState.menu)
        return
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
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "6")
        asyncio.create_task(log_bot_response(f"lesson 6 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l6_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Не могу тебе отказать!  \n\nНо для дневника питания выходных не бывает. Заполняй его после каждого приёма пищи. Так я сама расскажу, чего не хватает в твоём рационе 🥦",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Задать вопрос", callback_data="menu_nutri_yapp")],[InlineKeyboardButton(text="📖 Дневник питания", callback_data="menu_dnevnik")]]))
    await callback_query.answer()

async def process_l6_step_11(callback_query, state):
    await callback_query.message.answer(
        "Вечер — время душевных разговоров. Если весь день было не до вопросов Нутри, то сейчас — самое время спросить всё, что ты хотел(а) узнать о питании, но боялся(лась) спросить!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Задать вопрос", callback_data="menu_nutri_yapp")]]))
    await callback_query.answer()