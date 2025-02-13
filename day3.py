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

IMG1 = "AgACAgIAAxkBAAIBtGejgPZ9kYJqt7Dv9CUIRGEnNJzaAAJX5jEbvHgYSeZUS6-m9-ooAQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIBuGejgPwBj9RasqeLltCI1YxaQbn8AAJY5jEbvHgYSTykeXacbIEjAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIBvGejgQF5DSvk23CCGYtULNn_txN3AAJZ5jEbvHgYSQAB3JAZ0g0yiAEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAIBwGejgQdXiNy4lYaXTwhBkX9tmi4GAAJa5jEbvHgYScVLk2oUmCwKAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIBxGejgRKrCksTxH0SV0yK-osUez3ZAAJb5jEbvHgYSa5ckjn_I_LZAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIByGejgRgQIbk5UHZDlZ44NO2Dqq0VAAJd5jEbvHgYSXjg2nlFXbO5AQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIBzGejgR9YP59KTqzQtMLW8oipOCLdAAJf5jEbvHgYSWA6B0s6O-OJAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIB0GejgSc9VTz-uLkk3LfgHsBMpcKxAAJg5jEbvHgYSdS75CHvKdQuAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIB1GejgS1QE5Ym2gABBIp1LW16RNw-sQACYeYxG7x4GEnpEukVH0FsrAEAAwIAA3kAAzYE"
IMG10 = "AgACAgIAAxkBAAIB2GejgTMLnkurx3G2sn5qdMX_H3OsAAJi5jEbvHgYScsJrUjUnYPGAQADAgADeQADNgQ"

IMG11 = "AgACAgIAAxkBAAIB3Gej1xJcP8kbd6APU-JLdi2swGFUAAK56DEbvHgYScWMPhn5afDkAQADAgADeQADNgQ"
IMG12 = "AgACAgIAAxkBAAIB4Gej1xgvMcpDJa10xCZR6maSElxvAAIq6jEb12UgSToAAd4AAcz6SQ4BAAMCAAN5AAM2BA"
IMG13 = "AgACAgIAAxkBAAIB5Gej1x5jB_9bkGpx0ROxEqiP1oaeAAK66DEbvHgYSajILPcL32KvAQADAgADeQADNgQ"
IMG14 = "AgACAgIAAxkBAAIB6Gej1yQAATWOExQJZ6LpQG60XRUq0wACK-oxG9dlIEnSpxK1AiFNSAEAAwIAA3kAAzYE"
IMG15 = "AgACAgIAAxkBAAIB7Gej1yooC9hUTceTs_MiOU7tgoSZAAK76DEbvHgYSUBlYugqvg7BAQADAgADeQADNgQ"
IMG16 = "AgACAgIAAxkBAAIB8Gej1zDvqw7QuQwp7n4fPF56Lv0xAAK86DEbvHgYScpMWfGCFLfgAQADAgADeQADNgQ"
IMG17 = "AgACAgIAAxkBAAIB9Gej1zY3a8Z7xip1ayWMXmDmk-MSAAK96DEbvHgYSUFGlyTS2hZRAQADAgADeQADNgQ"
IMG18 = "AgACAgIAAxkBAAIB-Gej1zv0VBKCEoIp_AV8ZpMwrGdcAAK-6DEbvHgYSdZ_M9cr42pFAQADAgADeQADNgQ"

IMG19 = "AgACAgIAAxkBAAIB_Gej20bspZB55PIkWhQ_VRUloWzwAALQ6DEbvHgYSSgWPSVII5rcAQADAgADeQADNgQ"
IMG20 = "AgACAgIAAxkBAAICAAFno9tNHqBoD6gPsX19BRK-fM3uKQAC0egxG7x4GElJz7snEJs-lwEAAwIAA3kAAzYE"



from all_states import *


async def process_l3_step_1(callback_query, state):
    await state.set_state(LessonStates3.step_2)
    await callback_query.message.answer(
        "Доброе утро! \n\nЯ уже проснулась и чертовски голодна! А ты? Как дела с определением голода? Если возникли сложности — это нормально! \n\nО том, как распознать истинный голод, поговорим в сегодняшнем уроке. Начнём учиться?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l3_step_2(callback_query, state):
    await state.set_state(LessonStates3.step_3)
    media_files = [
        InputMediaPhoto(media=IMG1),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
        InputMediaPhoto(media=IMG10)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    link1 = "https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/weight-loss/art-20047342"
    link2 = "https://pubmed.ncbi.nlm.nih.gov/29476800/"
    link3 = "https://pubmed.ncbi.nlm.nih.gov/32213213/"
    link4 = "https://pubmed.ncbi.nlm.nih.gov/32195512/"
    text = f"<b>Урок 3</b> \n<b>С чем можно перепутать голод</b> \n\nИногда то, что мы принимаем за голод, бывает жаждой новых вкусов, новых эмоций и впечатлений. Всё это — разные типы голода! \n\nНа карточках вместе с нутрициологом рассказываем, какими бывают типы голода и как их различать. \n\nИсточники: \n🍏<i><a href=\'{link1}\'>Weight loss: Gain control of emotional eating</a> — Mayo Clinic</i> \n🍏<i><a href=\'{link2}\'>Emotion regulation difficulties interact with negative, not positive, emotional eating to strengthen relationships with disordered eating: An exploratory study</a> — Appetite</i> \n🍏<i><a href=\'{link3}\'>Emotional eating and obesity in adults: the role of depression, sleep and genes</a> — Proceedings of the Nutrition Society</i> \n🍏<i><a href=\'{link4}\'>The effect of taste and taste perception on satiation/satiety: a review</a> — ​​Food & Function</i>"
    await callback_query.message.answer(text, disable_web_page_preview=True,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Можно ли перепутать голод и жажду?", callback_data="next")]
        ])
    )
    
    await callback_query.answer()

async def process_l3_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Нутри уважает право на отдых! Сегодня не учимся, но вот  дневник питания лучше заполнять даже в выходной. \n\nНажимай на кнопку после приёма пищи, чтобы проанализировать свой завтрак, обед или ужин. \n\nЕсли хочешь посоветоваться с Нутри перед едой, сфотографируй тарелку или пришли её описания текстом или голосовым сообщением.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()
    
async def process_l3_step_3(callback_query, state):
    await state.set_state(LessonStates3.step_4)
    media_files = [
        InputMediaPhoto(media=IMG11),
        InputMediaPhoto(media=IMG12),
        InputMediaPhoto(media=IMG13),
        InputMediaPhoto(media=IMG14),
        InputMediaPhoto(media=IMG15),
        InputMediaPhoto(media=IMG16),
        InputMediaPhoto(media=IMG17),
        InputMediaPhoto(media=IMG18)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    link1 = "https://telegra.ph/6-nelovkih-voprosov-o-vode-i-drugih-napitkah-istochniki-informacii-07-16"
    text = f"<b>Когда хочется не есть, а пить</b> \nЗвучит странно, но часто мы едим, когда на самом деле хотим пить. Почему так происходит? Как отличить голод и жажду? И правда ли нам нужно выпивать 2 литра воды в день? (спойлер: нет). Ищи в карточках ответы на самые распространённые вопросы о воде и других напитках! \n\nИсточники информации — <a href=\'{link1}\'>по ссылке</a>."
    await callback_query.message.answer(text, disable_web_page_preview=True)
    await callback_query.message.answer(
        "✍️<b>Задания на день:</b> \n\n🍎 Выпей стакан воды прямо сейчас, не откладывай. \n\n🍎 Перед первым приёмом пищи сегодня нажми кнопку «Хочу поесть» и выбери, какой тип голода испытываешь. \n\n🍎Заноси все приёмы пищи в дневник питания — так Нутри поможет заметить вкусовой или эмоциональный голод.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хочу поесть", callback_data="next")]
        ])
    )
    
    await callback_query.answer()

async def process_l3_step_4(callback_query, state):
    await state.set_state(LessonStates3.step_5)
    media_files = [
        InputMediaPhoto(media=IMG19),
        InputMediaPhoto(media=IMG20)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "Прекрасно тебя пониманию! Я испытывают голод всегда: это голод по общению! \n\nА какой тип голода испытываешь ты? \n\nСравни свои ощущения с признаками физиологического голода с картинки и выбери один из вариантов:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Эмоциональный", callback_data="1"),InlineKeyboardButton(text="Вкусовой", callback_data="2"),InlineKeyboardButton(text="Физиологический", callback_data="3")]
        ])
    )
    
    await callback_query.answer()

async def process_l3_step_5(callback_query, state):
    await state.set_state(LessonStates3.step_6)
    await callback_query.message.answer("Здорово, что получилось его определить! \n\nПостарайся назвать эмоцию, которую испытываешь. \n\nЭто не всегда просто, поэтому завтра у нас будет отдельный урок. Но давай попробуем! \n\nКак ещё можно прожить эту эмоцию, без еды? Может быть, стоит отвлечься на пятиминутную зарядку?")
    await callback_query.message.answer("Если ты всё-таки заел(а) тревогу или скуку, не вини себя! Эта эмоция не помогает. Завтра будем учиться работать с эмоциями, а пока занеси этот приём пищи в дневник питания.", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l3_step_5_2(callback_query, state):
    await state.set_state(LessonStates3.step_6)
    await callback_query.message.answer("Здорово, что получилось его определить! \n\nЕсли очень хочется попробовать новое, можно не спеша положить в рот кусочек, прожевать его и получить удовольствие. А потом сделать паузу подумать: надо ли мне ещё? И так после каждого кусочка. \n\nНе забудь занести этот приём пищи в дневник питания!", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l3_step_5_3(callback_query, state):
    await state.set_state(LessonStates3.step_6)
    await callback_query.message.answer("Значит, действительно пора поесть! \n\nНе забывай: делай это не спеша, чтобы вовремя почувствовать насыщение. Старайся оценить его уровень по 10-баллльной шкале. \n\nСытость на 6–7 баллов — то, к чему мы стремимся. \n\nИ обязательно заноси приём пищи в дневник питания.", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

    ############ EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING #############

async def process_l3_step_11(callback_query, state):
    await callback_query.message.answer("Берём контроль над чувством голода и эмоциями и приближаемся к осознанному питанию уже три дня. Это очень круто, поздравляю 💪 \n\nКак дела с заданием сегодняшнего дня: получилось определять, какой тип голода испытываешь?", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да!", callback_data="1"),InlineKeyboardButton(text="Нет, давай подумаем об этом сейчас", callback_data="2")]]))
    await callback_query.answer()

async def process_l3_step_12(callback_query, state):
    await callback_query.message.answer("Очень рада, что ты делаешь задания! (Главное, не пойти сейчас на радостях и не съесть что-нибудь). \n\nЗавтра будем разбираться, что делать, если эмоции слишком сильные и контролировать их сложно. \n\nА пока хорошего тебе вечера, отдыхай ❤️")
    await callback_query.answer()

async def process_l3_step_12_2(callback_query, state):
    await state.set_state(LessonStates3.step_12)
    await callback_query.message.answer("Вспомни последний приём пищи. В каких обстоятельствах ты решил(а) поесть и что чувствовала? Какой это был голод?", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Эмоциональный", callback_data="1"),InlineKeyboardButton(text="Вкусовой", callback_data="2"),InlineKeyboardButton(text="Физиологический", callback_data="3")]]))
    await callback_query.answer()

async def process_l3_step_13(callback_query, state):
    await state.set_state(LessonStates3.step_13)
    await callback_query.message.answer("Здорово, что получилось его определить! \n\nНе вини себя! Эта эмоция не помогает осознанному питанию. \n\nЗавтра будем учиться работать с эмоциями, а пока занеси этот приём пищи в дневник питания.", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📖  Дневник питания", callback_data="menu_dnevnik")]]))
    await callback_query.answer()

async def process_l3_step_13_2(callback_query, state):
    await state.set_state(LessonStates3.step_13)
    await callback_query.message.answer("Здорово, что удалось его определить! \n\nНадеюсь, у тебя получилось не переесть. А если не получилось, то не вини себя, ведь мы только учимся! \n\nЕсли в следующий раз хочется попробовать новое, можно не спеша положить в рот кусочек, прожевать его и получить удовольствие. А потом сделать паузу подумать: надо ли мне ещё? И так после каждого кусочка. \n\nНе забудь занести этот приём пищи в дневник питания!", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📖  Дневник питания", callback_data="menu_dnevnik")]]))
    await callback_query.answer()

async def process_l3_step_13_3(callback_query, state):
    await state.set_state(LessonStates3.step_13)
    await callback_query.message.answer("Отлично! \nНе забывай оценивать уровень насыщения по 10-баллльной шкале. \n\nСытость на 6–7 баллов — то, к чему мы стремимся. \n\nИ обязательно занеси этот приём пищи в дневник питания.", 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📖  Дневник питания", callback_data="menu_dnevnik")]]))
    await callback_query.answer()