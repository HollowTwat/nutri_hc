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

# IMG1 = "AgACAgIAAxkBAAIJ_me1B2ueyOfFL9kc6WRIuOwtE7t6AAKO9TEb2NCpSTFCqmNxv7neAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEXC1n2e6HS1qrV29FQy2T2csYlda6tAACuvAxG2W90EoVWPJVGOI4EQEAAwIAA3kAAzYE"

async def process_l14_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 13:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates14.step_2)
    await callback_query.message.answer(
        "Доброе утро! \n6 дней мы творили тело мечты, на седьмой можно и отдохнуть и подвести итоги недели. \n\nСегодня в программе: \n🍏чек-лист по выполнению заданий \n🍏твой прогресс за неделю, \n🍏как спланировать питание на следующей неделе, чтобы достичь твоих целей."
    )

    await callback_query.message.answer(
        "Начнём с проверки: какие задания удалось сделать на этой неделе? "
    )

    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        question="Составить хотя бы один приём пищи по принципу Гарвардской тарелки",
        options=["Было!", "Нет, попробую сегодня!"],
        is_anonymous=False
    )

async def process_l14_step_2(poll_answer, state):
    await state.set_state(LessonStates14.step_3)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Заменить привычные напитки, соусы и ингредиенты в блюдах на более полезные",
        options=["Получилось!", "Нет, посоветуюсь сегодня с Нутри, как это сделать"],
        is_anonymous=False
    )

async def process_l14_step_3(poll_answer, state):
    await state.set_state(LessonStates14.step_4)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Съесть десерт и встроить его в КБЖУ",
        options=["Вот с этим заданием никаких проблем!", "Удивительно, но это не сделано"],
        is_anonymous=False
    )

async def process_l14_step_4(poll_answer, state):
    await state.set_state(LessonStates14.step_5)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Лечь до 23.00",
        options=["Спалось отлично!", "У меня не было ни единого шанса лечь так рано…"],
        is_anonymous=False
    )

async def process_l14_step_5(poll_answer, state):
    await state.set_state(LessonStates14.step_6)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Поесть не позже чем за 2 часа до сна",
        options=["Получилось!", "Увы, холодильник был сильнее меня"],
        is_anonymous=False
    )

async def process_l14_step_6(poll_answer, state):
    await state.set_state(LessonStates14.step_7)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="Заняться спортом",
        options=["Было!", "Пока не нашлось времени"],
        is_anonymous=False
    )

async def process_l14_step_7(poll_answer, state):
    await state.clear()
    await bot.send_message(
        chat_id = poll_answer.user.id,
        text = "Если получилось сделать не все задания — самое время их выполнить. Если получилось сделать — самое время повторить потому что вся фишка заданий этой недели — в регулярности. \n\nЭто же день мечты: выспаться, позаниматься спортом, поделать психологические практики и съесть сладкое! \n\nА пока ты планируешь день, я расскажу о твоём прогрессе за неделю."
        )
    
    await bot.send_photo(chat_id = poll_answer.user.id,
                         photo=IMG1
        )
    
    iserror, week_resp = await long_rate(poll_answer.user.id, "3")
    if not iserror:
        await bot.send_message(chat_id=poll_answer.user.id,text = week_resp)
    else: 
        await bot.send_message(chat_id=poll_answer.user.id,text = "Ошибка")
    
    await bot.send_message(
        chat_id = poll_answer.user.id,
        text = "Вот и подвели итоги! Хорошего выходного, и не забывай заполнять дневник питания."
        )
    try:
        issuccess = await add_user_lesson(poll_answer.user.id, "14")
        asyncio.create_task(log_bot_response(f"lesson 14 saved status{issuccess} ", poll_answer.user.id))
    except Exception as e:
        print(e)