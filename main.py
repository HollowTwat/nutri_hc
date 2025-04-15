import asyncio
import re
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
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo
from openai import AsyncOpenAI, OpenAI
import shelve
import json
import asyncpg
import signal

from functions import *
from functions2 import *
from menu_functions import *
from day1 import *
from day2 import *
from day3 import *
from day4 import *
from day5 import *
from day6 import *
from day7 import *
from day8 import *
from day9 import *
from day10 import *
from day11 import *
from day12 import *
from day13 import *
from day14 import *
from day15 import *
from day16 import *
from day17 import *
from day18 import *
from day19 import *
from day20 import *
from day21 import *
from questionnaire import *
import all_states
from all_states import *
from stickerlist import STICKER_IDS

ADMIN_IDS = [389054202, 464682207]
BOT_TOKEN = os.getenv("BOT_TOKEN")                    ##ACTUALISED
OPENAI_KEY = os.getenv("OPENAI_KEY")                  ##ACTUALISED

# STICKER_ID = os.getenv("STICKER_ID")

#ASSISTANTS FFS HOW MANY CAN THERE BE MAAAAAN
VISION_ASSISTANT_ID = os.getenv('VISION_ASSISTANT_ID')
CITY_ASSISTANT_ID = os.getenv('CITY_ASSISTANT_ID')
ASSISTANT2_ID = os.getenv('ASSISTANT2_ID')
YAPP_SESH_ASSISTANT_ID = os.getenv('YAPP_SESH_ASSISTANT_ID')    ##ACTUALISED 
RATE_DAY_ASS_ID = os.getenv('RATE_DAY_ASS_ID')                  ##ACTUALISED 
RATE_MID_ASS_ID = os.getenv('RATE_MID_ASS_ID')
RATE_SMOL_ASS_ID = os.getenv('RATE_SMOL_ASS_ID')
RATE_WEEK_ASS_ID = os.getenv('RATE_WEEK_ASS_ID')
RATE_TWONE_ASS_ID = os.getenv('RATE_TWONE_ASS_ID')
ETIK_ASS_ID = os.getenv('ETIK_ASS_ID')
RECIPE_ASS_ID = os.getenv('RECIPE_ASS_ID')
RATE_TRIAL_ASS_ID = os.getenv('RATE_TRIAL_ASS_ID')
VISION_ASS_ID_2 = os.getenv("VISION_ASS_ID_2")        ##ACTUALISED

TOKEN = BOT_TOKEN

DATABASE_URL = (
    f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}"
    f"@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)

# CHAT_ID = os.getenv('LOGS_CHAT_ID')
arrow_back = "⬅️"
arrow_menu = "⏏️" #🆕

bot = Bot(token=TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)

errorbuttons = [[InlineKeyboardButton(text=" 🆘 Помощь", url="t.me/nutri_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
errorkeys = InlineKeyboardMarkup(inline_keyboard=errorbuttons)
noanketbuttons = [[InlineKeyboardButton(text="Заполнить анкету", callback_data="menu_settings_profile_re-anket")],[InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
noankeys = InlineKeyboardMarkup(inline_keyboard=noanketbuttons)

class StateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        state = data['state']
        current_state = await state.get_state()
        data['current_state'] = current_state
        return await handler(event, data)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    asyncio.create_task(log_user_message(message))
    await state.set_state(Questionnaire.prefirst)
    await ensure_user(message)
    await process_prefirst(message, state)
    await state.set_state(Questionnaire.first)
    # await state.update_data(full_sequence=False)
    # buttons = [
    #     [InlineKeyboardButton(text="Меню", callback_data="menu")],
    #     ]
    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    # step0txt = "in_dev"
    # await message.answer(step0txt, reply_markup=keyboard)




################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################
@router.message(Command("menu"))
async def main_menu_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data(extra_plate=False)
    except Exception as e:
        print(f"error{e}")
    asyncio.create_task(log_user_message(message))
    await state.clear()
    await menu_handler(message, state)




@router.callback_query(lambda c: c.data == 'menu')
async def main_menu_cb_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.update_data(extra_plate=False)
    except Exception as e:
        print(f"error{e}")
    asyncio.create_task(log_user_callback(callback_query))
    await state.clear()
    await menu_cb_handler(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_back')
async def main_menu_back_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await menu_back_handler(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_no_edit')
async def main_menu_no_edit(callback_query: CallbackQuery, state: FSMContext) -> None:
    asyncio.create_task(log_user_callback(callback_query))
    await menu_no_edit(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_course')
async def main_process_menu_course(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_course(callback_query.message, state, callback_query.from_user.id)

@router.callback_query(lambda c: c.data == 'menu_dnevnik')
async def main_process_menu_dnevnik(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_dnevnik(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'menu_nutri')
async def main_process_menu_nutri(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_nutri(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'menu_settings')
async def main_process_menu_settings(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_settings(callback_query.message, state)

@router.message(Command("1"))
async def menu_main_process_menu_course(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.menu)
    await state.update_data(extra_plate=False)
    asyncio.create_task(log_user_message(message))
    await process_menu_course(message, state, message.from_user.id)

@router.message(Command("2"))
async def menu_main_process_menu_dnevnik(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.menu)
    await state.update_data(extra_plate=False)
    asyncio.create_task(log_user_message(message))
    await process_menu_dnevnik(message, state)

@router.message(Command("3"))
async def menu_main_process_menu_nutri(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.menu)
    await state.update_data(extra_plate=False)
    asyncio.create_task(log_user_message(message))
    await process_menu_nutri(message, state)

@router.message(Command("4"))
async def menu_main_process_menu_settings(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.menu)
    await state.update_data(extra_plate=False)
    asyncio.create_task(log_user_message(message))
    await process_menu_settings(message, state)
################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_course_lesson_x')
async def main_process_menu_course_lesson(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_course_lesson(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_course_info')
async def main_process_menu_course_info(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_course_info(callback_query, state)

@router.callback_query(lambda c: c.data.startswith('menu_course_info_lessons_week'))
async def main_process_menu_cource_info_lessons(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_cource_info_lessons(callback_query, state)

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

################## Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover ##################

async def dnevnik_layover(message, state, callback_mssg):
    prev_state = await state.get_state()

    await state.set_state(LayoverState.recognition)
    await state.update_data(extra_plate=False)

    await state.update_data(prev_state=prev_state)
    await state.update_data(callback_mssg=callback_mssg)

    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await process_img_rec(message, state, confirm_text, buttons)
        await state.set_state(LayoverState.saving_confirmation)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(LayoverState.saving_confirmation)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(LayoverState.saving_confirmation)
    else: message.answer("0_o")


@router.callback_query(StateFilter(LayoverState.saving_confirmation))
async def layover_state_switch(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    state_data = await state.get_data()
    old_cb = state_data["callback_mssg"]
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    if callback_query.data == "redact":
        await state.set_state(LayoverState.redact)
        await callback_query.message.edit_text(edit_text, reply_markup=None)
    elif callback_query.data == "save":
        if old_cb == "saving_edit":
            await saving_edit(callback_query, state)
            pass
        else:
            mealtype_buttons = [
                [InlineKeyboardButton(text="Завтрак", callback_data="0"), InlineKeyboardButton(text="Обед", callback_data="2")],
                [InlineKeyboardButton(text="Ужин", callback_data="4"), InlineKeyboardButton(text="Перекус", callback_data="5")]
                ]
            mealtype_keyboard = InlineKeyboardMarkup(inline_keyboard=mealtype_buttons)
            await state.set_state(LayoverState.saving)
            await callback_query.message.edit_text("Какой это прием пищи?", reply_markup=mealtype_keyboard)


@router.message(StateFilter(LayoverState.redact))
async def layover_functional_redact(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await message.answer(edit_text)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(LayoverState.saving_confirmation)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(LayoverState.saving_confirmation)
    else: message.answer("0_o")

@router.callback_query(StateFilter(LayoverState.saving))
async def layover_saving(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    data = await state.get_data()
    callback_mssg = data["callback_mssg"]
    prev_state = data["prev_state"]
    food = data["latest_food"]
    id = str(callback_query.from_user.id)
    buttons = [[InlineKeyboardButton(text="Ок", callback_data=callback_mssg)],]
    if callback_mssg == "saving_edit":
        await state.set_state(prev_state)
        state_data = state.get_data()
        old_date = state_data["date"]
        Iserror, answer = await save_meal_old_date(callback_query.from_user.id, food, callback_query.data, old_date)
    else:
        Iserror, answer = await save_meal(callback_query.from_user.id, food, callback_query.data)
    if Iserror:
        await callback_query.message.edit_text(f"Ошибка при сохранении {answer}")
        asyncio.create_task(log_bot_response(f"Ошибка при сохранении {answer}", callback_query.from_user.id))
    else:
        if answer != 0:
            await callback_query.message.edit_text(f"Успешно сохранено", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            asyncio.create_task(log_bot_response("Успешно сохранено", callback_query.from_user.id))
            await state.set_state(UserState.rating_meal)
    
    await state.set_state(prev_state)
    
    

################## Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover Layover ##################

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_dnevnik_input')
async def main_process_menu_dnevnik_input(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await state.set_state(UserState.recognition)
    await state.update_data(extra_plate=False)
    await process_menu_dnevnik_input(callback_query, state)

@router.callback_query(lambda c: c.data.startswith("menu_dnevnik_edit"))
async def main_process_menu_dnevnik_edit(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_dnevnik_edit(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis')
async def main_process_menu_dnevnik_analysis(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_dnevnik_analysis(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_instruction')
async def main_process_menu_dnevnik_instruction(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await state.set_state(UserState.instruction)
    await process_menu_dnevnik_instruction(callback_query, state)

@router.callback_query(StateFilter(UserState.instruction), lambda c: c.data == 'next')
async def main_process_menu_dnevnik_instruction_2(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_dnevnik_instruction_2(callback_query, state)

@router.callback_query(StateFilter(UserState.instruction), lambda c: c.data == 'next2')
async def main_process_menu_dnevnik_instruction_3(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_dnevnik_instruction_3(callback_query, state)
    await state.set_state(UserState.menu)

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_nutri_yapp')
async def main_process_menu_nutri_yapp(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_nutri_yapp(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_nutri_reciepie')
async def main_process_menu_nutri_reciepie(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_nutri_reciepie(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_nutri_etiketka')
async def main_process_menu_nutri_etiketka(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await state.set_state(UserState.etiketka)
    await process_menu_nutri_etiketka(callback_query, state)

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

################## ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ##################

@router.message(StateFilter(UserState.etiketka))
async def main_process_etiketka_input(message: Message, state: FSMContext):
     
    asyncio.create_task(log_user_message(message))
    if message.photo:
        sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
        iserror, user_data = await get_user_info(message.from_user.id)
        user_info = json.loads(user_data)
        isempty = user_info.get("isempty", False)
        if isempty == "true":
            await sticker_mssg.delete()
            await message.answer("Ваша анкета не заполнена", reply_markup=noankeys)
            return
        allergies = user_info.get("user_info_meals_ban")
        url = await get_url(message.photo[-1].file_id)
        try:
            gpt_response = await process_url_etik(url, allergies, ETIK_ASS_ID)
            await sticker_mssg.delete()
            await message.answer(gpt_response)
            asyncio.create_task(log_bot_response(gpt_response, message.from_user.id))
            await state.set_state(UserState.menu)
        except Exception as e:
            await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
    else:
        await message.answer("Отправь, пожалуйста, фото")

################## ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ETIKETKA ##################

################## RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE ##################

@router.callback_query(lambda c: c.data.startswith("recimt_"))
async def main_process_menu_nutri_rec_mealtype(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await remove_rec_thread(str(callback_query.from_user.id))
    await state.set_state(UserState.reci_mt)
    meal_type_rec = callback_query.data.split("_")[1]
    await state.update_data(meal_type_rec=meal_type_rec)
    await process_menu_nutri_rec_inputType(callback_query, state)

@router.callback_query(lambda c: c.data.startswith("reciIt_"))
async def main_process_menu_nutri_rec_Inputtype(callback_query: CallbackQuery, state: FSMContext):
     
    asyncio.create_task(log_user_callback(callback_query))
    input_type = callback_query.data.split("_")[1]
    await state.update_data(input_rec_type=input_type)

    state_data = await state.get_data()
    meal_type = state_data["meal_type_rec"]
    meal_type_mapping = {"0": "Завтрак", "2": "Обед", "4": "Ужин", "5":"Перекус"}
    if input_type == "1":
        await state.set_state(UserState.reci)
        await menu_nutri_rec_input_1(callback_query, state)
        return
    elif input_type == "0":
        await process_menu_nutri_rec_inputType_2(callback_query, state)
        return
    elif input_type == "2":
        await state.set_state(UserState.reci)
        await menu_nutri_rec_input_2(callback_query, state)
        return
    elif input_type == "3":
        sticker_mssg = await callback_query.message.answer_sticker(random.choice(STICKER_IDS))
        buttons = [[InlineKeyboardButton(text="Да, спасибо", callback_data="menu")], [InlineKeyboardButton(text="Изменить продукты", callback_data="reciIt_2")], [InlineKeyboardButton(text="Нет, подбери другой рецепт", callback_data="reciIt_retry")]]
        await state.set_state(UserState.reci)
        iserror1, user_data = await get_user_info(callback_query.from_user.id)
        user_info = json.loads(user_data)
        isempty = user_info.get("isempty", False)
        if isempty == "true":
            await sticker_mssg.delete()
            await callback_query.message.answer("Ваша анкета не заполнена", reply_markup=noankeys)
            return
        question = f"Придумай полезный и вкусный рецепт {meal_type_mapping.get(meal_type)} для пользователя с информацией: {user_data}"
        iserror, gptresponse = await create_reciepie(question, callback_query.from_user.id)
        if not iserror:
            await sticker_mssg.delete()
            await callback_query.message.edit_text(gptresponse, reply_markup=None)
            asyncio.create_task(log_bot_response(gptresponse, callback_query.from_user.id))
            await callback_query.message.answer("Готовим по этому рецепту?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        elif iserror:
            await callback_query.message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
    elif input_type == "retry":
        sticker_mssg = await callback_query.message.answer_sticker(random.choice(STICKER_IDS))
        buttons = [[InlineKeyboardButton(text="Да, спасибо", callback_data="menu")], [InlineKeyboardButton(text="Изменить продукты", callback_data="reciIt_2")], [InlineKeyboardButton(text="Нет, подбери другой рецепт", callback_data="reciIt_retry")]]
        question = f"Придумай другой рецепт"
        iserror, gptresponse = await create_reciepie(question, callback_query.from_user.id)
        if not iserror:
            await sticker_mssg.delete()
            await callback_query.message.edit_text(gptresponse, reply_markup=None)
            asyncio.create_task(log_bot_response(gptresponse, callback_query.from_user.id))
            await callback_query.message.answer("Готовим по этому рецепту?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        elif iserror:
            await callback_query.message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
            
@router.message(StateFilter(UserState.reci))
async def main_process_reci_input(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    meal_type_mapping = {"0": "Завтрака", "2": "Обеда", "4": "Ужина", "5":"Перекуса"}
    state_data = await state.get_data()
    input_type = state_data["input_rec_type"]
    meal_type = state_data["meal_type_rec"]
    iserror1, user_data = await get_user_info(message.from_user.id)
    user_info = json.loads(user_data)
    isempty = user_info.get("isempty", False)
    if isempty == "true":
        await sticker_mssg.delete()
        await message.answer("Ваша анкета не заполнена", reply_markup=noankeys)
        return
    buttons = [[InlineKeyboardButton(text="Да, спасибо", callback_data="menu")], [InlineKeyboardButton(text="Изменить продукты", callback_data="reciIt_2")], [InlineKeyboardButton(text="Нет, подбери другой рецепт", callback_data="reciIt_retry")]]
    if message.text:
        user_input = message.text
    elif message.voice:
        user_input = await audio_file(message.voice.file_id)

    if input_type == "1":
        question = f"Распиши рецепт {meal_type_mapping.get(meal_type)} по рецепту : {user_input} для пользователя с информацией: {user_data}, "
        iserror, gptresponse = await create_reciepie(question, message.from_user.id)
        if not iserror:
            await sticker_mssg.delete()
            await message.answer(gptresponse)
            asyncio.create_task(log_bot_response(gptresponse, message.from_user.id))
            await message.answer("Готовим по этому рецепту?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    elif input_type == "2":
        question = f"Придумай рецепт {meal_type_mapping.get(meal_type)} вот с этими продуктами: {user_input} для пользователя с информацией: {user_data}"
        iserror, gptresponse = await create_reciepie(question, message.from_user.id)
        if not iserror:
            await sticker_mssg.delete()
            await message.answer(gptresponse)
            asyncio.create_task(log_bot_response(gptresponse, message.from_user.id))
            await message.answer("Готовим по этому рецепту?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


################## RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE RECIEPE ##################


async def get_url(file_id: str) -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    return file_url

async def audio_file(file_id: str) -> str:
    file_url = await get_url(file_id)
    transcription = await transcribe_audio_from_url(file_url)
    return transcription


@router.callback_query(StateFilter(UserState.perehvat))
async def perehvat_actual(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    state_data = await state.get_data()
    perehvat_mssg = state_data["perehvat_mssg"]
    if callback_query.data == "perehvat_yapp":
        await state.set_state(UserState.yapp_new)
        await yapp_functional(perehvat_mssg, state)
    elif callback_query.data == "perehvat_dnevnik":
        await state.set_state(UserState.recognition)
        await state.update_data(extra_plate=False)
        await dnevnik_functional(perehvat_mssg, state)




################## YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP ##################

@router.message(StateFilter(UserState.yapp_new, UserState.yapp))
async def yapp_functional(message: Message, state: FSMContext):
     
    asyncio.create_task(log_user_message(message))
    if await state.get_state() == UserState.yapp_new:
        new_thread = True
    elif await state.get_state() == UserState.yapp:
        new_thread = False
    id = str(message.from_user.id)
    buttons = [[InlineKeyboardButton(text=arrow_menu, callback_data='menu_back')]]
    errormessage = "Гпт вернул ошибку"
    if message.text:
        try:
            sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
            flag, response = await yapp(id, message.text, new_thread)
            if flag:
                await sticker_mssg.delete()
                if response == "Ваша анкета не заполнена":
                    await message.answer(response, reply_markup=noankeys)    
                    return
                await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
                # await message.answer(errormessage)
            else: 
                await sticker_mssg.delete()
                if len(response) <= 4050:
                    await message.answer(f"{response}\n\nТы можешь продолжить общаться со мной или нажать кнопку", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
                else:
                    chunks = [response[i:i + 4050] for i in range(0, len(response), 4050)]
                    for i, chunk in enumerate(chunks):
                        if i == len(chunks) - 1:
                            chunk += "\n\nТы можешь продолжить общаться со мной или нажать кнопку"
                            await message.answer(chunk, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
                        else:
                            await message.answer(chunk)
                asyncio.create_task(log_bot_response(response, message.from_user.id))
                await state.set_state(UserState.yapp)
        except Exception as e:
            await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
        
    elif message.voice:
        try:
            sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
            transcription = await audio_file(message.voice.file_id)
            flag, response = await yapp(id, transcription, new_thread)
            if flag:
                await sticker_mssg.delete()
                await message.answer(errormessage)
            else:
                await sticker_mssg.delete()
                await message.answer(f"{response}\n\n Ты можешь продолжить общаться со мной или нажать кнопку", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
                asyncio.create_task(log_bot_response(response, message.from_user.id))
                await state.set_state(UserState.yapp)
        except Exception as e:
            await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
            
    else:
        await message.answer("Для распознания фото зайди в раздел дневник", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

################## YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP ##################

user_locks = {}

def get_lock_for_user(user_id: str) -> asyncio.Lock:
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]

async def process_media_group_after_delay(message: Message, media_group_id: str, user_id: str, state: FSMContext, confirm_text: str, buttons, delay: float = 3.0):
    sticker_mssg = await message.answer_sticker(random.choice(STICKER_IDS))
    await asyncio.sleep(delay)
    lock = get_lock_for_user(user_id)
    async with lock:
        state_data = await state.get_data()
        media_group = state_data.get("media_group", {})
        group_entry = media_group.get(media_group_id)
        if group_entry and group_entry.get("urls"):
            urls = group_entry["urls"]
            print(f"Processing media group {media_group_id} for user {user_id} with URLs: {urls}")
        else:
            urls = []
        # Remove this group from state.
        if "media_group" in state_data and media_group_id in state_data["media_group"]:
            state_data["media_group"].pop(media_group_id, None)
            await state.update_data(media_group=state_data["media_group"])
    
    if urls:
        vision = await process_urls(urls, user_id, VISION_ASS_ID_2)
        print("Vision response:", vision)
        Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
        if Iserror:
            await sticker_mssg.delete()
            errorkeyboard = [
                [InlineKeyboardButton(text="Написать в поддержку", url="t.me/nutri_care")],
                [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]
            ]
            await message.answer("Не могу распознать еду", reply_markup=InlineKeyboardMarkup(inline_keyboard=errorkeyboard))
        else:
            await sticker_mssg.delete()
            await state.update_data(latest_food = food)
            await message.answer(pretty)
            await message.answer(confirm_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))



################## DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK ##################

@router.message(StateFilter(UserState.recognition))
async def dnevnik_functional(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    state_data = await state.get_data()
    extra_plate = state_data.get('extra_plate', False)
    id = str(message.from_user.id)
    isActive = await check_is_active_state(id, state)
    if not isActive:
        bttns = [
            [InlineKeyboardButton(text="Хочу оплатить", url="https://nutri-ai.ru/?promo=COMMUNITY&utm_medium=referral&utm_source=telegram&utm_campaign=COMMUNITY")], 
            [InlineKeyboardButton(text="🆘 Помощь", url="t.me/nutri_care")]
            ]
        await message.answer("Ваша подписка не активна", reply_markup=InlineKeyboardMarkup(inline_keyboard=bttns))
        asyncio.create_task(log_bot_response(f"СТАТУС ПОДПИСКИ {isActive}", message.from_user.id))
        return
    if not extra_plate:
        confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    elif extra_plate:
        confirm_text = "Все верно?"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
            [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        if message.media_group_id:
            url = await get_url(message.photo[-1].file_id)
            lock = get_lock_for_user(id)
            async with lock:
                # Reload state data under the lock.
                state_data = await state.get_data()
                media_group = state_data.get("media_group", {})
                if message.media_group_id not in media_group:
                    media_group[message.media_group_id] = {"urls": [], "scheduled": False}
                media_group[message.media_group_id]["urls"].append(url)
                print(f"Appended URL {url} to media group {message.media_group_id} for user {id}. "
                      f"Current URLs: {media_group[message.media_group_id]['urls']}")
                if not media_group[message.media_group_id]["scheduled"]:
                    media_group[message.media_group_id]["scheduled"] = True
                    await state.update_data(media_group=media_group)
                    asyncio.create_task(
                        process_media_group_after_delay(message, message.media_group_id, id, state, confirm_text, buttons, delay=2.0)
                    )
                else:
                    await state.update_data(media_group=media_group)
        else:
            await process_img_rec(message, state, confirm_text, buttons)
        if not extra_plate:
            await state.set_state(UserState.saving_confirmation)
        elif extra_plate:
            await state.set_state(UserState.saving)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        if not extra_plate:
            await state.set_state(UserState.saving_confirmation)
        elif extra_plate:
            await state.set_state(UserState.saving)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        if not extra_plate:
            await state.set_state(UserState.saving_confirmation)
        elif extra_plate:
            await state.set_state(UserState.saving)
    else: message.answer("0_o")

@router.message(StateFilter(UserState.redact))
async def dnevnik_functional_edit(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    state_data = await state.get_data()
    extra_plate = state_data.get('extra_plate', False)
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    # confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    confirm_text = "Все верно?"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await message.answer(edit_text)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        if not extra_plate:
            await state.set_state(UserState.saving_confirmation)
        elif extra_plate:
            await state.set_state(UserState.saving)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        if not extra_plate:
            await state.set_state(UserState.saving_confirmation)
        elif extra_plate:
            await state.set_state(UserState.saving)
    else: message.answer("0_o")

@router.callback_query(StateFilter(UserState.saving_confirmation))
async def state_switch(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    if callback_query.data == "redact":
        await state.set_state(UserState.redact)
        await callback_query.message.edit_text(edit_text, reply_markup=None)
    elif callback_query.data == "save":
        mealtype_buttons = [
            [InlineKeyboardButton(text="Завтрак", callback_data="0"), InlineKeyboardButton(text="Обед", callback_data="2")],
            [InlineKeyboardButton(text="Ужин", callback_data="4"), InlineKeyboardButton(text="Перекус", callback_data="5")]
            ]
        mealtype_keyboard = InlineKeyboardMarkup(inline_keyboard=mealtype_buttons)
        await state.set_state(UserState.saving)
        await callback_query.message.edit_text("Какой это прием пищи?", reply_markup=mealtype_keyboard)

@router.callback_query(StateFilter(UserState.saving))
async def saving(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    state_data = await state.get_data()
    food = state_data["latest_food"]
    extra_plate = state_data.get('extra_plate', False)
    if not extra_plate:
        Iserror, answer = await save_meal(callback_query.from_user.id, food, callback_query.data)
        await state.update_data(meal_id=answer)
    elif extra_plate:
        if callback_query.data == "redact":
            edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
            await state.set_state(UserState.redact)
            await callback_query.message.edit_text(edit_text, reply_markup=None)
            return
        meal_id = state_data["meal_id"]
        Iserror, answer = await save_meal_plate(callback_query.from_user.id, food, meal_id)
        await state.update_data(meal_id=answer)
    if not extra_plate:
        buttons = [
            [InlineKeyboardButton(text="Да, добавить", callback_data="add_extra_plate")],
            [InlineKeyboardButton(text="Получить оценку", callback_data="meal_rate")],
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu")]
        ]
    elif extra_plate:
        buttons = [
            [InlineKeyboardButton(text="Да, добавить", callback_data="add_extra_plate")],
            [InlineKeyboardButton(text="Хватит, все что хотел добавил", callback_data="extra_plate_done")],
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu")]
        ]
    if Iserror:
        await callback_query.message.edit_text("Ошибка при сохранении {answer}")
    else:
        if answer != 0:
            await callback_query.message.edit_text("Сохранено в дневник ✅\nДобавить в твой прием пищи еще одно блюдо?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            await state.set_state(UserState.rating_meal)

@router.callback_query(lambda c: c.data == 'add_extra_plate')
async def add_extra_plate(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await state.set_state(UserState.recognition)
    await state.update_data(extra_plate=True)
    await process_menu_dnevnik_input(callback_query, state)

@router.callback_query(lambda c: c.data == 'extra_plate_done')
async def add_extra_plate(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.recognition)
    state_data = await state.get_data()
    meal_id = state_data["meal_id"]
    await state.update_data(extra_plate=False)
    buttons = [
            [InlineKeyboardButton(text="Хочу оценку", callback_data="meal_rate_extra")],
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu")]
        ]
    asyncio.create_task(log_user_callback(callback_query))
    iserror, pretty, meals  = await get_user_meal_by_mealid(callback_query.from_user.id, meal_id)
    if not iserror:
        await state.set_state(UserState.menu)
        await state.update_data(extra_plate_meal=str(meals))
        await callback_query.message.edit_text(f"Принято, вот твой прием по итогу всех тарелок:\n{pretty}", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@router.callback_query(lambda c: c.data.startswith("meal_rate"))
async def main_meal_rate(callback_query: CallbackQuery, state: FSMContext):
    
    id = callback_query.from_user.id
    isActive = await check_is_active_state(id, state)
    if not isActive:
        bttns = [[InlineKeyboardButton(text="Хочу оплатить", url="https://nutri-ai.ru/?promo=COMMUNITY&utm_medium=referral&utm_source=telegram&utm_campaign=COMMUNITY")], [InlineKeyboardButton(text=" 🆘 Помощь", url="t.me/nutri_care")]]
        await callback_query.message.answer("Ваша подписка не активна", reply_markup=InlineKeyboardMarkup(inline_keyboard=bttns))
        asyncio.create_task(log_bot_response(f"СТАТУС ПОДПИСКИ {isActive}", id))
        return
    asyncio.create_task(log_user_callback(callback_query))
    sticker_mssg = await callback_query.message.answer_sticker(random.choice(STICKER_IDS))
    state_data = await state.get_data()
    if callback_query.data == "meal_rate":
        food = state_data["latest_food"]
    elif callback_query.data == "meal_rate_extra":
        food = state_data["extra_plate_meal"]
    Iserror, user_data = await get_user_info(callback_query.from_user.id)
    user_info = json.loads(user_data)
    isempty = user_info.get("isempty", False)
    if isempty == "true":
        await sticker_mssg.delete()
        await callback_query.message.answer("Ваша анкета не заполнена", reply_markup=noankeys)
        return
    if Iserror:
        await sticker_mssg.delete()
        await callback_query.message.edit_text("Ошибка при получении инфы пользователя из дб")
        return
    try:
        question = create_day_rate_question(user_data, food)
        print(question)
        gpt_resp = await no_thread_ass(question, RATE_DAY_ASS_ID)
        cleaned_resp = await remove_reference(gpt_resp)
        buttons = [
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu")]
        ]
        await sticker_mssg.delete()
        await callback_query.message.edit_text(cleaned_resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        asyncio.create_task(log_bot_response(cleaned_resp, callback_query.from_user.id))
        await state.clear()
    except Exception as e:
            print(f"user {callback_query.from_user.id} error {e}")
            await callback_query.message.answer("Упс, поймали ошибку", reply_markup=errorkeys)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis_rate-week')
async def main_meal_rate_week(callback_query: CallbackQuery, state: FSMContext):
    id = callback_query.from_user.id
    isActive = await check_is_active_state(id, state)
    if not isActive:
        bttns = [[InlineKeyboardButton(text="Хочу оплатить", url="https://nutri-ai.ru/?promo=COMMUNITY&utm_medium=referral&utm_source=telegram&utm_campaign=COMMUNITY")], [InlineKeyboardButton(text=" 🆘 Помощь", url="t.me/nutri_care")]]
        await callback_query.message.answer("Ваша подписка не активна", reply_markup=InlineKeyboardMarkup(inline_keyboard=bttns))
        asyncio.create_task(log_bot_response(f"СТАТУС ПОДПИСКИ {isActive}", id))
        return
    asyncio.create_task(log_user_callback(callback_query))
    sticker_mssg = await callback_query.message.answer_sticker(sticker=random.choice(STICKER_IDS))
    iserror, resp = await long_rate(callback_query.from_user.id, "3")
    await sticker_mssg.delete()
    if iserror:
        await callback_query.answer()
        if resp == "Ваша анкета не заполнена":
            await callback_query.message.answer(resp, reply_markup=noankeys)
            return
        await callback_query.message.answer("Ошибка в обработке оценки", reply_markup=errorkeys)
    buttons = [[InlineKeyboardButton(text=arrow_menu, callback_data="menu")]]
    buttons1 = [[InlineKeyboardButton(text="Показать график за неделю", callback_data="menu_dnevnik_analysis_graph")],[InlineKeyboardButton(text=arrow_menu, callback_data="menu")]]
    if await state.get_state() == UserState.graph:
        await callback_query.message.answer(resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        asyncio.create_task(log_bot_response(resp, callback_query.from_user.id))
    else:
        await callback_query.message.edit_text(resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons1))
        asyncio.create_task(log_bot_response(resp, callback_query.from_user.id))

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis_rate-day')
async def main_meal_rate_day(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    try:
        id = callback_query.from_user.id
        isActive = await check_is_active_state(id, state)
        if not isActive:
            bttns = [[InlineKeyboardButton(text="Хочу оплатить", url="https://nutri-ai.ru/?promo=COMMUNITY&utm_medium=referral&utm_source=telegram&utm_campaign=COMMUNITY")], [InlineKeyboardButton(text=" 🆘 Помощь", url="t.me/nutri_care")]]
            await callback_query.message.answer("Ваша подписка не активна", reply_markup=InlineKeyboardMarkup(inline_keyboard=bttns))
            asyncio.create_task(log_bot_response(f"СТАТУС ПОДПИСКИ {isActive}", id))
            return
        sticker_mssg = await callback_query.message.answer_sticker(sticker=random.choice(STICKER_IDS))
        iserror, resp = await long_rate(callback_query.from_user.id, "0")
        await sticker_mssg.delete()
        if iserror:
            await callback_query.answer()
            if resp == "Ваша анкета не заполнена":
                await callback_query.message.answer(resp, reply_markup=noankeys)
                return
            print(f"user {callback_query.from_user.id} error {resp}")
            await callback_query.message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
        buttons = [[InlineKeyboardButton(text=arrow_menu, callback_data="menu")]]
        await callback_query.message.edit_text(resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        asyncio.create_task(log_bot_response(resp, callback_query.from_user.id))
    except Exception as e:
            print(f"user {callback_query.from_user.id} error {e}")
            await callback_query.message.answer("Упс, поймали ошибку", reply_markup=errorkeys)

######################################################### EDIT EDIT EDIT ##############################################
@router.callback_query(StateFilter(UserState.edit), lambda c: c.data.startswith("day_"))
async def day_selected(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    day = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    meal_data = user_data.get("meal_data", [])
    
    await callback_query.message.edit_text(f"Выбрана дата: {day}", reply_markup=generate_meal_buttons(meal_data, day))


@router.callback_query(StateFilter(UserState.edit), lambda c: c.data.startswith("meal_"))
async def meal_selected(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    id = str(callback_query.from_user.id)
    isEmpty = callback_query.data.split("_")[1]
    date = callback_query.data.split("_")[2]
    meal_type = callback_query.data.split("_")[3]
    await state.update_data(date=date, meal_type=meal_type)
    if isEmpty == "True":
        buttons = [
            [InlineKeyboardButton(text="Нет, выбрать другую дату", callback_data="menu_dnevnik_edit_same")],
            [InlineKeyboardButton(text="Да, заносим", callback_data="menu_dnevnik_add_edit")],
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu"), InlineKeyboardButton(text=arrow_back, callback_data=f"day_{date}")]
        ]
        await callback_query.message.edit_text("У тебя нету занесенного приема пищи за эту дату, заносим?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        return
    else:
        meal_id, pretty, food_items = await get_singe_meal(id, date, meal_type)
        await state.update_data(old_food=food_items, meal_id=meal_id)
        buttons = [
            [InlineKeyboardButton(text="Да", callback_data=f"yesChange_{meal_id}")],
            [InlineKeyboardButton(text="Удалить", callback_data=f"deletemeal_{meal_id}")],
            [InlineKeyboardButton(text="Выбрать другой день", callback_data="menu_dnevnik_edit_same")],
            [InlineKeyboardButton(text=arrow_menu, callback_data="menu"), InlineKeyboardButton(text=arrow_back, callback_data=f"day_{date}")]
        ]
        await callback_query.message.edit_text(f"{pretty}", reply_markup=None)
        await callback_query.message.answer("Меняем?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@router.callback_query(StateFilter(UserState.edit), lambda c: c.data.startswith("deletemeal_"))
async def delete_meal_selected(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    id = str(callback_query.from_user.id)
    meal_id = callback_query.data.split("_")[1]
    Iserror, response = await delete_meal(id, meal_id)
    print(f"{Iserror}, {response}")
    buttons = [
        [InlineKeyboardButton(text=arrow_menu, callback_data="menu"), InlineKeyboardButton(text=arrow_back, callback_data="menu_dnevnik_edit")]
    ]
    if Iserror : 
        await callback_query.message.edit_text("Что-то пошло не так", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        pass
    if response == "true":
        await callback_query.message.edit_text("Успешно удалено", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    elif response == "false": 
        await callback_query.message.edit_text("Не вышло удалить", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@router.callback_query(StateFilter(UserState.edit), lambda c: c.data == "menu_dnevnik_add_edit")
async def edit_new_await(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    step0txt = "Отправь фото еды.\nТакже можешь воспользоваться 🎤 аудио или ввести текстом в формате:\n<i>Яичница из 2 яиц, чай без сахара</i>"
    await callback_query.message.edit_text(step0txt, reply_markup=None)
    await state.set_state(UserState.edit_new)

@router.message(StateFilter(UserState.edit_new))
async def edit_newmeal(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    await dnevnik_layover(message,state,"saving_edit")

@router.callback_query(StateFilter(UserState.edit), lambda c: c.data.startswith("yesChange"))
async def edit_new_await(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    mssg_txt = "Говори/пиши что менять"
    await callback_query.message.edit_text(mssg_txt, reply_markup=None)
    await state.set_state(UserState.edit_rec)

@router.message(StateFilter(UserState.edit_rec))
async def dnevnik_functional_recc(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await message.answer(edit_text)
    elif message.voice:
        await edit_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.edit_save_confirm)
    elif message.text:
        await edit_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.edit_save_confirm)
    else: message.answer("0_o")

@router.callback_query(StateFilter(UserState.edit_save_confirm))
async def state_switch(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    if callback_query.data == "redact":
        await state.set_state(UserState.edit_redact)
        await callback_query.message.edit_text(edit_text, reply_markup=None)
    elif callback_query.data == "save":
        state_data = await state.get_data()
        food = state_data["latest_food"]
        meal_id = state_data["meal_id"]
        meal_type = state_data["meal_type"]
        Iserror, answer = await edit_existing_meal(callback_query.from_user.id, food, meal_type, meal_id)
        if Iserror:
            await callback_query.message.edit_text("Ошибка при сохранении", reply_markup=None)
        else:
            if answer != 0:
                saving_text = f"Изменение сохранено"
                await callback_query.message.edit_text(saving_text)

@router.message(StateFilter(UserState.edit_redact))
async def dnevnik_functional_edit(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await message.answer(edit_text)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.edit_save_confirm)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.edit_save_confirm)
    else: message.answer("0_o")

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis_graph')
async def main_meal_rate_week(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await state.set_state(UserState.graph)
    await request_for_graph(callback_query.from_user.id)

################## DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK ##################

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_settings_profile')
async def main_process_menu_settings_profile(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_settings_profile(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_settings_help')
async def main_process_menu_settings_help(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_settings_help(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_settings_sub')
async def main_process_menu_settings_sub(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await process_menu_settings_sub(callback_query, state)

@router.callback_query(StateFilter(UserState.change_user_info), lambda c: True)
async def main_change_user_info(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    state_data = await state.get_data()
    name = state_data["name"]
    kkal = state_data["target_calories"]
    allergies = state_data["allergies"]
    timeslide = state_data["timeslide"]
    if callback_query.data == "menu_settings_profile_name":
        await change_user_name(callback_query, state, name)
    elif callback_query.data == "menu_settings_profile_kkal":
        await change_user_kkal(callback_query, state, kkal)
    elif callback_query.data == "menu_settings_profile_allergies":
        await change_user_allergies(callback_query, state, allergies)
    elif callback_query.data == "menu_settings_profile_timeslide":
        await change_user_timeslide(callback_query, state, timeslide)
    elif callback_query.data == "menu_settings_profile_re-anket":
        await process_reanket(callback_query, state)
        await state.set_state(Questionnaire.name)
    elif callback_query.data == "menu_settings_profile_notif":
        await change_user_notifs(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_settings_profile_re-anket')
async def main_process_reanket_from_anywhere(callback_query: CallbackQuery, state: FSMContext):
    await process_reanket(callback_query, state)
    await state.set_state(Questionnaire.name)

@router.message(StateFilter(UserState.name_change))
async def main_change_name(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    await process_change_name(message, state)
    await state.set_state(UserState.menu)

@router.message(StateFilter(UserState.kkal_change))
async def main_change_kkal(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    pattern = r'^-?\d+$'
    if re.match(pattern, message.text):
        await process_change_kkal(message, state)
    else:
        await message.answer("Напиши число")

@router.message(StateFilter(UserState.allergy_change))
async def main_change_allergies(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    await process_change_allergies(message, state)

@router.message(StateFilter(UserState.slide_change))
async def main_change_slide(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    pattern = r'^(0|[+-]\d+)$'
    if re.match(pattern, message.text):
        await process_change_slide(message, state)
    else:
        await message.answer("Введи отклонение в формате: <i>+2 или 0 или -10</i>")

@router.callback_query(lambda c: c.data == 'user_change_notif_time')
async def main_process_menu_settings_notif(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    await ping_change_start(callback_query, state)

@router.callback_query(lambda c: c.data == 'user_notif_toggle')
@router.callback_query(StateFilter(UserState.notif_toggle))
async def main_process_menu_settings_notif_toggle(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.notif_toggle)
    await process_menu_settings_notif_toggle(callback_query, state)
                
@router.message(StateFilter(UserState.morning_ping_change))
async def main_change_morning_ping(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await change_morning_ping(message, state)
    else:
        await message.answer("Укажи время в формате ЧЧ:ММ Например 10:00")

@router.message(StateFilter(UserState.evening_ping_change))
async def main_change_evening_ping(message: types.Message, state:FSMContext):
    asyncio.create_task(log_user_message(message))
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await change_evening_ping(message, state)
    else:
        await message.answer("Укажи время в формате ЧЧ:ММ Например, 20:00")


################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################

@router.callback_query(lambda c: c.data == 'lesson_0_done')
async def start_lesson(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(LessonStates.step_1)
    await process_step_1(callback_query, state)

################## LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 ##################

@router.callback_query(StateFilter(LessonStates.step_1), lambda c: True)
async def main_process_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_1(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_2), lambda c: True)
async def main_process_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_3), lambda c: True)
async def main_process_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_3(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_4), lambda c: True)
async def main_process_step_4(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_4(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_5), lambda c: True)
async def main_process_step_5(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_5(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_6), lambda c: True)
async def main_process_step_6(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "quitout":
        await callback_query.message.answer("Лучше ловить мотивацию, пока она есть!\nПоэтому жду тебя завтра с новыми силами и первым уроком! Хорошего дня 😉")
        await state.set_state(UserState.menu)
        await callback_query.answer()
        return
    await process_step_6(callback_query, state)

@router.callback_query(StateFilter(LessonStates.step_7), lambda c: True)
async def main_process_step_7(callback_query: types.CallbackQuery, state: FSMContext):
    await process_step_7(callback_query, state)

################## LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 LESSON_1 ##################

##################### GETTING INTO THE LESSONS

@router.message(Command("lessons_manage"))
async def lessons_manage_command(message: types.Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    await state.clear()
    buttons = [
        [InlineKeyboardButton(text='Урок1', callback_data='d1')],
        [InlineKeyboardButton(text='Урок2', callback_data='d2'), InlineKeyboardButton(text='Урок2_2', callback_data='d2_2')],
        [InlineKeyboardButton(text='Урок3', callback_data='d3'),InlineKeyboardButton(text='Урок3_2', callback_data='d3_2')],
        [InlineKeyboardButton(text='Урок4', callback_data='d4'),InlineKeyboardButton(text='Урок4_2', callback_data='d4_2')],
        [InlineKeyboardButton(text='Урок5', callback_data='d5'),InlineKeyboardButton(text='Урок5_2', callback_data='d5_2')],
        [InlineKeyboardButton(text='Урок6', callback_data='d6'),InlineKeyboardButton(text='Урок6_2', callback_data='d6_2')],
        [InlineKeyboardButton(text='Урок7', callback_data='d7')],
        [InlineKeyboardButton(text='Урок8', callback_data='d8'),InlineKeyboardButton(text='Урок8_2', callback_data='d8_2')],
        [InlineKeyboardButton(text='Урок9', callback_data='d9'),InlineKeyboardButton(text='Урок9_2', callback_data='d9_2')],
        [InlineKeyboardButton(text='Урок10', callback_data='d10'),InlineKeyboardButton(text='Урок10_2', callback_data='d10_2')],
        [InlineKeyboardButton(text='Урок11', callback_data='d11'),InlineKeyboardButton(text='Урок11_2', callback_data='d11_2')],
        [InlineKeyboardButton(text='Урок12', callback_data='d12'),InlineKeyboardButton(text='Урок12_2', callback_data='d12_2')],
        [InlineKeyboardButton(text='Урок13', callback_data='d13'),InlineKeyboardButton(text='Урок13_2', callback_data='d13_2')],
        [InlineKeyboardButton(text='Урок14', callback_data='d14')],
        [InlineKeyboardButton(text='Урок15', callback_data='d15'),InlineKeyboardButton(text='Урок15_2', callback_data='d15_2')],
        [InlineKeyboardButton(text='Урок16', callback_data='d16'),InlineKeyboardButton(text='Урок16_2', callback_data='d16_2')],
        [InlineKeyboardButton(text='Урок17', callback_data='d17'),InlineKeyboardButton(text='Урок17_2', callback_data='d17_2')],
        [InlineKeyboardButton(text='Урок18', callback_data='d18')],
        [InlineKeyboardButton(text='Урок19', callback_data='d19')],
        [InlineKeyboardButton(text='Урок20', callback_data='d20')],
        [InlineKeyboardButton(text='Урок21', callback_data='d21')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("pick a lesson", reply_markup=keyboard)

# dayslist = ["d1", "d2", "d2_2", "d3", "d3_2", "d4", "d4_2", "d5", "d5_2","d6","d6_2","d7","d8","d8_2","d9","d9_2","d10","d10_2","d11","d11_2","d12","d12_2","d13","d13_2","d14","d15","d15_2","d16","d16_2","d17","d17_2","d18","d19","d20","d21"]
# @router.callback_query(lambda c: c.data in dayslist)
@router.callback_query(lambda c: c.data in ["d1", "d2", "d2_2", "d3", "d3_2", "d4", "d4_2", "d5", "d5_2","d6","d6_2","d7","d8","d8_2","d9","d9_2","d10","d10_2","d11","d11_2","d12","d12_2","d13","d13_2","d14","d15","d15_2","d16","d16_2","d17","d17_2","d18","d19","d20","d21"])
async def set_lesson_state(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    if callback_query.data == "d1":
        await state.set_state(LessonStates.step_1)
        await process_step_1(callback_query, state)
    elif callback_query.data == "d2":
        await state.set_state(LessonStates2.step_1)
        await process_l2_step_1(callback_query, state)
    elif callback_query.data == "d2_2":
        await state.set_state(LessonStates2.step_11)
        await process_l2_step_11(callback_query, state)
    elif callback_query.data == "d3":
        await state.set_state(LessonStates3.step_1)
        await process_l3_step_1(callback_query, state)
    elif callback_query.data == "d3_2":
        await state.set_state(LessonStates3.step_11)
        await process_l3_step_11(callback_query, state)
    elif callback_query.data == "d4":
        await state.set_state(LessonStates4.step_1)
        await process_l4_step_1(callback_query, state)
    elif callback_query.data == "d4_2":
        await state.set_state(LessonStates4.step_11)
        await process_l4_step_11(callback_query, state)
    elif callback_query.data == "d5":
        await state.set_state(LessonStates5.step_1)
        await process_l5_step_1(callback_query, state)
    elif callback_query.data == "d5_2":
        await state.set_state(LessonStates5.step_11)
        await process_l5_step_11(callback_query, state)
    elif callback_query.data == "d6":
        await state.set_state(LessonStates6.step_1)
        await process_l6_step_1(callback_query, state)
    elif callback_query.data == "d6_2":
        await state.set_state(LessonStates6.step_11)
        await process_l6_step_11(callback_query, state)
    elif callback_query.data == "d7":
        await state.set_state(LessonStates7.step_1)
        await process_l7_step_1(callback_query, state)
    elif callback_query.data == "d8":
        await state.set_state(LessonStates8.step_1)
        await process_l8_step_1(callback_query, state)
    elif callback_query.data == "d8_2":
        await state.set_state(LessonStates8.step_11)
        await process_l8_step_11(callback_query, state)
    elif callback_query.data == "d9":
        await state.set_state(LessonStates9.step_1)
        await process_l9_step_1(callback_query, state)
    elif callback_query.data == "d9_2":
        await state.set_state(LessonStates9.step_11)
        await process_l9_step_11(callback_query, state)
    elif callback_query.data == "d10":
        await state.set_state(LessonStates10.step_1)
        await process_l10_step_1(callback_query, state)
    elif callback_query.data == "d10_2":
        await state.set_state(LessonStates10.step_11)
        await process_l10_step_11(callback_query, state)
    elif callback_query.data == "d11":
        await state.set_state(LessonStates11.step_1)
        await process_l11_step_1(callback_query, state)
    elif callback_query.data == "d11_2":
        await state.set_state(LessonStates11.step_11)
        await process_l11_step_11(callback_query, state)
    elif callback_query.data == "d12":
        await state.set_state(LessonStates12.step_1)
        await process_l12_step_1(callback_query, state)
    elif callback_query.data == "d12_2":
        await state.set_state(LessonStates12.step_11)
        await process_l12_step_11(callback_query, state)
    elif callback_query.data == "d13":
        await state.set_state(LessonStates13.step_1)
        await process_l13_step_1(callback_query, state)
    elif callback_query.data == "d13_2":
        await state.set_state(LessonStates13.step_11)
        await process_l13_step_11(callback_query, state)
    elif callback_query.data == "d14":
        await state.set_state(LessonStates14.step_1)
        await process_l14_step_1(callback_query, state)
    elif callback_query.data == "d15":
        await state.set_state(LessonStates15.step_1)
        await process_l15_step_1(callback_query, state)
    elif callback_query.data == "d15_2":
        await state.set_state(LessonStates15.step_11)
        await process_l15_step_11(callback_query, state)
    elif callback_query.data == "d16":
        await state.set_state(LessonStates16.step_1)
        await process_l16_step_1(callback_query, state)
    elif callback_query.data == "d16_2":
        await state.set_state(LessonStates16.step_11)
        await process_l16_step_11(callback_query, state)
    elif callback_query.data == "d17":
        await state.set_state(LessonStates17.step_1)
        await process_l17_step_1(callback_query, state)
    elif callback_query.data == "d17_2":
        await state.set_state(LessonStates17.step_11)
        await process_l17_step_11(callback_query, state)
    elif callback_query.data == "d18":
        await state.set_state(LessonStates18.step_1)
        await process_l18_step_1(callback_query, state)
    elif callback_query.data == "d19":
        await state.set_state(LessonStates19.step_1)
        await process_l19_step_1(callback_query, state)
    elif callback_query.data == "d20":
        await state.set_state(LessonStates20.step_1)
        await process_l20_step_1(callback_query, state)
    elif callback_query.data == "d21":
        await state.set_state(LessonStates21.step_1)
        await process_l21_step_1(callback_query, state)
    
    
    
    
##################### GETTING INTO THE LESSONS

################## LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 ##################

@router.callback_query(StateFilter(LessonStates2.step_2), lambda c: True)
async def main_process_l2_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_2_2(callback_query, state)

@router.message(StateFilter(LessonStates2.step_3))
async def main_process_l2_step_3(message: Message, state: FSMContext):
    await dnevnik_layover(message,state,"trigger_xyz")

@router.callback_query(lambda c: c.data == 'trigger_xyz')
async def trigger_xyz(callback_query: types.CallbackQuery, state: FSMContext):
    await xyz(callback_query, state)


@router.callback_query(StateFilter(LessonStates2.step_4), lambda c: True)
async def main_process_l2_step_4(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_4_1(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_4_2(callback_query, state)
    await process_l2_step_4(callback_query, state)

@router.callback_query(StateFilter(LessonStates2.step_5), lambda c: True)
async def main_process_l2_step_5(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)
#############################################################
@router.callback_query(StateFilter(LessonStates2.step_11), lambda c: True)
async def main_process_l2_step_12(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_13(callback_query, state)

@router.message(StateFilter(LessonStates2.step_12))
async def main_process_l2_step_13(message: Message, state: FSMContext):
    await dnevnik_layover(message,state,"trigger_xyz2")

@router.callback_query(lambda c: c.data == 'trigger_xyz2')
async def trigger_xyz2(callback_query: types.CallbackQuery, state: FSMContext):
    await xyz2(callback_query, state)

@router.callback_query(StateFilter(LessonStates2.step_13), lambda c: True)
async def main_process_l2_step_14(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_14_1(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_14_2(callback_query, state)
    await process_l2_step_14(callback_query, state)

################## LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 ##################

################## LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 #################

@router.callback_query(StateFilter(LessonStates3.step_2), lambda c: True)
async def main_process_l3_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l3_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l3_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates3.step_3), lambda c: True)
async def main_process_l3_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l3_step_3(callback_query, state)

@router.callback_query(StateFilter(LessonStates3.step_4), lambda c: True)
async def main_process_l3_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l3_step_4(callback_query, state)

@router.callback_query(StateFilter(LessonStates3.step_5), lambda c: True)
async def main_process_l3_step_4(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "1":
       await process_l3_step_5(callback_query, state)
    elif callback_query.data == "2":
       await process_l3_step_5_2(callback_query, state)
    elif callback_query.data == "3":
       await process_l3_step_5_3(callback_query, state)

@router.callback_query(StateFilter(LessonStates3.step_6), lambda c: True)
async def main_process_l3_step_5(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

###############################

@router.callback_query(StateFilter(LessonStates3.step_11), lambda c: True)
async def main_process_l3_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "1":
       await process_l3_step_12(callback_query, state)
    elif callback_query.data == "2":
       await process_l3_step_12_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates3.step_12), lambda c: True)
async def main_process_l3_step_12(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "1":
       await process_l3_step_13(callback_query, state)
    elif callback_query.data == "2":
       await process_l3_step_13_2(callback_query, state)
    elif callback_query.data == "3":
       await process_l3_step_13_3(callback_query, state)


################## LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 LESSON_3 #################

################## LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 #################

@router.callback_query(StateFilter(LessonStates4.step_2), lambda c: True)
async def main_process_l4_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l4_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l4_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates4.step_3), lambda c: True)
async def main_process_l4_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l4_step_3(callback_query, state)


################################

@router.callback_query(StateFilter(LessonStates4.step_12), lambda c: True)
async def main_process_l4_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l4_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l4_step_12_2(callback_query, state)

################## LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 LESSON_4 #################

################## LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 #################

@router.callback_query(StateFilter(LessonStates5.step_2), lambda c: True)
async def main_process_l5_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l5_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l5_step_2_2(callback_query, state)

@router.poll_answer(StateFilter(LessonStates5.step_3), lambda c: True)
async def main_process_l5_step_2(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_3(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_4), lambda c: True)
async def main_process_l5_step_3(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_4(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_5), lambda c: True)
async def main_process_l5_step_4(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_5(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_6), lambda c: True)
async def main_process_l5_step_5(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_6(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_7), lambda c: True)
async def main_process_l5_step_6(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_7(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_8), lambda c: True)
async def main_process_l5_step_7(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_8(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates5.step_9), lambda c: True)
async def main_process_l5_step_8(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l5_step_9(poll_answer, state)

@router.callback_query(StateFilter(LessonStates5.step_10), lambda c: True)
async def main_process_l5_step_9(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates5.step_12), lambda c: True)
async def main_process_l5_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "1":
       await process_l5_step_12(callback_query, state)
    elif callback_query.data == "2":
       await process_l5_step_12_2(callback_query, state)
    elif callback_query.data == "3":
       await process_l5_step_12_3(callback_query, state)

################## LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 LESSON_5 #################

################## LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6#################

@router.callback_query(StateFilter(LessonStates6.step_2), lambda c: True)
async def main_process_l6_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l6_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l6_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates6.step_3), lambda c: True)
async def main_process_l6_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates6.step_11), lambda c: True)
async def main_process_l6_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)


################## LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6 LESSON_6#################

################## LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7#################

@router.poll_answer(StateFilter(LessonStates7.step_2), lambda c: True)
async def main_process_l7_step_1(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_2(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates7.step_3), lambda c: True)
async def main_process_l7_step_2(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_3(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates7.step_4), lambda c: True)
async def main_process_l7_step_3(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_4(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates7.step_5), lambda c: True)
async def main_process_l7_step_4(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_5(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates7.step_6), lambda c: True)
async def main_process_l7_step_5(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_6(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates7.step_7), lambda c: True)
async def main_process_l7_step_6(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l7_step_7(poll_answer, state)




################## LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7 LESSON_7#################

################## LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8#################

@router.callback_query(StateFilter(LessonStates8.step_2), lambda c: True)
async def main_process_l8_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l8_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l8_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates8.step_3), lambda c: True)
async def main_process_l8_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l8_step_3(callback_query, state)

@router.callback_query(StateFilter(LessonStates8.step_4), lambda c: True)
async def main_process_l8_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)


@router.callback_query(StateFilter(LessonStates8.step_12), lambda c: True)
async def main_process_l8_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l8_step_12(callback_query, state)
    
@router.poll_answer(StateFilter(LessonStates8.step_13), lambda c: True)
async def main_process_l8_step_12(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_13(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates8.step_14), lambda c: True)
async def main_process_l8_step_13(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_14(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates8.step_15), lambda c: True)
async def main_process_l8_step_14(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_15(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates8.step_16), lambda c: True)
async def main_process_l8_step_15(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_16(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates8.step_17), lambda c: True)
async def main_process_l8_step_16(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_17(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates8.step_18), lambda c: True)
async def main_process_l8_step_17(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l8_step_18(poll_answer, state)

################## LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8 LESSON_8#################

################## LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9#################

@router.callback_query(StateFilter(LessonStates9.step_2), lambda c: True)
async def main_process_l9_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l9_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l9_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates9.step_3), lambda c: True)
async def main_process_l9_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates9.step_11), lambda c: True)
async def main_process_l9_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l9_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l9_step_12_2(callback_query, state)



################## LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9 LESSON_9#################

################## LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10#################

@router.callback_query(StateFilter(LessonStates10.step_2), lambda c: True)
async def main_process_l10_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l10_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l10_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates10.step_3), lambda c: True)
async def main_process_l10_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates10.step_11), lambda c: True)
async def main_process_l10_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l10_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l10_step_12_2(callback_query, state)

################## LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10 LESSON_10#################

################## LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11#################

@router.callback_query(StateFilter(LessonStates11.step_2), lambda c: True)
async def main_process_l11_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l11_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l11_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates11.step_3), lambda c: True)
async def main_process_l11_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates11.step_11), lambda c: True)
async def main_process_l11_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l11_step_12(callback_query, state)
    elif callback_query.data == "question":
       await main_menu_cb_handler(callback_query, state)

################## LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11 LESSON_11#################

################## LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12#################

@router.callback_query(StateFilter(LessonStates12.step_2), lambda c: True)
async def main_process_l12_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l12_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l12_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates12.step_3), lambda c: True)
async def main_process_l12_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

################## LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12 LESSON_12#################

################## LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13#################

@router.callback_query(StateFilter(LessonStates13.step_2), lambda c: True)
async def main_process_l13_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l13_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l13_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates13.step_3), lambda c: True)
async def main_process_l13_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates13.step_11), lambda c: True)
async def main_process_l13_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l13_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l13_step_12_2(callback_query, state)

################## LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13 LESSON_13#################

################## LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14#################

@router.poll_answer(StateFilter(LessonStates14.step_2), lambda c: True)
async def main_process_l14_step_1(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_2(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates14.step_3), lambda c: True)
async def main_process_l14_step_2(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_3(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates14.step_4), lambda c: True)
async def main_process_l14_step_3(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_4(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates14.step_5), lambda c: True)
async def main_process_l14_step_4(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_5(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates14.step_6), lambda c: True)
async def main_process_l14_step_5(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_6(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates14.step_7), lambda c: True)
async def main_process_l14_step_6(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l14_step_7(poll_answer, state)

################## LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14 LESSON_14#################

################## LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15#################
@router.callback_query(StateFilter(LessonStates15.step_2), lambda c: True)
async def main_process_l15_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l15_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l15_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates15.step_3), lambda c: True)
async def main_process_l15_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates15.step_11), lambda c: True)
async def main_process_l15_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l15_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l15_step_12_2(callback_query, state)
################## LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15 LESSON_15#################

################## LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16#################
@router.callback_query(StateFilter(LessonStates16.step_2), lambda c: True)
async def main_process_l16_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l16_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l16_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates16.step_11), lambda c: True)
async def main_process_l16_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l16_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l16_step_12_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates16.step_12), lambda c: True)
async def main_process_l16_step_12(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)
################## LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16 LESSON_16#################

################## LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17#################
@router.callback_query(StateFilter(LessonStates17.step_2), lambda c: True)
async def main_process_l17_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l17_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l17_step_2_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates17.step_3), lambda c: True)
async def main_process_l17_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

@router.callback_query(StateFilter(LessonStates17.step_11), lambda c: True)
async def main_process_l17_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l17_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l17_step_12_2(callback_query, state)
################## LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17 LESSON_17#################

################## LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18#################
@router.callback_query(StateFilter(LessonStates18.step_2), lambda c: True)
async def main_process_l18_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l18_step_2(callback_query, state)
    elif callback_query.data == "stop":
       await process_l18_step_2_2(callback_query, state)
    
@router.poll_answer(StateFilter(LessonStates18.step_3), lambda c: True)
async def main_process_l18_step_2(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_3(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_4), lambda c: True)
async def main_process_l18_step_3(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_4(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_5), lambda c: True)
async def main_process_l18_step_4(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_5(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_6), lambda c: True)
async def main_process_l18_step_5(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_6(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_7), lambda c: True)
async def main_process_l18_step_6(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_7(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_8), lambda c: True)
async def main_process_l18_step_7(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_8(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_9), lambda c: True)
async def main_process_l18_step_8(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_9(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_10), lambda c: True)
async def main_process_l18_step_9(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_10(poll_answer, state)

@router.poll_answer(StateFilter(LessonStates18.step_11), lambda c: True)
async def main_process_l18_step_10(poll_answer: types.PollAnswer, state: FSMContext):
    await process_l18_step_11(poll_answer, state)

@router.callback_query(StateFilter(LessonStates18.step_12), lambda c: True)
async def main_process_l18_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

################## LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18 LESSON_18#################

################## LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19#################

@router.callback_query(StateFilter(LessonStates19.step_1), lambda c: True)
async def main_process_l18_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

################## LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19 LESSON_19#################

################## LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20#################

@router.callback_query(StateFilter(LessonStates20.step_1), lambda c: True)
async def main_process_l20_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l20_step_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates20.step_2), lambda c: True)
async def main_process_l20_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

################## LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20 LESSON_20#################

################## LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21#################

@router.callback_query(StateFilter(LessonStates21.step_1), lambda c: True)
async def main_process_l21_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    await process_l21_step_2(callback_query, state)

@router.callback_query(StateFilter(LessonStates21.step_2), lambda c: True)
async def main_process_l21_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    await main_menu_cb_handler(callback_query, state)

################## LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21 LESSON_21#################

################## HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP################

# @router.callback_query(StateFilter(LessonStates.step_7), lambda c: True)
# async def main_process_step_L2(callback_query: types.CallbackQuery, state: FSMContext):
#     if callback_query.data == "callback1":
#        await process_step_L2(callback_query, state)
#     elif callback_query.data in ["callback2", "callback2"]:
#        await process_step_L2(callback_query, state)


# @router.callback_query(lambda c: c.data == 'd2_2')
# @router.message(Command('lesson_1'))
# async def start_lesson(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
#     await state.set_state(LessonStates.step_1)
#     if isinstance(message_or_callback, types.Message):
#         await message_or_callback.answer(
#             "Welcome to the lesson! Press the button to start.",
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="Start Lesson", callback_data="start")]
#             ])
#         )
#     elif isinstance(message_or_callback, types.CallbackQuery):
#         await message_or_callback.message.answer(
#             "Welcome to the lesson! Press the button to start.",
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text="Start Lesson", callback_data="start")]
#             ])
#         )


# await bot.send_poll(
#         chat_id=poll_answer.user.id,
#         question="Викторина 2: Какой фреймворк вы используете?",
#         options=["Django", "Flask", "FastAPI", "Aiogram"],
#         is_anonymous=False
#     )


################## HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP################

################## QUESTIONNAIRE  QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE ##################

@router.message(Command('questionaire'))
async def main_questionaire_mail(message: Message, state: FSMContext):
    await state.set_state(Questionnaire.prefirst)
    await message.answer("напиши ченить")

@router.callback_query(lambda c: c.data == 'retry_mail')
async def main_rerty_mail(callback_query: CallbackQuery, state: FSMContext):
    # await process_first(callback_query.message, state)
    await callback_query.message.answer("Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно")
    await state.set_state(Questionnaire.mail)

@router.message(StateFilter(Questionnaire.prefirst))
async def main_process_prefirst(message: Message, state: FSMContext):
    await process_prefirst(message, state)
    await state.set_state(Questionnaire.first)

@router.callback_query(StateFilter(Questionnaire.first), lambda c: True)
async def main_process_first(callback_query: types.CallbackQuery, state: FSMContext):
    await process_first(callback_query.message, state)
    await state.set_state(Questionnaire.name)

@router.message(StateFilter(Questionnaire.name))
async def main_process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await process_name(message, state)
    await state.set_state(Questionnaire.gender)

@router.callback_query(StateFilter(Questionnaire.gender), lambda c: True)
async def main_process_gender(callback_query: types.CallbackQuery, state: FSMContext):
    gender = callback_query.data
    await state.update_data(gender=gender)
    if gender == "female":
        await process_gender(callback_query.message, state)
        await state.set_state(Questionnaire.f_preg)
    elif gender == "male":
        await state.update_data(pregnancy="False")
        await state.update_data(breastfeeding="False")
        await process_f_breastfeed(callback_query.message, state)
        await state.set_state(Questionnaire.height)
    else: 
        await callback_query.message.answer("Что-то не так с полом")

@router.callback_query(StateFilter(Questionnaire.f_preg), lambda c: True)
async def main_process_f_preg(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(pregnancy=callback_query.data)
    await process_f_preg(callback_query.message, state)
    await state.set_state(Questionnaire.f_breastfeed)

@router.callback_query(StateFilter(Questionnaire.f_breastfeed), lambda c: True)
async def main_process_f_breastfeed(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(breastfeeding=callback_query.data)
    await process_f_breastfeed(callback_query.message, state)
    await state.set_state(Questionnaire.height)

@router.message(StateFilter(Questionnaire.height))
async def main_process_geight(message: Message, state: FSMContext):
    pattern = r'^[0-9.]+$'
    if not re.match(pattern, message.text):
        await message.answer("Пожалуйста, введи целое число или число в формате 170.5")
        return
    await state.update_data(height=message.text)
    await process_height(message, state)
    await state.set_state(Questionnaire.weight)

@router.message(StateFilter(Questionnaire.weight))
async def main_process_weight(message: Message, state: FSMContext):
    pattern = r'^[0-9.]+$'
    if not re.match(pattern, message.text):
        await message.answer("Пожалуйста, введи целое число или число в формате 70.5")
        return
    await state.update_data(weight=message.text)
    await process_weight(message, state)
    await state.set_state(Questionnaire.age)

@router.message(StateFilter(Questionnaire.age))
async def main_process_age(message: Message, state: FSMContext):
    pattern = r'^\d+$'
    if not re.match(pattern, message.text):
        await message.answer("Пожалуйста введи целое число")
        return
    await state.update_data(age=message.text)
    await process_age(message, state)
    await state.set_state(Questionnaire.water)

@router.callback_query(StateFilter(Questionnaire.water), lambda c: True)
async def main_process_water(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(water=callback_query.data)
    await process_water(callback_query.message, state)
    await state.set_state(Questionnaire.booze)

@router.callback_query(StateFilter(Questionnaire.booze), lambda c: True)
async def main_process_booze(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(booze=callback_query.data)
    await process_booze(callback_query.message, state)
    await state.set_state(Questionnaire.meals)

@router.callback_query(StateFilter(Questionnaire.meals), lambda c: True)
async def main_process_meals(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(meals=callback_query.data)
    await process_meals(callback_query.message, state)
    await state.set_state(Questionnaire.meals_extra)

@router.message(StateFilter(Questionnaire.meals_extra))
@router.callback_query(StateFilter(Questionnaire.meals_extra))
async def main_process_meals_extra(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_bot_response("🟠🟠🟠🟠🟠", message_or_callback.from_user.id))
    if isinstance(message_or_callback, types.Message):
        await state.update_data(meals_extra=message_or_callback.text)
        await process_meals_extra(message_or_callback, state)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await state.update_data(meals_extra=message_or_callback.data)
        await process_meals_extra(message_or_callback.message, state)
    await state.set_state(Questionnaire.allergies)

@router.message(StateFilter(Questionnaire.allergies))
@router.callback_query(StateFilter(Questionnaire.allergies))
async def main_process_allergies(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message_or_callback, types.Message):
        await state.update_data(allergies=message_or_callback.text)
        await process_allergies(message_or_callback, state)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await state.update_data(allergies=message_or_callback.data)
        await process_allergies(message_or_callback.message, state)
    await state.set_state(Questionnaire.part3)

@router.callback_query(StateFilter(Questionnaire.part3), lambda c: True)
async def main_process_part3(callback_query: types.CallbackQuery, state: FSMContext):
    await process_part3(callback_query.message, state)
    await state.set_state(Questionnaire.jogging)

@router.message(StateFilter(Questionnaire.jogging))
async def main_process_jogging(message: Message, state: FSMContext):
    pattern = r'^[0-9.]+$'
    if re.match(pattern, message.text):

        await state.update_data(jogging=message.text)
        await process_jogging(message, state)
        await state.set_state(Questionnaire.lifting)
    else: 
        await message.answer("Попробуй ввести число ещё раз, с первого раза я не поняла.")

@router.message(StateFilter(Questionnaire.lifting))
async def main_process_lifting(message: Message, state: FSMContext):
    pattern = r'^[0-9.]+$'
    if re.match(pattern, message.text):
        await state.update_data(lifting=message.text)
        await process_lifting(message, state)
        await state.set_state(Questionnaire.stress)
    else: 
        await message.answer("Попробуй ввести число ещё раз, с первого раза я не поняла.")

@router.callback_query(StateFilter(Questionnaire.stress), lambda c: True)
async def main_process_stress(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_bot_response("🔵🔵🔵🔵", callback_query.from_user.id))
    await state.update_data(stress=callback_query.data)
    await process_stress(callback_query.message, state)
    await state.set_state(Questionnaire.sleep)

@router.callback_query(StateFilter(Questionnaire.sleep), lambda c: True)
async def main_process_sleep(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(sleep=callback_query.data)
    await process_sleep(callback_query.message, state)
    await state.set_state(Questionnaire.goal)

@router.callback_query(StateFilter(Questionnaire.goal), lambda c: True)
async def main_process_goal(callback_query: types.CallbackQuery, state: FSMContext):
    goal1 = callback_query.data
    await state.update_data(goal=goal1)
    asyncio.create_task(log_bot_response(f"goal:{goal1}", callback_query.from_user.id))

    await calculate(state)
    user_data = await state.get_data()
    goal = user_data['goal']

    if goal in ["+", "-"]:
        await process_goal(callback_query.message, state, goal)
        await state.set_state(Questionnaire.w_loss)
    elif goal == "=":
        await process_w_loss_amount(callback_query.message, state, goal)
        await state.update_data(w_loss_amount="0")
        input_text = await gen_text(state)
        await give_plan(callback_query.message, state, input_text)
        await state.set_state(Questionnaire.city)

@router.callback_query(StateFilter(Questionnaire.w_loss), lambda c: True)
async def main_process_w_loss(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    goal = user_data["goal"]
    await process_w_loss(callback_query, state, goal)
    await state.set_state(Questionnaire.w_loss_amount)

@router.message(StateFilter(Questionnaire.w_loss_amount))
async def main_process_w_loss_amount(message: Message, state: FSMContext):
    pattern = r'^[0-9.]+$'
    if not re.match(pattern, message.text):
        await message.answer("Напиши число в чат.\nНапример, «3» или «4.5».")
        return
    user_data = await state.get_data()
    goal = user_data["goal"]
    tdee = user_data['tdee']
    bmr = user_data['bmr']
    pregnancy = user_data['pregnancy']
    await process_w_loss_amount(message, state, goal)
    input_text = await gen_text(state)
    if pregnancy == "True":
        await give_plan(message, state, input_text)
    else:
        if goal in ["+","-"]:
            if goal == "+": 
                goal_txt = "набрать вес"
                await state.update_data(w_loss_amount=f"+{message.text}")
            elif goal == "-": 
                goal_txt = "сбросить вес"
                await state.update_data(w_loss_amount=f"-{message.text}")
            asyncio.create_task(log_bot_response(f"w_loss_amount:{message.text}", message.from_user.id))
            text1 = f"Чтобы помочь тебе в достижении твоей цели {goal_txt}, я рассчитала, сколько калорий тебе нужно есть в день. Я использую формулу Mifflin-St Jeor, так как она считается одной из самых точных.\n\n\nТвои результаты следующие:\nБазовый уровень метаболизма (BMR): примерно <b>{bmr}</b> ккал/день.\nОбщая суточная потребность в энергии (TDEE) при умеренной активности: примерно <b>{tdee}</b> ккал/день."
            await message.answer(text1)
            await give_plan(message, state, input_text)
    await state.set_state(Questionnaire.city)


@router.message(StateFilter(Questionnaire.city))
async def main_process_city(message: Message, state: FSMContext):
    # timeslide, city = await process_city(message, state)
    # state.update_data(timeslide=timeslide, city=city)
    await process_city(message, state)
    await state.set_state(Questionnaire.morning_ping)

@router.message(StateFilter(Questionnaire.morning_ping))
async def main_process_morning_ping(message: Message, state: FSMContext):
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await state.update_data(morning_ping=message.text)
        await process_morning_ping(message, state)
        await state.set_state(Questionnaire.evening_ping)
    else:
        await message.answer("Не поняла, попробуй, пожалуйста, ещё раз")

@router.message(StateFilter(Questionnaire.evening_ping))
async def main_process_evening_ping(message: Message, state: FSMContext):
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await state.update_data(evening_ping=message.text)
        await process_evening_ping(message, state)
        await state.set_state(Questionnaire.community_invite)
        state_data = await state.get_data()
        data = {
            "userTgId": message.from_user.id,
            "info": {
                "user_info_name": state_data["name"],
                "user_info_timeslide" : state_data["timeslide"],
                "user_info_morning_ping": state_data["morning_ping"],
                "user_info_evening_ping": state_data["evening_ping"],
                "user_info_city": state_data["city"],
                "user_info_bmi":  state_data["bmi"],
                "target_calories": state_data["target_calories"],
                "bmr":  state_data["bmr"],
                "tdee":  state_data["tdee"],
                "user_info_weight_change":  state_data["w_loss_amount"],
                "user_info_goal": state_data["goal"],
                "user_info_sleep": state_data["sleep"],
                "user_info_stress": state_data["stress"],
                "user_info_gym_hrs": state_data["lifting"],
                "user_info_excersise_hrs": state_data["jogging"],
                "user_info_meals_ban": state_data["allergies"],
                "user_info_meals_extra": state_data["meals_extra"],
                "user_info_meal_amount": state_data["meals"],
                "user_info_booze": state_data["booze"],
                "user_info_water": state_data["water"],
                "user_info_age": state_data["age"],
                "user_info_weight": state_data["weight"],
                "user_info_height": state_data["height"],
                "user_info_breastfeeding": state_data["breastfeeding"],
                "user_info_pregnancy": state_data["pregnancy"],
                "user_info_gender": state_data["gender"]
                }
    }   
        try:
            iserror, response = await add_or_update_usr_info(json.dumps(data))
            issuccess = await add_user_lesson(message.from_user.id, "99")
            print(f"saving data for user {message.from_user.id} has returned {iserror}, {response}")
            if response != "true":
                await message.answer("Произошла ошибка при сохранении информации")
            asyncio.create_task(log_bot_response(f"user {message.from_user.id} \nsaved_info_to_db {response}\nlesson_99_save={issuccess}", message.from_user.id))
        except Exception as e:
            asyncio.create_task(log_bot_response(f"user {message.from_user.id} \nERROR_ON_INFO_SAVE {e}", message.from_user.id))
        

    else:
        await message.answer("Не поняла, попробуй, пожалуйста, ещё раз")

@router.callback_query(StateFilter(Questionnaire.community_invite), lambda c: True)
async def main_process_community_invite(callback_query: types.CallbackQuery, state: FSMContext):
    await plan_info_dump(callback_query, state)
    await state.set_state(Questionnaire.community_invite_2)

@router.callback_query(StateFilter(Questionnaire.community_invite_2), lambda c: True)
async def main_process_community_invite(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await process_community_invite(callback_query.message, state)
    await state.set_state(Questionnaire.premail)

@router.message(Command("test_premail"))
async def test_premail(message: types.Message, state: FSMContext):
    await state.set_state(Questionnaire.premail)
    await message.answer("Тык", reply_markup=(InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="тык", callback_data="tik")]])))

@router.callback_query(StateFilter(Questionnaire.premail), lambda c: True)
async def main_premail_ask_a_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    id = callback_query.from_user.id
    isActive = await check_is_active_state(id, state)
    if not isActive:
        await callback_query.message.edit_text("Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно")
        await state.set_state(Questionnaire.mail)
    else:
        await state.set_state(LessonStates.step_1)
        await process_step_1(callback_query, state)

@router.message(StateFilter(Questionnaire.mail))
async def main_process_mail(message: Message, state: FSMContext):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, message.text):
        await process_mail(message, state)
    else:
        await message.answer("Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно")

################## QUESTIONNAIRE  QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE ##################

@router.message(Command("set_state_recogni"))
async def set_user_state(message: types.Message):
    # Initialize FSMContext for the target user
    # ctx = FSMContext(storage=dp.storage, user_id=464682207, chat_id=464682207)
    # await ctx.set_state(UserState.recognition)
    storage_key = StorageKey(bot.id, 464682207, 464682207)
    storage_key1 = StorageKey(bot.id, 389054202, 389054202)
    fsm_context = FSMContext(storage=dp.storage, key=storage_key)
    print(f"[GOOD KEY] {StorageKey(bot.id, 464682207, 464682207)}")
    print(f"[SETSTATE_RECOGNI_KEY] {storage_key}")
    fsm_context1 = FSMContext(storage=dp.storage, key=storage_key1)
    await fsm_context.set_state(UserState.recognition)
    await fsm_context1.set_state(UserState.recognition)
    await message.answer("set user 389054202 and 464682207 to recogni")

@router.message(Command("setstate"))
async def start_state_setting(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ You are not authorized to use this command.")
        return 
    await state.set_state(AdminState.waiting_for_state_input)
    await message.answer("Send: user_id StateGroup.State\n\nExample:\n464682207 UserState.recognition")

@router.message(AdminState.waiting_for_state_input)
async def apply_user_state(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id_str, state_str = message.text.strip().split(maxsplit=1)
        group_name, state_name = state_str.split(".")
        print(f"user_id_str:{user_id_str} state_str:{group_name}.{state_name}")
        user_id = int(user_id_str)

        # Controlled eval environment
        # safe_globals = vars(all_states)
        safe_globals = {
            name: cls
            for name, cls in vars(all_states).items()
            if isinstance(cls, type)
        }
        print(f"{safe_globals}")
        # state_obj = eval(state_str, safe_globals)
        group_class = safe_globals[group_name]
        state_obj = getattr(group_class, state_name)
        if not isinstance(state_obj, State):
            print("value_error")
            raise ValueError(f"{state_str} is not a valid State.")

        key = StorageKey(bot.id, user_id, user_id)
        print(f"[DYNAMIC KEY] {key}")
        target_fsm = FSMContext(storage=state.storage, key=key)
        await target_fsm.set_state(state_obj)
        current = await target_fsm.get_state()
        print(f"[DEBUG] FSM state for {user_id}: {current}")

        await message.answer(f"✅ Set user {user_id} to state `{state_str}`.")
        if user_id != message.from_user.id:
            await state.clear()
    except Exception as e:
        await message.answer(f"⚠️ Failed to set state: {e}")

@router.message(Command("upload_image"))
async def upload_image_command(message: types.Message, state: FSMContext):
    await state.set_state(ImageUploadState.waiting_for_image)
    await message.answer("Please send me an image, and I'll give you its file_id.")

@router.message(ImageUploadState.waiting_for_image, lambda message: message.photo)
async def handle_image_upload(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id

    await message.answer(f"Here is the file_id of your image:\n\n<code>{file_id}</code>\n\n"
                         "You can use this file_id to send the image in your bot.")

    await state.clear()


@router.message(Command("get_meal"))
async def get_meals_command(message: types.Message):
    print("GET_USERS")
    pool = dp["db_pool"]
    try:
        async with pool.acquire() as connection:
            rows = await connection.fetch("SELECT id FROM meal WHERE type =0")
            # print(rows)
            
            response = "Users:\n"
            for row in rows[:15]:
                response += f"{row['id']}\n"
            
            await message.answer(response)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@router.message(Command("get_users"))
async def get_users_command(message: types.Message):
    print("GET_USERS")
    pool = dp["db_pool"]
    try:
        async with pool.acquire() as connection:
            rows = await connection.fetch('SELECT id, username FROM railway."public".user WHERE "IsActive" = TRUE')
            # print(rows)
            
            response = "Users:\n"
            for row in rows[:15]:
                response += f"ID: {row['id']}, Username: {row['username']}\n"
                # response += f"{row}\n"
            
            await message.answer(response)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@router.message(Command("check_active"))
async def user_active_command(message: types.Message):
    pool = dp["db_pool"]
    try:
        async with pool.acquire() as connection:
            rows = await connection.fetch(f'SELECT "IsActive" FROM "user" WHERE "tgId"={message.from_user.id}')
            print(rows)
            
            response = f"{rows['IsActive']}"
            # for row in rows[:15]:
            #     response += f"ID: {row['id']}, Username: {row['username']}\n"
            #     # response += f"{row}\n"
            
            await message.answer(response)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")


@router.message(Command("rassilka_test"))
async def start_test(message: types.Message, state: FSMContext):
    if message.from_user.id not in ["464682207", "389054202", "7726313921"]:
        message.answer("You shall not pass!")
        return
    await message.answer("📝 Пришли мне пост <i>Текст(html-форматирование) + фото</i> и я пришлю тебе то как он будет выглядеть")
    await state.set_state(PostStates.waiting_for_post)

@dp.message(Command("messagetouser"))
async def send_message_to_user(message: types.Message):
    if message.from_user.id not in ["464682207", "389054202", "7726313921"]:
        message.answer("You shall not pass!")
        return
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.reply("Usage: /messagetouser_<user_id> <message>")
            return
            
        user_id = int(parts[0].split('_')[1])
        message_text = parts[2]
        
        await bot.send_message(user_id, message_text)
        await message.reply(f"Message sent to user {user_id}")
        
    except IndexError:
        await message.reply("Invalid format. Use: /messagetouser_<user_id> <message>")
    except ValueError:
        await message.reply("Invalid user ID. It should be a number.")
    except Exception as e:
        await message.reply(f"Failed to send message: {str(e)}")

@router.message(StateFilter(PostStates.waiting_for_post))
async def handle_post_with_photo(message: types.Message, state: FSMContext):
    buttons = [[InlineKeyboardButton(text="Отправить всем", callback_data="send_to_users"), InlineKeyboardButton(text="Отменить отправку", callback_data="reset_post")], [InlineKeyboardButton(text="Отправить разрабам", callback_data="send_to_us"), InlineKeyboardButton(text="Отправить @natailini", callback_data="send_to_natailini")]]
    try:
        if message.photo:
            photo = message.photo[-1]
            caption = message.caption if message.caption else ""
            
            await state.update_data(photo_id=photo.file_id, caption=caption)
            await state.set_state(PostStates.post_received)
            
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo.file_id,
                caption=f"{caption}"
            )
        elif message.text:
            await state.update_data(text=message.text)
            await state.set_state(PostStates.post_received)
            await message.answer(f"{message.text}")
        await message.answer("Что делаем?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        await message.answer(error_message)

@router.callback_query(StateFilter(PostStates.post_received))
async def handle_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    successful = 0
    unsuccessful = 0
    
    if callback_query.data == "reset_post":
        await callback_query.message.edit_reply_markup()
        await callback_query.answer("Post reset! Send a new one.")
        await state.set_state(PostStates.waiting_for_post)

    elif callback_query.data == "send_to_us":
        caption = data.get("caption", data.get("text", ""))
        photo_id = data.get("photo_id")
        user_list = await get_user_list(True)

        for user_id in user_list:
            try:
                if photo_id:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=photo_id,
                        caption=f"{caption}",
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"{caption}",
                        parse_mode="HTML"
                    )
                successful += 1
            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")
                unsuccessful += 1
        result_message = (
        f"Post delivery results:\n"
        f"✅ Successful: {successful}\n"
        f"❌ Unsuccessful: {unsuccessful}\n"
        f"📊 Total attempted: {len(user_list)}")
        await callback_query.message.answer(result_message)

    elif callback_query.data == "send_to_natailini":
        caption = data.get("caption", data.get("text", ""))
        photo_id = data.get("photo_id")
        # user_list = await get_user_list(True)
        user_list = ["464682207", "389054202", "7726313921"] #

        for user_id in user_list:
            try:
                if photo_id:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=photo_id,
                        caption=f"{caption}",
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"{caption}",
                        parse_mode="HTML"
                    )
                successful += 1
            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")
                unsuccessful += 1
        result_message = (
        f"Результат отправки поста:\n"
        f"✅ Удачно: {successful}\n"
        f"❌ Неудачно: {unsuccessful}\n"
        f"📊 Всего пользователей: {len(user_list)}")
        await callback_query.message.answer(result_message)
    
    elif callback_query.data == "send_to_users":
        caption = data.get("caption", data.get("text", ""))
        photo_id = data.get("photo_id")
        user_list = await get_user_list(False)

        for user_id in user_list:
            try:
                if photo_id:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=photo_id,
                        caption=f"{caption}",
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"{caption}",
                        parse_mode="HTML"
                    )
                successful += 1
            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")
                unsuccessful += 1
        # print((f"Post sent to {len(user_list)} users!"))
        result_message = (
        f"Результат отправки поста:\n"
        f"✅ Удачно: {successful}\n"
        f"❌ Неудачно: {unsuccessful}\n"
        f"📊 Всего пользователей: {len(user_list)}")
        await callback_query.message.answer(result_message)











@router.message()
async def default_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    # await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    # if not current_state:
    if current_state and current_state.startswith("Questionnaire"):
        await message.answer("Вы не закончили анкету")
        return
    if message.sticker:
        sticker_id = message.sticker.file_id
        await message.answer(f"{sticker_id}")
    else: 
        if message.photo:
            await state.set_state(UserState.recognition)
            await state.update_data(extra_plate=False)
            await dnevnik_functional(message, state)
        elif message.voice:
            await state.set_state(UserState.perehvat)
            await perehvat(message, state)
        elif message.text:
            await state.set_state(UserState.perehvat)
            await perehvat(message, state)
    #         else:
    #             await message.answer("Будут перехватчики", reply_markup=keyboard)
    # else:
    #     await message.answer(f"Текущее состояние: {current_state}", reply_markup=keyboard)


# @router.message()
# async def default_handler(message: Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     # await state.update_data(full_sequence=False)
#     buttons = [
#         [InlineKeyboardButton(text="Меню", callback_data="menu")],
#         ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     no_perehvat_states = [UserState.change_user_info, UserState.name_change, UserState.kkal_change, UserState.morning_ping_change, UserState.evening_ping_change, UserState.info_coll, UserState.recognition, LayoverState.recognition, LayoverState.redact]
#     if current_state not in no_perehvat_states:
#         if message.sticker:
#             sticker_id = message.sticker.file_id
#             await message.answer(f"{sticker_id}")
#         else: 
#             if message.photo:
#                 await state.set_state(UserState.recognition)
#                 await dnevnik_functional(message, state)
#             elif message.voice:
#                 await state.set_state(UserState.perehvat)
#                 await perehvat(message, state)
#             elif message.text:
#                 await state.set_state(UserState.perehvat)
#                 await perehvat(message, state)
#             else:
#                 await message.answer("Будут перехватчики", reply_markup=keyboard)
#     else:
#         await message.answer(f"Текущее состояние: {current_state}", reply_markup=keyboard)

async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

async def on_shutdown(dp: Dispatcher):
    logging.info("Shutting down...")
    print("on_shutdown")
    
    pool = dp.get("db_pool")
    if pool:
        await pool.close()
        logging.info("Database connection pool closed.")
    
    bot = dp.bot
    await bot.send_message(chat_id=464682207, text="Bot is shutting down. Goodbye!")
    
    
    logging.info("Shutdown complete.")


async def main() -> None:
    init_db()
    pool = await create_db_pool()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.include_router(router)
    dp.message.middleware(StateMiddleware())
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp["db_pool"] = pool
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):  # Handle SIGTERM and SIGINT
        loop.add_signal_handler(sig, lambda: asyncio.create_task(on_shutdown(dp)))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# async def on_shutdown(dp: Dispatcher):
#     logging.info("Shutting down...")
#     pool = dp.get("db_pool")
#     if pool:
#         await pool.close()
#         logging.info("Database connection pool closed.")
#     bot = dp.bot
#     try:
#         await bot.send_message(chat_id=464682207, text="Bot is shutting down. Goodbye!")
#         logging.info("Shutdown notification sent to users.")
#     except Exception as e:
#         logging.error(f"Failed to send shutdown notification: {e}")
    
#     logging.info("Shutdown complete.")

# async def main() -> None:
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     pool = await create_db_pool()
#     dp["db_pool"] = pool
#     dp.include_router(router)
#     dp.message.middleware(StateMiddleware())
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     logging.info("Starting bot...")
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     dp = Dispatcher()
#     for sig in (signal.SIGTERM, signal.SIGINT):
#         loop.add_signal_handler(
#             sig,
#             lambda sig=sig: asyncio.create_task(on_shutdown(dp))
#         )

#     try:
#         loop.run_until_complete(main())
#     except Exception as e:
#         logging.error(f"Unexpected error: {e}")
#     finally:
#         loop.close()
#         logging.info("Application stopped.")