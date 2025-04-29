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

# IMG1 = "AgACAgIAAxkBAAILBme1D8B1yWyEFbyV9aYd2MHdnhfIAALv9TEb2NCpSb-dC-WD4FwaAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAILCme1D8M8vh6S32_ztWOi4bXMMpWVAALw9TEb2NCpSXqjDR5svBUBAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAILDme1D8f5Epk0Ka64Jk25OTMcYvAHAALx9TEb2NCpSWqcNNqSLFMuAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAILEme1D8sqK5DME6WZ6BmX7HDBeMoeAALy9TEb2NCpSW91Od2YvXY-AQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAILFme1D875jPvEGaRrE9OJBixko-YnAALz9TEb2NCpSSPyjSi1XqevAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAILGme1D9LSiq8JFh32M31leD2v7SkYAAL09TEb2NCpSeOEVmkTrY5ZAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAILHme1D9ZhdDvQRHuPyS1JUDqCg2-ZAAIT8zEb41ioSbJMFBMfC7pRAQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAILIme1D9rFw9yAlMfmjTo-jaj0bp-WAAIU8zEb41ioSf-9HKSvqgAByQEAAwIAA3kAAzYE"
# IMG9 = "AgACAgIAAxkBAAILJme1D97a2Pda2rVOsFH2rmS635cYAAL29TEb2NCpSUny1AzMgoiCAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAILKme1D-PfuG33bgABp9H97JHLNfFBeAAC9_UxG9jQqUlZENYpEV386gEAAwIAA3kAAzYE"

IMG1 = "AgACAgIAAxkBAAEEXGBn2fKL0EAvkVHRS3Llb8M0Xep6fQACUO4xG1ap0UqIU2Men_BfVQEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEXGNn2fKS0U-1JlBMLo-EQXG88IwjMgACUe4xG1ap0UqlERlbZkSZdAEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEEXGZn2fKzxjKrQzE3Cu0o6F0T9EkOOgACUu4xG1ap0UpBAAHQNaC4u-sBAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAAEEXGln2fK6WaksmIRkxfuDxqRGqBLiEAACU-4xG1ap0Up1507mlBp-1wEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEEXGxn2fLAGfSJY7prLbX5fx1VcEJadAACVO4xG1ap0Urxy1WprUbf9gEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEXG9n2fLH9gJmowYnVfTuN11RvV82HgACVe4xG1ap0Upp8powHlC4rwEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEXHJn2fLOGhTUw2UtyihJqii-0emmEwACVu4xG1ap0UqD_ZUlyW6o3gEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEXHVn2fLVHJN7J62NShCNKJgrI2nFIgACV-4xG1ap0Uql_U9DcFV2JwEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEXHhn2fLcR2iw9Gp-x7_u_7HSSlIcxAACWO4xG1ap0UqsUb_RSz27QQEAAwIAA3kAAzYE"
IMG10 = "AgACAgIAAxkBAAEEXHtn2fLiC1Bg5RL2yqnhwFD8qruPTAACWe4xG1ap0Ur4hc6_K1cYogEAAwIAA3kAAzYE"



async def process_l16_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 15:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
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
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "16")
        asyncio.create_task(log_bot_response(f"lesson 16 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)
    

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
    


