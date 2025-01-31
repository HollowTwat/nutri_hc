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
    age = State()
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

IMG1 = "AgACAgIAAxkBAAIBNGeb_tu4yBOsz2-sDzPYYXUnWgzKAAIo4jEbaQvgSAw5usWAGBI6AQADAgADeQADNgQ"
IMG2 = "AgACAgIAAxkBAAIBOGeb_uF2DBu8vwy4yAtDOuwtepHRAAIp4jEbaQvgSAcx4I3mM6pdAQADAgADeQADNgQ"
IMG3 = "AgACAgIAAxkBAAIBRGeb_vhtj5spM5DEL2Y_C--j2ipUAAIs4jEbaQvgSNUedpEuLn5CAQADAgADeQADNgQ"
IMG4 = "AgACAgIAAxkBAAIBPGeb_un_uAwNoElxdjt9xHOCiLoYAAIq4jEbaQvgSA7-22yWnlE8AQADAgADeQADNgQ"
IMG5 = "AgACAgIAAxkBAAIBQGeb_vH5BhY44cE4Y1bGKja0YmxiAAIr4jEbaQvgSLUl0FYt3LRJAQADAgADeQADNgQ"
IMG6 = "AgACAgIAAxkBAAIBSGeb_wTvPaRty8giiJ4ty4hgIOScAAIt4jEbaQvgSHP4M3wlKZt_AQADAgADeQADNgQ"
IMG7 = "AgACAgIAAxkBAAIBTGeb_wvV4EvYfmQ7yVV1PeZtgKoLAAIu4jEbaQvgSBsBOYuwPPQRAQADAgADeQADNgQ"
IMG8 = "AgACAgIAAxkBAAIBUGeb_xIecDerLszcSJ64OSbyPNyxAAIv4jEbaQvgSFANxSVekJwlAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAIBVGeb_xj5C7ZigNR0vMIyoBaut02gAAIw4jEbaQvgSMu7vY1tCdzJAQADAgADeQADNgQ"

IMG10 = "AgACAgIAAxkBAAIBWGecA5dsf2OriobXiC-17r5_8K6gAAIx4jEbaQvgSNZxXaMawsFFAQADAgADeQADNgQ"
IMG11 = "AgACAgIAAxkBAAIBXGecA54_-uc29nPhwteLnjrCoN0fAAIy4jEbaQvgSFMxd_Xx3bDuAQADAgADeQADNgQ"
IMG12 = "AgACAgIAAxkBAAIBXmecA6SMl4eYAl8erQKWr9pXsc24AAIz4jEbaQvgSOCio8PwbvnVAQADAgADeQADNgQ"
IMG13 = "AgACAgIAAxkBAAIBZmecA7TbMfRBey4LiWOT-0ZXZVoVAAI04jEbaQvgSK4foXut4QcOAQADAgADeQADNgQ"
IMG14 = "AgACAgIAAxkBAAIBamecA7xiY7cWzt6gtsRJDbsbzHVeAAI14jEbaQvgSFz65Zzip3MIAQADAgADeQADNgQ"
IMG15 = "AgACAgIAAxkBAAIBbmecA8LjgQH_0EALNLVX3blTE3JRAAI24jEbaQvgSOqy6E3LZAb_AQADAgADeQADNgQ"
IMG16 = "AgACAgIAAxkBAAIBcmecA8cEgt_UPCbzAqKVKTtPJwNKAAI34jEbaQvgSFo2OCCBpuJeAQADAgADeQADNgQ"

async def calculate(state):
    user_data = await state.get_data()
    goal = user_data['goal']
    weight = int(user_data['weight'])
    height = int(user_data['height'])
    age = int(user_data['age'])
    gender = user_data['gender']
    pregnancy = user_data['pregnancy']

    bmr1 = round(10*weight + 6.25*height - 5*age)

    if gender == "male":
        bmr = bmr1 +5
    elif gender == "female":
        bmr = bmr1 -161

    await state.update_data(bmr=bmr)

    tdee1 = round(bmr*1.55)
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
    
    text_preg = f"Во время беременности важно обеспечить достаточное количество питательных веществ для поддержки здоровья матери и ребёнка. Традиционные методы расчета дефицита или избытка калорий для снижения или набора веса не применяются в период беременности. Вместо этого фокус делается на сбалансированном питании, достаточном количестве калорий и питательных веществах.\n\nОднако я могу рассчитать твой базовый уровень метаболизма (BMR) и общую суточную потребность в энергии (TDEE) для информационных целей, используя формулу Mifflin-St Jeor, так как она считается одной из самых точных.\n\n- Базовый уровень метаболизма (BMR): примерно <b>{bmr}</b> ккал/день.\n- Общая суточная потребность в энергии (TDEE) при умеренной активности: примерно <b>{tdee}</b> ккал/день.\n\nВажно подчеркнуть, что эти расчеты предназначены только для информации и не должны использоваться для создания дефицита или избытка калорий во время беременности. Ваши пищевые потребности в этот период могут отличаться, и вам следует проконсультироваться с врачом, чтобы определить оптимальное питание для поддержания здоровья вашего и вашего ребенка."
    text_gain = f"Для постепенного и контролируемого набора массы рекомендую увеличить целевое количество калорий: примерно <b>{target_calories}</b> ккал/день (это на 500 ккал больше, чем ваш TDEE).\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\nЭти рекомендации учитывают твой текущий вес, твою цель и умеренную физическую активность. Основная цель — обеспечить твой организм достаточным количеством энергии и питательных веществ для построения мышечной массы. Важно сосредоточиться на качестве потребляемой пищи, включая достаточное количество белка для поддержки мышечного роста, здоровых жиров и сложных углеводов."
    text_gain_bf = f"Рекомендую тебе есть примерно <b>{target_calories}</b> ккал/день (это на 500 ккал больше, чем ваш TDEE).\n\nРаспределение макронутриентов при целевом количестве калорий <b>{target_calories}</b> ккал/день:\n\n• Углеводы: примерно <b>{carbs_grams}</b> грамм (55% от общего количества калорий).\n• Белки: примерно <b>{proteins_grams}</b> грамм (22.5% от общего количества калорий).\n• Жиры: примерно <b>{fats_grams}</b> грамм (27.5% от общего количества калорий).\nЭти расчёты предполагают умеренную физическую активность и учитывают дополнительные потребности в калориях для кормления грудью. Однако важно помнить, что каждый организм уникален, и потребности могут варьироваться. Перед началом любой диеты или программы питания, особенно во время кормления грудью, рекомендуется проконсультироваться с врачом."
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

async def process_first(message, state):
    text = f"Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно"
    await message.answer(text, reply_markup=None)

async def process_mail(message, state):
    answer = await check_mail(message.from_user.id, message.text)
    print(answer)
    if answer == "true":
        text = "<b>Как тебя зовут?</b>"
        await message.answer(text)
    elif answer == "false":
        await state.clear()
        text = "К сожалению, я не нашла твою почту. Напиши пожалуйста в тех поддержку  @nutri_care"
        buttons = [
        [InlineKeyboardButton(text="Поддержка", callback_data="retry_mail")],
        [InlineKeyboardButton(text="Попробовать еще раз", url="t.me/nutri_care")],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text, reply_markup=keyboard)
    

async def process_name(message, state):
    link = "https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm"
    text1 = f"<b>Часть 1/3\n4 вопроса о тебе</b>\n{message.text}, при составлении твоего плана питания я буду ориентироваться на КБЖУ: твою норму калорий, белков, жиров и углеводов.\n\nЧтобы рассчитать её, <a href=\'{link}\'>мне нужно узнать</a>твой пол, возраст, вес и рост: если для роста 155 см вес в 50 кг — норма, то для роста 180 см это уже очень мало."
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
    await message.answer(text1)
    await message.answer(text)

async def process_age(message, state):
    link = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5108589/"
    text1 = "Спасибо за доверие!"
    text2 = "🟠⚪️⚪️⚪️⚪️ \nСколько воды ты пьёшь в день? \nВопрос про чистую воду, чай и кофе не в счёт!"
    text = f"<b>Часть 2/3\n5 вопросов о питании</b>\n\nПривычки не меняются за один день. Резко начинать новую жизнь «с понедельника» — <a href=\'{link}\'>верный путь к срывам.</a> Ты продержишься неделю-другую, получишь первые результаты, а потом так же стремительно откатишься назад.\n\nЧтобы этого не случилось, я построю плавный путь из твоей исходной точки к цели. Для этого мне важно знать, как ты питаешься сейчас. Я задам 5 вопросов, на которые важно ответить честно."
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
    text = f"<b>Часть 3/3 \n4 вопроса об образе жизни</b>\nОсознанное питание — это не только еда. Чтобы выстроить здоровые отношения с едой, важно <a href=\'{link1}\'>научиться работать с эмоциями</a>, <a href=\'{link2}\'>наладить режим сна</a>, <a href=\'{link3}\'>установить контакт с телом</a>, быть физически активными.\n\nЭтому мы будем учиться на курсе, который мы составили вместе с нутрициологами. Но сначала мне нужно понять: какой ритм жизни у тебя сейчас?\n\nБуквально 4 вопроса, и мы размеренно и с удовольствием пойдём вперед к твоим целям!"
    buttons = [
        [InlineKeyboardButton(text="Задавай!", callback_data="next")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(text, reply_markup=keyboard)

async def process_part3(message, state):
    text = "🔵⚪️⚪️⚪️ \nСколько часов в неделю ты уделяешь лёгким и средним физическим нагрузкам: бегу, быстрой ходьбе, йоге, плаванию, танцам или другим игровым видам спорта? В общем, что угодно, кроме силовых и выосокинтенсивных функциональных тренировок.\n\nЭто важно для расчёта КБЖУ!"
    await message.edit_text(text, reply_markup=None)

async def process_jogging(message, state):
    text = "🔵🔵⚪️⚪️\nРасскажи, сколько часов в неделю ты занимаешься силовыми или высокоинтенсивными функциональными тренировками.   \nЕсли не занимаешься вообще, напиши «0»  \nЕсли число не целое, напиши через запятую. Например, «1,5»."
    await message.answer(text, reply_markup=None)

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
        [InlineKeyboardButton(text="Нет, Нутри, посчитай за менй", callback_data="no")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.edit_text(text, reply_markup=keyboard)

async def process_w_loss(message, state, goal):
    text_add = "Знаешь, сколько кг хочешь набрать?"
    text_remove = "Знаешь, сколько кг хочешь скинуть?"
    if goal == "+":
        text = text_add
    elif goal == "-":
        text = text_remove
    await message.answer(text)

async def process_w_loss_amount(message, state, goal):
    text11 = "Считаю комфортную скорость похудения, чтобы результат закрепился надолго, а процесс тебе понравился!"
    text12 = "C удовольствием помогу тебе правильно питаться и чувствовать себя всё лучше с каждым днём!"
    if goal in ['+', '-']:
        text1 = text11
    elif goal in ['?', '=']:
        text1 = text12
    await message.answer(text1)

async def give_plan(message, state, input_text):
    text = "Пока я составляю твой персональный план, почитай про общие принципы, которых мы будем придерживаться в ближайший месяц.\n\nОни помогут тебе не просто похудеть, но закрепить результат и не вернуться к исходному весу через полгода."
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
    await message.answer_media_group(media=media_files)
    link = "https://telegra.ph/8-principov-osoznannogo-pitaniya-istochniki-informacii-07-16"
    text2 = f"<b>8 принципов осознанного питания: чему мы будем учиться</b>\n\nНа картинках — главные принципы осознанного питания, на основе которых я даю рекомендации.\n\nОни довольно простые, но вот сделать их привычкой — настоящий челлендж. Но мы будем выполнять его вместе — и так победим ❤️ \n\nИсточники — <a href=\'{link}\'>по ссылке</a>."
    await message.answer(text2)
    await message.answer(input_text)
    text4 = "План составлен! У нас есть тактика! Но как теперь её придерживаться? 🤔 Есть несколько идей на этот счёт!"
    await message.answer(text4)
    text5 = "Я буду присылать тебе напоминания о том, что нам пора пообщаться!\n\nПодскажи, в каком городе ты живёшь?\n\nСпрашиваю, чтобы напоминать о себе только в дневные часы."
    await message.answer(text5)

async def process_city(message, state):
    text1 = "ответ гпт про город"
    text2 = "Я буду писать два раза в день: перед завтраком и после ужина.   \n\nВ какое время тебе удобно получать от меня утренний план на день?   \n\nИдеально, если это будет перед едой: так ты сможешь делать все мои задания вовремя.   \n\nУкажи время в формате ЧЧ:ММ \nНапример 10:00"

    await message.answer(text1),
    await message.answer(text2)

async def process_morning_ping(message, state):
    text = "Договорились! А во сколько присылать вечерние итоги?   \b\bУкажи время в формате ЧЧ:ММ \bНапример, 20:00"
    await message.answer(text)

async def process_evening_ping(message, state):
    text = "Хочу пригласить тебя в наше сообщество <b>Нутри Ai: как есть, чтобы лучше жить!</b>\n\nТебя будут поддерживать и мотивировать нутрициологи, диетологи и другие специалисты.\n\nТолько для участников сообщества — прямые эфиры с экспертами, ответы на вопросы, полезные гайды и чек-листы. \n\nПодпишись на @nutri_community 💖 в Telegram"
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
        InputMediaPhoto(media=IMG15),
        InputMediaPhoto(media=IMG16),
    ]
    await message.answer_media_group(media=media_files)
    buttons = [
        [InlineKeyboardButton(text="Хочу начать путь к своей цели!", callback_data="lesson_0_done")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=keyboard)