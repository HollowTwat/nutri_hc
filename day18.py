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


async def process_l18_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 17:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates18.step_2)
    await callback_query.message.answer(
        "Добрый вечер! \n\nПризнавайся: хоть раз за день тебе пришла в голову мысль: «Да как составить эту вашу гарвардскую тарелку из моей привычной еды?!» \n\nЯ бы точно так подумала на твоём месте! \n\nГарвардская тарелка — это супер, но реальный мир сложнее. В кафе не раскладывают еду по четвертинкам тарелки, да и привычные рецепты под неё как будто не приспособлены! Как быть? \n\nПрактиковаться и применять теоретические знания в реальной жизни! \n\nПорепетируем на походе в кафе и попробуем по описанию блюд понять, какие из них — самые сбалансированные 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пройти тест", callback_data="next"), InlineKeyboardButton(text="Взять выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()

async def process_l18_step_2(callback_query, state):
    await state.set_state(LessonStates18.step_3)
    await callback_query.message.answer(
        "Я бережно передала тебе всю базу для осознанного питания. Предлагаю проверить, что из этой базы запомнилось, а что стоит перечитать."
    )

    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        question="Вопрос 1 \nВ каком из этих продуктов больше всего белков?",
        options=["Сметана", "Греческий йогурт","Творог"],
        correct_option_id=2,
        is_anonymous=False,
        type="quiz",
        explanation="Вопрос не из простых! Содержание белков на 100 г у каждого из продуктов примерно такое: сметена – 2г, йогурт – 3,5г, творог целый 21г!"
    )

async def process_l18_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Надеюсь, ты берёшь выходной, чтобы всё хорошенько повторить и завтра вернуться и всё-таки пройти тест 😉 \n\nОн не сложный, а я не строгая: скорее он нужен, чтобы помочь тебе понять, какие темы стоит ещё раз повторить. \n\nВозвращайся завтра, чтобы закончить курс!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ])
    )
    await callback_query.answer()

async def process_l18_step_3(poll_answer, state):
    await state.set_state(LessonStates18.step_4)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 2</b> \nСнизим уровень сложности! Перед рабочим звонком ты испытваешь стресс. Как лучше с ним справиться?",
        options=["Сделать дыхательную технику «4–7–8»", "В деталях представить свой провал на звонке","Съесть тортик"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="Ответить на этот вопрос было просто. Надеюсь, так же просто будет внедрить эту практику в жизнь!"
    )

async def process_l18_step_4(poll_answer, state):
    await state.set_state(LessonStates18.step_5)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 3</b> \nВ предыдущих вопросах приходилось отказываться от сладкого в пользу других вариантов. Может, вообще вычеркнуть сладости из рациона?",
        options=["Так и сделаем!", "Ну уж нет, иногда будем есть"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Если совсем отказаться от сахара, то такая резкость может привести к срывам. Поэтому лучше иногда вписывать немного сладостей в свой рацион."
    )

async def process_l18_step_5(poll_answer, state):
    await state.set_state(LessonStates18.step_6)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 4</b> \nВроде бы срывов нет, а вес всё равно не уходит. Больше того, даже набирается. Всему виной — две недели недосыпа. Сколько в среднем набирают по этой причине?",
        options=["0,5 кг", "2 кг","5 кг"],
        correct_option_id=0,
        is_anonymous=False,
        type="quiz",
        explanation="Набор веса не критичный, но всё же неприятный. Бегом спать!"
    )

async def process_l18_step_6(poll_answer, state):
    await state.set_state(LessonStates18.step_7)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 5</b> \nДругая ситуация. Вроде бы вес сброшен, но качество тела не устраивает. В чём может быть дело? ",
        options=["Нужно скинуть ещё несколько кг", "Не хватает спорта"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Без спорта вместе с жиром на диете уходят мышцы, в итоге получается фигура «скинни фэт»."
    )

async def process_l18_step_7(poll_answer, state):
    await state.set_state(LessonStates18.step_8)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 6</b> \nСпорт добавили, выспались! Продолжаем думать о здоровом рационе. Что, согласно средиземноморской диете, стоит есть не чаще раза в неделю?",
        options=["Курицу", "Рыбу","Красное мясо"],
        correct_option_id=2,
        is_anonymous=False,
        type="quiz",
        explanation="В красном мясе много белков, но много и жира. Поэтому с ним лучше не частить. Курицу стоит есть раз в 1–2 дня, рыбу — 3–4 раза в неделю."
    )

async def process_l18_step_8(poll_answer, state):
    await state.set_state(LessonStates18.step_9)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 7</b> \nОтлично, сегодня едим рыбу. А чем дополним её, чтобы всё было по принципам Гарвардской тарелки?",
        options=["Картошечкой с сыром (фиш энд чипс!)", "Овощным салатом и рисом","Зеленью и тушёными овощами"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Помимо белков в гарвардской тарелке должны быть крупы и фрукты с овощами. Поэтому добавим овощной салат и рис — и будем сыты!"
    )

async def process_l18_step_9(poll_answer, state):
    await state.set_state(LessonStates18.step_10)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 8</b> \nГарвардскую тарелку составили. Какой соус подадим к рыбе?",
        options=["Тартар (это же рыба!)", "Греческий йогурт с измельченным укропом","Сырный (фиш энд чипс!)"],
        correct_option_id=1,
        is_anonymous=False,
        type="quiz",
        explanation="Тартар — классический соус к рыбе. Но его делают на основе майонеза. Лучше заменить его соусами на основе греческого йогурта."
    )

async def process_l18_step_10(poll_answer, state):
    await state.set_state(LessonStates18.step_11)
    await bot.send_poll(
        chat_id=poll_answer.user.id,
        question="<b>Вопрос 9</b> \nК ужину придут гости. К рыбе решено заказать доставку со ещё одним блюдом. Какое блюдо закажем?",
        options=["Картофельная вафля с беконом", "Хашбрауны с говяжьими колбасками","Паста Альфредо с курицей"],
        correct_option_id=2,
        is_anonymous=False,
        type="quiz",
        explanation="Думаю, в пасте с курицей будет больше белка и меньше жира. Попросите соус отдельно, тогда сможете проконтролировать ещё и количество жиров."
    )

async def process_l18_step_11(poll_answer, state):
    await state.set_state(LessonStates18.step_12)
    await bot.send_message(
        chat_id=poll_answer.user.id,
        text="Ура, официально объявляю тебя мастером осознанного питания 🎉 \n\nКак твои результаты? \n\n<b>8–9 правильных ответов</b> \nПоздравляю! Кажется, ты внимательно читал(а) все карточки и делал(а) все задания! Уверена, что у тебя получится вести дневник питания и добиваться твоих целей и дальше! А я буду рядом и буду помогать 😉 \n\n<b>5–7 правильных ответов</b> \nТы на верном пути к новым привычкам! Но нам с тобой точно есть о чём поболтать! Перечитай пропущенные уроки или задай любой вопрос об осознанном питании Нутри, нажав кнопку «Задать вопрос». \n\n<b>1–4 правильных ответа</b> \nКажется, стоит ещё раз перечитать уроки! У тебя будет на это время: они останутся с тобой навсегда. Проходи уроки, делай задания, задавай вопросы Нутри и не забывай заполнять дневник питания! Он поможет тебе сделать осознанное питание привычкой ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]])
    )
    try:
        issuccess = await add_user_lesson(poll_answer.user.id, "18")
        asyncio.create_task(log_bot_response(f"lesson 18 saved status{issuccess} "), poll_answer.user.id)
    except Exception as e:
        print(e)