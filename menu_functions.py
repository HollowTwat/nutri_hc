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
# from stickerlist import STICKERLIST
import shelve
import json

from functions import *
from functions2 import *

################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################

async def menu_handler(message, state) -> None:
    await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="📚 Курс:", callback_data="menu_course")],
        [InlineKeyboardButton(text="🍽 Дневник питания:", callback_data="menu_dnevnik")],
        [InlineKeyboardButton(text="💬  Нутри:", callback_data="menu_nutri")],
        [InlineKeyboardButton(text="⚙️Дополнительное:", callback_data="menu_settings")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Меню"
    await message.answer(step0txt, reply_markup=keyboard)

async def menu_cb_handler(callback_query, state) -> None:
    await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="📚 Курс:", callback_data="menu_course")],
        [InlineKeyboardButton(text="🍽 Дневник питания:", callback_data="menu_dnevnik")],
        [InlineKeyboardButton(text="💬  Нутри:", callback_data="menu_nutri")],
        [InlineKeyboardButton(text="⚙️Дополнительное:", callback_data="menu_settings")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Меню"
    await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_course(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="📖Начать Урок X", callback_data="menu_course_lesson_x")],
        [InlineKeyboardButton(text="✏️ Программа курса", callback_data="menu_course_info")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "📚 Курс:"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_dnevnik(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="🍽 Занести в дневник", callback_data="menu_dnevnik_input")],
        [InlineKeyboardButton(text="🔄Редактировать", callback_data="menu_dnevnik_redact")],
        [InlineKeyboardButton(text="📊 Аналитика", callback_data="menu_dnevnik_analysis")],
        [InlineKeyboardButton(text="📸 Инструкция", callback_data="menu_dnevnik_instruction")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "🍽 Дневник питания:"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_nutri(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="🌿 Спросить Нутри", callback_data="menu_nutri_yapp")],
        [InlineKeyboardButton(text="👩‍🍳 Рецепт", callback_data="menu_nutri_reciepie")],
        [InlineKeyboardButton(text="🔍 Анализ этикетки", callback_data="menu_nutri_etiketka")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "💬  Нутри:"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_settings(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="📌 Ваш профиль", callback_data="menu_settings_profile")],
        [InlineKeyboardButton(text="🆘 Помощь", callback_data="menu_settings_help")],
        [InlineKeyboardButton(text="💰 Условия подписки", callback_data="menu_settings_sub")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "⚙️Дополнительное:"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)
################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

async def process_menu_course_lesson(callback_query, state):
    step0txt = "in dev_lessons_n_shit"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_course_info(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Посмотреть пройденные уроки", callback_data="menu_course_info_lessons")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "💚 На первой неделе ты заметишь пищевые привычки, которые тебе мешают. \n💜 На второй получишь базу для формирования новых привычек. \n❤️ На третьей закрепишь новые привычки и начнёшь применять их в реальной жизни."
    step1txt = "Сейчас ты на X уроке этапа X 🧡"
    step2txt = "X уроков из 21 дня пройдено 💪  Осталось X уроков"
    await callback_query.message.edit_text(step0txt, reply_markup=None)
    await callback_query.message.answer(step1txt)
    await callback_query.message.answer(step2txt, reply_markup=keyboard)

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

async def process_menu_dnevnik_input(callback_query, state):
    step0txt = "in dev распознание еды"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_dnevnik_redact(callback_query, state):
    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_dnevnik_analysis(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Показать график за неделю", callback_data="menu_dnevnik_analysis_graph")],
        [InlineKeyboardButton(text="Получить анализ пищи за неделю", callback_data="menu_dnevnik_analysis_rate-week")],
        [InlineKeyboardButton(text="Получить аналитику за 5 дней", callback_data="menu_dnevnik_analysis_5day")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "<b>Ваша статистика на сегодня</b> 🍽\n\nДневная цель: X ккал., X г. белки, X г. жиры, X г. углеводы 💪.   \n\nСегодня вы съели: \nX ккал 🔥.   \n\nБелки: X г. \nЖиры: X г. \nУглеводы:X г.   \n\nТы можешь съесть еще 582 ккал."
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def process_menu_dnevnik_instruction(callback_query, state):
    # buttons = [
    #     [InlineKeyboardButton(text="Изменить имя", callback_data="menu_dnevnik_instruction_")],
    #     [InlineKeyboardButton(text="Изменить норму ККАЛ", callback_data="menu_dnevnik_instruction_")],
    #     [InlineKeyboardButton(text="Заполнить анкету заново", callback_data="menu_dnevnik_instruction_")],
    #     [InlineKeyboardButton(text="Настроить уведомления", callback_data="menu_dnevnik_instruction_")],
    #     ]
    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

async def process_menu_nutri_yapp(callback_query, state):
    # buttons = [
    #     [InlineKeyboardButton(text="Изменить имя", callback_data="menu_nutri_yapp_")],
    #     [InlineKeyboardButton(text="Изменить норму ККАЛ", callback_data="menu_nutri_yapp_")],
    #     [InlineKeyboardButton(text="Заполнить анкету заново", callback_data="menu_nutri_yapp_")],
    #     [InlineKeyboardButton(text="Настроить уведомления", callback_data="menu_nutri_yapp_")],
    #     ]
    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_nutri_reciepie(callback_query, state):
    # buttons = [
    #     [InlineKeyboardButton(text="Изменить имя", callback_data="menu_nutri_reciepie_")],
    #     [InlineKeyboardButton(text="Изменить норму ККАЛ", callback_data="menu_nutri_reciepie_")],
    #     [InlineKeyboardButton(text="Настроить уведомления", callback_data="menu_nutri_reciepie_")],
    #     ]
    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_nutri_etiketka(callback_query, state):
    step0txt = "Отправь мне фото с этикеткой любого товара. Я проанализирую состав за тебя и напишу, есть ли в нём ингредиенты, которых стоит опасаться 🔍   \n\nПодсказка💡 \n<i>Делай фото состава, не названия продукта. \nФото должно быть четким без бликов, на ровной поверхности</i>"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################

async def process_menu_settings_profile(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Изменить имя", callback_data="menu_settings_profile_name")],
        [InlineKeyboardButton(text="Изменить норму ККАЛ", callback_data="menu_settings_profile_kkal")],
        [InlineKeyboardButton(text="Заполнить анкету заново", callback_data="menu_settings_profile_re-anket")],
        [InlineKeyboardButton(text="Настроить уведомления", callback_data="menu_settings_profile_notif")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "<b>Имя, вот твои данные и цель, к которой ты идёшь:</b>   \n\nПол: Не указан \nВозраст: 0 лет \nВес: 0 кг \nРост: 0 см     \n\nЦель: (похудеть и тд) \nЦелевой вес: 0 кг   \n\nТекущая норма калорий: 0 ккал \nТекущая норма БЖУ: x г белков, x г жиров, x г углеводов \nУровень еженедельной активности: 0 часов"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def process_menu_settings_help(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Задать вопрос", callback_data="menu_settings_help_question")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Расскажи, с чем есть проблемы? \nПостараюсь помочь как можно быстрее"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def process_menu_settings_sub(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="📌 Ваш профиль", callback_data="menu_settings_profile")],
        [InlineKeyboardButton(text="🆘 Помощь", callback_data="menu_settings_help")],
        [InlineKeyboardButton(text="💰 Условия подписки", callback_data="menu_settings_sub")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Твой текущий тариф:   \n\n☑️ Подписка на сервис Нутри на X мес \n☑️Действует до:  X \n☑️ Дата автоматического продления: X"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################
