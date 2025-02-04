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

IMG1 = "AgACAgIAAxkBAANAZ6Izhb3-oRwlYaP2VqDUaNj2B40AAr3sMRundBFJUR0CTkcujnEBAAMCAAN5AAM2BA"
IMG2 = "AgACAgIAAxkBAANEZ6Izix5un3K9FJFIkhnYohD1ndoAAr7sMRundBFJIg8zZa_LlZ4BAAMCAAN5AAM2BA"

IMG3 = "AgACAgIAAxkBAAMWZ6EeHHZlQuvULWbsJ0pM73-eQGUAAuL2MRundAlJ1lkQgI65WD8BAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAAMaZ6EeInSKWO2MV5QgfFFTinbKz78AAuP2MRundAlJraM0a_v0fWoBAAMCAAN5AAM2BA"

IMG5 = "AgACAgIAAxkBAAMcZ6EeY6Cpo88iEVUuKp94QnS3IoMAAuj2MRundAlJCB5-3Qoyr9YBAAMCAAN5AAM2BA"



class LessonStates2(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()

async def process_l2_step_1(callback_query, state):
    await callback_query.answer("дошли до функции")
    await state.set_state(LessonStates2.step_2)
    media_files = [
        InputMediaPhoto(media=IMG1, caption=f"Доброе утро! \n\nКажется, распознавать сигналы тела легко:  хочешь есть — поешь, наелся — перестань. Но на деле всё сложнее. \n\nИногда мы пропускаем приёмы пищи и набрасываемся на еду из-за сильного голода. А иногда зачем-то едим, когда совершенно не хочется есть.</i>"),
        InputMediaPhoto(media=IMG2)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "<b>Девиз этой недели — научиться осознавать свои потребности, наладить контакт с телом и эмоциями.</b> \n\nА именно: \n\n🍏 слышать сигналы тела: правильно распознавать голод и насыщение \n🍏 начать замечать свои пищевые привычки \n🍏 разобраться с функциями Нутри и сделать их использование привычкой \n\nНу что, начнём урок?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Давай!", callback_data="next"), InlineKeyboardButton(text="Сегодня возьму выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l2_step_2(callback_query, state):
    await state.set_state(LessonStates2.step_3)
    text1 = "Первый секрет — настоящий голод не наступает внезапно. \n\nОн подкрадывается издалека и постепенно усиливается. На карточках — чек-лист с признаками голода. Они подскажут тебе, что пора поесть и откладывать дальше некуда."
    media_files = [
        InputMediaPhoto(media=IMG3, caption = text1),
        InputMediaPhoto(media=IMG4)
    ]
    await callback_query.message.answer(
        "<b>Урок 2</b> \n\n<b>Как понять, что пора поесть, и как — что пора остановиться</b> \n\nСегодня будем искать ответ на вопрос жизни, вселенной и всего такого: «Есть или не есть?». Говоря проще, будем весь день прислушиваться к себе и определять, когда чувствуем голод, а когда уже наелись."
    )
    await callback_query.message.answer_media_group(media=media_files)
    text2 = "Второй секрет — важно вовремя заметить не только голод, но и насыщение. Для этого ешь медленно и старайся оценить уровень сытости по 10-балльной шкале с картинки. В норме после еды должно оставаться ощущение комфорта, а вот тяжести быть не должно."
    await callback_query.message.answer_photo(photo=IMG5, caption=text2)
    await callback_query.message.answer(
        "✍️ <b>Задание на день</b> \n\n🍎 Заноси каждый приём пищи в дневник питания Нутри, а после оценивай уровень насыщения по шкале от 1 до 10. \n\nДля этого выбирай функцию «Дневник питания» в меню и рассказывай о съеденном в любой удобной форме: аудио, фото тарелки или описание съеденного. \n\nХорошего и вкусного дня!"
    )
    await callback_query.message.answer(
        "Расскажи о последнем съеденном блюде с помощью фото, текста или голосового сообщения. \n\n<i>Например, напиши в чат или продиктуй: «Курица с рисом и огурцами. 200 г курицы, 100 г риса, 1 огурец».</i>"
    )
    
    await callback_query.answer()


async def xyz(message,state):
    pass
