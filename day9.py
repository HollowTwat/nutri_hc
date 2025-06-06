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

# IMG1 = "AgACAgIAAxkBAAIKRme1CPrk8NhVHu9S2MsHWSd-XTCVAAKm9TEb2NCpSSre-XU1tbZ6AQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIKSme1CP5edoHrp8ie0NdjQkzPEbkSAAKn9TEb2NCpST8I6vftwIRwAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIKTme1CQLOjbO_crE0pra5pdyt_cI3AAKo9TEb2NCpSXlfTancXwR2AQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIKUme1CQWydI9IoBv-Si8ulZaag0g8AAKp9TEb2NCpSWDCPQuFeieXAQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIKVme1CQmy2Ixg1mVpa4XX_7hzH03bAAKq9TEb2NCpSZs9uFgakECLAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIKWme1CQ3WLJqe0FbeXHbzM4xB6DIFAAKr9TEb2NCpSd5eDSDCQ9BmAQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIKXme1CRHv9cS0fqDUtxvgN2GHv2HVAAKs9TEb2NCpSSQmv1GPnaM_AQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIKYme1CRRdGcJD03R19ewFPE52gxVQAAKt9TEb2NCpSVu6xhlE66gKAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEYkxn2mN3nFJvKkmJCuEdUBS80UsMIAACYvAxG1ap0UqaO6oNh2NpUwEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEYk9n2mOCi79cG6THQH5y07iJed6Q7gACY_AxG1ap0UqDO9XeGxFObwEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEEYldn2mOJ-gxz3ebzS2udvUVnNGv0pAACZvAxG1ap0Ur4-yPyKbaCkAEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEYlxn2mORL9gLeY1GjC3ylQ6EfBc5zwACZ_AxG1ap0Ur2NHlXrj4BLwEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEKgtxoNLAxy1b2VfMPP3Hs52aSH7_4mAACr_YxG1FZoUlqbOpTq7CR8QEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEYn9n2mPQuuL-EdECY40SrEoFcb2tZwACavAxG1ap0Ups_QH61fdd9QEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEKzMJoNwq9bZPsFpcnxqFlrECm6OnCZgACivExG8vfwEmCzbsR3W9C7wEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEKguFoNLA4N9N_s5jnuU9zdh35emBFvQACsPYxG1FZoUkMGTnamFL32QEAAwIAA3kAAzYE"



async def process_l9_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 8:
        await callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        await state.set_state(UserState.menu)
        return
    await state.set_state(LessonStates9.step_2)
    await callback_query.message.answer(
        "Доброе утро! \n\nВпереди нас точно ждёт ситуация: вроде гарвардскую тарелку составили, а в КБЖУ всё равно не вписались! \n\nКак так? Возможно, дело в коварных продуктах, который незаметно съедают калории! В сегодняшних карточках делюсь секретами, чем их заменить так, чтобы не страдать.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l9_step_2(callback_query, state):
    await state.set_state(LessonStates9.step_3)
    text = "<b>Урок 2 \nЧем заменить любимые продукты</b> \n\nКак говорится, почувствуйте разницу: \n☕ Чашка чёрного кофе без сахара — 0–5 ккал \n☕🥛Чашка капуччино — 100–200 ккал \n\nНапитки, соусы и переработанные продукты — источники калорий, которые быстро усваиваются, плохо насыщают и крадут дневную норму калорий. \n\nНо что делать, если потреблять такие калории — привычка? Искать замену привычным продуктам! В сегодняшних карточках предлагаем альтернативные варианты привычных напитков, заправок и блюд."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    text = "«Нутри, а почему ты предлагаешь заменить шоколад зефиркой, а не купить, например, шоколад с сахарозаменителем?», — спрашиваете вы (очень надеюсь, что спрашиваете!). \n\nПотому что в сахарозаменителях надо знать толк! И мы с нутрициологом посвятили им отдельный текст. Читайте по ссылкам всю правду про стевию, изомальт и прочие модные штучки."
    await callback_query.message.answer(text,reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Читать текст", url="https://telegra.ph/CHem-zamenit-sahar-i-stoit-li-voobshche-iskat-zamenu-08-09")],
        ])
    )

    await asyncio.sleep(5)

    await callback_query.message.answer(
        "✍️Задание на день: \n\n🍎 Спросить у Нутри, как снизить калорийность блюда, которое собираешься съесть сегодня. Для этого нажми кнопку «Задать вопрос» и напиши его в свободной форме. \n\n<i>Например: «Как снизить калорийность салата Оливье»?</i> \n\n🍎Не забывай заполнять дневник питания. Ты уже наверняка заметил(а), что я анализирую, насколько полезны твои приёмы пищи, и предлагаю скорректировать рацион.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Задать вопрос", callback_data="menu_nutri_yapp"),InlineKeyboardButton(text="Дневник питания", callback_data="menu_dnevnik")]
        ])
    )

    await callback_query.answer()
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "9")
        asyncio.create_task(log_bot_response(f"lesson 9 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l9_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Не могу тебе отказать!  \n\nНо для дневника питания выходных не бывает. Заполняй его после каждого приёма пищи. Так я сама расскажу, чего не хватает в твоём рационе 🥦",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l9_step_11(callback_query, state):
    await callback_query.message.answer(
        "Добрый вечер! \nКак прошёл этот день? Удалось ли посоветоватья с Нутри и, возможно, заменить стакан апельсинового сока на обычный апельсин? Или заменить майонез в салате на йогурт?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да!", callback_data="next"),InlineKeyboardButton(text="Нет, посоветуешь мне завтра", callback_data="stop")]]))
    await callback_query.answer()

async def process_l9_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Ура! \nЗа стойкость тебе полагается награда: завтра будем есть десерты! Да-да, я не ошиблась! Важно научиться вписывать их в свой рацион так, чтобы не срываться и не съедать целый торт или пачку печенья. \n\nЗаймёмся этим завтра! \nА пока — хорошего вечера ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l9_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Завтра хороший день, чтобы наверстать упущенное! \nВедь мы будем есть сладкое и при этом стараться вписаться в КБЖУ. \n\nДа-да, я не ошиблась! Важно научиться вписывать их в свой рацион так, чтобы не срываться и не съедать целый торт или пачку печенья. \n\nА пока — хорошего вечера ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()