# from cal_pretty import prettify_and_count
from functions import *
import json
# from bot2 import OPENAI_API_KEY, handle_assistant_response, encode_image, use_vision64
import openai
from openai import AsyncOpenAI
import requests
import base64
import os
import asyncio
import aiohttp
import shelve
import random
import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, html, Router, BaseMiddleware, types
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo
BOT_TOKEN = os.getenv("BOT_TOKEN")
VISION_ASS_ID_2 = os.getenv("VISION_ASS_ID_2")
RATE_WEEK_ASS_ID = os.getenv('RATE_WEEK_ASS_ID')
RATE_TWONE_ASS_ID = os.getenv('RATE_TWONE_ASS_ID')
RATE_DAY_ASS_ID = os.getenv("DAY_RATE")
RECIPE_ASS_ID = os.getenv("RECIPE_ASS_ID")

arrow_back = "⬅️"
arrow_menu = "⏏️"  #🆕

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from stickerlist import STICKER_IDS
# STICKER_ID = os.getenv("STICKER_ID")
CHAT_ID = os.getenv('LOGS_CHAT_ID')



VISION_ASSISTANT_ID_B = os.getenv("VISION_ASSISTANT_ID_B")


TOKEN = BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))


from functions import *

from all_states import *

debug = 0

async def get_url(file_id: str) -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    return file_url

async def audio_file(file_id: str) -> str:
    file_url = await get_url(file_id)
    transcription = await transcribe_audio_from_url(file_url)
    return transcription

async def get_user_meals(id, type):
    meals = ""
    return False, meals

async def get_average_from_meals(input):
    meals = json.loads(input)
    return meals

async def request_longrate_question(id, period):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserMealsKK"
    default_headers = {
        "Content-Type": "application/json"
    }
    data = {"userTgId": id, "period": period}
    print(f"url: {url} data: {json.dumps(data)}")
    async with aiohttp.ClientSession() as session:
        default_headers = {
            "Content-Type": "application/json"
        }
        try:
            async with session.post(url=url, data=json.dumps(data), headers=default_headers) as response:
                user_data = await response.text()
                return False, user_data
        except aiohttp.ClientError as e:
            return True, ""
    return

async def request_yapp_meals(id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserMealsForAnal?userTgId={id}"
    default_headers = {
        "Content-Type": "application/json"
    }
    # data = {"userTgId": id, "period": period}
    async with aiohttp.ClientSession() as session:
        default_headers = {
            "Content-Type": "application/json"
        }
        try:
            async with session.post(url=url, headers=default_headers) as response:
                user_data = await response.text()
                # print(f".text={user_data}")
                # try:
                #     user_jsoned = await response.json()
                #     print(f"ras_jsoned={user_jsoned}")
                #     print(f"jsoned= {user_jsoned['Meals']}")
                # except Exception as e:
                #     print(f"error:{e}")
                return False, user_data
        except aiohttp.ClientError as e:
            return True, ""
    return

def make_lesson_week_buttons(dict, week):
    emote_mapping = {True: "✅", False: "⭕️"}
    weekdays = 7*(week-1)
    l1_emote = emote_mapping.get(dict[f"lesson{1+weekdays}_done"])
    l2_emote = emote_mapping.get(dict[f"lesson{2+weekdays}_done"])
    l3_emote = emote_mapping.get(dict[f"lesson{3+weekdays}_done"])
    l4_emote = emote_mapping.get(dict[f"lesson{4+weekdays}_done"])
    l5_emote = emote_mapping.get(dict[f"lesson{5+weekdays}_done"])
    l6_emote = emote_mapping.get(dict[f"lesson{6+weekdays}_done"])
    l7_emote = emote_mapping.get(dict[f"lesson{7+weekdays}_done"])
    buttons = [
        [InlineKeyboardButton(text=f"{l1_emote}Урок {1+weekdays}", callback_data=f"d{1+weekdays}")],
        [InlineKeyboardButton(text=f"{l2_emote}Урок {2+weekdays}", callback_data=f"d{2+weekdays}")],
        [InlineKeyboardButton(text=f"{l3_emote}Урок {3+weekdays}", callback_data=f"d{3+weekdays}")],
        [InlineKeyboardButton(text=f"{l4_emote}Урок {4+weekdays}", callback_data=f"d{4+weekdays}")],
        [InlineKeyboardButton(text=f"{l5_emote}Урок {5+weekdays}", callback_data=f"d{5+weekdays}")],
        [InlineKeyboardButton(text=f"{l6_emote}Урок {6+weekdays}", callback_data=f"d{6+weekdays}")],
        [InlineKeyboardButton(text=f"{l7_emote}Урок {7+weekdays}", callback_data=f"d{7+weekdays}")],
    ]

    navigation_buttons = []
    if week > 1:
        navigation_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"menu_course_info_lessons_week_{week-1}"))
    if week < 3:
        navigation_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"menu_course_info_lessons_week_{week+1}"))

    if navigation_buttons:
        buttons.append(navigation_buttons)

    return buttons

async def get_user_lessons(id):
    async with aiohttp.ClientSession() as session:
        url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserLessons?UserTgId={id}"
        try:
            async with session.get(url=url) as response:
                lesson_data = await response.json()
                lessons_dict = {}
                for i, status in enumerate(lesson_data):
                    if i > 21:
                        break
                    lessons_dict[f"lesson{i}_done"] = status
                return False, lessons_dict
        except aiohttp.ClientError as e:
            return True, e
        
async def get_last_user_lesson(id):
    async with aiohttp.ClientSession() as session:
        url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetLastUserLesson?UserTgId={id}"
        try:
            async with session.get(url=url) as response:
                last_lesson = await response.text()
                return False,  int(last_lesson)
        except aiohttp.ClientError as e:
            return True, e

async def add_user_lesson(id, lesson):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/AddUserLesson?UserTgId={id}&lesson={lesson}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                if data == "true":
                    return True
                else: return False
        except aiohttp.ClientError as e:
            return False
        
async def get_user_list(onlyus):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUsersIds?onlyUs={onlyus}&onlyActive=true"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                user_list = json.loads(data)
                return user_list
        except aiohttp.ClientError as e:
            return False

async def long_rate(id, period):
    iserror, longrate_data = await request_longrate_question(id, period)
    assistant_mapping = {"3": RATE_WEEK_ASS_ID, "4": RATE_TWONE_ASS_ID, "0": RATE_DAY_ASS_ID}
    assistant = assistant_mapping.get(period)
    data = json.loads(longrate_data)
    isempty = data.get("user_info", {}).get("isempty", False)
    if isempty == "true":
        return True, "Ваша анкета не заполнена"
    if not iserror:
        gpt_resp1 = await no_thread_ass(str(longrate_data), assistant)
        gpt_resp = await remove_reference(gpt_resp1)
        return False, gpt_resp
    else:
        return True, ""


async def change_ping_activation_status(id, status):
    url=f"https://nutridb-production.up.railway.app/api/TypesCRUD/SetNotifyStatus?UserTgId={id}&status={status}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e

async def get_user_info(id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserExtraInfo?userTgId={id}"
    async with aiohttp.ClientSession() as session:
            default_headers = {
                "Content-Type": "application/json"
            }
            try:
                async with session.post(url=url, headers=default_headers) as response:
                    user_data = await response.text()
                    print(f"НИКИТИН ОТВЕТ {user_data}")
                    return False, user_data
            except aiohttp.ClientError as e:
                return True, ""
            

async def create_reciepie(question, id):
    try: 
        assistant_response = await rec_assistant(question, str(id), RECIPE_ASS_ID)
        if assistant_response == "error":
            return True, assistant_response
        else:
            return False, assistant_response
    except Exception as e: 
        return True, f"ERROR {e}"

async def get_total_kkal(id, period):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserMealsTotal?userTgId={id}&period={period}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as response:
                user_data = await response.text()
                print(f"НИКИТИН ОТВЕТ {user_data}")
                return False, user_data
        except aiohttp.ClientError as e:
            return True, ""
        
def generate_kkal_text(data1):
    data = json.loads(data1)
    goal_kkal = data["GoalKkal"]
    total_kkal = data["TotalKkal"]
    total_prot = data["TotalProt"]
    total_fats = data["TotalFats"]
    total_carbs = data["TotalCarbs"]

    goal_prot = round((0.225 * goal_kkal) / 4, 1)
    goal_fats = round((0.275 * goal_kkal) / 9, 1)
    goal_carbs = round((0.55 * goal_kkal) / 4, 1)
    remaining_kkal = round(goal_kkal - total_kkal, 1)
    
    summary = (
        f"<b>Ваша статистика на сегодня 🍽️</b>\n\n"
        f"Дневная цель : {goal_kkal} ккал., {goal_prot} г. белки, {goal_fats} г. жиры, {goal_carbs} г. углеводы 💪.\n"
        f"Сегодня вы съели {total_kkal} ккал.🔥\n\n"
        f"Белки: {total_prot} г. 💪\n"
        f"Жиры: {total_fats} г. 🧈\n"
        f"Углеводы: {total_carbs} г. 🍞\n\n"
        f"Вы можете еще съесть {remaining_kkal} ккал."
    )
    
    return summary
            
async def add_or_update_usr_info(data):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/AddOrUpdateUserExtraInfo"
    default_headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        default_headers = {
            "Content-Type": "application/json"
        }
        try:
            async with session.post(url=url, data=data, headers=default_headers) as response:
                user_data = await response.text()
                return False, user_data
            
        except aiohttp.ClientError as e:
            return True, ""
        
async def ensure_user(message):
   async with aiohttp.ClientSession() as session:
        url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/EnsureUserH?userTgId={message.from_user.id}&userName={message.from_user.username}"
        try:
            async with session.get(url=url) as response:
                ensure_response = await response.text()
                print(ensure_response)
                return False, ensure_response
        except aiohttp.ClientError as e:
            return True, e

def create_day_rate_question(user_info, food):
    data = json.loads(user_info)
    parsed_info = {
        "user_info": {
            "age": data.get("user_info_age"),
            "gender": data.get("user_info_gender"),
            "bmi": data.get("user_info_bmi"),
            "bmr": data.get("bmr"),
            "allergies": data.get("user_info_meals_ban")
        },
        "food": food,
        "meal_type": data.get("meal_type"),
        "goal": data.get("user_info_goal"),
        "target_calories": data.get("target_calories")
    }
    return str(parsed_info)

async def yapp(id, question, new_thread):
    
    if new_thread:
        await remove_yapp_thread(id)
        iserror1, user_data = await get_user_info(id)
        iserror2, week_data = await request_yapp_meals(id)
        user_info = json.loads(user_data)
        isempty = user_info.get("isempty", False)
        if isempty == "true":
            return True, "Ваша анкета не заполнена"
        await create_thread_with_extra_info(f"user_data: {str(user_data)} user_meals:{str(week_data)}", id, YAPP_SESH_ASSISTANT_ID)
    try:
        response = await yapp_assistant(question, id, YAPP_SESH_ASSISTANT_ID)
        if debug == 1:
            print(response)
        
        if response != "error":
            isError = False
            final_response = response
            if debug == 1:
                print(f"{isError} {final_response}")
        else:
            isError = True
            final_response = "Ошибка: неверный запрос"
            if debug == 1:
                print(f"{isError} {final_response}")
        return isError, final_response

    except Exception as e:
        print(f"Error occurred: {e}")
        return True, "Ошибка обработки запроса"
    
async def process_img_rec(message, state, text, buttons):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    id = str(message.from_user.id)
    url = await get_url(message.photo[-1].file_id)
    vision = await process_url(url, id, VISION_ASS_ID_2)
    print(vision)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        errorkeyboard = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/ai_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
        await sticker_mssg.delete()
        # await message.answer(f"ошибка!!! \n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        await message.answer(f"Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        asyncio.create_task(log_bot_response(f"ошибка в распознании {pretty}", message.from_user.id))
    else: 
        await sticker_mssg.delete()
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        asyncio.create_task(log_bot_response(pretty, message.from_user.id))
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


async def process_audio_rec(message, state, text, buttons):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    if await state.get_state() == LayoverState.recognition:
        await remove_thread(id)
    vision = await generate_response(transcription, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        errorkeyboard = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/ai_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
        await sticker_mssg.delete()
        # await message.answer(f"ошибка!!! \n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        await message.answer(f"Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        asyncio.create_task(log_bot_response(f"ошибка в распознании {pretty}", message.from_user.id))
    else: 
        await sticker_mssg.delete()
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        asyncio.create_task(log_bot_response(pretty, message.from_user.id))
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        

async def process_txt_rec(message, state, text, buttons):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    id = str(message.from_user.id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    if await state.get_state() == LayoverState.recognition:
        await remove_thread(id)
    vision = await generate_response(message.text, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        errorkeyboard = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/ai_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
        await sticker_mssg.delete()
        # await message.answer(f"ошибка!!! \n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        await message.answer(f"Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        asyncio.create_task(log_bot_response(f"ошибка в распознании {pretty}", message.from_user.id))
    else: 
        await sticker_mssg.delete()
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        asyncio.create_task(log_bot_response(pretty, message.from_user.id))
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        

async def edit_txt_rec(message, state, text, buttons):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    id = str(message.from_user.id)
    state_data = await state.get_data()
    old = state_data["old_food"]
    await remove_thread(id)
    request_mssg = f"Старый прием пищи: {old}, измени его вот так: {message.text}"
    vision = await generate_response(request_mssg, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        errorkeyboard = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/ai_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
        await sticker_mssg.delete()
        # await message.answer(f"ошибка!!! \n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        await message.answer(f"Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        asyncio.create_task(log_bot_response(f"ошибка в распознании {pretty}", message.from_user.id))
    else: 
        await sticker_mssg.delete()
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        asyncio.create_task(log_bot_response(pretty, message.from_user.id))
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def edit_audio_rec(message, state, text, buttons):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    await remove_thread(id)
    state_data = await state.get_data()
    old = state_data["old_food"]
    request_mssg = f"Старый прием пищи: {old}, измени его вот так: {transcription}"
    vision = await generate_response(request_mssg, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        errorkeyboard = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/ai_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
        await sticker_mssg.delete()
        # await message.answer(f"ошибка!!! \n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        await message.answer(f"Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        asyncio.create_task(log_bot_response(f"ошибка в распознании {pretty}", message.from_user.id))
    else: 
        await sticker_mssg.delete()
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        asyncio.create_task(log_bot_response(pretty, message.from_user.id))
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


def generate_day_buttons(data):
    buttons = []
    first = True
    for i, day in enumerate(data):
        emote = "⭕️" if day["isEmpty"] else "✅"

        display_day = "Сегодня" if i == len(data) - 1 else day["DisplayDay"][:5]

        text = f"{emote} {display_day} - {day['TotalKkal']} ккал"
        callback_data = f"day_{day['DisplayDay']}"
        buttons.insert(0,[InlineKeyboardButton(text=text, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton(text=arrow_menu, callback_data="menu"), InlineKeyboardButton(text=arrow_back, callback_data="menu_dnevnik")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def generate_meal_buttons(data, day):
    meal_mapping = {0: "Завтрак", 2: "Обед", 4: "Ужин", 5: "Перекус"}
    buttons = []
    
    day_data = next((d for d in data if d["DisplayDay"] == day), None)
    if not day_data:
        return None
    
    for meal in day_data["MealStatus"]:
        if meal["Type"] in meal_mapping:
            emote = "⭕️" if meal["isEmpty"] else "✅"
            text = f"{emote} {meal_mapping[meal['Type']]}"
            callback_data = f"meal_{meal["isEmpty"]}_{day}_{meal['Type']}"
            buttons.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_dnevnik_edit_same")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def parse_meal_data(response_json):
    data = json.loads(response_json)
    
    meal_id = data.get("MealId")
    food_items = []
    
    for item in data.get("Meal", {}).get("food", []):
        food_items.append({
            "description": item.get("description"),
            "weight": item.get("weight"),
            "fats": item["nutritional_value"].get("fats"),
            "carbs": item["nutritional_value"].get("carbs"),
            "protein": item["nutritional_value"].get("protein"),
            "kcal": item["nutritional_value"].get("kcal")
        })
    
    return meal_id, food_items

async def save_meal(id, food, type):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/CreateMeal"
    req_headers = {
        "Content-Type": "application/json"
    }
    meal_data ={
            "userTgId": id,
            "meal": {
                "description": "string",
                "totalWeight": 0,
                "food": food,
                "type": type
            },
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e
        
async def save_meal_plate(id, food, meal_id):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/CreateMeal"
    req_headers = {
        "Content-Type": "application/json"
    }
    meal_data ={
            "mealid": meal_id,
            "userTgId": id,
            "meal": {
                "description": "string",
                "totalWeight": 0,
                "food": food
            },
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e
        
async def save_meal_old_date(id, food, type, date):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/CreateMeal"
    req_headers = {
        "Content-Type": "application/json"
    }
    meal_data ={
            "userTgId": id,
            "meal": {
                "description": "string",
                "totalWeight": 0,
                "food": food,
                "type": type
            },
            "eatedAt": date,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e
        
async def edit_existing_meal(id, food, type, mealId):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/EditMeal"
    req_headers = {
        "Content-Type": "application/json"
    }
    meal_data ={
            "userTgId": id,
            "meal": {
                "description": "string",
                "totalWeight": 0,
                "food": food,
                "type": type
            },
            "eatedAt": "",
            "mealId": mealId
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e


async def saving_edit(callback_query, state):
    state_data = await state.get_data()
    food = state_data["latest_food"]
    prev_state = state_data["prev_state"]
    await state.set_state(prev_state)
    state_data_2 = await state.get_data()
    date = state_data_2["date"]
    meal_type = state_data_2["meal_type"]
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/CreateMeal"
    req_headers = {
        "Content-Type": "application/json"
    }
    meal_data ={
            "userTgId": callback_query.from_user.id,
            "meal": {
                "description": "string",
                "totalWeight": 0,
                "food": food,
                "type": meal_type
            },
            "eatedAt": f"{date}"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                print(data)
                # await callback_query.message.answer(f"{data}")
                await callback_query.answer()
                if data != 0:
                    await callback_query.message.answer("Успешно сохранено")
                else:
                    await callback_query.message.answer("Ошибка при сохранении")
        except aiohttp.ClientError as e:
            print(f"Поймали ошибку{e}")

async def get_singe_meal(id, date, mealtype):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/GetSingleUserMeal"
    meal_data = {
        "userTgId": f"{id}",
        "dayStr": f"{date}",
        "typemeal": f"{mealtype}",
    }
    req_headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                meal_id, food_items = parse_meal_data(data)
                iserror, food_pretty_items, pretty = await prettify_and_count(data, detailed_format=False)
                return meal_id, pretty, food_items
        except aiohttp.ClientError as e:
            print(f"Поймали ошибку{e}")

async def delete_meal(id, meal_id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/DeleteMeal?mealId={meal_id}&userTgId={id}"
    # print(url)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e
        
async def request_for_graph(id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserWeekPlotH?userTgId={id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                return False, data
        except aiohttp.ClientError as e:
            return True, e
        
async def get_user_sub_info(id):
    url = f"https://nutridb-production.up.railway.app/api/Subscription/GetUserSubDetail?tgId={id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as response:
                data = await response.text()
                data1 = json.loads(data)
                type_value = data1["type"]
                date_update = data1["dateUpdate"]
                formatted_date_update = datetime.fromisoformat(date_update).strftime("%Y-%m-%d")
                return type_value, formatted_date_update
        except aiohttp.ClientError as e:
            return False, e
        
async def get_user_meal_by_mealid(id, meal_id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetUserMealById?userTgId={id}&mealId={meal_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as response:
                data = await response.text()
                data1 = json.loads(data)
                pretty = data1.get('pretty')
                meals = data1.get('Meals')
                return False, pretty, meals
        except aiohttp.ClientError as e:
            return True, e

DATABASE_FILE = "topics.db"
    
def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                user_id INTEGER PRIMARY KEY,
                thread_id INTEGER
            )
        """)
        conn.commit()

def get_thread_id(user_id: int) -> int:
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT thread_id FROM topics WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None

def save_thread_id(user_id: int, thread_id: int):
    """Save the thread ID for a user in the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO topics (user_id, thread_id)
            VALUES (?, ?)
        """, (user_id, thread_id))
        conn.commit()
    
async def log_user_message(message):

    user_id = message.from_user.id

    thread_id = get_thread_id(user_id)
    if not thread_id:
        topic = await bot.create_forum_topic(CHAT_ID, name=str(user_id))
        thread_id = topic.message_thread_id
        save_thread_id(user_id, thread_id)
        logger.info(f"Created new topic for user {user_id} with thread ID {thread_id}")

    # if message.text:
    #     content = message.text
    # elif message.photo:
    #     photo = message.photo[-1]
    #     content = f"📷 Photo: {photo.file_id}"
    # elif message.voice:
    #     content = f"🎤 Voice: {message.voice.file_id}"
    # elif message.document:
    #     content = f"📄 Document: {message.document.file_id}"
    # elif message.video:
    #     content = f"🎥 Video: {message.video.file_id}"
    # elif message.audio:
    #     content = f"🎵 Audio: {message.audio.file_id}"
    # else:
    #     content = "Unsupported message type"

    # await bot.send_message(
    #     chat_id=CHAT_ID,
    #     text=f"User {user_id} sent:\n{content}",
    #     message_thread_id=thread_id
    # )
    if message.text:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"User {user_id} sent:\n{message.text}",
            message_thread_id=thread_id
        )
    elif message.photo:
        photo = message.photo[-1]
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo.file_id,
            caption=f"User {user_id} sent a photo.",
            message_thread_id=thread_id
        )
    elif message.voice:
        await bot.send_voice(
            chat_id=CHAT_ID,
            voice=message.voice.file_id,
            caption=f"User {user_id} sent a voice message.",
            message_thread_id=thread_id
        )
    elif message.document:
        await bot.send_document(
            chat_id=CHAT_ID,
            document=message.document.file_id,
            caption=f"User {user_id} sent a document.",
            message_thread_id=thread_id
        )
    elif message.video:
        await bot.send_video(
            chat_id=CHAT_ID,
            video=message.video.file_id,
            caption=f"User {user_id} sent a video.",
            message_thread_id=thread_id
        )
    elif message.audio:
        await bot.send_audio(
            chat_id=CHAT_ID,
            audio=message.audio.file_id,
            caption=f"User {user_id} sent an audio file.",
            message_thread_id=thread_id
        )
    else:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"User {user_id} sent an unsupported message type.",
            message_thread_id=thread_id
        )

async def log_user_callback(callback_query):

    user_id = callback_query.from_user.id

    thread_id = get_thread_id(user_id)
    if not thread_id:
        topic = await bot.create_forum_topic(CHAT_ID, name=str(user_id))
        thread_id = topic.message_thread_id
        save_thread_id(user_id, thread_id)
        logger.info(f"Created new topic for user {user_id} with thread ID {thread_id}")

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"callback:{callback_query.data}",
        message_thread_id=thread_id
    )

async def log_bot_response(text, user_id):

    thread_id = get_thread_id(user_id)
    if not thread_id:
        # Create a new topic with the user's ID as the topic name
        topic = await bot.create_forum_topic(CHAT_ID, name=str(user_id))
        thread_id = topic.message_thread_id
        save_thread_id(user_id, thread_id)
        logger.info(f"Created new topic for user {user_id} with thread ID {thread_id}")

    # Send the bot's response to the corresponding topic
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        message_thread_id=thread_id
    )
    logger.info(f"Logged bot response for user {user_id} in topic {thread_id}")

async def check_is_active_state(id, state):
    state_data = await state.get_data()
    is_active = state_data.get('isActive', False)
    if not is_active:
        is_active = await fetch_is_active_from_db(id)
        await state.update_data(isActive=is_active)
    print(f"{id} isActive:{is_active}")
    return is_active

async def fetch_is_active_from_db(id):
    url = f"https://nutridb-production.up.railway.app/api/Subscription/IsActiveUser?userTgId={id}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status == 200:
                data = await response.text()
                # return data.get('isActive', False)
                is_active = data.strip().lower() == "true"
                return is_active
            else:
                print(f"Failed to fetch 'isActive' from the database: {response.status}")
                return False