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

class LessonStates5(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_11 = State()
    step_12 = State()
    step_13 = State()

async def process_l5_step_1(callback_query, state):
    await state.set_state(LessonStates5.step_2)
    await callback_query.message.answer(
        "🍽 <i>«Аппетит приходит во время еды», «Посуда любит чистоту», «Пока всё не съешь, из-за стола не выйдешь».</i> \n\nТебе в детстве так говорили? Нутри постоянно слышала что-то подобное. \n\nТак у меня сформировались привычки и установки, которые мешали питаться осознанно. И знаешь, что было самым сложным? Осознать, что мои привычки вредные. Ведь я с ними с самого детства! Но я справилась, и теперь хочу помочь справиться тебе! \n\nСегодня будем находить у себя эти привычки с помощью небольшой игры. Начнём?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Сегодня не до игр...", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l5_step_2(callback_query, state):
    await state.set_state(LessonStates5.step_3)
    await bot.send_poll(
        chat_id=callback_query.poll_answer.user.id,
        question="Викторина 1: Какой язык программирования вы используете?",
        options=["Python", "JavaScript", "C++"],
        is_anonymous=False
    )
    await callback_query.answer()

async def process_l5_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Принято! Поиграем завтра. \n\nНо для дневника питания выходных не бывает. Заполняй его после каждого приёма пищи. Так я, возможно, смогу заметить вредные пищевые привычки за тебя и помогу их исправить 🍏",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l5_step_3(poll_answer, state):
    await state.set_state(LessonStates5.step_4)
    
    await bot.send_poll(
        chat_id=poll_answer.poll_answer.user.id,
        question="Викторина 2: Какой фреймворк вы используете?",
        options=["Django", "Flask", "FastAPI", "Aiogram"],
        is_anonymous=False
    )

async def process_l5_step_4(poll_answer, state):
    await state.set_state(LessonStates5.step_4)
    
    await bot.send_poll(
        chat_id=poll_answer.poll_answer.user.id,
        question="Викторина 2",
        options=["Django", "Flask", "FastAPI", "Aiogram"],
        is_anonymous=False
    )