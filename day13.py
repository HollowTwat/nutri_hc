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

IMG1 = "AgACAgIAAxkBAAIFj2eqPsZVhAHk7bv_lao1GBkg0l5lAAIK6zEbtfVQSa4jK804YRo2AQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIFk2eqPstfB9UgcNfiSUnlmTOuaScTAAJ3_TEbMp9RSb2eBuJnHJQcAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIFl2eqPtC9ONDgMph3G93xPo1frA7IAAJ4_TEbMp9RSRdSBl09DQ8nAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIFm2eqPtSDifQTEdwWXtfrhfa7f1AGAAJ5_TEbMp9RSZutfQ_t1ChIAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIFn2eqPtjOsqnKaQNlZlZsXxkyAiPWAAJ6_TEbMp9RSWYamNyTK4iOAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIFo2eqPtz8avVqLF5iB1jLmILQUMtVAAJ9_TEbMp9RSfOEwk25vNTjAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIFp2eqPuGJUlNiHBglq5jtQoPJZ_KUAAJ-_TEbMp9RSfgFoffBVYcrAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIFq2eqPuWKBxHBTFlxIxPHfSORlIZbAAJ__TEbMp9RSU5K8EZVSgH_AQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIFr2eqPuqwRvG32m1mV115LWqd9qtqAAKA_TEbMp9RSU3sHpxXXg82AQADAgADeQADNgQ"



async def process_l13_step_1(callback_query, state):
    await state.set_state(LessonStates13.step_2)
    await callback_query.message.answer(
        "Доброе утро! \nПоспали, теперь можно и… позаниматься спортом! \n\nСпорт и сон — два наших помощника на пути к осознанному питанию и здоровому телу. Спорт может быть разным, но вот совсем без него не получится 🤷‍♀️ Точно так же, как не получится заниматься спортом и не следить за питанием. Почему? \n\nВыясним в сегодняшнем уроке!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Сегодня без спорта", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l13_step_2(callback_query, state):
    await state.set_state(LessonStates13.step_3)
    link = "https://telegra.ph/Mozhno-li-pohudet-ne-zanimayas-sportom-istochniki-07-16"
    link2 = "https://www.youtube.com/watch?v=M-8FvC3GD8c&ab_channel=YogaWithAdriene"
    text = f"<b>Урок 6 \nМожно ли похудеть, не занимаясь спортом</b> \n\nНеприятная правда: похудеть без можно и без спорта, но получить тело мечты — вряд ли. Почему, читайте в сегодняшнем уроке. \n\nА я убежала на свою утреннюю йогу. Всем собака мордой вниз! \n\nИсточники, по которым мы написали урок — <a href=\'{link}\'>по ссылке.</a>"
    text2= f"✍️<b>Задание на день (которое лучше не откладывать):</b> \n\n🧘Уделить хотя бы 15 минут любому занятию спортом. Вот, например, <a href=\'{link2}\'>15 минут йоги, которую можно сделать в обеденный перерыв</a> (даже на рабочем месте!). \n\nА ещё лучше — позаниматься прямо сейчас. Можно прямо перед завтраком. И не забудь занести завтрак в дневник питания."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(text2,disable_web_page_preview=True,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Сделать зарядку", url = "https://www.youtube.com/watch?v=M-8FvC3GD8c&ab_channel=YogaWithAdriene")],[InlineKeyboardButton(text="Дневник питания", callback_data="dnevnik")],
        ])
    )
    await callback_query.answer()

async def process_l13_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Жаль(   \n\nЯ надеялась, мы сделаем вместе зарядку или сходим на вечернюю пробежку. Предлагаю не откладывать этот план в долгий ящик и позаниматься вместе спортом завтра!   \n\nА сегодня не забывай заполнять дневник питания 📖",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l13_step_11(callback_query, state):
    await callback_query.message.answer(
        "Прислушайся к ощущениям! \n\nКак чувствует себя твоё тело в конце дня? Может быть, зажаты плечи или болит поясница? Может быть, чувствуется усталость? Или, наоборот, всё классно? \n\nКакие бы ощущения ни были внутри, вечерняя разминка поможет почувствовать себя лучше и более качественно спать. Сделаем её вместе?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Спорт сегодня уже был!", callback_data="next")], [InlineKeyboardButton(text="Сделать разминку", url = "https://www.youtube.com/watch?v=v7SN-d4qXx0&ab_channel=YogaWithAdriene", callback_data="stop")]
        ])
        )
    await callback_query.answer()

async def process_l13_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Это здорово! \n\nТогда хорошего вечера тебе. Завтра будем подводить итоги второго этапа с Нутри, а пока желаю тебе хорошо выспаться ❤️"
        )

async def process_l13_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Приятная лёгкая разминка — отличное завершение второго этапа учёбы с Нутри. \n\nЗавтра будем подводить итоги, а пока желаю тебе хорошо выспаться ❤️"
        )

