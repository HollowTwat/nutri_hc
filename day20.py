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

IMG1 = "AgACAgIAAxkBAAIGdGerwQ2j1C0knRa8zFO6R4dLr-AfAAJ06zEbJvVhSQbSY5xz9mkFAQADAgADeQADNgQ"

async def process_l20_step_1(callback_query, state):
    await callback_query.message.answer(
        "В этот знаменательный день хочу сказать, что образовательная программа от Нутри подошла к концу! 🎉🎉🎉 \n\nНадеваю на тебя шапочку выпускника курса по осознанному питанию 🎓 \n\nЧто бы ни говорили, 21 день — не так уж много для внедрения новых привычек. Но этого достаточно, чтобы почувствовать первые изменения. \n\nЯ уверена, раз ты до сих пор терпишь мою компанию (а я ведь бываю занудой, я в курсе), у тебя уже есть большой прогресс! Ниже анализируем, какой!"
    )
    await callback_query.message.answer_photo(photo=IMG1)

    iserror, week_resp = await long_rate(callback_query.from_user.id, "4")
    if not iserror:
        await callback_query.message.answer(week_resp)
    else: 
        await callback_query.message.answer("Ошибка")

    await callback_query.message.answer(
        "<b>Что будет дальше?</b> \n\nЭти три недели я учила тебя пользоваться функциями Нутри. А ещё вместе мы изучали базу, необходимую для осознанного питания. \n\nЧтобы закрепить новые привычки, сохранить и улучшить результаты, продолжай пользоваться Нутри."
    )
    await callback_query.message.answer(
        "Напомню, что я могу: \n\n📖 Вести твой дневник питания \n❓ Отвечать на твои вопросы \n📸 Анализировать блюдо по фотографии \n🎤 Анализировать приём пищи по голосовому сообщению или текстовому описанию \n🏷️ Анализировать этикетки товаров \n📋 Анализировать меню ресторана \n👨‍🍳 Подсказывать тебе рецепты \n\nЧтобы воспользоваться любой из этих функций, вызови меню. Для этого нажми на иконку с полосками в левой нижней части экрана и выбери пункт «Меню»."
    )
    await callback_query.message.answer(
        "А ещё мне важно знать, как тебе программа этих трех недель. С какой вероятностью от 1 до 10 ты порекомендуешь её друзьям?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="1", callback_data="1"),InlineKeyboardButton(text="2", callback_data="2"),InlineKeyboardButton(text="3", callback_data="3"),InlineKeyboardButton(text="4", callback_data="4"),InlineKeyboardButton(text="5", callback_data="5")],
                                                           [InlineKeyboardButton(text="6", callback_data="6"),InlineKeyboardButton(text="7", callback_data="7"),InlineKeyboardButton(text="8", callback_data="8"),InlineKeyboardButton(text="9", callback_data="9"),InlineKeyboardButton(text="10", callback_data="10")]])
    )

async def process_l20_step_2(callback_query, state):
    await state.set_state(LessonStates20.step_2)
    await callback_query.message.answer(
        "Спасибо за ответ! \n\nВ качестве благодарности у меня для тебя сюрприз: завтра тебя ждёт ещё один бонусный урок! 🎁 \n\nОн поможет продолжить твой путь к осознанному питанию и не откатиться к исходным результатам."
    )

    await callback_query.message.answer(
        "А сегодня не забывай про дневник питания! Курс закончился, но дневник по-прежнему важно заполнять каждый день.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
    )