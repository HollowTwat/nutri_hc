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

from all_states import LessonStates5

async def process_l5_step_1(callback_query, state):
    await state.set_state(LessonStates5.step_2)
    await callback_query.message.answer(
        "🍽 <i>«Аппетит приходит во время еды», «Посуда любит чистоту», «Пока всё не съешь, из-за стола не выйдешь».</i> \n\nТебе в детстве так говорили? Нутри постоянно слышала что-то подобное. \n\nТак у меня сформировались привычки и установки, которые мешали питаться осознанно. И знаешь, что было самым сложным? Осознать, что мои привычки вредные. Ведь я с ними с самого детства! Но я справилась, и теперь хочу помочь справиться тебе! \n\nСегодня будем находить у себя эти привычки с помощью небольшой игры. Начнём?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать урок", callback_data="next"), InlineKeyboardButton(text="Сегодня не до игр...", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l5_step_2(callback_query, state):
    await state.set_state(LessonStates5.step_3)
    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        question="<b>Вопрос 1</b> \n«Еду нельзя выбрасывать!» Правда ведь?",
        options=["Правда", "Неправда. Можно выбрасывать."],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="К этому сложно привыкнуть, но еду правда можно выбрасывать!"
    )

async def process_l5_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Принято! Поиграем завтра. \n\nНо для дневника питания выходных не бывает. Заполняй его после каждого приёма пищи. Так я, возможно, смогу заметить вредные пищевые привычки за тебя и помогу их исправить 🍏",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l5_step_3(poll_answer, state):
    await state.set_state(LessonStates5.step_4)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 2</b> \n«Опаздываю на работу, нет времени садиться и завтракать. Съем завтрак по дороге». Бывало такое?",
        options=["Конечно. А что ещё остаётся…", "Стараюсь не есть на ходу"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Если есть на ходу, риски поправиться выше! Читай про это в тексте, который пришлю после этого квиза."
    )

async def process_l5_step_4(poll_answer, state):
    await state.set_state(LessonStates5.step_5)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 3</b> \n«А такое случается? «На работе полный завал, пообедаю попозже. Ой, уже ужин? Как-то незаметно время пролетело…»",
        options=["Случается", "Ну нет. Обед — это святое"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Пропуски приёмов пищи увеличивают риски сердечно-сосудистых заболеваний и набора веса."
    )

async def process_l5_step_5(poll_answer, state):
    await state.set_state(LessonStates5.step_6)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 4</b> \n«А теперь другой вариант. «До обеда ещё час, надо что-то перекусить. У меня как раз есть сникерс». Перекусываешь сладостями?",
        options=["Случается", "Нет"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Сладости — это простые углеводы. Организм быстро их усвоит, и есть захочется снова ещё до наступления обеда."
    )

async def process_l5_step_6(poll_answer, state):
    await state.set_state(LessonStates5.step_7)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 5</b> \n«В целом есть не очень хочется. Не буду накладывать еду в тарелку. Съем буквально пару кусочков из сковородки». Делаешь так?",
        options=["Да! Есть из сковородки очень приятно!", "Нет, люблю разложить всё по тарелочкам"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Сковородки и кастрюли коварны! С ними риск переесть гораздо выше, чем с тарелками!"
    )

async def process_l5_step_7(poll_answer, state):
    await state.set_state(LessonStates5.step_8)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 6</b> \n«Мне очень грустно. Этот чизкейк явно меня порадует». Съесть вкусное, когда грустно. Как тебе такой план?",
        options=["Нормальный план, это работает", "Мою грусть сладости и фастфуд не лечат"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="Это и правда работает! Но лучше искать источники радости не только в еде, но и в общении, движении, разных хобби."
    )

async def process_l5_step_8(poll_answer, state):
    await state.set_state(LessonStates5.step_9)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 7</b> \nПора в гости к родным. Застолье. Наложили полную тарелку, хотя есть не хочется. Твои действия?",
        options=["Поем. Отказываться — себе дороже", "Наберусь терпения и объясню, что не хочу есть"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Нутри знает, как сложно отказать маме, бабушке или тёте! Но это важно делать, чтобы заботиться о себе."
    )

async def process_l5_step_9(poll_answer, state):
    await state.set_state(LessonStates5.step_10)
    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="Любой результат — норма, ведь пищевые привычки сложно менять. Но вместе у нас получится. Читай текст, в котором мы с нутрициологом объясняем, почему подобные привычки мешают нам питаться осознанно и советуем, как от них избавиться 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Читать текст про пищевые привычки",url="https://telegra.ph/EHmocii-i-ustanovki-kak-psihika-upravlyaet-nashim-pitaniem-08-09",callback_data="next")]
        ])
    )
    await asyncio.sleep(5)

    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="✍️<b>Задание на день:</b> \n\n🍎 <b>Зафиксируй вредные пищевые привычки</b> \n1.Выпиши в блокнот или в заметки на телефоне список вредных пищевых привычек, которые обнаружил(а) у себя. \n\n2. Напротив каждой напиши привычки, которыми хочешь их заменить. Это поможет держать фокус на твоих целях. \n\n<i>Например</i> \nКак сейчас: перекусываю сладким \nКак будет: перекусываю небольшой горстью орехов \n\n3. Старайся следовать новой привычке. Если не понимаешь, как это делать, выбери функцию «Задать вопрос» и спроси совет Нутри с помощью текста или голосового сообщения. \n\n<i>Например</i> \nНутри, я опять съел(а) сникерс в качестве перекуса. Что делать?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 Задать вопрос", callback_data="question"),InlineKeyboardButton(text="📖  Дневник питания", callback_data="dnevnik")]
        ])
    )



    ############ EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING #############

async def process_l5_step_11(callback_query, state):
    await state.set_state(LessonStates5.step_12)
    await callback_query.message.answer(
        "Поняла сегодня, что моя вредная привычка — бесконечно рассматривать фото еды в соцсетях. От этого только больше хочется есть! \n\nА у тебя получилось выписать привычки, которые мешают осознанному питанию?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="1"), InlineKeyboardButton(text="И так были полезные", callback_data="2"),  InlineKeyboardButton(text="Иду выписывать", callback_data="3")]
        ])
    )
    await callback_query.answer()

async def process_l5_step_12(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Здорово, что удалось их заметить! На следующей неделе начнём перестраивать рацион и менять их. \n\nУверена, что всё получится, ведь ты учишься у Нутри уже 5 дней подряд, и это уже 5 шагов к осознанному питанию!"
    )
    await callback_query.answer()

async def process_l5_step_12_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Моё уважение! \n🧐 Буду равняться на тебя! \nМоя полезная вечерняя привычка — с вечера готовить для тебя завтрашний урок! Так что я пойду собирать материалы, хорошего тебе вечера 😉"
    )
    await callback_query.answer()

async def process_l5_step_12_3(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Отлично! \nЧем больше ты узнаешь про себя, тем проще потом будет менять старые установки на новые. Лёгкой тебе домашки! \n\nА я побежала готовить твой завтрашний урок."
    )
    await callback_query.answer()