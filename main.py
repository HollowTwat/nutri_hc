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
# from stickerlist import STICKERLIST
import shelve
import json

from functions import *
from functions2 import *
from menu_functions import *
from day1 import *
# from day2 import *
from questionnaire import *

BOT_TOKEN = os.getenv("BOT_TOKEN")                    ##ACTUALISED
OPENAI_KEY = os.getenv("OPENAI_KEY")                  ##ACTUALISED

#ASSISTANTS FFS HOW MANY CAN THERE BE MAAAAAN
VISION_ASSISTANT_ID = os.getenv('VISION_ASSISTANT_ID')
CITY_ASSISTANT_ID = os.getenv('CITY_ASSISTANT_ID')
ASSISTANT2_ID = os.getenv('ASSISTANT2_ID')
YAPP_SESH_ASSISTANT_ID = os.getenv('YAPP_SESH_ASSISTANT_ID')    ##ACTUALISED 
RATE_DAY_ASS_ID = os.getenv('RATE_DAY_ASS_ID')
RATE_MID_ASS_ID = os.getenv('RATE_MID_ASS_ID')
RATE_SMOL_ASS_ID = os.getenv('RATE_SMOL_ASS_ID')
RATE_WEEK_ASS_ID = os.getenv('RATE_WEEK_ASS_ID')
RATE_TWONE_ASS_ID = os.getenv('RATE_TWONE_ASS_ID')
ETIK_ASS_ID = os.getenv('ETIK_ASS_ID')
RECIPE_ASS_ID = os.getenv('RECIPE_ASS_ID')
RATE_TRIAL_ASS_ID = os.getenv('RATE_TRIAL_ASS_ID')
VISION_ASS_ID_2 = os.getenv("VISION_ASS_ID_2")        ##ACTUALISED

TOKEN = BOT_TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)


class StateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        state = data['state']
        current_state = await state.get_state()
        data['current_state'] = current_state
        return await handler(event, data)


class UserState(StatesGroup):
    info_coll = State()
    recognition = State()
    redact = State()
    yapp_new = State()
    yapp = State()
    menu = State()
    saving_confirmation = State()
    saving = State()

class LessonStates(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()

class LessonStates2(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()

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


class ImageUploadState(StatesGroup):
    waiting_for_image = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    step0txt = "in_dev"
    await message.answer(step0txt, reply_markup=keyboard)




################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################
@router.message(Command("menu"))
async def main_menu_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await menu_handler(message, state)

@router.callback_query(lambda c: c.data == 'menu')
async def main_menu_cb_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await menu_cb_handler(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_back')
async def main_menu_back_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await menu_back_handler(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_course')
async def main_process_menu_course(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_course(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik')
async def main_process_menu_dnevnik(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_dnevnik(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'menu_nutri')
async def main_process_menu_nutri(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_nutri(callback_query.message, state)

@router.callback_query(lambda c: c.data == 'menu_settings')
async def main_process_menu_settings(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_settings(callback_query.message, state)

@router.message(Command("1"))
async def menu_main_process_menu_course(message: Message, state: FSMContext) -> None:
    await process_menu_course(message, state)

@router.message(Command("2"))
async def menu_main_process_menu_dnevnik(message: Message, state: FSMContext) -> None:
    await process_menu_dnevnik(message, state)

@router.message(Command("3"))
async def menu_main_process_menu_nutri(message: Message, state: FSMContext) -> None:
    await process_menu_nutri(message, state)

@router.message(Command("4"))
async def menu_main_process_menu_settings(message: Message, state: FSMContext) -> None:
    await process_menu_settings(message, state)
################## MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU MENU ##################

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_course_lesson_x')
async def main_process_menu_course_lesson(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_course_lesson(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_course_info')
async def main_process_menu_course_info(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_course_info(callback_query, state)

################## COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU COURSE_MENU ##################

async def dnevnik_layover(message, state, nextfunc):
    prev_state = await state.get_state()
    print(f"{prev_state}")
    step0txt = "in dev распознание еды"
    await message.answer(step0txt, reply_markup=None)


    await state.set_state(prev_state)
    await nextfunc(message, state)



################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_dnevnik_input')
async def main_process_menu_dnevnik_input(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.recognition)
    await process_menu_dnevnik_input(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_redact')
async def main_process_menu_dnevnik_redact(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_dnevnik_redact(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_analysis')
async def main_process_menu_dnevnik_analysis(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_dnevnik_analysis(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_dnevnik_instruction')
async def main_process_menu_dnevnik_instruction(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_dnevnik_instruction(callback_query, state)

################## DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU DNEVNIK_MENU ##################

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_nutri_yapp')
async def main_process_menu_nutri_yapp(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_nutri_yapp(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_nutri_reciepie')
async def main_process_menu_nutri_reciepie(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_nutri_reciepie(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_nutri_etiketka')
async def main_process_menu_nutri_etiketka(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_nutri_etiketka(callback_query, state)

################## YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU YAPP_MENU ##################

async def get_url(file_id: str) -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    return file_url

async def audio_file(file_id: str) -> str:
    file_url = await get_url(file_id)
    transcription = await transcribe_audio_from_url(file_url)
    return transcription


################## YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP ##################

@router.message(StateFilter(UserState.yapp_new, UserState.yapp))
async def yapp_functional(message: Message, state: FSMContext):
    if await state.get_state() == UserState.yapp_new:
        new_thread = True
    elif await state.get_state() == UserState.yapp:
        new_thread = False
    id = str(message.from_user.id)
    buttons = [[InlineKeyboardButton(text='Меню', callback_data='menu')]]
    errormessage = "Гпт вернул ошибку"
    if message.text:
        flag, response = yapp(id, message.text, new_thread)
        if flag:
            await message.answer(f"{response}\n\nТы можешь продолжить общаться со мной или нажать кнопку", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        else: message.answer(errormessage)
    elif message.voice:
        transcription = await audio_file(message.voice.file_id)
        flag, response = yapp(id, transcription, new_thread)
        if flag:
            await message.answer(f"response\n\n Ты можешь продолжить общаться со мной или нажать кнопку", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        else: message.answer(errormessage)
    else:
        message.answer("Я читаю только текст/аудио")

################## YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP YAPP ##################

################## DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK ##################

@router.message(StateFilter(UserState.recognition))
async def dnevnik_functional(message: Message, state: FSMContext):
    id = str(message.from_user.id)
    confirm_text = "Все верно?\n\n💡Кстати не забывай пить воду, чтобы избежать обезвоживания"
    buttons = [[InlineKeyboardButton(text="Редактировать", callback_data="redact")],
               [InlineKeyboardButton(text="Все хорошо", callback_data="save")]]
    if message.photo:
        url = await get_url(message.photo[-1].file_id)
        vision = await process_url(url, id, VISION_ASS_ID_2)
        Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
        if Iserror:
            await message.answer(f"офибка!!! \n{pretty}")
        else: 
            state.update_data(latest_food = food)
            await message.answer(pretty)
            await message.answer(confirm_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            await state.set_state(UserState.saving_confirmation)
    elif message.voice:
        transcription = await audio_file(message.voice.file_id)
        vision = await generate_response(transcription, id, VISION_ASS_ID_2)
        Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
        if Iserror:
            await message.answer(f"офибка!!! \n{pretty}")
        else: 
            state.update_data(latest_food = food)
            await message.answer(pretty)
            await message.answer(confirm_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            await state.set_state(UserState.saving_confirmation)
    elif message.text:
        vision = await generate_response(message.text, id, VISION_ASS_ID_2)
        Iserror, food, pretty = await prettify_and_count(vision, detailed_format=True)
        if Iserror:
            await message.answer(f"офибка!!! \n{pretty}")
        else: 
            await state.update_data(latest_food = food)
            await message.answer(pretty)
            await message.answer(confirm_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            await state.set_state(UserState.saving_confirmation)
    else: message.answer("0_o")

@router.callback_query(StateFilter(UserState.saving_confirmation))
async def state_switch(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "redact":
        await state.clear()
        await callback_query.message.edit_text("Тут будет редакция", reply_markup=None)
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
    data = await state.get_data()
    str_food = str(data["latest_food"])
    await callback_query.message.edit_text(f"Тут будет сохранение приема пищи {callback_query.data} с инфой: \n {str_food}")

################## DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK DNEVNIK ##################

################## SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU SETTINGS_MENU ##################

@router.callback_query(lambda c: c.data == 'menu_settings_profile')
async def main_process_menu_settings_profile(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_settings_profile(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_settings_help')
async def main_process_menu_settings_help(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_settings_help(callback_query, state)

@router.callback_query(lambda c: c.data == 'menu_settings_sub')
async def main_process_menu_settings_sub(callback_query: CallbackQuery, state: FSMContext):
    await process_menu_settings_sub(callback_query, state)

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

@router.callback_query(lambda c: c.data in ["d1", "d2"])
async def set_lesson_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "d1":
        await state.set_state(LessonStates.step_1)
    elif callback_query.data == "d2":
        await state.set_state(LessonStates2.step_1)
##################### GETTING INTO THE LESSONS

################## LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 ##################



################## LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 ##################

################## HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP HELP################

@router.callback_query(StateFilter(LessonStates.step_7), lambda c: True)
async def main_process_step_L2(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "callback1":
       pass #await process_step_L2(callback_query, state)
    elif callback_query.data in ["callback2", "callback2"]:
       pass #await process_step_L2(callback_query, state)

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
        input_text = await gen_text(state)
        await give_plan(callback_query.message, state, input_text)
        await state.set_state(Questionnaire.city)

@router.callback_query(StateFilter(Questionnaire.w_loss), lambda c: True)
async def main_process_w_loss(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    goal = user_data["goal"]
    await process_w_loss(callback_query.message, state, goal)
    await state.set_state(Questionnaire.w_loss_amount)

@router.message(StateFilter(Questionnaire.w_loss_amount))
async def main_process_w_loss_amount(message: Message, state: FSMContext):
    pattern = r'^\d+$'
    if not re.match(pattern, message.text):
        pass
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
            if goal == "+": goal_txt = "набрать вес"
            elif goal == "-": goal_txt = "сбросить вес"
            text1 = f"Чтобы помочь тебе в достижении твоей цели {goal_txt}, я рассчитала, сколько калорий тебе нужно есть в день. Я использую формулу Mifflin-St Jeor, так как она считается одной из самых точных.\n\n\nТвои результаты следующие:\nБазовый уровень метаболизма (BMR): примерно <b>{bmr}</b> ккал/день.\nОбщая суточная потребность в энергии (TDEE) при умеренной активности: примерно <b>{tdee}</b> ккал/день."
            await message.answer(text1)
            await give_plan(message, state, input_text)
    await state.set_state(Questionnaire.city)


@router.message(StateFilter(Questionnaire.city))
async def main_process_city(message: Message, state: FSMContext):
    await process_city(message, state)
    await state.set_state(Questionnaire.morning_ping)

@router.message(StateFilter(Questionnaire.morning_ping))
async def main_process_morning_ping(message: Message, state: FSMContext):
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await process_morning_ping(message, state)
        await state.set_state(Questionnaire.evening_ping)
    else:
        await message.answer("Не поняла, попробуй, пожалуйста, ещё раз")

@router.message(StateFilter(Questionnaire.evening_ping))
async def main_process_evening_ping(message: Message, state: FSMContext):
    pattern = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, message.text):
        await process_evening_ping(message, state)
        await state.set_state(Questionnaire.community_invite)
    else:
        await message.answer("Не поняла, попробуй, пожалуйста, ещё раз")

@router.callback_query(StateFilter(Questionnaire.community_invite), lambda c: True)
async def main_process_community_invite(callback_query: types.CallbackQuery, state: FSMContext):
    await process_community_invite(callback_query.message, state)
    await state.clear()

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

@router.message(ImageUploadState.waiting_for_image)
async def handle_invalid_content(message: types.Message):
    await message.answer("Please send an image to get its file_id.")


















@router.message()
async def default_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    # await state.update_data(full_sequence=False)
    buttons = [
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    if not current_state:
        if message.sticker:
            sticker_id = message.sticker.file_id
            await message.answer(f"{sticker_id}")
        else: 
            await message.answer("Будут перехватчики", reply_markup=keyboard)
    else:
        await message.answer(f"Текущее состояние: {current_state}")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.include_router(router)
    dp.message.middleware(StateMiddleware())
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
