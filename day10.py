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

IMG1 = "AgACAgIAAxkBAAIKZme1CZCRiUYc4SVWo-Fww7dLF2nsAAKu9TEb2NCpSWb5HTeVjsyBAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIKame1CZTb-z3waniWfb_v5qoL9EYoAAKv9TEb2NCpSdr3O6dqqLgGAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIKbme1CZjogMdOGXyA8KgPvkDrAAEyNAACsPUxG9jQqUlBY96r1IjQnQEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAIKcme1CZw0fTcD9MylymM7-3KLEVVBAAKx9TEb2NCpSc9L17hhq-9GAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIKdme1CZ_GWGlzIdxcPRnYDlmSWLeiAAKy9TEb2NCpSSyo9e_IaSB-AQADAgADeQADNgQ"


# IMG1 = "AgACAgIAAxkBAAIE7WeqLF10fuvplu_VTF6n6AnaOm2xAAJq_DEbMp9RSQ84VBzeGJ8fAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIE8WeqLGKAU_7POdsp7XASt4R5NKhrAAJr_DEbMp9RSW2l1Bxa0HHWAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIE9WeqLGc8vu3STd9EAgABn5MpGpLgSgACbPwxGzKfUUkLtrGV52DoOQEAAwIAA3kAAzYE"
# IMG4 = "AgACAgIAAxkBAAIE-WeqLGuo0KQ0a-OwGmsE73PW22NYAAJt_DEbMp9RSRSXogkvUgQeAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIE_WeqLG8gdivb3ziP4H6caz5ANhwKAAJu_DEbMp9RSSz0n5DZWgfYAQADAgADeQADNgQ"



async def process_l10_step_1(callback_query, state):
    last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 9:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates10.step_2)
    await callback_query.message.answer(
        "Доброе утро! \n\nНачнём его с признаний! Сколько раз за время учёбы с Нутри тебе хотелось сладкого? Лично мне хочется чего-нибудь вкусненького каждый раз, когда я вижу картинки с конфетами и тортиками в интернете. И это нормально! \n\nПревращать сладости в запретный плод — верный путь к срывам. Чтобы не съедать за раз целую пачку печенья или мармеладок, важно иногда себе их разрешать. \n\nКак именно — разберёмся в сегодняшнем уроке.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l10_step_2(callback_query, state):
    await state.set_state(LessonStates10.step_3)
    text = "<b>Урок 3 \nКак избегать срывов в питании</b> \n\n«Откажитесь от сахара, фастфуда, алкоголя и ешьте варёную и тушёную пищу», — базовые принципы здорового питания. Всё это правильные советы. Но загвоздка в том, что ты, в отличие от меня, не робот. \n\nПерейти на такой рацион очень сложно. Даже советы Нутри по управлению эмоциями, увы, не всегда помогают! Как же тогда питаться правильно? И как избегать срывов? Будем разбираться сегодня — листайте карточки."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    text = "✍️ <b>Задание на сегодняшний день — моё любимое!</b> \n\n🍰 Долой запреты — включи любимый десерт в сегодняшний рацион! Но так, чтобы сохранить норму КБЖУ (в этом весь подвох!). \n\n🍰Чтобы всё получилось, заноси приёмы пищи в дневник питания — и Нутри подскажет, как показать этот фокус с десертом без ущерба фигуре."
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")],
        ])
    )
    await callback_query.answer()

async def process_l10_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Отказаться от урока в день сладостей — это не просто смело, это суперсмело!   \n\nУважаю твой выбор!  Возвращайся завтра, и добавим немного сахара в наше общение 🍫   \n\nА сегодня не забывай заполнять дневник питания. Ведь переесть запросто можно и без десертов 😉",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l10_step_11(callback_query, state):
    await callback_query.message.answer(
        "🍒 Вишенка на торте — вечернее напоминание Нутри о задании дня. А был ли торт?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да, я съел(а) десерт!", callback_data="next"),InlineKeyboardButton(text="Удивительно, но нет...", callback_data="stop")]]))
    await callback_query.answer()

async def process_l10_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Класс! \nНадеюсь, тебе понравилось это задание. \n\nЗавтра будем разбираться, что делать, если ограничения в еде у тебя всё-таки есть. \n\nА пока — приятного завершения дня и сладких снов ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l10_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Это даже здорово! \nЕсть сладкое, когда не хочется, точно не стоит. Это задание можно сделать в любой другой день. \n\nЗавтра будем разбираться, что делать, если ты ограничиваешь себя не только в десертах, но и в других продуктах. \n\nА пока — приятного завершения дня и сладких снов ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()