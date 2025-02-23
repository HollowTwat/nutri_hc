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

IMG1 = "AgACAgIAAxkBAAILBme1D8B1yWyEFbyV9aYd2MHdnhfIAALv9TEb2NCpSb-dC-WD4FwaAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAILCme1D8M8vh6S32_ztWOi4bXMMpWVAALw9TEb2NCpSXqjDR5svBUBAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAILDme1D8f5Epk0Ka64Jk25OTMcYvAHAALx9TEb2NCpSWqcNNqSLFMuAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAILEme1D8sqK5DME6WZ6BmX7HDBeMoeAALy9TEb2NCpSW91Od2YvXY-AQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAILFme1D875jPvEGaRrE9OJBixko-YnAALz9TEb2NCpSSPyjSi1XqevAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAILGme1D9LSiq8JFh32M31leD2v7SkYAAL09TEb2NCpSeOEVmkTrY5ZAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAILHme1D9ZhdDvQRHuPyS1JUDqCg2-ZAAIT8zEb41ioSbJMFBMfC7pRAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAILIme1D9rFw9yAlMfmjTo-jaj0bp-WAAIU8zEb41ioSf-9HKSvqgAByQEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAILJme1D97a2Pda2rVOsFH2rmS635cYAAL29TEb2NCpSUny1AzMgoiCAQADAgADeQADNgQ"
IMG10 = "AgACAgIAAxkBAAILKme1D-PfuG33bgABp9H97JHLNfFBeAAC9_UxG9jQqUlZENYpEV386gEAAwIAA3kAAzYE"

# IMG1 = "AgACAgIAAxkBAAIGNGerkueZkRiGJ59uh-IQWd6EnrKsAAJk6jEbJvVhSSQKPRcEjCMpAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIGOGerkuumA0X-sPpUIYKqtZFgT37jAAJl6jEbJvVhSSP3gb2x4DklAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIGPGerku-kfqYZSrRgfyRYqw55Zo_zAAJm6jEbJvVhST5f5WajqJiJAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIGQGerkvPGXO7KKPu17ssH8Beihk2BAAJn6jEbJvVhSb-RYU7VA_wSAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIGRGerkvaGSckeBGF1w3AccWHJ4kE-AAJo6jEbJvVhSfQPM3Lx4kkLAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIGSGerkvpk_S-oS5dXEui2n9uYvxX9AAJp6jEbJvVhSdevmnQnaPy-AQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIGTGerkv-LUlbI6rOpaqB-VpreyMwuAAJq6jEbJvVhSejUBAoPRRg3AQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIGUGerkwMElkSxuO3AmuwFZVS_w66fAAJr6jEbJvVhSYiMZTL8_AYEAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIGVGerkwf0O32YZ5d1kuHSGBXOwUCWAAJs6jEbJvVhSYpUwe5w0edoAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAIGWGerkwv3xYhdeQABQDMoGTAFOkJsWAACbeoxGyb1YUnDCK-8Qfm15QEAAwIAA3kAAzYE"



async def process_l16_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 15:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates16.step_2)
    await callback_query.message.answer(
        "Доброе утро! \nЧто ни день, то новый квест! \nВчера мы научились составлять рацион на неделю. Сегодня счастливо отправляемся в магазин, а там... 20 видов йогуртов, 5 видов гречки, 3 вида курицы. Что выбрать? \n\nРешать тебе, но я немного помогу! Некоторые продукты можно отсеять только по этикетке, если читать её правильно 😉 \n\nВ сегодняшнем уроке будем учиться читать этикетки. Начнём?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l16_step_2(callback_query, state):
    await state.clear()
    link = "https://telegra.ph/Kak-chitat-ehtiketki-produktov-istochniki-informacii-07-16"
    text = f"<b>Урок 2 \nКак читать этикетки продуктов</b> \n\nМы уже знаем, что важно обращать внимание на разнообразие в питании, калорийность продуктов и баланс белков, жиров и углеводов. Но на что ещё? \n\nНа этикетках продуктов миллион подписей, и не всегда понятно, что за ними скрывается. \n\nНо без паники! Во всём разберёмся в сегодняшнем уроке. Спойлер: КБЖУ и разнообразное питание по-прежнему в приоритете. \n\nИсточники, по которым мы написали этот урок — <a href=\'{link}\'>по ссылке</a>."
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
    

async def process_l16_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Хорошо! Но обязательно возвращайся завтра 💔   \n\nА сегодня в свободную минутку обязательно заполни дневник питания.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l16_step_11(callback_query, state):
    await callback_query.message.answer(
        "«И мы пойдём с тобою гулять по магазинам», — напеваю я сегодня весь день. \n\nПолучилось ли проверить коварные этикетки в магазине или, может быть, уже дома, на купленных проудктах?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Получилось!", callback_data="next"),InlineKeyboardButton(text="Нет", callback_data="stop")],
        ])
        )
    await callback_query.answer()

async def process_l16_step_12(callback_query, state):
    await callback_query.message.answer(
        "Надеюсь, составы тебя не напугали! \n\nПотому что завтра нас ждёт ещё сложный уровень в нашем квесте: отправимся в кафе и выберем там уже готовое блюдо!",
        )
    await callback_query.answer()

async def process_l16_step_12_2(callback_query, state):
    await state.set_state(LessonStates16.step_12)
    await callback_query.message.answer(
        "Тогда не откладывай и попробуй проверить что-то, что у тебя под рукой. \n\nА завтра нас ждёт ещё сложный уровень в нашем квесте: отправимся в кафе и выберем там уже готовое блюдо!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Анализ этикетки", callback_data="menu_nutri_etiketka")]])
        )
    await callback_query.answer()


