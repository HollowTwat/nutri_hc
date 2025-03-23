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

IMG1 = "AgACAgIAAxkBAAIKvme1CxtGPCmPr8jeZxHLhd1tQelPAALL9TEb2NCpSUug-iwmzmprAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIKwme1Cx_PHq_tuv2BTr3jTNXVOg5MAALM9TEb2NCpSVufx0yJWlpvAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIKxme1CyPy4CA_XFPw0DgwsycSQ-z1AALN9TEb2NCpSW8xP5MmjMu_AQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIKyme1CybyUMownpBRjd_iY77DrUXiAALO9TEb2NCpSekAAb13EvRLVAEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAIKzme1CyrloimMMv_YwcdLXxtq0TF1AALP9TEb2NCpSZkmXf5g6jsrAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIK0me1Cy55d3PlGDYOMdZ66dREU8FAAALQ9TEb2NCpSQWeeGyEE947AQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIK1me1CzLnEegWNSFTgdJMKmZ2tSVJAALR9TEb2NCpSaddbnMMSQr5AQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIK2me1CzeSrUNUpk7jaga2oTKesob5AAIK8zEb41ioSZmPcKHz8B-FAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIK3me1CzoCuh_QWl33sPu_IsPmD_sAA9L1MRvY0KlJ5lyvRGK8BwoBAAMCAAN5AAM2BA"

# IMG1 = "AgACAgIAAxkBAAEEZ3dn2pcUcqEzU02-1YrXwvOmqowyTgAC4fExG1ap2Uod_UFa8QABnOcBAAMCAAN5AAM2BA"
# IMG2 = "AgACAgIAAxkBAAEEZ39n2pccAvp_adf0TBRKjMSJJTMNzgAC4vExG1ap2Up0N6Blk5ilrwEAAwIAA3kAAzYE"
# IMG3 = "AgACAgIAAxkBAAEEZ4Nn2pclAnvi0lGqAsG7caSR43fUjgAC5vExG1ap2UpSBONV-yVJaAEAAwIAA3kAAzYE"
# IMG4 = "AgACAgIAAxkBAAEEZ4dn2pctfA85wTn5ZYmq569AjO6sOwAC5_ExG1ap2Uo7vN7jNTHt1gEAAwIAA3kAAzYE"
# IMG5 = "AgACAgIAAxkBAAEEZ4tn2pc0qJUE2Qbtab836MGjXDfqVQAC6PExG1ap2Urm_uw3rF34eAEAAwIAA3kAAzYE"
# IMG6 = "AgACAgIAAxkBAAEEZ5Fn2pc-errf8cu9kCdRF-Cz8pn3NAAC6fExG1ap2Upf5iODr45AhwEAAwIAA3kAAzYE"
# IMG7 = "AgACAgIAAxkBAAEEZ5Vn2pdHg8C3lnHwzNTVWEPHAAH_vj0AAuvxMRtWqdlKyiMBktTR22cBAAMCAAN5AAM2BA"
# IMG8 = "AgACAgIAAxkBAAEEZ5hn2pdTGE5jFnaTmyREuxyCWUxaKAAC7vExG1ap2UpmRss4wdh1KAEAAwIAA3kAAzYE"
# IMG9 = "AgACAgIAAxkBAAEEZ5xn2pdd4F7_puvCU5UkBvOMo4NZnAAC7_ExG1ap2Up2S6aULhEFgAEAAwIAA3kAAzYE"



async def process_l13_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 12:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates13.step_2)
    await callback_query.message.answer(
        "Доброе утро! \nПоспали, теперь можно и… позаниматься спортом! \n\nСпорт и сон — два наших помощника на пути к осознанному питанию и здоровому телу. Спорт может быть разным, но вот совсем без него не получится 🤷‍♀️ Точно так же, как не получится заниматься спортом и не следить за питанием. Почему? \n\nВыясним в сегодняшнем уроке!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Сегодня без спорта", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l13_step_2(callback_query, state):
    await state.set_state(LessonStates13.step_3)
    link = "https://telegra.ph/Mozhno-li-pohudet-ne-zanimayas-sportom-istochniki-07-16"
    link2 = "https://www.youtube.com/watch?v=M-8FvC3GD8c&ab_channel=YogaWithAdriene"
    text = f"<b>Урок 6 \nМожно ли похудеть, не занимаясь спортом</b> \n\nНеприятная правда: похудеть без можно и без спорта, но получить тело мечты — вряд ли. Почему, читайте в сегодняшнем уроке. \n\nА я убежала на свою утреннюю йогу. Всем собака мордой вниз! \n\nИсточники, по которым мы написали урок — <a href=\'{link}\'>по ссылке.</a>"
    text2= f"✍️<b>Задание на день (которое лучше не откладывать):</b> \n\n🧘Уделить хотя бы 15 минут любому занятию спортом. Вот, например, <a href=\'{link2}\'>15 минут йоги, которую можно сделать в обеденный перерыв</a> (даже на рабочем месте!). \n\nА ещё лучше — позаниматься прямо сейчас. Можно прямо перед завтраком. И не забудь занести завтрак в дневник питания."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(text2,disable_web_page_preview=True,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Сделать зарядку", url = "https://www.youtube.com/watch?v=M-8FvC3GD8c&ab_channel=YogaWithAdriene")],[InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")],
        ])
    )
    await callback_query.answer()

async def process_l13_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Жаль(   \n\nЯ надеялась, мы сделаем вместе зарядку или сходим на вечернюю пробежку. Предлагаю не откладывать этот план в долгий ящик и позаниматься вместе спортом завтра!   \n\nА сегодня не забывай заполнять дневник питания 📖",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l13_step_11(callback_query, state):
    await callback_query.message.answer(
        "Прислушайся к ощущениям! \n\nКак чувствует себя твоё тело в конце дня? Может быть, зажаты плечи или болит поясница? Может быть, чувствуется усталость? Или, наоборот, всё классно? \n\nКакие бы ощущения ни были внутри, вечерняя разминка поможет почувствовать себя лучше и более качественно спать. Сделаем её вместе?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Спорт сегодня уже был!", callback_data="next")], [InlineKeyboardButton(text="Сделать разминку", url = "https://www.youtube.com/watch?v=v7SN-d4qXx0&ab_channel=YogaWithAdriene", callback_data="stop")]
        ])
        )
    await callback_query.answer()

async def process_l13_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Это здорово! \n\nТогда хорошего вечера тебе. Завтра будем подводить итоги второго этапа с Нутри, а пока желаю тебе хорошо выспаться ❤️"
        )

async def process_l13_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Приятная лёгкая разминка — отличное завершение второго этапа учёбы с Нутри. \n\nЗавтра будем подводить итоги, а пока желаю тебе хорошо выспаться ❤️"
        )

