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
from all_states import *

BOT_TOKEN = os.getenv("BOT_TOKEN")                    ##ACTUALISED
OPENAI_KEY = os.getenv("OPENAI_KEY")                  ##ACTUALISED

STICKER_ID = os.getenv("STICKER_ID")

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
# storage = MemoryStorage()
router = Router()
# dp = Dispatcher(storage=storage)

errorbuttons = [[InlineKeyboardButton(text="Написать в поддержку", url="t.me/nutri_care")], [InlineKeyboardButton(text=arrow_menu, callback_data="menu_back")]]
errorkeys = InlineKeyboardMarkup(inline_keyboard=errorbuttons)


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
    asyncio.create_task(log_user_message(message))
    await state.clear()
    await menu_handler(message, state)


@router.callback_query(lambda c: c.data == 'menu')
async def main_menu_cb_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
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
    asyncio.create_task(log_user_message(message))
    await process_menu_course(message, state, message.from_user.id)

@router.message(Command("2"))
async def menu_main_process_menu_dnevnik(message: Message, state: FSMContext) -> None:
    asyncio.create_task(log_user_message(message))
    await process_menu_dnevnik(message, state)

@router.message(Command("3"))
async def menu_main_process_menu_nutri(message: Message, state: FSMContext) -> None:
    asyncio.create_task(log_user_message(message))
    await process_menu_nutri(message, state)

@router.message(Command("4"))
async def menu_main_process_menu_settings(message: Message, state: FSMContext) -> None:
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
    str_food = str(data["latest_food"])
    id = str(callback_query.from_user.id)
    buttons = [[InlineKeyboardButton(text="Ок", callback_data=callback_mssg)],]
    if callback_mssg == "saving_edit":
        await state.set_state(prev_state)
        state_data = state.get_data()
        old_date = state_data["date"]
        Iserror, answer = await save_meal_old_date(callback_query.from_user.id, str_food, callback_query.data, old_date)
    else:
        Iserror, answer = await save_meal(callback_query.from_user.id, str_food, callback_query.data)
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
        sticker_mssg = await message.answer_sticker(STICKER_ID)
        iserror, user_data = await get_user_info(message.from_user.id)
        user_info = json.loads(user_data)
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
        sticker_mssg = await callback_query.message.answer_sticker(STICKER_ID)
        buttons = [[InlineKeyboardButton(text="Да, спасибо", callback_data="menu")], [InlineKeyboardButton(text="Изменить продукты", callback_data="reciIt_2")], [InlineKeyboardButton(text="Нет, подбери другой рецепт", callback_data="reciIt_retry")]]
        await state.set_state(UserState.reci)
        iserror1, user_data = await get_user_info(callback_query.from_user.id)
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
        sticker_mssg = await callback_query.message.answer_sticker(STICKER_ID)
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
    sticker_mssg = await message.answer_sticker(STICKER_ID)
    meal_type_mapping = {"0": "Завтрака", "2": "Обеда", "4": "Ужина", "5":"Перекуса"}
    state_data = await state.get_data()
    input_type = state_data["input_rec_type"]
    meal_type = state_data["meal_type_rec"]
    iserror1, user_data = await get_user_info(message.from_user.id)
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
    buttons = [[InlineKeyboardButton(text='Меню', callback_data='menu')]]
    errormessage = "Гпт вернул ошибку"
    if message.text:
        try:
            sticker_mssg = await message.answer_sticker(STICKER_ID)
            flag, response = await yapp(id, message.text, new_thread)
            if flag:
                await sticker_mssg.delete()
                await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
                # await message.answer(errormessage)
            else: 
                await sticker_mssg.delete()
                await message.answer(f"{response}\n\nТы можешь продолжить общаться со мной или нажать кнопку", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
                asyncio.create_task(log_bot_response(response, message.from_user.id))
                await state.set_state(UserState.yapp)
        except Exception as e:
            await message.answer("Упс, поймали ошибку", reply_markup=errorkeys)
        
    elif message.voice:
        try:
            sticker_mssg = await message.answer_sticker(STICKER_ID)
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
        message.answer("Я читаю только текст/аудио")

################## YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP ##################

################## DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK ##################

@router.message(StateFilter(UserState.recognition))
async def dnevnik_functional(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    id = str(message.from_user.id)
    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    # confirm_text = "Все верно?"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await process_img_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.saving_confirmation)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.saving_confirmation)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.saving_confirmation)
    else: message.answer("0_o")

@router.message(StateFilter(UserState.redact))
async def dnevnik_functional_edit(message: Message, state: FSMContext):
    asyncio.create_task(log_user_message(message))
    edit_text = "Напиши <b>текстом</b> или продиктуй <b>голосовым сообщением</b>, что добавить или изменить в составе.\nНапример, <i>«Добавь 2 чайные ложки сахара в состав» или «Это не курица, это индейка»</i>."
    # confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    confirm_text = "Все верно?"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        await message.answer(edit_text)
    elif message.voice:
        await process_audio_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.saving_confirmation)
    elif message.text:
        await process_txt_rec(message, state, confirm_text, buttons)
        await state.set_state(UserState.saving_confirmation)
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
    Iserror, answer = await save_meal(callback_query.from_user.id, food, callback_query.data)
    buttons = [
        [InlineKeyboardButton(text="Получить оценку", callback_data="meal_rate")],
        [InlineKeyboardButton(text=arrow_menu, callback_data="menu")]
    ]
    if Iserror:
        await callback_query.message.edit_text("Ошибка при сохранении {answer}")
    else:
        if answer != 0:
            await callback_query.message.edit_text(f"Сохранение успешно", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            await state.set_state(UserState.rating_meal)

@router.callback_query(lambda c: c.data == 'meal_rate')
async def main_meal_rate(callback_query: CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    sticker_mssg = await callback_query.message.answer_sticker(STICKER_ID)
    state_data = await state.get_data()
    food = state_data["latest_food"]
    Iserror, user_data = await get_user_info(callback_query.from_user.id)
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
    asyncio.create_task(log_user_callback(callback_query))
    sticker_mssg = await callback_query.message.answer_sticker(sticker=STICKER_ID)
    iserror, resp = await long_rate(callback_query.from_user.id, "3")
    await sticker_mssg.delete()
    buttons = [[InlineKeyboardButton(text=arrow_menu, callback_data="menu")]]
    buttons1 = [[InlineKeyboardButton(text="Показать график за неделю", callback_data="menu_dnevnik_analysis_graph")],[InlineKeyboardButton(text=arrow_menu, callback_data="menu")]]
    if await state.get_state() == UserState.graph:
        await callback_query.message.answer(resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        asyncio.create_task(log_bot_response(resp, callback_query.from_user.id))
    else:
        await callback_query.message.edit_text(resp, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons1))
        asyncio.create_task(log_bot_response(resp, callback_query.from_user.id))

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis_rate-day')
async def main_meal_rate_week(callback_query: CallbackQuery, state: FSMContext):
     
    asyncio.create_task(log_user_callback(callback_query))
    try:
        sticker_mssg = await callback_query.message.answer_sticker(sticker=STICKER_ID)
        iserror, resp = await long_rate(callback_query.from_user.id, "0")
        await sticker_mssg.delete()
        if iserror:
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
    if callback_query.data == "menu_settings_profile_name":
        await change_user_name(callback_query, state, name)
    elif callback_query.data == "menu_settings_profile_kkal":
        await change_user_kkal(callback_query, state, kkal)
    elif callback_query.data == "menu_settings_profile_re-anket":
        await state.set_state(Questionnaire.first)
        await process_name(callback_query.message, state)
    elif callback_query.data == "menu_settings_profile_notif":
        await change_user_notifs(callback_query, state)

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
@router.message(Command('lesson_1'))
async def start_lesson(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(LessonStates.step_1)
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(
            "Welcome to the lesson! Press the button to start.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Start Lesson", callback_data="start")]
            ])
        )
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.message.answer(
            "Welcome to the lesson! Press the button to start.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Start Lesson", callback_data="start")]
            ])
        )

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


@router.callback_query(lambda c: c.data in ["d1", "d2", "d2_2", "d3", "d3_2", "d4", "d4_2", "d5", "d5_2","d6","d6_2","d7","d8","d8_2","d9","d9_2","d10","d10_2","d11","d11_2","d12","d12_2","d13","d13_2","d14","d15","d15_2","d16","d16_2","d17","d17_2","d18","d19","d20","d21"])
async def set_lesson_state(callback_query: types.CallbackQuery, state: FSMContext):
    asyncio.create_task(log_user_callback(callback_query))
    if callback_query.data == "d1":
        await state.set_state(LessonStates.step_1)
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
    await process_first(callback_query.message, state)
    await state.set_state(Questionnaire.mail)

@router.message(StateFilter(Questionnaire.prefirst))
async def main_process_prefirst(message: Message, state: FSMContext):
    await process_prefirst(message, state)
    await state.set_state(Questionnaire.first)

@router.callback_query(StateFilter(Questionnaire.first), lambda c: True)
async def main_process_first(callback_query: types.CallbackQuery, state: FSMContext):
    await process_first(callback_query.message, state)
    await state.set_state(Questionnaire.mail)

@router.message(StateFilter(Questionnaire.mail))
async def main_process_mail(message: Message, state: FSMContext):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, message.text):
        await process_mail(message, state)
        await state.set_state(Questionnaire.name)
    else:
        await message.answer("Какая у тебя электронная почта?\nПожалуйста введи ту же почту, что и при оплате — это важно")
    

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
    await state.update_data(height=message.text)
    await process_height(message, state)
    await state.set_state(Questionnaire.weight)

@router.message(StateFilter(Questionnaire.weight))
async def main_process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await process_weight(message, state)
    await state.set_state(Questionnaire.age)

@router.message(StateFilter(Questionnaire.age))
async def main_process_age(message: Message, state: FSMContext):
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
    pattern = r'^[0-9.,]+$'
    if re.match(pattern, message.text):
        await state.update_data(jogging=message.text)
        await process_jogging(message, state)
        await state.set_state(Questionnaire.lifting)
    else: 
        await message.answer("Попробуй ввести число ещё раз, с первого раза я не поняла.")

@router.message(StateFilter(Questionnaire.lifting))
async def main_process_lifting(message: Message, state: FSMContext):
    pattern = r'^[0-9.,]+$'
    if re.match(pattern, message.text):
        await state.update_data(lifting=message.text)
        await process_lifting(message, state)
        await state.set_state(Questionnaire.stress)
    else: 
        await message.answer("Попробуй ввести число ещё раз, с первого раза я не поняла.")

@router.callback_query(StateFilter(Questionnaire.stress), lambda c: True)
async def main_process_stress(callback_query: types.CallbackQuery, state: FSMContext):
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
    pattern = r'^\d+$'
    if not re.match(pattern, message.text):
        await message.answer("Пожалуйста введи целое число")
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
                "user_info_gym_hrs": state_data["jogging"],
                "user_info_excersise_hrs": state_data["lifting"],
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
        iserror, response = await add_or_update_usr_info(json.dumps(data))
        print(f"saving data for user {message.from_user.id} has returned {iserror}, {response}")
    else:
        await message.answer("Не поняла, попробуй, пожалуйста, ещё раз")

@router.callback_query(StateFilter(Questionnaire.community_invite), lambda c: True)
async def main_process_community_invite(callback_query: types.CallbackQuery, state: FSMContext):
    await process_community_invite(callback_query.message, state)


################## QUESTIONNAIRE  QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE ##################

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














@router.message()
async def default_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    # await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    # if not current_state:
    if message.sticker:
        sticker_id = message.sticker.file_id
        await message.answer(f"{sticker_id}")
    else: 
        if message.photo:
            await state.set_state(UserState.recognition)
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


# async def on_startup(dp):
#     conn = sqlite3.connect('user_states.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT user_id, state, data FROM user_states')
#     for user_id, state, data in cursor.fetchall():
#         await dp.storage.set_state(user=user_id, state=state)
#         await dp.storage.set_data(user=user_id, data=eval(data))
#     conn.close()

async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

# async def on_shutdown(dp: Dispatcher):
#     logging.info("Shutting down...")
    
#     pool = dp.get("db_pool")
#     if pool:
#         await pool.close()
#         logging.info("Database connection pool closed.")
    
#     bot = dp.bot
#     await bot.send_message(chat_id=464682207, text="Bot is shutting down. Goodbye!")
    
    
#     logging.info("Shutdown complete.")


# async def main() -> None:
#     init_db()
#     pool = await create_db_pool()
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     dp.include_router(router)
#     dp.message.middleware(StateMiddleware())
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(
#         parse_mode=ParseMode.HTML))
#     dp["db_pool"] = pool
#     # loop = asyncio.get_event_loop()
#     # for sig in (signal.SIGTERM, signal.SIGINT):  # Handle SIGTERM and SIGINT
#     #     loop.add_signal_handler(sig, lambda: asyncio.create_task(on_shutdown(dp)))

#     await dp.start_polling(bot)

# async def shutdown(signal, loop, dp: Dispatcher):
#     logging.info(f"Received {signal.name}. Shutting down...")
#     await on_shutdown(dp)
#     loop.stop()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     dp = Dispatcher()

#     for sig in (signal.SIGTERM, signal.SIGINT):
#         loop.add_signal_handler(
#             sig,
#             lambda sig=sig: asyncio.create_task(shutdown(sig, loop, dp))
#         )
#     try:
#         loop.run_until_complete(main())
#     except Exception as e:
#         logging.error(f"Unexpected error: {e}")
#     finally:
#         loop.close()
#         logging.info("Application stopped.")

# if __name__ == "__main__":
#     asyncio.run(main())

async def on_shutdown(dp: Dispatcher):
    logging.info("Shutting down...")
    
    pool = dp.get("db_pool")
    if pool:
        await pool.close()
        logging.info("Database connection pool closed.")
    
    bot = dp.bot
    try:
        await bot.send_message(chat_id=464682207, text="Bot is shutting down. Goodbye!")
        logging.info("Shutdown notification sent to users.")
    except Exception as e:
        logging.error(f"Failed to send shutdown notification: {e}")
    logging.info("Shutdown complete.")

async def main() -> None:
    storage = MemoryStorage()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    pool = await create_db_pool()
    dp = Dispatcher(close_loop_on_shutdown=False, storage=storage)
    dp["db_pool"] = pool
    dp.include_router(router)
    dp.message.middleware(StateMiddleware())
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler( sig,lambda sig=sig: asyncio.create_task(on_shutdown(dp)))
    
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info("Application stopped.")