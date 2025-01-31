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

IMG1 = "AgACAgIAAxkBAANBZ5lgYwEpPE_Io6f8HNjvQcDzA94AAs_lMRsKINBI0WwjOw6l8GEBAAMCAAN5AAM2BA"
IMG2 = "AgACAgIAAxkBAANFZ5lgm-ygzgfXpqc3ve7HKnbVvKIAAtDlMRsKINBI4fFmr856K5oBAAMCAAN5AAM2BA"
IMG3 = "AgACAgIAAxkBAANJZ5lgpFx0Zas0CNi_hymLjq5sCHgAAtHlMRsKINBI3BEh1d5asj8BAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAANNZ5lgrpra2SqjwqeN0A3sCYz7I4kAAtLlMRsKINBIBd3vqFSbtvkBAAMCAAN5AAM2BA"

IMG5 = "AgACAgIAAxkBAAPsZ5pp5PjRJkbwMjuM0ISDp27sAAFaAALK6DEbCiDYSGA3s2txTrNjAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAPwZ5pqK7B4wt64mjMfK2LbzmfL310AAszoMRsKINhIAa-NxsllhSABAAMCAAN5AAM2BA"
IMG7 = "AgACAgIAAxkBAAP0Z5pqMq3mh1bNXEOAxyS5H0xTnr0AAs3oMRsKINhIF42rKcKsb6oBAAMCAAN5AAM2BA"
IMG8 = "AgACAgIAAxkBAAP4Z5pqOjP47UJjcDnh1O6Lh9FPrXgAAs7oMRsKINhIV6uh9y1UtesBAAMCAAN5AAM2BA"

IMG18 = "AgACAgIAAxkBAANyZ5lqKVO1CJVNZJb9VZvDpUzLeG4AAtflMRsKINBI7SfuvxvVtqEBAAMCAAN5AAM2BA"
IMG19 = "AgACAgIAAxkBAAN2Z5lqM0QtKa39OjLxNqUYbrmWg6MAAtjlMRsKINBIlOl8FjXWH4IBAAMCAAN5AAM2BA"
IMG20 = "AgACAgIAAxkBAAN6Z5lqPhZp7wWYrAMo9t9IeBoaLxQAAtnlMRsKINBIkrwZSpYgx94BAAMCAAN5AAM2BA"
IMG21 = "AgACAgIAAxkBAAN-Z5lqR89b5ye_F7FopZ_1di60okMAAtrlMRsKINBIlfNnGqnYYsYBAAMCAAN5AAM2BA"
IMG22 = "AgACAgIAAxkBAAOCZ5lqU3fTOA9Ys1f9vOPl-W9APJ8AAtzlMRsKINBI8teB8fC2egUBAAMCAAN5AAM2BA"
IMG23 = "AgACAgIAAxkBAAOGZ5lqXLPAMB9OQlhqMBEs-R2MOpwAAt3lMRsKINBIZWBGl_gM9BcBAAMCAAN5AAM2BA"
IMG24 = "AgACAgIAAxkBAAOKZ5lqZPe6Pig-jyBsS-mnTlcKWdcAAt7lMRsKINBId15BAtofSuMBAAMCAAN5AAM2BA"
IMG25 = "AgACAgIAAxkBAAOOZ5lqbQMNjlkvwVPBHdCjCHnNxdcAAt_lMRsKINBILN6hWWTxqjcBAAMCAAN5AAM2BA"
IMG26 = "AgACAgIAAxkBAAOSZ5lqda_vGmPtm6iVpMD1rWuETIgAAuDlMRsKINBIbcF15g8QCjMBAAMCAAN5AAM2BA"

class LessonStates(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()

async def process_step_1(callback_query, state):
    await state.set_state(LessonStates.step_2)
    text = "<b>Как добиваться целей вместе с Нутри</b>\nНемного о том, как именно я приеду тебя к целям.\n\n<b>📒 Мы будем вести дневник питания\n Время</b>: не больше 3 мин в день\n\n<b>Как это работает</b>:\n\nПросто присылай в чат фото приёма пищи или голосовое с описанием твоей еды, а я сама рассчитаю КБЖУ (калории, белки, жиры и углеводы) и внесу их в дневник.\n\nТебе только нужно будет выбрать, в какой из приёмов пищи мне записать блюдо: завтрак, обед или ужин."
    await callback_query.message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Надо вносить все приёмы пищи?", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_2(callback_query, state):
    await state.set_state(LessonStates.step_3)
    link1 = "https://pmc.ncbi.nlm.nih.gov/articles/PMC3268700/"
    link2 = "https://www.researchgate.net/publication/233778002_Is_Obesity_Caused_by_Calorie_Underestimation_A_Psychophysical_Model_of_Fast-Food_Meal_Size_Estimation"
    text1 = f'Звучит сложно, как и с любой новой привычкой, но я советую делать именно так!\nЕсть десятки исследований, которые <a href=\'{link1}\'>доказывают</a>, что регулярное ведение дневника помогает успешно терять вес и сохранять достигнутые результаты.'
    text2 = f"<b>Вот пара причин, почему важно регулярно заполнять дневник:</b>\n\n✅ <b>Ты поймёшь, сколько калорий ешь на самом деле</b>\n\nМы склонны недооценивать количество съеденного за день Эксперименты <a href=\'{link2}\'>доказывают</a>: если порция большая, можно просчитаться на целых 356 ккал и даже больше!\n\n✅ <b>Заметишь, какие продукты «съедают» норму калорий за день и при этом не насыщают </b>\nНапример, булочка с корицей и кремом может быть приятным перекусом и при этом состоять из 500 ккал жира и углеводов. Для кого-то это треть дневной нормы. При этом после неё ты снова захочешь есть через полчаса.\n\n✅ <b>Отследишь, насколько разнообразен твой рацион</b>\nНапример, вовремя заметишь, что всю неделю в качестве гарнира ешь макароны что пора бы вместо них съесть какую-нибудь крупу."
    await callback_query.message.answer(text1, disable_web_page_preview=True)
    await callback_query.message.answer(
        text2,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Как заполнять дневник", callback_data="next")]
        ]), disable_web_page_preview=True
    )
    await callback_query.answer()

async def process_step_3(callback_query, state):
    await state.set_state(LessonStates.step_4)
    media_files = [
        InputMediaPhoto(media=IMG1, caption="<i>💡 Внимательно изучи примеры, как правильно заносить приемы пищи </i>"),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "Дальше — вперёд к гармоничным отношениям с едой. Главное, не забывай делать записи регулярно.\n\nЯ же в ближайшие три недели буду помогать тебе не только помнить про приёмы пищи, но ещё и делать это осознанно.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Как ты будешь учить меня осознанному питанию?", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_4(callback_query, state):
    await state.set_state(LessonStates.step_5)
    await callback_query.message.answer(
        "📚 <b>У нас будет образовательная программа!</b>\nВнедрять новые привычки проще, когда понимаешь, как они формируются и что влияет на твоё желание съесть шоколадку или овощной салат.\n\n<b>Что за программа</b>\nОна будет длиться 21 день.\n\nОдин день — один урок урок. На каждый — не больше 10 мин в день. Коротко и по делу.\n\nПоэтому каждое утро по будням я буду присылать тебе небольшой материал про осознанное питание — карточки, тест или текст. А после — давать короткое задание, которое поможет лучше узнавать себя и налаживать контакт с телом.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Чему я научусь за эти 3 недели?", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_step_5(callback_query, state):
    await state.set_state(LessonStates.step_6)
    media_files = [
        InputMediaPhoto(media=IMG5, caption="За эти три недели ты разберёшься в принципах осознанного питания и заложишь фундамент для нового подхода к отношениям с едой.\n\n💚 На первой неделе ты заметишь пищевые привычки, которые тебе мешают.\n💜 На второй получишь базу для формирования новых привычек.\n❤️ На третьей закрепишь новые привычки и начнёшь применять их в реальной жизни."),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    
    await callback_query.message.answer(
        "Как насчёт первого короткого урока прямо сейчас?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начать первый урок", callback_data="next"), InlineKeyboardButton(text="Отложить до завтра", callback_data="quitout")]
        ])
    )
    await callback_query.answer()

async def process_step_6(callback_query, state):
    await state.set_state(LessonStates.step_7)
    media_files = [
        InputMediaPhoto(media=IMG18),
        InputMediaPhoto(media=IMG19),
        InputMediaPhoto(media=IMG20),
        InputMediaPhoto(media=IMG21),
        InputMediaPhoto(media=IMG22),
        InputMediaPhoto(media=IMG23),
        InputMediaPhoto(media=IMG24),
        InputMediaPhoto(media=IMG25),
        InputMediaPhoto(media=IMG26),
    ]
    await callback_query.message.answer_media_group(media=media_files)
    link = "https://telegra.ph/Pochemu-diety-ne-rabotayut-istochniki-informacii-07-16"
    await callback_query.message.answer(
        f"<b>Урок 1\nПочему диеты не работают</b>\n«Нутри, почему бы мне просто не сесть не диету?, — наверняка спрашиваешь ты. — Ведь на диете я могу скинуть 5 кг за пару недель, а это крутой результат!»\n\nПотому что диеты дают краткосрочный результат. Да, фотографии до/после с марафонов похудения часто впечатляют. Но вы хоть раз видели участников таких экстремальных курсов спустя полгода-год? Большинство из них набирают все сброшенные кг до грамма.\n\nПочему так происходит и чем осознанное питание отличается от диет, рассказываем в сегодняшнем уроке.\n\nИсточники, по которым мы написали эти карточки — <a href=\'{link}\'>по ссылке.</a>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="В чём фишка осознанного питания?", callback_data="next")]
        ]), disable_web_page_preview=True
    )
    await callback_query.answer()

async def process_step_7(callback_query, state):
    await state.clear()
    await callback_query.message.answer("Начнём осваивать эти принципы уже завтра!\nБудем разбираться, как почувствовать голод и как не переедать.")
    await callback_query.message.answer("А на сегодня информации достаточно. Осталось задание — небольшое и приятное — поболтать с Нутри!\n\nХотя день был насыщенным, у тебя наверняка остались ко мне вопросы. Нажми кнопку <b>«Задать вопрос»</b> спроси всё, что хочешь.\n\nНапример: <i>«Сколько раз в день нужно есть?»</i> или <i>«Нужно ли планировать приёмы пищи?»</i>\n\nЭто можно сделать с помощью текста или голосового сообщения.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Задать вопрос", callback_data="menu_nutri_yapp")]
        ])
    )
    await callback_query.answer()