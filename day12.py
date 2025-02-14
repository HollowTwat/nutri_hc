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

IMG1 = "AgACAgIAAxkBAAIFWmeqNpWACTNo_Icl7xPXMgABLPiH0gAC3PwxGzKfUUnc68oaV9w2vAEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAIFXmeqNqF2MMAZ-Fq5SW-e-m0FRWK7AALd_DEbMp9RSVbqgp_URwOVAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIFYmeqNqaieNZVknMEo6jNwNm9TifNAALe_DEbMp9RSf3CkZP80UNIAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIFZmeqNqrHgzkrwcho6l65iXnLbEF4AALf_DEbMp9RSdwie6ZzX2mFAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIFameqNq6_eHLGIUbAStrPXGzszkMUAALg_DEbMp9RSZKOb3hntt1aAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIFbmeqNrKSzF52ksbsAVtHo4-2H_DhAALi_DEbMp9RSQAB8xK-EX7EdwEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAIFcmeqNrYSvXXMi_3wlTB9_0DBjeIEAALj_DEbMp9RSSQSoA_DUKFPAQADAgADeQADNgQ"



async def process_l12_step_1(callback_query, state):
    await state.set_state(LessonStates12.step_2)
    await callback_query.message.answer(
        "Утро — время рефлексии! \n\n<i>«Нутри, я считаю КБЖУ, чувствую голод и насыщение и уже гораздо лучше управляю эмоциями! Этого хватит для осознанного питания?».</i> \n\nПодозреваю, что ты хочешь спросить у Нутри что-то такое. Понимаю! \n\nМы уже заложили отличную базу для осознанного питания — два кирпичика — работу с эмоциями и телом 👷 Но есть ещё третий, без которого всё развалится — образ жизни. \n\nНапример, без здорового сна сложно поддерживать желаемый вес. Почему? Разберёмся в сегодняшнем уроке!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l12_step_2(callback_query, state):
    await state.set_state(LessonStates12.step_3)
    link = "https://nafi.ru/analytics/rossiyskaya-ekonomika-teryaet-3-5-trln-rubley-v-god-iz-za-nevysypayushchikhsya-sotrudnikov/"
    link2 = "https://telegra.ph/Pochemu-bez-zdorovogo-sna-ne-poluchitsya-pohudet-istochniki-informacii-07-16"
    text = f"<b>Урок 5 \nПочему без здорового сна похудеть не получится</b> \n\nНемного грустной статистики:  48% россиян <a href=\'{link}\'>страдают от недосыпа</a>. Недостаток сна влияет плохо на питание, а неправильное питание,  в свою очередь, тоже влияет на качество сна. \n\nПолучается замкнутый круг. Но вместе мы сможем из него вырваться! Как? Читай в сегодняшнем уроке! \n\nИсточники — <a href=\'{link2}\'>по ссылке</a>."
    
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "✍️<b>Задание на день:</b> \n\n🍎Спланируй сегодня последний приём пищи не позже чем за 2 часа до сна. Ты сможешь! \n\n🍎Постарайся лечь в 23.00 (можно и чуть попозже, но отведи на сон 8 часов)."
    )
    text = "Но до этого домашнего задания ещё целый день! А в этом дне — несколько приёмов пищи 🍳🥗🥘 \n\nЗаноси их в дневник питания. \n\nМожно фотографировать тарелку, можно записывать голосовые, можно описывать съеденное текстом."
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")],
        ])
    )
    await callback_query.answer()

async def process_l12_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Надеюсь, ты просыпаешь урок про сон, чтобы поспать! 😉 Тогда я ставлю тебе «пять»: домашнее задание выполнено!   \n\nНо если ты собираешься работать допоздна или заниматься другими делами, решительно протестую! Постарайся лечь пораньше и не забывай про дневник питания.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
        )
    await callback_query.answer()

async def process_l12_step_11(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Обычно по вечерам я спрашиваю, удалось ли тебе сделать задание, но сегодня особый день. \n\nЕсли ты ещё не ужинал(а), то самое время сделать последний приём пищи и спланировать, во сколько ты ляжешь спать! \n\nЛожись пораньше, потому что завтра нас ждёт ещё один важный ингредиент, без которого осознанное питание пойдёт насмарку. Это спорт! 🏃",
        )
    await callback_query.answer()


