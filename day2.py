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

# IMG1 = "AgACAgIAAxkBAAIJNme1A6KDC56jHkjtyzfPYmP6m2HAAAJT9TEb2NCpSVjK6LtzmAIyAQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIJOme1A6hNVEe3TekpIcoOPnibEt6MAAJU9TEb2NCpSWTJbK-ISxfDAQADAgADeQADNgQ"

# IMG3 = "AgACAgIAAxkBAAIJPme1A7I3Cz4-QSg4MAef4gF7wTg_AAJV9TEb2NCpSWJ-ytyPzx84AQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIJQme1A7YQUU3KYueuUylKtwdO8HLhAAJX9TEb2NCpSSP2uE-Io5kRAQADAgADeQADNgQ"

# IMG5 = "AgACAgIAAxkBAAIJRme1A7_h58YE9yNu4YGs5J9xLvYgAAJY9TEb2NCpSYBAcmb6Moe2AQADAgADeQADNgQ"

# IMG6 = "AgACAgIAAxkBAAIJSme1A8bbFTI4ICBdjuO7kWmaNJj5AAJZ9TEb2NCpSfY3s5PpHi_8AQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIJTme1A8pGMwlDCAVpHXzGMjP_UKIaAAJa9TEb2NCpSfnvdyleyo64AQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIJUme1A86o9ideoP5XEEPbKxgNdW2WAAJb9TEb2NCpSSmtN8jmz3d1AQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIJVme1A9K-jXNvL2fqJ5EYZcauk2ONAAJc9TEb2NCpSeavgFmW8mEVAQADAgADeQADNgQ"
# IMG10 = "AgACAgIAAxkBAAIJWme1A9ZqYn7F7TdpQ6-vxjoQqg3VAAJd9TEb2NCpSXMVHVwGxKAhAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEW2Fn2eaSsntWZpuYmpmGShndLpI0WAACe_AxG2W90Eo5ZkhLrLMX4AEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEW2Rn2eabrBAlEzeXxuxhGFZYsQhO3AACfPAxG2W90EqaSSJR_Q3LTQEAAwIAA3kAAzYE"

IMG3 = "AgACAgIAAxkBAAEEW2dn2eaqopdb2mFkPqLfUOMQ_6-48wACf_AxG2W90ErW1ED5JlX88gEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEW2pn2eazPJ5qWH_zdjzncYslmtovSwACgPAxG2W90Eo1ie5wz_UPVgEAAwIAA3kAAzYE"

IMG5 = "AgACAgIAAxkBAAEEW21n2ea7hjB-LGRqFXCU681laOv9BwACgfAxG2W90EqsVZ7Gop-3PQEAAwIAA3kAAzYE"

IMG6 = "AgACAgIAAxkBAAEEW3Bn2ebDoOXE-pdJYrhRoSt6pW9KQgACgvAxG2W90EqR03IKYvtPugEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEW3Nn2ebKATJOwYqmFKScjT_2fPAngwACg_AxG2W90EpuI30eSlJb1gEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEW3Zn2ebTRDtHbWoIHyROvLxkJKgLLwAChPAxG2W90EovMdzYo70vYwEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEW3ln2ebnHEF7NBJy-YBLsYgsIubJ8wAChfAxG2W90EpJh-qtXs8BuwEAAwIAA3kAAzYE"
IMG10 = "AgACAgIAAxkBAAEEW3xn2ecVX5euELeR3G-gGi-ojFcCnAAChvAxG2W90EqsTYQqIecCCQEAAwIAA3kAAzYE"


from all_states import *

async def process_l2_step_1(callback_query, state):
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    if last_lesson < 1:
        callback_query.message.answer("Ты пока не прошел прошлый урок, так-что этот тебе не доступен")
        return
    await state.set_state(LessonStates2.step_2)
    await callback_query.answer()
    text="Доброе утро! \n\nКажется, распознавать сигналы тела легко:  хочешь есть — поешь, наелся — перестань. Но на деле всё сложнее. \n\nИногда мы пропускаем приёмы пищи и набрасываемся на еду из-за сильного голода. А иногда зачем-то едим, когда совершенно не хочется есть."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(
        "<b>Девиз этой недели — научиться осознавать свои потребности, наладить контакт с телом и эмоциями.</b> \n\nА именно: \n\n🍏 слышать сигналы тела: правильно распознавать голод и насыщение \n🍏 начать замечать свои пищевые привычки \n🍏 разобраться с функциями Нутри и сделать их использование привычкой \n\nНу что, начнём урок?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Давай!", callback_data="next"), InlineKeyboardButton(text="Сегодня возьму выходной", callback_data="stop")]
        ])
    )
    await callback_query.answer()


async def process_l2_step_2(callback_query, state):
    await state.set_state(LessonStates2.step_3)
    text1 = "Первый секрет — настоящий голод не наступает внезапно. \n\nОн подкрадывается издалека и постепенно усиливается. На карточках — чек-лист с признаками голода. Они подскажут тебе, что пора поесть и откладывать дальше некуда."
    media_files = [
        InputMediaPhoto(media=IMG3, caption = text1),
        InputMediaPhoto(media=IMG4)
    ]
    await callback_query.message.answer(
        "<b>Урок 2</b> \n\n<b>Как понять, что пора поесть, и как — что пора остановиться</b> \n\nСегодня будем искать ответ на вопрос жизни, вселенной и всего такого: «Есть или не есть?». Говоря проще, будем весь день прислушиваться к себе и определять, когда чувствуем голод, а когда уже наелись."
    )
    await callback_query.message.answer_media_group(media=media_files)
    text2 = "Второй секрет — важно вовремя заметить не только голод, но и насыщение. Для этого ешь медленно и старайся оценить уровень сытости по 10-балльной шкале с картинки. В норме после еды должно оставаться ощущение комфорта, а вот тяжести быть не должно."
    await callback_query.message.answer_photo(photo=IMG5, caption=text2)
    await callback_query.message.answer(
        "✍️ <b>Задание на день</b> \n\n🍎 Заноси каждый приём пищи в дневник питания Нутри, а после оценивай уровень насыщения по шкале от 1 до 10. \n\nДля этого выбирай функцию «Дневник питания» в меню и рассказывай о съеденном в любой удобной форме: аудио, фото тарелки или описание съеденного. \n\nХорошего и вкусного дня!"
    )
    await callback_query.message.answer(
        "Расскажи о последнем съеденном блюде с помощью фото, текста или голосового сообщения. \n\n<i>Например, напиши в чат или продиктуй: «Курица с рисом и огурцами. 200 г курицы, 100 г риса, 1 огурец».</i>"
    )
    
    await callback_query.answer()
    try:
        issuccess = await add_user_lesson(callback_query.from_user.id, "2")
        asyncio.create_task(log_bot_response(f"lesson 2 saved status{issuccess} ", callback_query.from_user.id))
    except Exception as e:
        print(e)

async def process_l2_step_2_2(callback_query, state):
    await state.clear()
    await callback_query.message.answer(
        "Хорошо! Но обязательно возвращайся завтра 💔   \n\nА сегодня в свободную минутку обязательно заполни дневник питания.   \n\nНажимай на кнопку после приёма пищи, чтобы проанализировать свой завтрак, обед или ужин.   \n\nЕсли хочешь посоветоваться с Нутри перед едой, сфотографируй тарелку или пришли её описания текстом или голосовым сообщением.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()
    


async def xyz(callback_query,state):
    await state.set_state(LessonStates2.step_4)
    await callback_query.message.answer(
        "Записала! А теперь прислушайся к себе и отметь, на сколько баллов ты чувствуешь насыщение.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="4–5: по-прежнему есть лёгкий голод", callback_data="next"), 
             InlineKeyboardButton(text="8–9: я переел (а), есть тяжесть", callback_data="stop")],
             [InlineKeyboardButton(text="6–7: наелся (лась), в самый раз", callback_data="next"), 
             InlineKeyboardButton(text="10: съел (а) так много, что мне плохо", callback_data="stop")]
        ])
    )

async def process_l2_step_4_1(callback_query, state):
    await state.set_state(LessonStates2.step_5)
    await callback_query.message.answer(
        "Отличная работа, горжусь тобой! Продолжай есть медленно и тщательно пережёвывать в следующие приёмы пищи, чтобы не случилось перееданий!"
    )

async def process_l2_step_4_2(callback_query, state):
    await state.set_state(LessonStates2.step_5)
    link = "https://www.medicalnewstoday.com/articles/14085"
    text = f"Так бывает! \nВот что советую прямо сейчас: \n\n1.<b>Не кори себя</b> \nТы только в начале пути, и мы только начали учиться. \n\n2.<b>Не ложись спать</b> \nПоговорка «после плотного обеда по закону Архимеда полагается поспать» вводит в заблуждение. \n\nДа, это хочется сделать после переедания. Но так ты увеличиваешь риск того, что что кислота из желудка <a href=\'{link}\'>начнёт забрасываться</a> в пищевод. Это может вызвать изжогу, станет только хуже. \n\n3.<b>Лучше погуляй</b> \nДаже 15 минут помогут почувствовать себя лучше. \n\n4.<b>В следующий раз ешь медленнее</b> \nДумай о том, правда ли хочешь съесть следующий кусочек. Доедать не обязательно."
    await callback_query.message.answer(text, disable_web_page_preview=True)

async def process_l2_step_4(callback_query, state):
    await callback_query.message.answer(
        "Не забудь занести в дневник питания следующий приём пищи! \n\nЕсли хочешь заранее проверить калорийность блюда, можешь прислать его фото или описание в чат, и я дам совет."
    )
    media_files = [
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
        InputMediaPhoto(media=IMG10)
    ]
    await callback_query.message.answer_media_group(media=media_files)
    link = "https://telegra.ph/Kak-naedatsya-no-ne-pereedat-istochniki-informacii-07-21"
    text = f"<b>Как наедаться, но не переедать</b> \n\n«Нутри, а что делать, если я вроде бы наедаюсь, но через полчаса опять приходит чувство голода? Или вроде бы голода нет, но всё равно хочется чего-нибудь сладкого или солёного?» \n\nКак поесть так, чтобы наесться — действительно целая наука. Ближайшие 3 недели мы будем её изучать. А пока листай к карточки с самыми простыми правилами, которые помогут тебе утолить голод и при этом не переесть. \n\nИсточники информации, по которым мы написали эти карточки — <a href=\'{link}\'>по ссылке.</a>"
    await callback_query.message.answer(text, disable_web_page_preview=True, 
    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
    await callback_query.answer()
    ############ EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING EVENING_PING #############

async def process_l2_step_11(callback_query, state):
    await callback_query.message.answer(
        "Завершился второй день с Нутри, и ты по-прежнему здесь! 🎉 Кажется, у тебя серьёзные намерения! \n\nКак тебе наше общение? Удалось ли сделать задание дня и хотя бы разочек определить уровень насыщения?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да!", callback_data="next"),InlineKeyboardButton(text="Нет, давай сделаем сейчас", callback_data="stop")]]))
    await callback_query.answer()

async def process_l2_step_12(callback_query, state):
    await callback_query.message.answer("Класс! Люблю обстоятельный подход к делу. Уверена, если ты продолжишь в том же темпе, через пару недель уже заметишь результат! \n\nПродолжим завтра ❤️ \nХорошего тебе вечера!")
    await callback_query.answer()

async def process_l2_step_13(callback_query, state):
    await state.set_state(LessonStates2.step_12)
    await callback_query.message.answer("Занеси последний приём пищи в дневник питания с помощью текста или голосового сообщения. \n\nОпиши состав блюда и примерный вес ⚖️ \n\n<i>Например: Чебурек с мясом, примерно 300 граммов.</i>")
    await callback_query.answer()

async def xyz2(callback_query, state):
    await state.set_state(LessonStates2.step_13)
    await callback_query.message.answer(
        "Записала! А теперь прислушайся к себе и отметь, на сколько баллов ты чувствуешь насыщение.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="4–5: по-прежнему есть лёгкий голод", callback_data="next"), 
             InlineKeyboardButton(text="8–9: я переел (а), есть тяжесть", callback_data="stop")],
             [InlineKeyboardButton(text="6–7: наелся (лась), в самый раз", callback_data="next"), 
             InlineKeyboardButton(text="10: съел (а) так много, что мне плохо", callback_data="stop")]
        ])
    )

async def process_l2_step_14_1(callback_query, state):
    await callback_query.message.answer(
        "Отличная работа, горжусь тобой! Продолжай есть медленно и тщательно пережёвывать в следующие приёмы пищи, чтобы не случилось перееданий!"
    )

async def process_l2_step_14_2(callback_query, state):
    link = "https://www.medicalnewstoday.com/articles/14085"
    text = f"Так бывает! \nВот что советую прямо сейчас: \n\n1.<b>Не кори себя</b> \nТы только в начале пути, и мы только начали учиться. \n\n2.<b>Не ложись спать сразу после еды</b>  \nДа, это хочется сделать после переедания. Но так ты увеличиваешь риск того, что что кислота из желудка <a href=\'{link}\'>начнёт забрасываться</a> в пищевод. Это может вызвать изжогу, станет только хуже. \n\n3.<b>Лучше погуляй</b> \nДаже 15 минут помогут почувствовать себя лучше. \n\n4.<b>В следующий раз ешь медленнее</b> \nДумай о том, правда ли хочешь съесть следующий кусочек. Доедать не обязательно."
    await callback_query.message.answer(text, disable_web_page_preview=True)

async def process_l2_step_14(callback_query, state):
    await callback_query.message.answer(
        "А пока поздравляю с завершением второго дня и верю, что плавно помогу тебе перестроиться на новый режим питания. \n\nПродолжим завтра ❤️ \nХорошего тебе вечера!"
    )
