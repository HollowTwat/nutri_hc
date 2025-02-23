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

IMG1 = "AgACAgIAAxkBAAIJrme1BjKGwg971FVQMMOgAAHG5JwNJAACcvUxG9jQqUlWo56h38JeHAEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAIJsme1Bje5CgTlvggRIvWrF5HOSEujAAJz9TEb2NCpSbyIPTOKw2TKAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIJtme1BjtQm-2HramupvyuUwABvm4U4gACdPUxG9jQqUkb4V4paRrwQQEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAIJume1Bj8c9mo7uG0f3oIe-kYD-K12AAJ19TEb2NCpSfNZCS5fNniSAQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIJvme1BkIk1p81MLyTpSgBYsXXb4ekAAJ29TEb2NCpSV8mlfiFg0IJAQADAgADeQADNgQ"

IMG6 = "AgACAgIAAxkBAAIJwme1Bkwhmlc5A7JA_KdggvjNhRNsAAJ39TEb2NCpScRtwpijgFsxAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIJxme1BlAItqPdrDQQQ0ZydSkgIC7WAAJ49TEb2NCpSS-q-iS3-UKbAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIJyme1BlR2TV1KwCtDKNq_paR__9HLAAJ59TEb2NCpSWhA24blzTIzAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIJzme1BloT4qE1c9nSRgesJrDOGG-sAAJ69TEb2NCpSd6dwpt6TPzPAQADAgADeQADNgQ"
IMG10 = "AgACAgIAAxkBAAIJ0me1Bl4m60W-VEM8QH9w0QuadKUzAAJ79TEb2NCpSX7tJ-3wqgOAAQADAgADeQADNgQ"
IMG11 = "AgACAgIAAxkBAAIJ1me1BmJVfDW_bW2o9Pa86qKzjRj4AAL28jEb41ioSUSxDlzAz00iAQADAgADeQADNgQ"
IMG12 = "AgACAgIAAxkBAAIJ2me1BmZ_FDJ5s4GBfzrhNkWkeCcHAAJ89TEb2NCpScb1ad-ghrZHAQADAgADeQADNgQ"

# IMG1 = "AgACAgIAAxkBAAICs2ej7ZIRMmrZjPetwbvYi65V8e-nAAL_6DEbvHgYSTSQmgYmPApzAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAICt2ej7Zj8p-KANkKapL0fgcYz-cdiAAPpMRu8eBhJthG4lfssmzwBAAMCAAN5AAM2BA"
# IMG3 = "AgACAgIAAxkBAAICu2ej7Z3lv2EZWBYCLVegdFeP_DagAAIB6TEbvHgYSc1zcPUK4PT1AQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAICv2ej7aLH9OXsdxGeh43leIC1CVknAAIC6TEbvHgYSQ0YO5xl_o9RAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAICw2ej7av7jBVj4zeIm6W6L0Mj-e4LAAID6TEbvHgYSWuw9R9XCD0tAQADAgADeQADNgQ"

# IMG6 = "AgACAgIAAxkBAAICx2ej8iciNk4UugAB10Pz1jb75nND1AACB-kxG7x4GEksJkx8YxsjbwEAAwIAA3kAAzYE"
# IMG7 = "AgACAgIAAxkBAAICy2ej8iy5q5SXXfaS5Lfj5zpd8ZruAAII6TEbvHgYSbCzfLAnDr7EAQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAICz2ej8jD3aHWpk1B9RMQgMmcoNP74AAIJ6TEbvHgYSUSaYpjEKftbAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIC02ej8jXjeIHNOqTHNOTlvPgwwZBNAAIK6TEbvHgYSZ6v7Mc1YWOnAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAIC12ej8j2C38zWb727w0IvJb6iGVRlAAIL6TEbvHgYSQkJRKapjEpbAQADAgADeQADNgQ"
# IMG11 = "AgACAgIAAxkBAAIC22ej8kN5GsmP4mueiPm438wzd-_1AAIM6TEbvHgYSQABdlyJtu-HQgEAAwIAA3kAAzYE"
# IMG12 = "AgACAgIAAxkBAAIC32ej8kc2dKkWLomvF6AnFg6m-AweAAIN6TEbvHgYSYkyavsC-YUfAQADAgADeQADNgQ"

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