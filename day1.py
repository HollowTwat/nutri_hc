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

IMG1 = "AgACAgIAAxkBAANBZ5lgYwEpPE_Io6f8HNjvQcDzA94AAs_lMRsKINBI0WwjOw6l8GEBAAMCAAN5AAM2BA"
IMG2 = "AgACAgIAAxkBAANFZ5lgm-ygzgfXpqc3ve7HKnbVvKIAAtDlMRsKINBI4fFmr856K5oBAAMCAAN5AAM2BA"
IMG3 = "AgACAgIAAxkBAANJZ5lgpFx0Zas0CNi_hymLjq5sCHgAAtHlMRsKINBI3BEh1d5asj8BAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAANNZ5lgrpra2SqjwqeN0A3sCYz7I4kAAtLlMRsKINBIBd3vqFSbtvkBAAMCAAN5AAM2BA"

class LessonStates(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()
    step_8 = State()
    step_9 = State()
    step_10 = State()

async def process_step_1(callback_query, state):
    await state.set_state(LessonStates.step_2)
    text = "<b>Как добиваться целей вместе с Нутри</b>\nНемного о том, как именно я приеду тебя к целям.\n\n<b>📒 Мы будем вести дневник питания\n Время</b>: не больше 3 мин в день\n\n<b>Как это работает</b>:\n\nПросто присылай в чат фото приёма пищи или голосовое с описанием твоей еды, а я сама рассчитаю КБЖУ (калории, белки, жиры и углеводы) и внесу их в дневник.\n\nТебе только нужно будет выбрать, в какой из приёмов пищи мне записать блюдо: завтрак, обед или ужин."
    await callback_query.message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Надо вносить все приёмы пищи?", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_2(callback_query, state):
    await state.set_state(LessonStates.step_3)
    link = "https://pmc.ncbi.nlm.nih.gov/articles/PMC3268700/"
    text1 = f'Звучит сложно, как и с любой новой привычкой, но я советую делать именно так!\nЕсть десятки исследований, которые <a href="{link}">доказывают, что регулярное ведение дневника помогает успешно терять вес и сохранять достигнутые результаты.'
    text2 = "<b>Вот пара причин, почему важно регулярно заполнять дневник:</b>\n\n✅ <b>Ты поймёшь, сколько калорий ешь на самом деле</b>\n\nМы склонны недооценивать количество съеденного за день Эксперименты доказывают: если порция большая, можно просчитаться на целых 356 ккал и даже больше!\n\n✅ <b>Заметишь, какие продукты «съедают» норму калорий за день и при этом не насыщают </b>\nНапример, булочка с корицей и кремом может быть приятным перекусом и при этом состоять из 500 ккал жира и углеводов. Для кого-то это треть дневной нормы. При этом после неё ты снова захочешь есть через полчаса.\n\n✅ <b>Отследишь, насколько разнообразен твой рацион</b>\nНапример, вовремя заметишь, что всю неделю в качестве гарнира ешь макароны что пора бы вместо них съесть какую-нибудь крупу."
    await callback_query.message.answer(text1)
    await callback_query.message.answer(
        text2,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Как заполнять дневник", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_3(callback_query, state):
    await state.set_state(LessonStates.step_4)
    media_files = [
        InputMediaPhoto(IMG1, caption="Here is a video!"),
        InputMediaPhoto(IMG2),
        InputMediaPhoto(IMG3),
        InputMediaPhoto(IMG4)
    ]

    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "Дальше — вперёд к гармоничным отношениям с едой. Главное, не забывай делать записи регулярно.\n\nЯ же в ближайшие три недели буду помогать тебе не только помнить про приёмы пищи, но ещё и делать это осознанно.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Как ты будешь учить меня осознанному питанию?", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_4(callback_query, state):
    await state.set_state(LessonStates.step_5)
    await callback_query.message.answer(
        "Step 4: This is the fourth step of the lesson.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Next", callback_data="next")]
        ])
    )
    await callback_query.answer()


async def process_step_5(callback_query, state):
    await state.set_state(LessonStates.step_6)
    await callback_query.message.answer(
        "Step 5: This is the fifth step of the lesson.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Next", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_6(callback_query, state):
    await state.set_state(LessonStates.step_7)
    await callback_query.message.answer(
        "Step 6: This is the sixth step of the lesson.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Next", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_7(callback_query, state):
    await state.set_state(LessonStates.step_8)
    await callback_query.message.answer(
        "Step 7: This is the seventh step of the lesson.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Next", callback_data="next")]
        ])
    )
    await callback_query.answer()