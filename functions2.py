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


TOKEN = BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))


from functions import *

class UserState(StatesGroup):
    info_coll = State()
    recognition = State()
    redact = State()
    edit = State()
    yapp_new = State()
    yapp = State()
    menu = State()
    saving_confirmation = State()
    saving = State()

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
        state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.saving_confirmation)

async def process_audio_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    vision = await generate_response(transcription, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.saving_confirmation)

async def process_txt_rec(message, state, text, buttons):
    id = str(message.from_user.id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    vision = await generate_response(message.text, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        await state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.saving_confirmation)

async def edit_txt_rec(message, state, text, buttons, old):
    id = str(message.from_user.id)
    if await state.get_state() == UserState.recognition:
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
        await state.set_state(UserState.saving_confirmation)

async def edit_audio_rec(message, state, text, buttons, old):
    id = str(message.from_user.id)
    transcription = await audio_file(message.voice.file_id)
    if await state.get_state() == UserState.recognition:
        await remove_thread(id)
    request_mssg = f"Старый прием пищи: {old}, измени его вот так: {transcription}"
    vision = await generate_response(request_mssg, id, VISION_ASS_ID_2)
    Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
    if Iserror:
        await message.answer(f"офибка!!! \n{pretty}")
    else: 
        state.update_data(latest_food = food)
        await message.answer(pretty)
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        await state.set_state(UserState.saving_confirmation)


def generate_day_buttons(data):
    buttons = []
    for day in data:
        emote = "⭕️" if day["isEmpty"] else "✅"
        text = f"{emote} {day['DisplayDay'][:5]} - {day['TotalKkal']} ккал"
        callback_data = f"day_{day['DisplayDay']}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
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
    # data = json.loads(response_json)
    data = response_json
    print(data)
    
    meal_id = data.get("MealId")
    pretty = data["pretty"] if "pretty" in data else None
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
    
    return meal_id, pretty, food_items

async def get_singe_meal(id, date, mealtype):
    url = "https://nutridb-production.up.railway.app/api/TypesCRUD/GetSingleUserMeal"
    meal_data = {
        "userTgId": id,
        "dayStr": date,
        "typemeal": mealtype
    }
    req_headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, data=meal_data, headers=req_headers) as response:
                # data = await response.text()
                data = await response.json()
                meal_id, pretty, food_items = parse_meal_data(data)
                return meal_id, pretty, food_items
        except aiohttp.ClientError as e:
            print(e)

async def delete_meal(id, meal_id):
    url = f"https://nutridb-production.up.railway.app/api/TypesCRUD/DeleteMeal?mealId={id}&userTgId={meal_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url) as response:
                data = await response.text()
                return meal_id
        except aiohttp.ClientError as e:
            print(e)