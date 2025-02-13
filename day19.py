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


async def process_l19_step_1(callback_query, state):
    await callback_query.message.answer(
        "Доброе утро! \nУже три недели мы идём к твоей цели! \nСамое время увидеть первые ощутимые результаты! \nНиже — твой прогресс на этом этапе."
    )
    iserror, week_resp = await long_rate(callback_query.from_user.id, "3")
    if not iserror:
        await callback_query.message.answer(chat_id=callback_query.from_user.id,text = week_resp)
    else: 
        await callback_query.message.answer(callback_query.from_user.id.id,text = "Ошибка")

    await callback_query.message.answer(
        "<b>Вот к каким результатам ты смог(ла) прийти с моей помощью за эти три этапа:</b> \n\n🍓 Понять, что такое осознанное питание, и начать следовать его принципам. \n🍒 Разобраться, как белки, жиры и углеводы влияют на чувство насыщения. \n🍑 Научиться утолять голод и при этом не передать. \n🍊 Составить сбалансированный, вкусный и полезный рацион на день и неделю. \n🍌 Начать лучше определять свои эмоции и регулировать их; понять, как они влияют на питание. \n🍐 Понять, как связаны питание и остальные аспекты жизни: сон, отдых, уровень стресса. \n🥭 Начать получать удовольствие от еды и не испытывать за это вину."
    )
    await callback_query.message.answer(
        "Это очень прочный фундамент для того, чтобы начать новую жизнь! Чтобы точно превратить осознанное питание в привычку, продолжай пользоваться дневником и другими функциями Нутри. \n\nЗавтра будем звонить в колокольчик последнего звонка и отправлять тебя в самостоятельную жизнь! Но с поддержкой Нутри, конечно!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
    )