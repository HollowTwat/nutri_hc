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


STICKER_ID = os.getenv("STICKER_ID")


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
                lessons_dict = {f"lesson{i+1}_done": status for i, status in enumerate(lesson_data)}
                return False, lessons_dict
        except aiohttp.ClientError as e:
            return True, e
        
async def get_last_user_lesson(id):
    async with aiohttp.ClientSession() as session:
        url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/GetLastUserLesson?UserTgId={id}"
        try:
            async with session.get(url=url) as response:
                last_lesson = await response.text()
                print(await response.json())
                return False, last_lesson
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

async def long_rate(id, period):
    iserror, longrate_data = await request_longrate_question(id, period)
    assistant_mapping = {"3": RATE_WEEK_ASS_ID, "4": RATE_TWONE_ASS_ID, "0": RATE_DAY_ASS_ID}
    assistant = assistant_mapping.get(period)
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
                    # user_data = json.loads(text_data)
                    return False, user_data
            except aiohttp.ClientError as e:
                return True, ""
            

async def create_reciepie(question, id):
    print(f"create_rec_hit with question: {question}")
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
                # user_data = json.loads(text_data)
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
                # print(f"НИКИТИН ОТВЕТ {user_data}")
                # user_data = json.loads(text_data)
                return False, user_data
        except aiohttp.ClientError as e:
            return True, ""

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
    print('day1_yapp triggered')
    
    if new_thread:
        await remove_yapp_thread(id)
        await create_thread_with_extra_info("user_info_is_empty_for_now", id, YAPP_SESH_ASSISTANT_ID)
    
    try:
        response = await yapp_assistant(question, id, YAPP_SESH_ASSISTANT_ID)
        if debug == 1:
            print(response)
        
        if response != "error":
            isError = False
            final_response = f"Ответ: {response}"
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
    id = str(message.from_user.id)
    url = await get_url(message.photo[-1].file_id)
    vision = await process_url(url, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


async def process_audio_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    if await state.get_state() == LayoverState.recognition:
        await remove_thread(id)
    vision = await generate_response(transcription, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        

async def process_txt_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    if await state.get_state() == LayoverState.recognition:
        await remove_thread(id)
    vision = await generate_response(message.text, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        

async def edit_txt_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    state_data = await state.get_data()
    old = state_data["old_food"]
    await remove_thread(id)
    request_mssg = f"Старый прием пищи: {old}, измени его вот так: {message.text}"
    vision = await generate_response(request_mssg, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

async def edit_audio_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    await remove_thread(id)
    state_data = await state.get_data()
    old = state_data["old_food"]
    request_mssg = f"Старый прием пищи: {old}, измени его вот так: {transcription}"
    vision = await generate_response(request_mssg, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
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
    buttons.append([InlineKeyboardButton(text="⏏️", callback_data="menu"), InlineKeyboardButton(text="◀️", callback_data="menu_dnevnik")])
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
    # print(response_json)
    data = json.loads(response_json)
    # print(data)
    
    meal_id = data.get("MealId")
    # pretty = data["pretty"] if "pretty" in data else None
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
    # print(f"url={url}, data={json.dumps(meal_data)}, headers={req_headers}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=json.dumps(meal_data), headers=req_headers) as response:
                data = await response.text()
                print(data)
                await callback_query.message.answer(f"{data}")
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
    # print(f"url={url}, \ndata = {meal_data}, \nheaders={meal_data}")
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