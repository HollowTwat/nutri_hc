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


class Questionnaire(StatesGroup):
    prefirst = State()
    first = State()
    mail = State()
    name = State()
    gender = State()
    f_preg = State()
    f_breastfeed = State()
    height = State()
    weight = State()
    water = State()
    booze = State()
    meals = State()
    meals_extra = State()
    allergies = State()
    part3 = State()
    jogging = State()
    lifting = State()
    stress = State()
    sleep  = State()
    goal = State()
    w_loss = State()
    w_loss_amount = State()
    city = State()
    morning_ping = State()
    evening_ping = State()
    community_invite = State()

async def process_prefirst(message, state):
    text = f"{message.from_user.first_name},\n\nЯ очень рада, что теперь у меня есть такой приятный собеседник как ты!\n\nСделаю всё, чтобы ты смог(ла) комфортно прийти к своим целям!\n\nНо сначала эти цели нужно правильно поставить. Для этого я задам несколько важных вопросов.\n\nОтветы займут не больше 5 минут и помогут мне создать персональный план питания под твои параметры и запросы.\n\nРасскажешь мне о себе?"
    buttons = [
        [InlineKeyboardButton(text="Конечно!", callback_data="next")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)

async def process_first(message, state):
    text = f"Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно"
    await message.answer(text, reply_markup=None)

async def process_mail(message, state):
    answer = await check_mail(message.text)
    if answer == True:
        text = "<b>Как тебя зовут?</b>"
        await message.answer(text)
    elif answer == False:
        await state.clear()
        text = "К сожаление, я не нашла твою почту. Напиши пожалуйста в тех поддержку  XXX"
        buttons = [
        [InlineKeyboardButton(text="Поддержка", url="retry_mail")],
        [InlineKeyboardButton(text="Попробовать еще раз", url="t.me/nutri_care")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text, reply_markup=keyboard)
    

async def process_name(message, state):
    link = ""
    text1 = f"<b>Часть 1/3\n4 вопроса о тебе</b>\n{message.text}, при составлении твоего плана питания я буду ориентироваться на КБЖУ: твою норму калорий, белков, жиров и углеводов.\n\nЧтобы рассчитать её, <a href=\'{link}\'>мне нужно узнать</a>твой пол, возраст, вес и рост: если для роста 155 см вес в 50 кг — норма, то для роста 180 см это уже очень мало."
    text = "🟢⚪️⚪️⚪️ \nТвой пол"
    buttons = [
        [InlineKeyboardButton(text="Женский", url="female")],
        [InlineKeyboardButton(text="Мужской", url="male")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text1)
    await message.answer(text, reply_markup=keyboard)

async def process_gender(message, state):
    text = "Тогда еще пара важных вопросов, которые влияют на рекомендации (например, можно ли вам алкоголь).\n\nТы беременна?"
    buttons = [
        [InlineKeyboardButton(text="Женский", url="female")],
        [InlineKeyboardButton(text="Мужской", url="male")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_f_preg(message, state):
    text = "Кормишь грудью?"
    buttons = [
        [InlineKeyboardButton(text="Женский", url="female")],
        [InlineKeyboardButton(text="Мужской", url="male")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_f_breastfeed(message, state):
    text = "🟢🟢⚪️⚪️ \nТвой рост в сантиметрах. Укажи только число. \n<i>Например, 170.</i>"
    await message.edit_text(text, reply_markup=None)

async def process_height(message, state):
    text1 = "Записала!"
    text = "🟢🟢🟢⚪️ \nТвой текущий вес в килограммах. Укажи только число.  \n<i>Например, 80</i>"
    await message.answer(text1)
    await message.answer(text)

async def process_weight(message, state):
    text1 = "Записала! Теперь я могу посчитать твой индекс массы тела (ИМТ) и составить рекомендации по питанию! \nНо сначала уточню ещё один важный момент!"
    text = "🟢🟢🟢🟢 \nРаз уж у нас с тобой честный разговор, скажи, сколько тебе лет =) Обещаю, это останется между нами! Мне нужно это знать для расчёта твоего базового метаболизма.  \nНапиши только число.\n<i>Например, 35</i>"
    await message.answer(text1)
    await message.answer(text)

async def process_age(message, state):
    link = ""
    text1 = "Спасибо за доверие!"
    text2 = "🟠⚪️⚪️⚪️⚪️ \nСколько воды ты пьёшь в день? \nВопрос про чистую воду, чай и кофе не в счёт!"
    text = f"<b>Часть 2/3\n5 вопросов о питании</b>\n\nПривычки не меняются за один день. Резко начинать новую жизнь «с понедельника» — <a href=\'{link}\'>верный путь к срывам.</a> Ты продержишься неделю-другую, получишь первые результаты, а потом так же стремительно откатишься назад.\n\nЧтобы этого не случилось, я построю плавный путь из твоей исходной точки к цели. Для этого мне важно знать, как ты питаешься сейчас. Я задам 5 вопросов, на которые важно ответить честно."
    buttons = [
        [InlineKeyboardButton(text="Пару стаканов или меньше", url="<2")],
        [InlineKeyboardButton(text="3–5 стаканов", url="3-5")],
        [InlineKeyboardButton(text="6 стаканов и больше", url=">6")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text1)
    await message.answer(text)
    await message.answer(text2, reply_markup=keyboard)

async def process_water(message, state):
    text = "🟠🟠⚪️⚪️⚪️ \nКак часто ты пьёшь алкоголь?"
    buttons = [
        [InlineKeyboardButton(text="Вообще не пью", url="0")],
        [InlineKeyboardButton(text="Меньше 2х бокалов/рюмок в неделю", url="<2")],
        [InlineKeyboardButton(text="Меньше 7 бокалов/рюмок в неделю", url="2-6")],
        [InlineKeyboardButton(text="Больше 7 бокалов в неделю", url=">7")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_booze(message, state):
    text = "🟠🟠🟠⚪️⚪️\nСколько у тебя приёмов пищи в день,  включая перекусы?"
    buttons = [
        [InlineKeyboardButton(text="1", url="1")],
        [InlineKeyboardButton(text="2", url="2")],
        [InlineKeyboardButton(text="3", url="3")],
        [InlineKeyboardButton(text="4", url="4")],
        [InlineKeyboardButton(text="5", url="5")],
        [InlineKeyboardButton(text="6+", url="6+")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_meals(message, state):
    text = "🟠🟠🟠🟠⚪️\nКакие это приёмы пищи?   \n\nОпиши в паре предложений свой обычный режим питания и отправь их в чат.  \n\nНапример:  \n<i>«Обычно пропускаю завтрак, но плотно обедаю и ужинаю». \n«Ем три раза в день, два раза перекусываю сладким». \n«Нет режима питания, делаю большие перерывы между едой».</i>"
    buttons = [
        [InlineKeyboardButton(text="Пропустить", url="None")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_meals_extra(message, state):
    text = "🟠🟠🟠🟠🟠\nЕсть ли продукты или компоненты, которые ты не ешь?  \nНапиши про них в чат.  \n\nНапример:  \n<i>«Не ем мясо и птицу»  \n«Не ем молочные продукты» \n«Не ем глютен»</i>"
    buttons = [
        [InlineKeyboardButton(text="Ем всё!", url="None")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)

async def process_allergies(message, state):
    # Empty function for allergies step
    pass

async def process_part3(message, state):
    # Empty function for part3 step
    pass

async def process_jogging(message, state):
    # Empty function for jogging step
    pass

async def process_lifting(message, state):
    # Empty function for lifting step
    pass

async def process_stress(message, state):
    # Empty function for stress step
    pass

async def process_sleep(message, state):
    # Empty function for sleep step
    pass

async def process_goal(message, state):
    # Empty function for goal step
    pass

async def process_w_loss(message, state):
    # Empty function for w_loss step
    pass

async def process_w_loss_amount(message, state):
    # Empty function for w_loss_amount step
    pass

async def process_city(message, state):
    # Empty function for city step
    pass

async def process_morning_ping(message, state):
    # Empty function for morning_ping step
    pass

async def process_evening_ping(message, state):
    # Empty function for evening_ping step
    pass

async def process_community_invite(message, state):
    # Empty function for community_invite step
    pass