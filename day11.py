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

# IMG1 = "AgACAgIAAxkBAAIKeme1CgWyX3NVY0SXFBCJLKbXSzx2AAL_8jEb41ioSQOWhy6xToo6AQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIKfme1CgnO0TnDMLVJRwUCmyfc6udZAAK39TEb2NCpSSoK9BkJz6vaAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIKgme1CgyarddqSqloHiipV_zC7pJZAAK49TEb2NCpSafHiAn3_oHHAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIKhme1ChK4Aw39myaxGvo1gMH3xzwqAAK59TEb2NCpSZY-MUr2l1nlAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIKime1ChbNfyPLEUvNxIDB3cz8PXDdAAK69TEb2NCpSY6fVoqlnFLvAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIKjme1Chsdmfk193VEm9l0wG9LfEmlAAK79TEb2NCpSdjA6zpLd_XWAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIKkme1Ch7-mw9EqeRGsvddCoKLJkjTAAK89TEb2NCpSRAN_yNjMUAyAQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIKlme1CiPAjiEUhFIAAY2mivGecoEp5AACvfUxG9jQqUkSoJkHRZNDpgEAAwIAA3kAAzYE"
# IMG9 = "AgACAgIAAxkBAAIKmme1CibZp04Ydh3AscxOd2Tqla5TAAK-9TEb2NCpScY7iJdV54ICAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAIKnme1Cios-zdoPG8VOBwaGk9P8OUPAAK_9TEb2NCpSc6dkneRy-rdAQADAgADeQADNgQ"


IMG1 = "AgACAgIAAxkBAAEEZzJn2pTSgU8lguaQu7pC0BBOM5oZYAACw_ExG1ap2Uqc_lUXMi8PPQEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEKgwNoNLGZtedxiRdc5mPvJhmR7G1nywACwfYxG1FZoUnqPAMFTzfHfgEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEKgwdoNLG1nuX9VDE8LQ6Yi58QtplEHAACw_YxG1FZoUmliaBTxZgFkQEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEZztn2pTrZIiLR2qkkkdcT2nHqSXApAACxvExG1ap2Up7OAABm-xxt1oBAAMCAAN5AAM2BA"
IMG5 = "AgACAgIAAxkBAAEKgwtoNLG87IEIKWAG9-tM83SQtt9VFQACxPYxG1FZoUlK0bJD4SX5FAEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEZ0Fn2pT935qZqXagGRco8gpqsl6IAgACyPExG1ap2Uo_U3EtqX_T7QEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEKgw9oNLHDn2Q0LkYeaAMqjCKOY-ZCcQACxfYxG1FZoUlqqhWjMZiiIwEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEKgxNoNLHLZ-wayegIzXUocPnQHdaXMQACxvYxG1FZoUmhKQWxulktTgEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEZ0pn2pUTZSztLDWMmo4WzEwatrS68wACy_ExG1ap2Up3-N-nyw6FbAEAAwIAA3kAAzYE"
IMG10 = "AgACAgIAAxkBAAEKgxdoNLHPMa8aZX2fO24Ej1d4zCbbpQACx_YxG1FZoUm6CCS3bU5-JwEAAwIAA3kAAzYE"



async def process_l11_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 10:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        await state.set_state(UserState.menu)
        return
    await state.set_state(LessonStates11.step_2)
    await callback_query.message.answer(
        "Доброе утро! \n\nИногда мы исключаем из рациона продукты, в которых есть важные витамины и минералы. Происходить это может по разным причинам: аллергия, непереносимость, решение стать вегетарианцем. \n\nКак в такой ситуации поддерживать разнообразный рацион и получать все необходимые питательные вещества? Разберёмся в сегодняшнем уроке!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l11_step_2(callback_query, state):
    await state.set_state(LessonStates11.step_3)
    link = "https://telegra.ph/CHem-zamenit-myaso-pticu-rybu-ili-molochku-istochniki-informacii-07-16"
    text = f"<b>Урок 4 \nЧем заменить мясо, птицу, рыбу или молочку</b> \n\n<i>«Нутри, белки в рационе — это здорово. Но что, если не ем мясо или молчку? Например, я вегетарианец, веган или у меня непереносимость лактозы?»,</i> — ты запросто можешь спросить что-то подобное. А я отвечу: иметь ограничения в еде — нормально. Может, ты не ешь мясо по этическим или религиозным причинам. Может, не позволяет здоровье. Что же теперь, отказываться от осознанного питания? Совсем нет! Но это повод внимательно отнестись к своему рациону. Как при всех возможных ограничениях сохранять баланс белков, жиров и углеводов, рассказываю в сегодняшнем уроке. Листай карточки 👉 Источники информации — <a href=\'{link}\'>по ссылке</a>."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
        InputMediaPhoto(media=IMG10)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    text = "✍️ <b>Задание дня</b> \n\nПонимаю, что не у всех в рационе есть ограничение из сегодняшнего урока. В то же время витаминов и минералов организму может недоставать и без искусственных ограничений. \n\n🍏 Поэтому сегодняшнее задание — поболтать с Нутри и задать мне вопросы о питательных веществах. \n\nНапример, спроси меня: «Как заметить дефицит железа в организме?» или «Стоит ли пить биодобавки?» \n\nДля этого нажми кнопку «Задать вопрос» и напиши его в чат в свободной форме. Голосовое сообщение тоже подойдёт — я всё понимаю!"
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Задать вопрос", callback_data="menu_nutri_yapp"),InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")],
        ])
    )
    await callback_query.answer()
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "11")
        asyncio.create_task(log_bot_response(f"lesson 11 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l11_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Нутри не ругается, когда ты пропускаешь уроки, но всё же немного расстраивается!   \n\nОбязательно возвращайся к учёбе завтра, а сегодня не забывай заполнять дневник питания.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l11_step_11(callback_query, state):
    await callback_query.message.answer(
        "Перед сном бывает здорово поболтать с кем-нибудь! \nНапример, с Нутри про осознанное питание. Поговорим про витамины и минералы?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Уже задал(а)", callback_data="next"),InlineKeyboardButton(text="Задать вопрос", callback_data="question")]]))
    await callback_query.answer()

async def process_l11_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Нутри обожает вопросы и с удовольствием поговорит с тобой ещё, как только захочешь! \n\nА пока пойду отдохну немного, день был насыщенным! Завтра, кстати, поговорим о том, почему важно отдыхать и хорошо высыпаться 😴"
    )
    await callback_query.answer()

