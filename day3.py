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

# IMG1 = "AgACAgIAAxkBAAIJXme1BNKaAAFyJqEkGpXO2pP3Og7c5QACX_UxG9jQqUl_7P6XmO6C1AEAAwIAA3kAAzYE"
# IMG2 = "AgACAgIAAxkBAAIJYme1BNa0wbhN5b5D8j21y2ezJkS9AAJg9TEb2NCpSVJuNJEoJuBSAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIJZme1BNqJdTfoPi59MPElfSVttHa1AAJh9TEb2NCpSe03yHwbDAQeAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIJame1BN7_RdevsGRG2_8rKlZi9WHcAALu8jEb41ioSSUOGi6jnhwLAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIJbme1BOIvZeRM4xgyF8nfhaWXFAjmAALv8jEb41ioSY0qEUIUC6HhAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIJcme1BOadleFr-Gk4v2RKT036VFsnAALw8jEb41ioSfCKEukq2fX8AQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIJdme1BOpUrjCIEKtYrq76oWLOY57zAAJj9TEb2NCpSTJuFpKcuGg8AQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIJeme1BO40a_lonDhSnXvFhE2LMyFyAAJk9TEb2NCpSZ46nzkkStjTAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIJfme1BPLEZVb_TtNPoqAvdbx__hsAA2X1MRvY0KlJao6Sbzlby-wBAAMCAAN5AAM2BA"
# IMG10 = "AgACAgIAAxkBAAIJgme1BPUEP_1Jef8GQdY3UqQKr9fmAALx8jEb41ioSYWw-1uc8spaAQADAgADeQADNgQ"

# IMG11 = "AgACAgIAAxkBAAIJhme1BWaVBsevREcf1GTv2YkDzf85AAJp9TEb2NCpSfZNFKBcc0XdAQADAgADeQADNgQ"
# IMG12 = "AgACAgIAAxkBAAIJime1BWq-5XMVuG5Pm6FVKYi7ku8HAAJq9TEb2NCpSVm2yQOS8vWzAQADAgADeQADNgQ"
# IMG13 = "AgACAgIAAxkBAAIJjme1BW5OMmoc8BnrJ_P4Y9Q1oyv7AAJr9TEb2NCpSXaRkvapPflcAQADAgADeQADNgQ"
# IMG14 = "AgACAgIAAxkBAAIJkme1BXPWQlZZJpzHpWxNC4JAm_FLAAJs9TEb2NCpSVhs4Ms7xVDoAQADAgADeQADNgQ"
# IMG15 = "AgACAgIAAxkBAAIJlme1BXfHzKXV9RXI5CmWO-24TQKSAAJt9TEb2NCpSdt4ko8Z_wzdAQADAgADeQADNgQ"
# IMG16 = "AgACAgIAAxkBAAIJmme1BXsCDR5Cr8qjlUjJt8q5Oy51AAJu9TEb2NCpSS2mNFAmJ6fpAQADAgADeQADNgQ"
# IMG17 = "AgACAgIAAxkBAAIJnme1BX8SCX4qsNNWui0brnfwJmy1AAJv9TEb2NCpSRcpWheH8WCIAQADAgADeQADNgQ"
# IMG18 = "AgACAgIAAxkBAAIJome1BYNBo6AjWiQNmtXLh3AEXNcHAAJw9TEb2NCpSUgCFFmX3tyPAQADAgADeQADNgQ"

# IMG19 = "AgACAgIAAxkBAAIJPme1A7I3Cz4-QSg4MAef4gF7wTg_AAJV9TEb2NCpSWJ-ytyPzx84AQADAgADeQADNgQ"
# IMG20 = "AgACAgIAAxkBAAIJQme1A7YQUU3KYueuUylKtwdO8HLhAAJX9TEb2NCpSSP2uE-Io5kRAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEW39n2eiqVySh0XUPIwhkiLqAgKXZjQACiPAxG2W90ErvMO95vKn79gEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEKgnJoNK2g0gWythY_coMffme1lvK-4QACj_YxG1FZoUmN4iw1PyafZgEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEKgnZoNK2nkh2Vdj1PKQABuoT4V2qQRdkAApD2MRtRWaFJOjDuIWTJvjEBAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAAEKgnpoNK25vuRCitzh5kAq6-s1WjCzMAACkvYxG1FZoUnMgpNWnPG6_AEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEKgn5oNK2_a9yTmZNVtr2-YgFxBuxQQwACk_YxG1FZoUnqftQXfbdYygEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEW45n2ejmLGwWe8_gwPuetgWmUug05gACjfAxG2W90EoAAePugdcEL-cBAAMCAAN5AAM2BA"
IMG7 = "AgACAgIAAxkBAAEEW5Jn2ek2ErkKFl2h-6zOIbFFJgg9WQACjvAxG2W90Er7aaQDtXWKBwEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEW5Vn2ek8Pi6g-uc9MDpRVGk6wGCbVAACj_AxG2W90EqY0I9Pp73UwgEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEW5hn2elIo33y1hboXWAfZenkdKAmRQACkPAxG2W90Erb0eds3iQCdgEAAwIAA3gAAzYE"
IMG10 = "AgACAgIAAxkBAAEEW5tn2elOtpOj3Es5amZ31nT8BERpTAACkfAxG2W90EowhjD_4KVjRQEAAwIAA3kAAzYE"

IMG11 = "AgACAgIAAxkBAAEEW6Nn2el1NB7ryRfRr4G8Ao1pWIzV8wACkvAxG2W90Ep8s7io3jGZvAEAAwIAA3kAAzYE"
IMG12 = "AgACAgIAAxkBAAEKgoRoNK4lOS_dI5VeqYn6YSn4XuKb8QAClvYxG1FZoUmQ_fWKmclEwwEAAwIAA3kAAzYE"
IMG13 = "AgACAgIAAxkBAAEKgohoNK4pjU6F2iDEqhH0M55S8m_79wACl_YxG1FZoUmOeBBimcFzOwEAAwIAA3kAAzYE"
IMG14 = "AgACAgIAAxkBAAEEW7Bn2emiaJ5dTK2hwkuSq0bsrAXGBQAClfAxG2W90ErEmizhKB7SHgEAAwIAA3kAAzYE"
IMG15 = "AgACAgIAAxkBAAEEW7Nn2emq9FfXvB5HYYJ-kbSzX2_IjAAClvAxG2W90EqXKzTE_uaXCwEAAwIAA3kAAzYE"
IMG16 = "AgACAgIAAxkBAAEKgoxoNK4uWlveHDgmxphsGTNqhIM8eAACmPYxG1FZoUnF-L9Xz2O-bQEAAwIAA3kAAzYE"
IMG17 = "AgACAgIAAxkBAAEEW7pn2em5PC2zrDbUHG3g4RBDUMi3XwACmPAxG2W90ErVQQ5ZrvPoZwEAAwIAA3kAAzYE"
IMG18 = "AgACAgIAAxkBAAEEW71n2enBpaDnYLahHofEpqqeFIpaUQACmfAxG2W90Erk1jhXs_F1WgEAAwIAA3kAAzYE"

IMG19 = "AgACAgIAAxkBAAEEW2dn2eaqopdb2mFkPqLfUOMQ_6-48wACf_AxG2W90ErW1ED5JlX88gEAAwIAA3kAAzYE"
IMG20 = "AgACAgIAAxkBAAEEW2pn2eazPJ5qWH_zdjzncYslmtovSwACgPAxG2W90Eo1ie5wz_UPVgEAAwIAA3kAAzYE"



from all_states import *


async def process_l3_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 2:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        await state.set_state(UserState.menu)
        return
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
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "3")
        asyncio.create_task(log_bot_response(f"lesson 3 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l3_step_5(callback_query, state):
    await state.set_state(LessonStates3.step_11)
    await callback_query.message.answer("Здорово, что получилось его определить! \n\nПостарайся назвать эмоцию, которую испытываешь. \n\nЭто не всегда просто, поэтому завтра у нас будет отдельный урок. Но давай попробуем! \n\nКак ещё можно прожить эту эмоцию, без еды? Может быть, стоит отвлечься на пятиминутную зарядку?")
    await callback_query.message.answer("Если ты всё-таки заел(а) тревогу или скуку, не вини себя! Эта эмоция не помогает. Завтра будем учиться работать с эмоциями, а пока занеси этот приём пищи в дневник питания.")
    await callback_query.answer()
    await process_l3_step_11(callback_query, state)

async def process_l3_step_5_2(callback_query, state):
    await state.set_state(LessonStates3.step_11)
    await callback_query.message.answer("Здорово, что получилось его определить! \n\nЕсли очень хочется попробовать новое, можно не спеша положить в рот кусочек, прожевать его и получить удовольствие. А потом сделать паузу подумать: надо ли мне ещё? И так после каждого кусочка. \n\nНе забудь занести этот приём пищи в дневник питания!")
    await callback_query.answer()
    await process_l3_step_11(callback_query, state)

async def process_l3_step_5_3(callback_query, state):
    await state.set_state(LessonStates3.step_11)
    await callback_query.message.answer("Значит, действительно пора поесть! \n\nНе забывай: делай это не спеша, чтобы вовремя почувствовать насыщение. Старайся оценить его уровень по 10-баллльной шкале. \n\nСытость на 6–7 баллов — то, к чему мы стремимся. \n\nИ обязательно заноси приём пищи в дневник питания.")
    await callback_query.answer()
    await process_l3_step_11(callback_query, state)

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