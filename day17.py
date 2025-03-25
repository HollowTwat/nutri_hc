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

# IMG1 = "AgACAgIAAxkBAAILLme1EEhUiHkJ9dUX_lYLZvqPCn-2AAL49TEb2NCpSdCeQkaYhoYXAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAILMme1EEzBQNg_pBoH7YebH_OIPgfZAAL59TEb2NCpSY7zKTHnVzgZAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAILNme1EFCTknx6EjXYUL67NQ1lDRcYAAL69TEb2NCpSbTLirFy7TvWAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAILOme1EFQcLnlioQxg5GNSFQ-JN3pOAAL79TEb2NCpSZiI6L6bpGHLAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAILPme1EFgYytCU9ph6nwGaSKTzSky9AAL89TEb2NCpSWZNrAV89PfIAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAILQme1EFst0lSyeiHPKjWD0FlncuTcAAL99TEb2NCpSUfZl-FfPeWiAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEXE5n2fBPQzB6Szs30opUkSbrv9Fy_wACx_AxG2W90EqKEsngpd-MTAEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEXFFn2fBXzbWLep8U9suOnZxwbnV_jgACyPAxG2W90EpmOadIDFHJfgEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEEXFRn2fBdCi0lD6seXaVk_lFW7-QTewACyfAxG2W90EqrlnsIatGNmwEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEXFdn2fBm3kGOx2eLjnjjKwuTEz0KjAACyvAxG2W90EqjI8LuDfmziQEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEEXFpn2fBtMeJADi8CAtz584x1_Ud0qQACzPAxG2W90Eq8G8_qz_qHNAEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEXF1n2fB0SVib5MV28PWZaD3vRXZ-XwACzfAxG2W90EqpB7Pvn4ILoQEAAwIAA3kAAzYE"




async def process_l17_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 16:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates17.step_2)
    await callback_query.message.answer(
        "<i>«Нутри, я ведь ем не только дома, я бываю в кафе и ресторанах!»,</i> — скажете вы. \n\nА я отвечу: «Это здорово»! \n\nИ совсем никак не мешает осознанному питанию. \n\nВ сегодняшнем уроке вместе с нутрициологом даём несколько советов, на что обращать внимание в меню, чтобы найти блюдо, от которого будет радостно и тебе, и твоему дневнику питания.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l17_step_2(callback_query, state):
    await state.set_state(LessonStates17.step_3)
    text = "<b>Урок 3 \nКак питаться осознанно в кафе и ресторанах</b> \n\n🍝 Паста карбонара — 623 ккал в порции \n🥓 Хашбрауны с беконом — 485 ккал в порции \n🧀 Кесадилья с говядиной — 462 ккал в порции \n\nВсё это — калорийность блюд из популярной сети кофеен. \n\nВроде бы блюда сами по себе неплохие. Но порции большие, а в составе много соусов и добавок. Отсюда и столько калорий. \n\nНо как понять это, если в меню не указана калорийность? По косвенным признакам из наших карточек!"
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    
    await callback_query.message.answer(
        "✍️<b>Задание на день:</b> \n\n🍎 Проверь себя с Нутри: сфотографируй блюдо, которое ты съешь в кафе. И занеси в дневник питания. Про завтрак  тоже не забудь.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")]
        ])
    )
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "17")
        asyncio.create_task(log_bot_response(f"lesson 17 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l17_step_2_2(callback_query, state):
    await state.set_state(LessonStates17.step_3)
    await callback_query.message.answer(
        "Надеюсь, ты набираешься сил, чтобы потом наверстать упущенное! \n\nВозвращайся завтра, а сегодня не забудь заполнить дневник питания, для него выходных не существует 🤷",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l17_step_11(callback_query, state):
    await callback_query.message.answer(
        "Вечер! \nСамое время поужинать в каком-нибудь красивом месте. Или хотя бы пофантазировать, куда пойдёшь и что съешь в следующий раз. \n\nПолучилось ли сфотографировать меню?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Да!", callback_data="next"),InlineKeyboardButton(text="Пока нет", callback_data="stop")],
        ])
        )
    await callback_query.answer()

async def process_l17_step_12(callback_query, state):
    await callback_query.message.answer(
        "Па-бам! \nКажется, теперь все фишки Нутри тебе подвластны. И ты ещё ближе к привычке питаться осознанно. \n\nОчень рада за тебя ❤️ \n\nВозвращайся завтра, чтобы проверить знания, полученные на трёх этапах обучения.",
        )
    await callback_query.answer()

async def process_l17_step_12_2(callback_query, state):
    await callback_query.message.answer(
        "Понимаю! \nКафе и рестораны всё-таки случаются не каждый день. \n\nНичего страшного. Просто помни, что у меня есть такая функция, когда выберешься поесть вне дома. Просто вызови её в меню, и я приду на помощь 😉 \n\nИ возвращайся завтра, чтобы проверить знания, полученные на трёх этапах обучения."
        )
    await callback_query.answer()


