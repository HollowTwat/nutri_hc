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

IMG1 = "AgACAgIAAxkBAAIFFGeqMIMK8onTuzHBn63DQya3i1tPAAKM_DEbMp9RSS4k844XM6Z2AQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIFGGeqMIhZoXLOLwAB5kh8zW44XzSqJQACjfwxGzKfUUncx6zGRxp7cAEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAIFHGeqMIznLGg3c6NMt5yAIg_BwMHCAAKO_DEbMp9RSVTeDgnIN5qfAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIFIGeqMJFUPhYMarxLuq19gEm00pn9AAKP_DEbMp9RSUwDUHhhsiKEAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIFJGeqMJa5A8hpxq2eWBERlVInWLjaAAKQ_DEbMp9RSSlbwDqkrWqRAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIFKGeqMJv-KNoUX7g8d1VWRrypqUrdAAKR_DEbMp9RSR4vGBSLxNXTAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIFLGeqMKA2wtbwKGipqAkgb5aTbJlZAAKS_DEbMp9RSWp0H6B6sKI0AQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIFMGeqMKS_AhrDm701yQ97ut3RCSA9AAKT_DEbMp9RSaGkYGIJKGrKAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIFNGeqMKldcDUbPmXnJvhvO4Cy_bDBAAKU_DEbMp9RSVvKSAhzFEQzAQADAgADeQADNgQ"
IMG10 = "AgACAgIAAxkBAAIFOGeqMK37zgjZo3etekxffFCP2oikAAKV_DEbMp9RSf9mrdkqs9V6AQADAgADeQADNgQ"



async def process_l11_step_1(callback_query, state):
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
            [InlineKeyboardButton(text="Задать вопрос", callback_data="question"),InlineKeyboardButton(text="Дневник питания", callback_data="dnenik")],
        ])
    )
    await callback_query.answer()

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

