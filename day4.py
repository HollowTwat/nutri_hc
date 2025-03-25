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

# IMG1 = "AgACAgIAAxkBAAIJrme1BjKGwg971FVQMMOgAAHG5JwNJAACcvUxG9jQqUlWo56h38JeHAEAAwIAA3kAAzYE"
# IMG2 = "AgACAgIAAxkBAAIJsme1Bje5CgTlvggRIvWrF5HOSEujAAJz9TEb2NCpSbyIPTOKw2TKAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIJtme1BjtQm-2HramupvyuUwABvm4U4gACdPUxG9jQqUkb4V4paRrwQQEAAwIAA3kAAzYE"
# IMG4 = "AgACAgIAAxkBAAIJume1Bj8c9mo7uG0f3oIe-kYD-K12AAJ19TEb2NCpSfNZCS5fNniSAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIJvme1BkIk1p81MLyTpSgBYsXXb4ekAAJ29TEb2NCpSV8mlfiFg0IJAQADAgADeQADNgQ"

# IMG6 = "AgACAgIAAxkBAAIJwme1Bkwhmlc5A7JA_KdggvjNhRNsAAJ39TEb2NCpScRtwpijgFsxAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIJxme1BlAItqPdrDQQQ0ZydSkgIC7WAAJ49TEb2NCpSS-q-iS3-UKbAQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIJyme1BlR2TV1KwCtDKNq_paR__9HLAAJ59TEb2NCpSWhA24blzTIzAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIJzme1BloT4qE1c9nSRgesJrDOGG-sAAJ69TEb2NCpSd6dwpt6TPzPAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAIJ0me1Bl4m60W-VEM8QH9w0QuadKUzAAJ79TEb2NCpSX7tJ-3wqgOAAQADAgADeQADNgQ"
# IMG11 = "AgACAgIAAxkBAAIJ1me1BmJVfDW_bW2o9Pa86qKzjRj4AAL28jEb41ioSUSxDlzAz00iAQADAgADeQADNgQ"
# IMG12 = "AgACAgIAAxkBAAIJ2me1BmZ_FDJ5s4GBfzrhNkWkeCcHAAJ89TEb2NCpScb1ad-ghrZHAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEW-Jn2ewj4JCSJDuHPSbFQOuu_iA4TAACm_AxG2W90Epjw3N7nsTeUwEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEW-Vn2ewrmlmkXRpm2yZ_pBiQYsK1HQACnPAxG2W90Ep55tCqjDPURQEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEEW-hn2ewy_vmH-jYv9d1s40R0Sn-HPgACnfAxG2W90EpAg9iAb6D3EwEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEW-xn2exGaYTaZ3fLfGL9g35gbE2JKAACnvAxG2W90Eqm_bOHGxSVKQEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEEW_Bn2exMXhRldv5KHywPBk7G8KOevAACn_AxG2W90Eqgf_ikpHRcAgEAAwIAA3kAAzYE"

IMG6 = "AgACAgIAAxkBAAEEW_Nn2exXwNnTAdrvnAa_WTXbf6xG-gACoPAxG2W90EpnP07xqzuGcAEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEW_Zn2exeNlwV0rlRBA3Kkn7Gdqxq1wACofAxG2W90EoH6BGPSr94lQEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEW_ln2exlDLvjlp_zLFjaIOgGdOASxwACovAxG2W90ErzkyiPCkkoZwEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEW_xn2exrqzQxUfKvYPfduZjTeLYW2QACo_AxG2W90EpqasEGTjxGbgEAAwIAA3kAAzYE"
IMG10 = "AgACAgIAAxkBAAEEXAABZ9nsfK0gsIp9tEt7psnhvzxTy14AAqTwMRtlvdBKRISAjs7DSxMBAAMCAAN5AAM2BA"
IMG11 = "AgACAgIAAxkBAAEEXARn2eyE8MzrxoNXg-umSf4jIKYRqAACpfAxG2W90EpTEvXw9j9_jwEAAwIAA3kAAzYE"
IMG12 = "AgACAgIAAxkBAAEEXAdn2eyMMOWlP98fkQTWyot4DkUHlAACpvAxG2W90EriQBtDB-7rlwEAAwIAA3kAAzYE"

from all_states import *

async def process_l4_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 3:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates4.step_2)
    await callback_query.message.answer(
        "Привет, на связи Нутри! \n\nНемного завидую людям, которые встают с постели в настроении «проснулась-улыбнулась». Мне по утрам не до улыбок — в себя бы прийти! Чувствую раздражение на весь мир — и рука на автомате тянется к еде. \n\nК счастью, я научилась с этим справляться и готова передать знания тебе. Поучимся?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Поучимся!", callback_data="next"), InlineKeyboardButton(text="Не сегодня", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l4_step_2(callback_query, state):
    await state.set_state(LessonStates4.step_3)
    media_files = [
        InputMediaPhoto(media=IMG1),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    text = "<b>Урок 4 \nКак перестать заедать эмоции</b> \n\nЧасто с помощью еды мы заглушаем эмоции и чувства, с которыми трудно справиться: гнев, страх, грусть, тревогу, вину, скуку или одиночество. Поэтому научиться распознавать их и управлять ими — первый шаг к осознанному питанию. \n\nДля начала научимся определять, что мы чувствуем. Ведь с виной нужно работать одним образом, а с грустью — другим. При этом различить их часто не так просто, как кажется. \n\nВ определении эмоций поможет колесо, которое разработал американский психолог Роберт Плутчик. Читай гайд по эмоциям в карточках и определяй, какую эмоцию испытываешь прямо сейчас. \n\n<b>Источник:</b> \n🍏<i>The Nature of Emotions (Plutchik, 2001)</i>"
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="А что делать с этими эмоциями?", callback_data="next")]
        ])
    )
    
    await callback_query.answer()

async def process_l4_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Вовремя отдохнуть — тоже хороший способ регулировать эмоции! И это тоже помогает не заедать эмоции. \n\nТак что отдохни хорошенько, только не забывай про дневник питания!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l4_step_3(callback_query, state):
    await state.clear()
    text = "Есть много способов с ними работать! \n\nВ карточках — несколько практик, которые помогают справиться с эмоциями, которые мы «заедаем» чаще всего. \n\nНа самом деле таких практик больше, а полностью изменить поведение и реакции поможет когнитивно-поведенческая терапия. Но ведь надо с чего-то начать!"
    media_files = [
        InputMediaPhoto(media=IMG6, caption=text),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
        InputMediaPhoto(media=IMG10),
        InputMediaPhoto(media=IMG11),
        InputMediaPhoto(media=IMG12)
    ]
    
    await callback_query.message.answer_media_group(media=media_files)
    text1 = "✍️<b>Задание на день:</b> \n\n🍎 Выполни одну из практик. \n🍎Не забывай заполнять дневник питания — он тоже помогает отследить, как эмоции влияют на желание поесть."
    await callback_query.message.answer(text1,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📖  Дневник питания", callback_data="menu_dnevnik")]
        ])
    )
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "4")
        asyncio.create_task(log_bot_response(f"lesson 4 saved status{issuccess} "), callback_query.from_user.id)
    except Exception as e:
        print(e)

############ EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING #############

async def process_l4_step_11(callback_query, state):
    await state.set_state(LessonStates4.step_12)
    await callback_query.message.answer(
        "Что-то я сегодня весь день за тебя тревожилась: как ты там справляешься с эмоциональным голодом? \n\nДыхательные практики для работы с тревогой я делать не могу, поэтому просто представляла себя камнем. Помогло! \n\nА тебе удалось сделать сегодня одну из практик?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="next"), InlineKeyboardButton(text="Сегодня без негатива", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l4_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer("Очень рада! \nНадеюсь, она помогла тебе и теперь войдёт в список регулярных психологических практик.")
    await callback_query.message.answer("Кажется, мы уже рассмотрели наше пищевое поведение со всех сторон: \n🙂Начали лучше оценивать уровень голода и насыщения. \n🙃 Разобрались в типах голода. \n😀 Учимся не заедать эмоции. \n\nНо есть нюанс. Этот нюанс — привычки. Иногда нас ничего не тревожит, но мы всё равно питаемся неправильно. Просто потому что так привыкли. \n\nЗавтра посвятим день тому, чтобы отследить привычки, которые мешают осознанному питанию. \n\nА пока отдохнём и хорошенько выспимся! До завтра!")
    await callback_query.answer()

async def process_l4_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer("Если нет неприятных эмоций, которые хочется заесть, это тоже хорошо! Я рада. Но на случай эмоционального шторма сохрани себе карточки с практиками от Нутри, чтобы они всегда были под рукой.")
    await callback_query.message.answer("Кажется, мы уже рассмотрели наше пищевое поведение со всех сторон: \n🙂Начали лучше оценивать уровень голода и насыщения. \n🙃 Разобрались в типах голода. \n😀 Учимся не заедать эмоции. \n\nНо есть нюанс. Этот нюанс — привычки. Иногда нас ничего не тревожит, но мы всё равно питаемся неправильно. Просто потому что так привыкли. \n\nЗавтра посвятим день тому, чтобы отследить привычки, которые мешают осознанному питанию. \n\nА пока отдохнём и хорошенько выспимся! До завтра!")
    await callback_query.answer()