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

IMG1 = "AgACAgIAAxkBAAIEP2eqDs7-VhaMY4NHdrOPODx8THQ7AAII-zEbMp9RSeSmlqSD20b9AQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIEQ2eqDte9lMnHITr42_-GDKRDybNwAAIJ-zEbMp9RSV-qT63hcY7jAQADAgADeQADNgQ"

IMG3 = "AgACAgIAAxkBAAIER2eqERAQD8MMXNa1wcTjI2117KnWAAIZ-zEbMp9RSTbtjNYq0MhiAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIES2eqERW2uKiTSk40FQABs4hNwrNFjAACHPsxGzKfUUktlyi1xcktIQEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAIET2eqERsoA0QTwxaqJQABC9RgzmKjxgACHfsxGzKfUUkLu7Qv5RMD8AEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAIEU2eqESENqkwrsh7OoFar5i5Tvc1NAAIe-zEbMp9RSa0DUaMl94euAQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIEV2eqESgBfGrtp-LEYH5LhG-zlRxdAAIf-zEbMp9RSehviDYaBcT4AQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIEW2eqETAVvlYQyMdSeU4Qq6DgFyKdAAIg-zEbMp9RSUSCrgkvf65DAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIEX2eqETcKyUMzsb0os0vLrXasJuBuAAIh-zEbMp9RSfmBkG9y9y0wAQADAgADeQADNgQ"
IMG10 = "AgACAgIAAxkBAAIEY2eqET4YEdIiLG74HQZZoFDU4hGRAAIi-zEbMp9RSdLDJfZ775HUAQADAgADeQADNgQ"
IMG11 = "AgACAgIAAxkBAAIEZ2eqEUfsOlJPBpTC8cCHsXlnC8NuAAIj-zEbMp9RSeM4wfH6EqjpAQADAgADeQADNgQ"
IMG12 = "AgACAgIAAxkBAAIEa2eqEU5DK4Q7agtkNm92T68ktrPFAAIl-zEbMp9RSfQ47E7hDugdAQADAgADeQADNgQ"

IMG13 = "AgACAgIAAxkBAAIEb2eqEmyBOYtdEdK0JRnntRjMiFw4AAIr-zEbMp9RSeo70pOMAAGLyQEAAwIAA3kAAzYE"
IMG14 = "AgACAgIAAxkBAAIEc2eqEnP2LWKh0-e3kCtO4d7-RpDxAAIs-zEbMp9RSbZ1E49v6bfzAQADAgADeQADNgQ"
IMG15 = "AgACAgIAAxkBAAIEd2eqEnu0hKFdDJtm8P71xzIFjL_MAAIt-zEbMp9RSY-L2RH0ywABHwEAAwIAA3kAAzYE"
IMG16 = "AgACAgIAAxkBAAIEe2eqEoHsG30aT0WZnMaX0nNA8SWdAAIu-zEbMp9RSQNxzkqivtH3AQADAgADeQADNgQ"
IMG17 = "AgACAgIAAxkBAAIEf2eqEocufqrBDC0HmEFzgLdt_RPVAAIv-zEbMp9RSSOzq7jgMTCEAQADAgADeQADNgQ"


async def process_l8_step_1(callback_query, state):
    await state.set_state(LessonStates8.step_2)
    
    await callback_query.message.answer(
        "Всем утро! ☀️ Это второй этап учёбы с Нутри. \n\nНа прошлом этапе мы научились прислушиваться к сигналам тела: слышать голод и вовремя чувствовать насыщение, анализировать пищевые привычки. \n\nНо что теперь с этим делать?"
        )
    
    media_files = [
        InputMediaPhoto(media=IMG1),
        InputMediaPhoto(media=IMG2)
    ]
    await callback_query.message.answer_media_group(media=media_files)

    await callback_query.message.answer(
        "Следующий шаг — ввести в привычку правила, техники и инструменты, которые помогут регулировать голод и насыщение,. Это поможет нам заложить базу для новых пищевых привычек. \n\nА именно: \n\n🍏 научиться накладывать в тарелку ту еду, которая поможет утолить голод на несколько часов, а не на 30 минут; \n🍏 научиться иногда радовать себя, чтобы новый образ жизни не давался слишком тяжело; \n🍏 начать менять не только рацион, но и образ жизни; \n🍏продолжать вести дневник питания. \n\nНачнём?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Начнём!", callback_data="next"), InlineKeyboardButton(text="Отложим новый образ жизни до завтра", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l8_step_2(callback_query, state):
    await state.set_state(LessonStates8.step_3)
    
    media_files = [
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
        InputMediaPhoto(media=IMG10),
        InputMediaPhoto(media=IMG11),
        InputMediaPhoto(media=IMG12)
    ]
    await callback_query.message.answer_media_group(media=media_files)

    text = "<b>Урок 1 \nБелки, жиры и углеводы</b> \n\nУже несколько дней ты стараешься придерживаться рекомендаций Нутри. Признаю тебя героем моего сердечка ❤️ \n\nКстати! Ты замечаешь, что в нём помимо нормы калорий в дневнике питания есть белки, жиры и углеводы? Простой пример, почему важно считать ещё и их! \n\n🥐Миндальный круассан — 400 ккал. \n🥒250 г куриного филе с овощами — тоже 400 ккал. \n\nВ чём разница? Как раз в белках, жирах и углеводах! И, как следствие, в том, что после круассана есть захочется через 30 минут, а после филе с овощами — через 4 часа. \n\nПочему? Объясняем в карточках, которые мы составили вместе с нутрициологом."
    await callback_query.message.answer(text,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Как соблюсти баланс белков, жиров и углеводов?", callback_data="next")]
        ])
    )
    
    await callback_query.answer()

async def process_l8_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Понимаю, менять образ жизни и правда сложно! 💔   \n\nА вот продолжать делать то, что уже начато, немного проще!    \n\nТы уже больше недели ведёшь дневник питания, так что давай продолжим его заполнять!    \n\nНажимай на кнопку после приёма пищи, чтобы проанализировать свой завтрак, обед или ужин.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()

async def process_l8_step_3(callback_query, state):
    await state.set_state(LessonStates8.step_4)
    
    media_files = [
        InputMediaPhoto(media=IMG13),
        InputMediaPhoto(media=IMG14),
        InputMediaPhoto(media=IMG15),
        InputMediaPhoto(media=IMG16),
        InputMediaPhoto(media=IMG17)
    ]
    await callback_query.message.answer_media_group(media=media_files)

    await callback_query.message.answer(
        "Мы разобрались, что при составлении рациона важно ориентироваться на КБЖУ: калории, белки, жиры и углеводы. \n\nНо как спланировать питание, чтобы оно соответствовало <b>формуле 25% белков — 25% жиров — 50% углеводов</b>? Сидеть с калькулятором перед каждым приёмом пищи? Это точно не то, что хочется делать каждый день! \n\nХорошая новость в том, что эксперты по питанию из Гарварда придумали простой способ на глаз составить сбалансированный завтрак, обед или ужин. \n\nПринцип так и назвали — «Гарвардская тарелка» или «тарелка здорового питания». В карточках мы с нутрициологом рассказываем, что это за тарелка и как её составить."
        )
    
    await callback_query.message.answer(
        "✍️ <b>Задание на день</b> \n\nПопроси Нутри составить тебе рецепт по принципам Гарвардской тарелки и приготовь его на ужин. Для этого просто напиши в чат: <b>«Нутри, предложи рецепт по принципу Гарвадской тарелки».</b> \n\nИ, конечно, не забывай заполнять дневник питания!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Дневник питания", callback_data="dnevnik"), InlineKeyboardButton(text="Составить рецепт", callback_data="recept")]
        ])
    )
    await callback_query.answer()

############ EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING #############

async def process_l8_step_11(callback_query, state):
    await state.set_state(LessonStates8.step_12)
    await callback_query.message.answer(
        "Добрый вечер! \n\nПризнавайся: хоть раз за день тебе пришла в голову мысль: «Да как составить эту вашу гарвардскую тарелку из моей привычной еды?!» \n\nЯ бы точно так подумала на твоём месте! \n\nГарвардская тарелка — это супер, но реальный мир сложнее. В кафе не раскладывают еду по четвертинкам тарелки, да и привычные рецепты под неё как будто не приспособлены! Как быть? \n\nПрактиковаться и применять теоретические знания в реальной жизни! \n\nПорепетируем на походе в кафе и попробуем по описанию блюд понять, какие из них — самые сбалансированные 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Давай!", callback_data="next")]
        ])
    )
    await callback_query.answer()

async def process_l8_step_12(callback_query, state):
    await state.set_state(LessonStates8.step_13)
    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        question="<b>Вопрос 1</b> \nТы в кафе. Меню завтраков в тут отличное! Но в каком из них больше всего белков и меньше всего калорий? Вес, допустим, у всех одинаковый.",
        options=["Омлет с лососем, авокадо и зеленью", "Английский завтрак: яичница-глазунья, бекон, сосиски, помидоры","Сырники со сметаной и малиновым вареньем","Рисовая каша с фруктами"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="Омлет с лососем, авокадо и зеленью — идеальный завтрак по гарварду. В английском много жиров, в сырниках — сахара, в каше мало белка."
    )

async def process_l8_step_13(poll_answer, state):
    await state.set_state(LessonStates8.step_14)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 2</b> \nВпрочем, ты смотришь на часы и понимаешь, что уже 13.00. Для завтрака поздновато. Поэтому заглядываешь в раздел с основным меню. Первыми там идут салаты. Но какой из них полезнее?",
        options=["Цезарь", "Греческий","Оливье"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Секрет — в заправках. У цезаря и оливье они жирные, а греческий заправляют оливковым маслом с травами. Поэтому он менее калорийный."
    )

async def process_l8_step_14(poll_answer, state):
    await state.set_state(LessonStates8.step_15)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 3</b> \nС салатом определились. А что насчёт супа?",
        options=["Берём борщ с говядиной!", "Заказываем модный том ям с креветками","Отдаём предпочтение грибному крем-супу"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="Борщ — самый некалорийный + в нём много белка от говядины. В том яме больше калорий от кокосового молока, а в грибном крем-супе мало белка."
    )

async def process_l8_step_15(poll_answer, state):
    await state.set_state(LessonStates8.step_16)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 4</b> \nОказалось, что суп не очень-то и хочется. Смотрим в основное меню. А там — пасты. Что выберем: карбонару или болоньезе?",
        options=["Конечно, карбонару!", "Конечно, болоньезе!"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Болоньезе с фаршем и томатом, карбонара — с беконом и соусом из сливочного масла и муки. Получается, в болоньезе меньше жира и больше белка."
    )

async def process_l8_step_16(poll_answer, state):
    await state.set_state(LessonStates8.step_17)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 5</b> \nЛистаем меню дальше, а там — стейки! Какой из них менее жирный?",
        options=["Рибай", "Нью-Йорк"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Стейк «Нью-Йорк» вырезается из той же мышцы, что и Рибай, но вот объём жира в нем всегда ниже."
    )

async def process_l8_step_17(poll_answer, state):
    await state.set_state(LessonStates8.step_18)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 6</b> \nВ итоге у нас на столе стейк и греческий салат. А что насчёт десерта? Какой берём?",
        options=["Чизкейк", "Наполеон","Яблочный штрудель","Тирамису"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="В штруделе помимо сахара есть клетчатка, корица обладает антиоксидантными свойствами, в тесте используется минимум маргарина и масла."
    )

async def process_l8_step_18(poll_answer, state):
    await state.clear()
    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="Надеюсь, этот квиз не разбудил твой аппетит под вечер! \nНо если всё-таки разбудил, составь себе маленькую Гарвардскую тарелку! А уже завтра разберёмся, как выбрать для неё продукты, которые не съедят всю дневную норму калорий!"
    )