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
CITY_ASSISTANT_ID = os.getenv("CITY_ASSISTANT_ID")

# IMG1 = "AgACAgIAAxkBAAIBNGeb_tu4yBOsz2-sDzPYYXUnWgzKAAIo4jEbaQvgSAw5usWAGBI6AQADAgADeQADNgQ"
# IMG2 = "AgACAgIAAxkBAAIBOGeb_uF2DBu8vwy4yAtDOuwtepHRAAIp4jEbaQvgSAcx4I3mM6pdAQADAgADeQADNgQ"
# IMG3 = "AgACAgIAAxkBAAIBRGeb_vhtj5spM5DEL2Y_C--j2ipUAAIs4jEbaQvgSNUedpEuLn5CAQADAgADeQADNgQ"
# IMG4 = "AgACAgIAAxkBAAIBPGeb_un_uAwNoElxdjt9xHOCiLoYAAIq4jEbaQvgSA7-22yWnlE8AQADAgADeQADNgQ"
# IMG5 = "AgACAgIAAxkBAAIBQGeb_vH5BhY44cE4Y1bGKja0YmxiAAIr4jEbaQvgSLUl0FYt3LRJAQADAgADeQADNgQ"
# IMG6 = "AgACAgIAAxkBAAIBSGeb_wTvPaRty8giiJ4ty4hgIOScAAIt4jEbaQvgSHP4M3wlKZt_AQADAgADeQADNgQ"
# IMG7 = "AgACAgIAAxkBAAIBTGeb_wvV4EvYfmQ7yVV1PeZtgKoLAAIu4jEbaQvgSBsBOYuwPPQRAQADAgADeQADNgQ"
# IMG8 = "AgACAgIAAxkBAAIBUGeb_xIecDerLszcSJ64OSbyPNyxAAIv4jEbaQvgSFANxSVekJwlAQADAgADeQADNgQ"
# IMG9 = "AgACAgIAAxkBAAIBVGeb_xj5C7ZigNR0vMIyoBaut02gAAIw4jEbaQvgSMu7vY1tCdzJAQADAgADeQADNgQ"

# IMG10 = "AgACAgIAAxkBAAIBWGecA5dsf2OriobXiC-17r5_8K6gAAIx4jEbaQvgSNZxXaMawsFFAQADAgADeQADNgQ"
# IMG11 = "AgACAgIAAxkBAAIBXGecA54_-uc29nPhwteLnjrCoN0fAAIy4jEbaQvgSFMxd_Xx3bDuAQADAgADeQADNgQ"
# IMG12 = "AgACAgIAAxkBAAIBXmecA6SMl4eYAl8erQKWr9pXsc24AAIz4jEbaQvgSOCio8PwbvnVAQADAgADeQADNgQ"
# IMG13 = "AgACAgIAAxkBAAIBZmecA7TbMfRBey4LiWOT-0ZXZVoVAAI04jEbaQvgSK4foXut4QcOAQADAgADeQADNgQ"
# IMG14 = "AgACAgIAAxkBAAIBamecA7xiY7cWzt6gtsRJDbsbzHVeAAI14jEbaQvgSFz65Zzip3MIAQADAgADeQADNgQ"
# IMG15 = "AgACAgIAAxkBAAIBbmecA8LjgQH_0EALNLVX3blTE3JRAAI24jEbaQvgSOqy6E3LZAb_AQADAgADeQADNgQ"
# IMG16 = "AgACAgIAAxkBAAIBcmecA8cEgt_UPCbzAqKVKTtPJwNKAAI34jEbaQvgSFo2OCCBpuJeAQADAgADeQADNgQ"

IMG1 = "AgACAgIAAxkBAAEEcAhn2v1KPgmTDVa8wQxs-tsDL09mZwACy_UxG1ap2UqCBP_7Zx4zkQEAAwIAA3kAAzYE"
IMG2 = "AgACAgIAAxkBAAEEcBVn2v1TVyVwFv7nDn5of_Wv3ReWowACzPUxG1ap2UoNsN2E1DBRFAEAAwIAA3kAAzYE"
IMG3 = "AgACAgIAAxkBAAEEcB9n2v1nQokf1sl-EicUzpdCiPWjcAAC0PUxG1ap2UpHfekY4BmDlAEAAwIAA3kAAzYE"
IMG4 = "AgACAgIAAxkBAAEEcBln2v1a74nOV1Jx0Py3F-pWKeBLOAACzvUxG1ap2Uo3_HFmCd_lVwEAAwIAA3kAAzYE"
IMG5 = "AgACAgIAAxkBAAEEcBxn2v1gOJypQXCV6qjohOYtXD6x2AACz_UxG1ap2Ur4h_diEQHwfAEAAwIAA3kAAzYE"
IMG6 = "AgACAgIAAxkBAAEEcCJn2v1vQZIbw-nvpz--Nd9puSSoLgAC0fUxG1ap2UqQYUoRIBwr8QEAAwIAA3kAAzYE"
IMG7 = "AgACAgIAAxkBAAEEcCVn2v14Kz_GPjQNZQ-uYTc_iYcV6wAC0vUxG1ap2UoWzykOth9tmwEAAwIAA3kAAzYE"
IMG8 = "AgACAgIAAxkBAAEEcChn2v2B5PL9sCJWA1HJSGCfKkOZ8QAC0_UxG1ap2Up7MZzDT9kWWAEAAwIAA3kAAzYE"
IMG9 = "AgACAgIAAxkBAAEEcCtn2v2IBklcMSrlfRL5iK6I2-wk0wAC1fUxG1ap2UpTajZYiC-WEwEAAwIAA3kAAzYE"

IMG10 = "AgACAgIAAxkBAAEEcEpn2v6MW3VYJUyIVg4oXFMeus50KQAC3PUxG1ap2Uo1UzWCgPaOEQEAAwIAA3kAAzYE"
IMG11 = "AgACAgIAAxkBAAEEcE1n2v6RrcwD7yHZRkFoVMtcfojCowAC3fUxG1ap2UoJAjpOSItaBgEAAwIAA3kAAzYE"
IMG12 = "AgACAgIAAxkBAAEEcFBn2v6axhyk9owHwmBWAAEXhS4MR0YAAt71MRtWqdlKrHacXEdMZV0BAAMCAAN5AAM2BA"
IMG13 = "AgACAgIAAxkBAAEEcFNn2v6iCxHkBHDdOkQWyjOqljtDTAAC3_UxG1ap2UowLO7Fw9iGpgEAAwIAA3kAAzYE"
IMG14 = "AgACAgIAAxkBAAEEcFhn2v6uwfmHwA7qva0KXR0hyGAtHgAC4PUxG1ap2UpvoQ_GgRf3iAEAAwIAA3kAAzYE"
IMG15 = "AgACAgIAAxkBAAEEcFxn2v63_G2AcZsAAYYfxxgfyPfbZqAAAuH1MRtWqdlKniihs_5WwgUBAAMCAAN5AAM2BA"
IMG16 = "AgACAgIAAxkBAAEKgX9oNKi7sZtueLBB8VpO2tnKzkiGrAACV_YxG1FZoUm7hcdohtBr3QEAAwIAA3kAAzYE"

ADD_IMG_1 = "AgACAgIAAxkBAAEHZeZoEWVEG1K8zhxx1D5HayiddU2p_AACTvQxG4dsiUhJ8DL-jB3JlwEAAwIAA3kAAzYE"
ADD_IMG_2 = "AgACAgIAAxkBAAEHZfJoEWV1pbUIGwYim-O2YgABdo5kkvEAAn35MRs6RIhItW3sVBZUHwMBAAMCAAN5AAM2BA"
ADD_IMG_3 = "AgACAgIAAxkBAAEHZepoEWVX6TLhtikxLa4NXw6gW9qo9gACe_kxGzpEiEi5dqYcYfsruwEAAwIAA3kAAzYE"
ADD_IMG_4 = "AgACAgIAAxkBAAEHZe5oEWVroLIu7N-9K4KcrYss2GMFzwACfPkxGzpEiEjRBQtxkaBRuQEAAwIAA3kAAzYE"
ADD_IMG_5 = "AgACAgIAAxkBAAEHZfZoEWWRbjNxwPlBil6WZqStwZyXzgACfvkxGzpEiEiiC_55JbaX7wEAAwIAA3kAAzYE"
ADD_IMG_6 = "AgACAgIAAxkBAAEHZfpoEWWZwzIymGkd8Adqn3WAnIexdAACf_kxGzpEiEj1EV-c520pagEAAwIAA3kAAzYE"
ADD_IMG_7 = "AgACAgIAAxkBAAEHZgJoEWWkys4peASKFi4IuU1cRDh7CgACgPkxGzpEiEiwggb2u2OI0QEAAwIAA3kAAzYE"

def calculate_pal(hours_light, hours_heavy):
    effective_hours = hours_light + 1.5 * hours_heavy

    if effective_hours < 1:
        pal = 1.4
    elif effective_hours < 3:
        pal = 1.5
    elif effective_hours < 5:
        pal = 1.6
    elif effective_hours < 7:
        pal = 1.75
    else:
        pal = 1.9

    return pal

async def calculate(state):
    user_data = await state.get_data()
    goal = user_data['goal']
    weight = round(float(user_data['weight'].replace(",", ".")))
    height = round(float(user_data['height'].replace(",", ".")))
    age = int(user_data['age'])
    gender = user_data['gender']
    pregnancy = user_data['pregnancy']
    activity_l = round(float(user_data["jogging"].replace(",", ".")))
    activity_h = round(float(user_data["lifting"].replace(",", ".")))
    pal = calculate_pal(activity_l, activity_h)
    
    bonus = weight*0.5*activity_h
    bmr1 = round(10*weight + 6.25*height - 5*age)

    if gender == "male":
        bmr = bmr1 +5
    elif gender == "female":
        bmr = bmr1 -161

    await state.update_data(bmr=bmr)

    # tdee1 = round(bmr*1.55)
    tdee1 = round(bmr * pal + bonus)
    if pregnancy == "true":
        tdee = tdee1+500
    else:
        tdee = tdee1
    await state.update_data(tdee=tdee)

    height_m = height/100
    height_m_sq = round(height_m*height_m)
    bmi = round(weight/height_m_sq)
    ideal_weight_low = round(height_m_sq*18.5)
    ideal_weight_high = round(height_m_sq*25)
    await state.update_data(bmi=bmi)
    await state.update_data(ideal_weight_low=ideal_weight_low)
    await state.update_data(ideal_weight_high=ideal_weight_high)
    if goal == "?":
        if bmi > 25:
            goal = "-"
        elif 18.5 <= bmi <= 25:
            goal = "="
        elif bmi <18.5:
            goal = "+"
    await state.update_data(goal=goal)

async def calculate_w_loss_amount(state, goal):
    state_data = await state.get_data()
    ideal_w_l = state_data["ideal_weight_low"]
    ideal_w_h = state_data["ideal_weight_high"]
    user_w = round(float(state_data['weight'].replace(",", ".")))
    
    if goal == "+":
        user_weight_diff = int(ideal_w_l)-int(user_w)
        amount = int(user_w/10)
        if abs(user_weight_diff)<= amount:
            amount = abs(user_weight_diff)
        return f"Советую тебе набрать {amount} кг\n Но финальное решение все равно за тобой, сколько хочешь набрать?"
    elif goal == "-":
        user_weight_diff = int(user_w)-int(ideal_w_h)
        amount = int(user_w/10)
        if abs(user_weight_diff) <= amount:
            amount = abs(user_weight_diff)
        return f"Советую тебе сбросить {amount} кг \n Но финальное решение все равно за тобой, сколько хочешь скинуть?"


async def gen_text(state):
    user_data = await state.get_data()
    goal = user_data['goal']
    tdee = user_data['tdee']
    bmr = user_data['bmr']
    pregnancy = user_data['pregnancy']
    breastfeeding = user_data['breastfeeding']
    calories_per_gram_carbs = 4
    calories_per_gram_proteins = 4
    calories_per_gram_fats = 9
    carbs_percentage = 0.55
    proteins_percentage = 0.225
    fats_percentage = 0.275
    if goal == "+":
        target_calories = tdee + 500
    elif goal == "-":
        target_calories = tdee - 500
    elif goal == "=":
        target_calories = tdee
    proteins_grams = round((target_calories*proteins_percentage)/calories_per_gram_proteins)
    carbs_grams = round((target_calories*carbs_percentage)/calories_per_gram_carbs)
    fats_grams = round((target_calories*fats_percentage)/calories_per_gram_fats)
    await state.update_data(target_calories=target_calories)
    
    text_preg = f"Во время беременности важно обеспечить достаточное количество питательных веществ для поддержки здоровья матери и ребёнка. Традиционные методы расчета дефицита или избытка калорий для снижения или набора веса не применяются в период беременности. Вместо этого фокус делается на сбалансированном питании, достаточном количестве калорий и питательных веществах.\n\nОднако я могу рассчитать твой базовый уровень метаболизма (BMR) и общую суточную потребность в энергии (TDEE) для информационных целей, используя формулу Mifflin-St Jeor, так как она считается одной из самых точных.\n\n- Базовый уровень метаболизма (BMR): примерно <b>{bmr}</b> ккал/день.\n- Общая суточная потребность в энергии (TDEE) при вашей активности: примерно <b>{tdee}</b> ккал/день.\n\nВажно подчеркнуть, что эти расчеты предназначены только для информации и не должны использоваться для создания дефицита или избытка калорий во время беременности. Ваши пищевые потребности в этот период могут отличаться, и вам следует проконсультироваться с врачом, чтобы определить оптимальное питание для поддержания здоровья вашего и вашего ребенка."
    text_gain = f"Для постепенного и контролируемого набора массы рекомендую увеличить целевое количество калорий: примерно <b>{target_calories}</b> ккал/день (это на 500 ккал больше, чем ваш TDEE).\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\nЭти рекомендации учитывают твой текущий вес, твою цель и физическую активность. Основная цель — обеспечить твой организм достаточным количеством энергии и питательных веществ для построения мышечной массы. Важно сосредоточиться на качестве потребляемой пищи, включая достаточное количество белка для поддержки мышечного роста, здоровых жиров и сложных углеводов."
    text_gain_bf = f"Рекомендую тебе есть примерно <b>{target_calories}</b> ккал/день (это на 500 ккал больше, чем ваш TDEE).\n\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\nЭти расчёты учитывают дополнительные потребности в калориях для кормления грудью. Однако важно помнить, что каждый организм уникален, и потребности могут варьироваться. Перед началом любой диеты или программы питания, особенно во время кормления грудью, рекомендуется проконсультироваться с врачом."
    text_loss = f"Для безопасного и постепенного похудения (около 0,5 кг в неделю) рекомендую тебе есть примерно <b>{target_calories}</b> ккал/день (это на 500 ккал меньше, чем ваш TDEE).\n\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\n\nПри таком плане питания предполагаемая потеря веса может составить около 0,5 кг в неделю, учитывая дефицит в 500 ккал в день. Эти значения являются ориентировочными и могут варьироваться в зависимости от индивидуальных особенностей организма, уровня активности и других факторов."
    text_loss_bf = f"Для безопасного и постепенного похудения (около 0,5 кг в неделю) рекомендую уменьшить целевое количество калорий и есть примерно <b>{target_calories}</b> ккал/день (это на 500 ккал меньше, чем ваш TDEE).\n\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\n\nПри таком плане питания предполагаемая потеря веса может составить около 0,5 кг в неделю, учитывая дефицит в 500 ккал в день. Важно! При кормлении грудью тебе и ребенку нужно много питательных веществ. Поэтому перед началом диеты или программы похудения настоятельно рекомендуется проконсультироваться с врачом."
    text_keep = f"C удовольствием помогу тебе правильно питаться и чувствовать себя лучше с каждым днём. Чтобы оставаться в текущем весе, рекомендую тебе есть около <b>{target_calories}</b> ккал/день — это как раз твоя суточная потребность в энергии.\n\nРаспределение макронутриентов при таком количестве калорий <b>{target_calories}</b> ккал/день:\n\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\n\nПостараемся вместе сделать твоё питание более разнообразным и сбалансированным!"
    
    if pregnancy == "True": return text_preg
    else: 
        if goal == "=": return text_keep
        elif goal == "+":
            if breastfeeding == "True":
                return text_gain_bf
            else: return text_gain
        elif goal == "-":
            if breastfeeding == "True":
                return text_loss_bf
            else: return text_loss


async def process_prefirst(message, state):
    text = f"{message.from_user.first_name},\n\nЯ очень рада, что теперь у меня есть такой приятный собеседник как ты!\n\nСделаю всё, чтобы ты смог(ла) комфортно прийти к своим целям!\n\nНо сначала эти цели нужно правильно поставить. Для этого я задам несколько важных вопросов.\n\nОтветы займут не больше 5 минут и помогут мне создать персональный план питания под твои параметры и запросы.\n\nРасскажешь мне о себе?"
    buttons = [
        [InlineKeyboardButton(text="Конечно!", callback_data="next")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)

# async def process_first(message, state):
#     text = f"Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно" 
#     await message.answer(text, reply_markup=None)

async def process_first(message, state):
    text = f"<b>Как могу к тебе обращаться?</b>"
    await message.answer(text, reply_markup=None)

async def process_mail(message, state):
    answer = await check_mail(message.from_user.id, message.text)
    print(answer)
    if answer == "true":
        text = "Поздравляю!\nУ тебя есть подписка на Нутри 🥂"
        buttons = [
        [InlineKeyboardButton(text="Начать урок 1", callback_data="lesson_0_done")],
        [InlineKeyboardButton(text="В меню ⏏️", callback_data="menu_back")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text, reply_markup=keyboard)
        await state.set_state(UserState.menu)
    elif answer == "false":
        # await state.clear()
        text = "Кажется, у тебя еще нет подписки на Нутри. \nХочешь оформить сейчас с супер скидкой -70%?"
        buttons = [
        [InlineKeyboardButton(text="Да, купить со скидкой -70%", callback_data="send_purchase_add")], #url="https://nutri-ai.ru/?promo=nutribot&utm_medium=referral&utm_source=telegram&utm_campaign=nutribot"
        [InlineKeyboardButton(text="Попробовать еще раз", callback_data="retry_mail")],
        [InlineKeyboardButton(text="🆘 Написать в поддержку", url="t.me/ai_care")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text, reply_markup=keyboard)

async def process_ad_to_buy(callback_query, state):
    text = "🔥 <b>ВАУ! -70% на подписку Nutri + крутые подарки!</b> 🔥\n\nОплачивай подписку сейчас по <b>суперцене</b> и <b>получай бонусы</b>, которые помогут тебе прокачать питание, здоровье и осознанность!\n\n💎 НАВСЕГДА -70%\nвсего <b>3 590₽</b> вместо  <b><s>13 300₽</s></b>!\n\n🎁 <b>3 недели обучения</b> – курс по нутрициологии, чтобы ты точно знал, как питаться сбалансировано.\n🎁 <b>1 год подписки на Prosto</b> – приложение №1 для медитаций от Ирены Понарошку.\n🎁 <b>Умные весы Picooc Basic</b> – если пройдешь курс и ежедневно будешь заполнять дневник питания в первый месяц.\n\n💎 НА 1 ГОД -70%\nвсего <b>2 990₽</b> вместо <b><s>9 990₽</s></b>!\n\n💎 НА 3 МЕСЯЦА -70%\nвсего <b>1 990₽</b> вместо  <b><s>6 600₽</s></b>!\n\n⏰ <b>Только 24 часа! Успей забрать Nutri по лучшей цене и бонусы! Жми на кнопку!</b>"
    buttons = [[InlineKeyboardButton(text="Купить", url="https://nutri-ai.ru/?promo=nutribot&utm_medium=referral&utm_source=telegram&utm_campaign=nutribot")]]
    media_group = [
        InputMediaPhoto(media=ADD_IMG_1, caption="<b>Скидка -70% только для тебя</b> 💚\n\nЧто входит в любой тариф👇"),
        InputMediaPhoto(media=ADD_IMG_2),
        InputMediaPhoto(media=ADD_IMG_3),
        InputMediaPhoto(media=ADD_IMG_4),
        InputMediaPhoto(media=ADD_IMG_5),
        InputMediaPhoto(media=ADD_IMG_6),
        InputMediaPhoto(media=ADD_IMG_7),
        ]
    await callback_query.message.answer_media_group(media=media_group)
    await callback_query.message.answer(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_reanket(callback_query, state):
    text = "<b>Как тебя зовут?</b>"
    await callback_query.message.edit_text(text)
    

async def process_name(message, state):
    link = "https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm"
    text1 = f"<b>Часть 1/4\n4 вопроса о тебе</b>\n{message.text}, при составлении твоего плана питания я буду ориентироваться на КБЖУ: твою норму калорий, белков, жиров и углеводов.\n\nЧтобы рассчитать её, <a href=\'{link}\'>мне нужно узнать</a> твой пол, возраст, вес и рост: если для роста 155 см вес в 50 кг — норма, то для роста 180 см это уже очень мало."
    text = "🟢⚪️⚪️⚪️ \nТвой пол"
    buttons = [
        [InlineKeyboardButton(text="Женский", callback_data="female")],
        [InlineKeyboardButton(text="Мужской", callback_data="male")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text1)
    await message.answer(text, reply_markup=keyboard)

async def process_gender(message, state):
    text = "Тогда еще пара важных вопросов, которые влияют на рекомендации (например, можно ли вам алкоголь).\n\nТы беременна?"
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="True")],
        [InlineKeyboardButton(text="Нет", callback_data="False")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_f_preg(message, state):
    text = "Кормишь грудью?"
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="True")],
        [InlineKeyboardButton(text="Нет", callback_data="False")],
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
    asyncio.create_task(log_bot_response("🟢🟢🟢🟢", message.from_user.id))
    await message.answer(text1)
    await message.answer(text)

async def process_age(message, state):
    link = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5108589/"
    text1 = "Спасибо за доверие!"
    text2 = "🟠⚪️⚪️⚪️⚪️ \nСколько воды ты пьёшь в день? \nВопрос про чистую воду, чай и кофе не в счёт!"
    text = f"<b>Часть 2/4\n5 вопросов о питании</b>\n\nПривычки не меняются за один день. Резко начинать новую жизнь «с понедельника» — <a href=\'{link}\'>верный путь к срывам.</a> Ты продержишься неделю-другую, получишь первые результаты, а потом так же стремительно откатишься назад.\n\nЧтобы этого не случилось, я построю плавный путь из твоей исходной точки к цели. Для этого мне важно знать, как ты питаешься сейчас. Я задам 5 вопросов, на которые важно ответить честно."
    buttons = [
        [InlineKeyboardButton(text="Пару стаканов или меньше", callback_data="<2")],
        [InlineKeyboardButton(text="3–5 стаканов", callback_data="3-5")],
        [InlineKeyboardButton(text="6 стаканов и больше", callback_data=">6")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text1)
    await message.answer(text)
    await message.answer(text2, reply_markup=keyboard)

async def process_water(message, state):
    text = "🟠🟠⚪️⚪️⚪️ \nКак часто ты пьёшь алкоголь?"
    buttons = [
        [InlineKeyboardButton(text="Вообще не пью", callback_data="0")],
        [InlineKeyboardButton(text="Меньше 2х бокалов/рюмок в неделю", callback_data="<2")],
        [InlineKeyboardButton(text="Меньше 7 бокалов/рюмок в неделю", callback_data="2-6")],
        [InlineKeyboardButton(text="Больше 7 бокалов в неделю", callback_data=">7")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_booze(message, state):
    text = "🟠🟠🟠⚪️⚪️\nСколько у тебя приёмов пищи в день,  включая перекусы?"
    buttons = [
        [InlineKeyboardButton(text="1", callback_data="1")],
        [InlineKeyboardButton(text="2", callback_data="2")],
        [InlineKeyboardButton(text="3", callback_data="3")],
        [InlineKeyboardButton(text="4", callback_data="4")],
        [InlineKeyboardButton(text="5", callback_data="5")],
        [InlineKeyboardButton(text="6+", callback_data="6+")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_meals(message, state):
    text = "🟠🟠🟠🟠⚪️\nКакие это приёмы пищи?   \n\nОпиши в паре предложений свой обычный режим питания и отправь их в чат.  \n\nНапример:  \n<i>«Обычно пропускаю завтрак, но плотно обедаю и ужинаю». \n«Ем три раза в день, два раза перекусываю сладким». \n«Нет режима питания, делаю большие перерывы между едой».</i>"
    buttons = [
        [InlineKeyboardButton(text="Пропустить", callback_data="None")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_meals_extra(message, state):
    text = "🟠🟠🟠🟠🟠\nЕсть ли продукты или компоненты, которые ты не ешь?  \nНапиши про них в чат.  \n\nНапример:  \n<i>«Не ем мясо и птицу»  \n«Не ем молочные продукты» \n«Не ем глютен»</i>"
    buttons = [
        [InlineKeyboardButton(text="Ем всё!", callback_data="None")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)

async def process_allergies(message, state):
    link1 = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5964031/"
    link2 = "https://pmc.ncbi.nlm.nih.gov/articles/PMC9031614/"
    link3 = "https://www.sciencedaily.com/releases/2009/08/090803185712.htm"
    text = f"<b>Часть 3/4 \n4 вопроса об образе жизни</b>\nОсознанное питание — это не только еда. Чтобы выстроить здоровые отношения с едой, важно <a href=\'{link1}\'>научиться работать с эмоциями</a>, <a href=\'{link2}\'>наладить режим сна</a>, <a href=\'{link3}\'>установить контакт с телом</a>, быть физически активными.\n\nЭтому мы будем учиться на курсе, который мы составили вместе с нутрициологами. Но сначала мне нужно понять: какой ритм жизни у тебя сейчас?\n\nБуквально 4 вопроса, и мы размеренно и с удовольствием пойдём вперед к твоим целям!"
    buttons = [
        [InlineKeyboardButton(text="Задавай!", callback_data="next")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)

async def process_part3(message, state):
    text = "🔵⚪️⚪️⚪️ \nСколько часов в неделю ты уделяешь <b>лёгким и средним физическим нагрузкам:</b> бегу, быстрой ходьбе, йоге, плаванию, танцам или другим игровым видам спорта?\n\n 🚫 Кроме силовых и выосокинтенсивных функциональных тренировок."
    buttons = [
        [InlineKeyboardButton(text="Не занимаюсь вообще", callback_data="0")],
        [InlineKeyboardButton(text="Меньше 3 ч — редкие тренировки", callback_data="2")],
        [InlineKeyboardButton(text="От 3 до 5 ч — регулярные занятия", callback_data="4")],
        [InlineKeyboardButton(text=" Больше 5 ч — интенсивный режим", callback_data="5")],
    ]
    await message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_jogging(message, state):
    text = "🔵🔵⚪️⚪️\nА сколько часов в неделю ты занимаешься <b>силовыми или высокоинтенсивными функциональными тренировками?</b>"
    buttons = [
        [InlineKeyboardButton(text="Не занимаюсь силовыми", callback_data="0")],
        [InlineKeyboardButton(text="Меньше 3 ч — редкие тренировки", callback_data="2")],
        [InlineKeyboardButton(text="От 3 до 5 ч — регулярные занятия", callback_data="4")],
        [InlineKeyboardButton(text=" Больше 5 ч — интенсивный режим", callback_data="5")],
    ]
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_lifting(message, state):
    text = "🔵🔵🔵⚪️\nКстати, как ты оцениваешь свой текущий уровень стресса?  \nСпойлер: длительный стресс <u>мешает</u> сбрасывать вес."
    buttons = [
        [InlineKeyboardButton(text="Низкий", callback_data="low")],
        [InlineKeyboardButton(text="Средний", callback_data="mid")],
        [InlineKeyboardButton(text="Высокий", callback_data="high")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)

async def process_stress(message, state):
    link = "https://pmc.ncbi.nlm.nih.gov/articles/PMC9031614/"
    text = f"🔵🔵🔵🔵\nА сколько часов ты спишь в будние дни?   \nСпойлер №2: из-за недосыпа мы <a href=\'{link}\'>переедаем.</a>"
    buttons = [
        [InlineKeyboardButton(text="6–8 часов", callback_data="6-8"), InlineKeyboardButton(text="Меньше 6 часов", callback_data="<6")],
        [InlineKeyboardButton(text="8 и больше часов", callback_data=">8"), InlineKeyboardButton(text="Нет режима сна", callback_data="random")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_sleep(message, state):
    text = "Ура, мы закончили! Теперь самое главное: определимся с целью. Моя задача — помочь тебе выстроить гармоничные отношения с едой.  \nНо это довольно абстрактная цель, к такой тяжело идти. Попробуем придумать что-то более конкретное!   \n\nИтак, к какой цели мы будем идти ближайший месяц?"
    buttons = [
        [InlineKeyboardButton(text="Похудеть", callback_data="-")],
        [InlineKeyboardButton(text="Набрать мышечную массу", callback_data="+")],
        [InlineKeyboardButton(text="Сохранить вес, выстроить рацион", callback_data="=")],
        [InlineKeyboardButton(text="Нутри, поставь цель за меня", callback_data="?")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_goal(message, state, goal):
    text_add = "Знаешь, сколько кг хочешь набрать?"
    text_remove = "Знаешь, сколько кг хочешь скинуть?"
    if goal == "+":
        text = text_add
    elif goal == "-":
        text = text_remove
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="yes")],
        [InlineKeyboardButton(text="Нет, Нутри, посчитай за меня", callback_data="no")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_w_loss(callback_query, state, goal):
    if callback_query.data == "yes":
        await callback_query.message.answer("Это уже высокий уровень осознанности в отношениях с едой! Напиши число в чат.\nНапример, «3» или «4.5».")
        await state.set_state(Questionnaire.w_loss_amount)
        return
    elif callback_query.data == "no":
        text = await calculate_w_loss_amount(state, goal)
        await callback_query.message.answer(text)

async def process_w_loss_amount(message, state, goal):
    text11 = "Считаю комфортную скорость похудения, чтобы результат закрепился надолго, а процесс тебе понравился!"
    text12 = "C удовольствием помогу тебе правильно питаться и чувствовать себя всё лучше с каждым днём!"
    if goal in ['+', '-']:
        text1 = text11
    elif goal in ['?', '=']:
        text1 = text12
    await message.answer(text1)

async def give_plan(message, state, input_text):
    # text = "Пока я составляю твой персональный план, почитай про общие принципы, которых мы будем придерживаться в ближайший месяц.\n\nОни помогут тебе не просто похудеть, но закрепить результат и не вернуться к исходному весу через полгода."
    # media_files = [
    #     InputMediaPhoto(media=IMG1, caption=text),
    #     InputMediaPhoto(media=IMG2),
    #     InputMediaPhoto(media=IMG3),
    #     InputMediaPhoto(media=IMG4),
    #     InputMediaPhoto(media=IMG5),
    #     InputMediaPhoto(media=IMG6),
    #     InputMediaPhoto(media=IMG7),
    #     InputMediaPhoto(media=IMG8),
    #     InputMediaPhoto(media=IMG9),
    # ]
    # await message.answer_media_group(media=media_files)
    # link = "https://telegra.ph/8-principov-osoznannogo-pitaniya-istochniki-informacii-07-16"
    # text2 = f"<b>8 принципов осознанного питания: чему мы будем учиться</b>\n\nНа картинках — главные принципы осознанного питания, на основе которых я даю рекомендации.\n\nОни довольно простые, но вот сделать их привычкой — настоящий челлендж. Но мы будем выполнять его вместе — и так победим ❤️ \n\nИсточники — <a href=\'{link}\'>по ссылке</a>."
    # await message.answer(text2)
    await message.answer(input_text)
    text4 = "План составлен! У нас есть тактика! Но как теперь её придерживаться? 🤔 Есть несколько идей на этот счёт!"
    await message.answer(text4)
    text5 = "<b>Часть 4/4\nНастройка напоминаний</b>\nЯ буду присылать тебе напоминания о том, что нам пора пообщаться!\n\n🟣⚪️⚪️\nПодскажи, в каком городе ты живёшь?\n\nСпрашиваю, чтобы напоминать о себе только в дневные часы."
    await message.answer(text5)

async def plan_info_dump(callback_query, state):
    text = "Почитай про общие принципы, которых мы будем придерживаться в ближайший месяц.\n\nОни помогут тебе не просто похудеть, но закрепить результат и не вернуться к исходному весу через полгода."
    media_files = [
        InputMediaPhoto(media=IMG1, caption=text),
        InputMediaPhoto(media=IMG2),
        InputMediaPhoto(media=IMG3),
        InputMediaPhoto(media=IMG4),
        InputMediaPhoto(media=IMG5),
        InputMediaPhoto(media=IMG6),
        InputMediaPhoto(media=IMG7),
        InputMediaPhoto(media=IMG8),
        InputMediaPhoto(media=IMG9),
    ]
    await callback_query.message.answer_media_group(media=media_files)
    buttons = [[InlineKeyboardButton(text="Все понятно!", callback_data="next")]]
    link = "https://telegra.ph/8-principov-osoznannogo-pitaniya-istochniki-informacii-07-16"
    text2 = f"<b>8 принципов осознанного питания: чему мы будем учиться</b>\n\nНа картинках — главные принципы осознанного питания, на основе которых я даю рекомендации.\n\nОни довольно простые, но вот сделать их привычкой — настоящий челлендж. Но мы будем выполнять его вместе — и так победим ❤️ \n\nИсточники — <a href=\'{link}\'>по ссылке</a>."
    await callback_query.message.answer(text2, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_city(message, state):
    user_data = await state.get_data()
    goal = user_data["goal"]
    goal_mapping = {"+": "Набрать", "-": "Похудеть", "=": "Сохранить вес"}
    goal_str = goal_mapping.get(goal)
    request_message = f"Цель: {goal_str}. Город: {message.text}"
    sticker_mssg = await message.answer_sticker(sticker=random.choice(STICKER_IDS))

    response = await run_city(request_message, CITY_ASSISTANT_ID)
    data = json.loads(response)
    response_text = data["response"]
    city = data["city"]
    timeslide = data["timeslide"]
    await state.update_data(timeslide=timeslide, city=city)
    text1 = response_text
    text2 = "🟣🟣⚪️\nЯ буду писать тебе один раз в день.\n\nВ какое время будет удобно получать напоминание о дневнике питания?\n\nУкажи время в формате ЧЧ:ММ\nНапример 10:00"
    
    await sticker_mssg.delete()
    await message.answer(text1),
    await message.answer(text2)

# async def process_morning_ping(message, state):
#     text = "🟣🟣🟣⚪️\nДоговорились! А во сколько присылать вечерние итоги?   \b\bУкажи время в формате ЧЧ:ММ \bНапример, 20:00"
#     await message.answer(text)

async def process_evening_ping(message, state):
    text = "🟣🟣🟣\nХочу пригласить тебя в наше сообщество <b>Нутри Ai: как есть, чтобы лучше жить!</b>\n\nТебя будут поддерживать и мотивировать нутрициологи, диетологи и другие специалисты.\n\nТолько для участников сообщества — прямые эфиры с экспертами, ответы на вопросы, полезные гайды и чек-листы. \n\nПодпишись на @nutri_community 💖 в Telegram"
    buttons = [
        [InlineKeyboardButton(text="Перейти", url="t.me/nutri_community")],
        [InlineKeyboardButton(text="Ок, готово", callback_data="next")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)

async def process_community_invite(message, state):
    text = "И снова договорились!\n\nИдея вторая. Я буду учить тебя пользоваться моими фичами. Все они помогают поесть вкусно и при этом не переесть. Постепенно мы будем учиться использовать каждую из функций.\n\nВ карточках рассказываю про каждую из них.\n\nСамостоятельно ты можешь вызвать любую функцию, кликнув на графу «Меню» в левом нижнем углу экрана. Помимо этого основные некоторые функции, например, «Дневник питания», всегда будут у тебя на виду внизу экрана."
    media_files = [
        InputMediaPhoto(media=IMG10),
        InputMediaPhoto(media=IMG11),
        InputMediaPhoto(media=IMG12),
        InputMediaPhoto(media=IMG13),
        InputMediaPhoto(media=IMG14),
        # InputMediaPhoto(media=IMG15),  #ПО ИДЕЕ ТА ФОТКА, КОТОРУЮ НАДО БЫЛО УБРАТЬ
        InputMediaPhoto(media=IMG16),
    ]
    await message.answer_media_group(media=media_files)
    buttons = [
        [InlineKeyboardButton(text="Хочу начать путь к своей цели!", callback_data="comm_inv_2_done")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)