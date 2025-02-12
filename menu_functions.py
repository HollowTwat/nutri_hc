import asyncio
from decimal import Decimal
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
from all_states import *

COU_LESS_IMG_1 = "AgACAgIAAxkBAAIFq2esppgH39WhLjmdYQGn7CnH2VbyAAIe7jEbb-RpSZ-LMYskHd_tAQADAgADeQADNgQ"
COU_LESS_IMG_2 = "AgACAgIAAxkBAAIFr2espqUpBX8QZwXBahHhcR3-YadwAAIg7jEbb-RpSfx5HS7svr5LAQADAgADeQADNgQ"
COU_LESS_IMG_3 = "AgACAgIAAxkBAAIFs2esprGR_uTd7csprwsrrmbt7TzLAAKB7jEbLgppSZacNITqSzTvAQADAgADeQADNgQ"
COU_LESS_IMG_4 = "AgACAgIAAxkBAAIFt2esprvvZMQtjmxdFXf-bqDwZ91vAAIj7jEbb-RpSQKI2EU19u5_AQADAgADeQADNgQ"

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

async def menu_back_handler(callback_query, state) -> None:
    await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="📚 Курс:", callback_data="menu_course")],
        [InlineKeyboardButton(text="🍽 Дневник питания:", callback_data="menu_dnevnik")],
        [InlineKeyboardButton(text="💬  Нутри:", callback_data="menu_nutri")],
        [InlineKeyboardButton(text="⚙️Дополнительное:", callback_data="menu_settings")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Меню"
    try:
        await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    except Exception as e:
        await callback_query.message.answer(step0txt, reply_markup=keyboard)

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
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def menu_no_edit(callback_query, state) -> None:
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
    iserror, last_lesson = await get_last_user_lesson(callback_query.from_user.id)
    current_lesson = int(last_lesson)+1
    await state.update_data(current_lesson=current_lesson)
    buttons = [
        [InlineKeyboardButton(text=f"📖Начать Урок {current_lesson}", callback_data=f"menu_course_lesson_{current_lesson}")],
        [InlineKeyboardButton(text="✏️ Программа курса", callback_data="menu_course_info")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "📚 Курс:"
    try:
        await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    except Exception as e:
        await callback_query.message.answer(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_dnevnik(message, state):
    buttons = [
        [InlineKeyboardButton(text="🍽 Занести в дневник", callback_data="menu_dnevnik_input")],
        [InlineKeyboardButton(text="🔄Редактировать", callback_data="menu_dnevnik_edit")],
        [InlineKeyboardButton(text="📊 Аналитика", callback_data="menu_dnevnik_analysis")],
        [InlineKeyboardButton(text="📸 Инструкция", callback_data="menu_dnevnik_instruction")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "🍽 Дневник питания:"
    try:
        await message.edit_text(step0txt, reply_markup=keyboard)
    except Exception as e:
        await message.answer(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_nutri(message, state):
    buttons = [
        [InlineKeyboardButton(text="🌿 Спросить Нутри", callback_data="menu_nutri_yapp")],
        [InlineKeyboardButton(text="👩‍🍳 Рецепт", callback_data="menu_nutri_reciepie")],
        [InlineKeyboardButton(text="🔍 Анализ этикетки", callback_data="menu_nutri_etiketka")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "💬  Нутри:"
    try:
        await message.edit_text(step0txt, reply_markup=keyboard)
    except Exception as e:
        await message.answer(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)

async def process_menu_settings(message, state):
    buttons = [
        [InlineKeyboardButton(text="📌 Ваш профиль", callback_data="menu_settings_profile")],
        [InlineKeyboardButton(text="🆘 Помощь", callback_data="menu_settings_help")],
        [InlineKeyboardButton(text="💰 Условия подписки", callback_data="menu_settings_sub")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "⚙️Дополнительное:"
    try:
        await message.edit_text(step0txt, reply_markup=keyboard)
    except Exception as e:
        await message.answer(step0txt, reply_markup=keyboard)
    # await callback_query.message.answer(step0txt, reply_markup=keyboard)
################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

async def process_menu_course_lesson(callback_query, state):
    step0txt = "Выбирай урок"
    buttons = [
        [InlineKeyboardButton(text='Урок1', callback_data='d1')],
        [InlineKeyboardButton(text='Урок2', callback_data='d2'), InlineKeyboardButton(text='Урок2_2', callback_data='d2_2')],
        [InlineKeyboardButton(text='Урок2', callback_data='d3'), InlineKeyboardButton(text='Урок3_2', callback_data='d3_2')],
        [InlineKeyboardButton(text='Урок2', callback_data='d4'), InlineKeyboardButton(text='Урок4_2', callback_data='d4_2')],
        [InlineKeyboardButton(text='Урок2', callback_data='d5'), InlineKeyboardButton(text='Урок5_2', callback_data='d5_2')]
    ]
    await callback_query.message.edit_text(step0txt, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_menu_course_info(callback_query, state):
    iserror, lessons_dict = await get_user_lessons(callback_query.from_user.id)
    await state.update_data(lessons_dict=lessons_dict)
    state_data = await state.get_data()
    current_lesson = state_data["current_lesson"]
    buttons = [
        [InlineKeyboardButton(text="Посмотреть пройденные уроки", callback_data="menu_course_info_lessons")],
        [InlineKeyboardButton(text="◀️", callback_data="menu_course"), 
         InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    step0txt = "💚 На первой неделе ты заметишь пищевые привычки, которые тебе мешают. \n💜 На второй получишь базу для формирования новых привычек. \n❤️ На третьей закрепишь новые привычки и начнёшь применять их в реальной жизни."
    media_files = [
        InputMediaPhoto(media=COU_LESS_IMG_1, caption=step0txt),
        InputMediaPhoto(media=COU_LESS_IMG_2),
        InputMediaPhoto(media=COU_LESS_IMG_3),
        InputMediaPhoto(media=COU_LESS_IMG_4)
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    lesson_week = int(current_lesson/7)
    step = current_lesson-lesson_week*7
    step1txt = f"Сейчас ты на {step} уроке этапа {lesson_week} 🧡"
    step2txt = f"{current_lesson-1} уроков из 21 дня пройдено 💪  Осталось {22-current_lesson} уроков"

    await callback_query.message.delete()
    await callback_query.message.answer_media_group(media=media_files)
    await callback_query.message.answer(step1txt)
    await callback_query.message.answer(step2txt, reply_markup=keyboard)

async def process_menu_cource_info_lessons(callback_query, state):
    iserror, lessons_dict = await get_user_lessons(callback_query.from_user.id)
    await state.update_data(lessons_dict=lessons_dict)

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

async def process_menu_dnevnik_input(callback_query, state):
    step0txt = "Отправь фото еды.\nТакже можешь воспользоваться 🎤 аудио или ввести текстом в формате:\n<i>Яичница из 2 яиц, чай без сахара</i>"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_dnevnik_edit(callback_query, state):
    if callback_query.data == "menu_dnevnik_edit":
        await state.set_state(UserState.edit)
        id = str(callback_query.from_user.id)
        API_URL = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserWeekMealsStatus?userTgId={id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(API_URL) as response:
                    text_data = await response.text()
                    meal_data = json.loads(text_data)
                    await state.update_data(meal_data=meal_data)
            except aiohttp.ClientError as e:
                await callback_query.message.edit_text(f"Error fetching data: {str(e)}")
                return
    else:
        user_data = await state.get_data()
        meal_data = user_data.get("meal_data", [])

    await callback_query.message.edit_text("Выбирай день", reply_markup=generate_day_buttons(meal_data))


async def process_menu_dnevnik_analysis(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Показать график за неделю", callback_data="menu_dnevnik_analysis_graph")],
        [InlineKeyboardButton(text="Получить анализ пищи за неделю", callback_data="menu_dnevnik_analysis_rate-week")],
        [InlineKeyboardButton(text="Получить аналитику за сегодня", callback_data="menu_dnevnik_analysis_rate-day")],
        [InlineKeyboardButton(text="◀️", callback_data="menu_dnevnik"), 
         InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    iserror, total_kkal = await get_total_kkal(callback_query.from_user.id, "0")
    generated_text = generate_kkal_text(total_kkal)
    # step0txt = "<b>Ваша статистика на сегодня</b> 🍽\n\nДневная цель: X ккал., X г. белки, X г. жиры, X г. углеводы 💪.   \n\nСегодня вы съели: \nX ккал 🔥.   \n\nБелки: X г. \nЖиры: X г. \nУглеводы:X г.   \n\nТы можешь съесть еще 582 ккал."
    await callback_query.message.edit_text(generated_text, reply_markup=keyboard)

async def process_menu_dnevnik_instruction(callback_query, state):

    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

async def process_menu_nutri_yapp(callback_query, state):
    await state.set_state(UserState.yapp_new)
    step0txt = "Задай мне любой вопрос в части питания. Текстом или 🎤 аудио\nНапример: <i>Какие перекусы ты мне рекомендуешь исходя из моей цели?</i>"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_nutri_reciepie(callback_query, state):

    step0txt = "in dev"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

async def process_menu_nutri_etiketka(callback_query, state):
    step0txt = "Отправь мне фото с этикеткой любого товара. Я проанализирую состав за тебя и напишу, есть ли в нём ингредиенты, которых стоит опасаться 🔍   \n\nПодсказка💡 \n<i>Делай фото состава, не названия продукта. \nФото должно быть четким без бликов, на ровной поверхности</i>"
    await callback_query.message.edit_text(step0txt, reply_markup=None)

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################
async def check_user_variable(state: FSMContext, var_name: str):
    """Check if a specific variable is set in the state."""
    user_data = await state.get_data()
    
    # Check if variable exists and is not empty
    if var_name in user_data and user_data[var_name]:
        return True
    return False

async def parse_state_for_settings(state):
    user_info = await state.get_data()
    gender_mapping = {"male": "Мужской", "female": "Женский"}
    gender_str = gender_mapping.get(user_info.get("gender"), "Неизвестно")
    
    response_str = f"<b>{user_info.get('name')}, вот твои данные и цель, к которой ты идёшь:</b>   \n\n"
    response_str += f"Пол: {gender_str} \nВозраст: {user_info['age']} лет \nВес: {user_info['weight']} кг \nРост: {user_info['height']} см     \n\n"
    response_str += f"Цель: {user_info['goal']} \nЦелевой вес: {user_info['goal_weight']} кг   \n\n"
    response_str += f"Текущая норма калорий: {user_info['target_calories']} ккал \nУровень еженедельной активности: {user_info['gym_hours']}+{user_info['exercise_hours']} часов"
    
    return response_str

async def new_request_for_settings(id, state):
    iserror, input_data = await get_user_info(id)
    data = json.loads(input_data)
    
    goal_mapping = {"+": "Набрать", "-": "Похудеть", "=": "Сохранить"}
    gender_mapping = {"male": "Мужской", "female": "Женский"}
    
    goal_str = goal_mapping.get(data.get("user_info_goal"), "Неизвестно")
    gender_str = gender_mapping.get(data.get("user_info_gender"), "Неизвестно")

    try:
        weight_change = Decimal(data.get("user_info_weight_change", 0))
        current_weight = Decimal(data.get("user_info_weight", 0))
    except (ValueError, TypeError):
        weight_change = Decimal(0)
        current_weight = Decimal(0)
    
    goal_weight = (
        current_weight + weight_change if data.get("user_info_goal") == "+"
        else current_weight - weight_change if data.get("user_info_goal") == "-"
        else current_weight
    )
    
    user_info = {
        "name": data.get("user_info_name"),
        "age": data.get("user_info_age"),
        "gender": data.get("user_info_gender"),
        "bmi": data.get("user_info_bmi"),
        "bmr": data.get("bmr"),
        "allergies": data.get("user_info_meals_ban"),
        "weight": str(current_weight),
        "height": data.get("user_info_height"),
        "goal": goal_str,
        "goal_weight": str(goal_weight),
        "target_calories": data.get("target_calories"),
        "gym_hours": data.get("user_info_gym_hrs"),
        "exercise_hours": data.get("user_info_excersise_hrs")
    }
    
    await state.update_data(**user_info)
    
    response_str = f"<b>{data.get('user_info_name')}, вот твои данные и цель, к которой ты идёшь:</b>   \n\n"
    response_str += f"Пол: {gender_str} \nВозраст: {user_info['age']} лет \nВес: {user_info['weight']} кг \nРост: {user_info['height']} см     \n\n"
    response_str += f"Цель: {user_info['goal']} \nЦелевой вес: {user_info['goal_weight']} кг   \n\n"
    response_str += f"Текущая норма калорий: {user_info['target_calories']} ккал \nУровень еженедельной активности: {user_info['gym_hours']}+{user_info['exercise_hours']} часов"
    return response_str

async def process_menu_settings_profile(callback_query, state):
    await state.set_state(UserState.user_settings)
    is_set = await check_user_variable(state, "goal_weight")
    if is_set:
        step0txt = await parse_state_for_settings(state)
    if not is_set:
        step0txt = await new_request_for_settings(callback_query.from_user.id, state)

    buttons = [
        [InlineKeyboardButton(text="Изменить имя", callback_data="menu_settings_profile_name")],
        [InlineKeyboardButton(text="Изменить норму ККАЛ", callback_data="menu_settings_profile_kkal")],
        [InlineKeyboardButton(text="Заполнить анкету заново", callback_data="menu_settings_profile_re-anket")],
        [InlineKeyboardButton(text="Настроить уведомления", callback_data="menu_settings_profile_notif")],
        [InlineKeyboardButton(text="◀️", callback_data="menu_settings"), 
         InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)
    await state.set_state(UserState.change_user_info)

async def process_menu_settings_help(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Задать вопрос", callback_data="menu_settings_help_question")],
        [InlineKeyboardButton(text="◀️", callback_data="menu_settings"), 
         InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Расскажи, с чем есть проблемы? \nПостараюсь помочь как можно быстрее"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def process_menu_settings_sub(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="📌 Ваш профиль", callback_data="menu_settings_profile")],
        [InlineKeyboardButton(text="🆘 Помощь", callback_data="menu_settings_help")],
        [InlineKeyboardButton(text="💰 Условия подписки", callback_data="menu_settings_sub")],
        [InlineKeyboardButton(text="◀️", callback_data="menu_settings"), 
         InlineKeyboardButton(text="⏏️", callback_data="menu_back")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "Твой текущий тариф:   \n\n☑️ Подписка на сервис Нутри на X мес \n☑️Действует до:  X \n☑️ Дата автоматического продления: X"
    await callback_query.message.edit_text(step0txt, reply_markup=keyboard)

async def change_user_name(callback_query, state, name):
    buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
    await callback_query.message.edit_text(f"Твоё имя у меня сейчас {name}, пиши то, на которое поменять", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(UserState.name_change)

async def change_user_kkal(callback_query, state, kkal):
    buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
    await callback_query.message.edit_text(f"Текущая норма калорий: {kkal} ккал\nВведи новое число ккал", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(UserState.kkal_change)

async def restart_anket(callback_query, state):
    buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
    await callback_query.message.edit_text(f"indev", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def change_user_notifs(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Изменить время", callback_data="user_change_notif_time")],
        [InlineKeyboardButton(text="Отключить все уведомления", callback_data="user_notif_toggle")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]
    ]
    await callback_query.message.edit_text("Меню уведомлений", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(UserState.menu)

async def process_menu_settings_notif_toggle(callback_query, state):
    buttons = [
        [InlineKeyboardButton(text="Вкл", callback_data="True"), InlineKeyboardButton(text="Выкл", callback_data="False")],
        [InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]
    ]
    text_mapping = {"True": "Уведомления включены", "False": "Уведомления отключены", "user_notif_toggle": "Выбирай что хочешь сделать с уведомлениями"}
    text = text_mapping.get(callback_query.data)

    if callback_query.data in ["True", "False"]:
        Iserror, respo = await change_ping_activation_status(callback_query.from_user.id, callback_query.data)
        if not Iserror: await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.notif_toggle)
        return
    else:
        await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.notif_toggle)

async def ping_change_start(callback_query, state):
    buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
    text = "В какое время тебе удобно получать от меня утренний план на день?\n\nИдеально, если это будет перед едой: так ты сможешь делать все мои задания вовремя.\n\nУкажи время в формате ЧЧ:ММ Например 10:00"
    await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(UserState.morning_ping_change)

async def change_morning_ping(message, state):
    data = {
        "userTgId": f"{message.from_user.id}",
        "info": {
            "user_info_morning_ping" : f"{message.text}"
        }
    }
    text = "Договорились! А во сколько присылать вечерние итоги?\n\nУкажи время в формате ЧЧ:ММ Например, 20:00"  
    iserror, answer = await add_or_update_usr_info(json.dumps(data))
    if not iserror:
        await message.answer(text)
        await state.set_state(UserState.evening_ping_change)

async def change_evening_ping(message, state):
    data = {
        "userTgId": f"{message.from_user.id}",
        "info": {
            "user_info_evening_ping" : f"{message.text}"
        }
    }
    text = "Я обновила твои данные ✅"  
    buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
    iserror, answer = await add_or_update_usr_info(json.dumps(data))
    if not iserror:
        await message.answer(text)
        await state.set_state(UserState.menu, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_change_kkal(message, state):
    await state.update_data(target_calories=message.text)
    data = {
        "userTgId": f"{message.from_user.id}",
        "info": {
            "target_calories" : f"{message.text}"
        }
    }
    iserror, answer = await add_or_update_usr_info(json.dumps(data))
    if not iserror:
        buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
        await message.answer("Я обновила твои данные ✅", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def process_change_name(message, state):
    await state.update_data(name=message.text)
    data = {
        "userTgId": f"{message.from_user.id}",
        "info": {
            "user_info_name" : f"{message.text}"
        }
    }
    iserror, answer = await add_or_update_usr_info(json.dumps(data))
    if not iserror:
        buttons = [[InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_settings_profile")]]
        await message.answer("Я обновила твои данные ✅", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################
