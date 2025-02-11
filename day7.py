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

IMG1 = "AgACAgIAAxkBAAIEG2encb1OSLDZT2oTOYOWLwfTzCsSAALK-jEbjtVBSVYXlKg8K9QKAQADAgADeQADNgQ"

async def process_l7_step_1(callback_query, state):
    await state.set_state(LessonStates7.step_2)
    await callback_query.message.answer(
        "Па-бам! \nПервая неделя с Нутри позади! Поздравляю 🎉🎉🎉 \n\nНа этой неделе мы учились осознавать свои потребности и налаживали контакт с телом и эмоциями. Теперь мы готовы менять питание! Этим займёмся на следующем этапе курса. \n\nНо сначала проверим, что тебе удалось сделать на этой неделе, и подведём итоги."
    )

    await callback_query.message.answer(
        "Отмечай, что удалось сделать, а до чего не дошли руки."
    )

    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        question="Вопрос 1 \nЗанести больше одного приёма пищи в дневник питания",
        options=["Да, и даже больше!", "Пока не до дневника…"],
        is_anonymous=False
    )

async def process_l7_step_2(poll_answer, state):
    await state.set_state(LessonStates7.step_3)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Вопрос 2 \nОтметить количество выпитой воды",
        options=["Получилось!", "Сейчас выпью и отмечу"],
        is_anonymous=False
    )

async def process_l7_step_3(poll_answer, state):
    await state.set_state(LessonStates7.step_4)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Вопрос 3 \nОценить уровень насыщения по 10-балльной шкале",
        options=["Было", "Всё время забывал(а) это сделать"],
        is_anonymous=False
    )

async def process_l7_step_4(poll_answer, state):
    await state.set_state(LessonStates7.step_5)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Вопрос 4 \nООпределить, какой тип голода испытываешь: физиологический, вкусовой или эмоциональный",
        options=["Сделано!", "Нет"],
        is_anonymous=False
    )

async def process_l7_step_5(poll_answer, state):
    await state.set_state(LessonStates7.step_6)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Вопрос 5 \nСделать одну из практик на работу с эмоциями",
        options=["Сделал(а)", "Пока нет"],
        is_anonymous=False
    )

async def process_l7_step_6(poll_answer, state):
    await state.set_state(LessonStates7.step_7)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Вопрос 6 \nВыписать свои вредные пищевые привычки",
        options=["Список есть!", "Нет, сегодня напишу"],
        is_anonymous=False
    )

async def process_l7_step_7(poll_answer, state):
    await state.clear()
    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="Любой результат — норма, ведь пищевые привычки сложно менять. Но вместе у нас получится. Читай текст, в котором мы с нутрициологом объясняем, почему подобные привычки мешают нам питаться осознанно и советуем, как от них избавиться 👇"
        )
    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="Ну а теперь подведём первые итоги. \nНиже рассказываю: \n\n🍏про твой прогресс за неделю, \n🍏как стоит скорректировать питание на следующей неделе, чтобы достичь твоих целей."
        )
    await bot.send_photo(chat_id=poll_answer.user.id,
                         photo=IMG1
        )
    
    iserror, week_resp = await long_rate(poll_answer.user.id, "3")
    if not iserror:
        await bot.send_message(chat_id=poll_answer.user.id,text = week_resp)
    else: 
        await bot.send_message(chat_id=poll_answer.user.id,text = "офибка")

