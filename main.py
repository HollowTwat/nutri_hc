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
from day2 import *
from questionnaire import *

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

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
    yapp = State()
    menu = State()

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
    step_11 = State()
    step_12 = State()
    step_13 = State()
    step_14 = State()
    step_15 = State()
    step_16 = State()

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

@router.message(Command("lessons_manage"))
async def lessons_manage_command(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [
        [InlineKeyboardButton(text='Урок1', callback_data='d1')],
        [InlineKeyboardButton(text='Урок2', callback_data='d2'), InlineKeyboardButton(text='Урок2_2', callback_data='d2_2')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("pick a lesson", reply_markup=keyboard)


@router.callback_query(lambda c: c.data in ["d1", "d2", "d2_2"])
async def set_lesson_state(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "d1":
        await state.set_state(LessonStates.step_1)
    elif callback_query.data == "d2":
        await state.set_state(LessonStates2.step_1)
        await process_l2_step_1(callback_query, state)
    elif callback_query.data == "d2_2":
        await state.set_state(LessonStates2.step_11)
        await process_l2_step_11(callback_query, state)
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
    await dnevnik_layover(message,state,xyz)

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

@router.callback_query(StateFilter(LessonStates2.step_11), lambda c: True)
async def main_process_l2_step_12(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_12(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_13(callback_query, state)

@router.message(StateFilter(LessonStates2.step_12))
async def main_process_l2_step_13(message: Message, state: FSMContext):
    await dnevnik_layover(message,state,xyz2)

@router.callback_query(StateFilter(LessonStates2.step_13), lambda c: True)
async def main_process_l2_step_14(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "next":
       await process_l2_step_14_1(callback_query, state)
    elif callback_query.data == "stop":
       await process_l2_step_14_2(callback_query, state)
    await process_l2_step_14(callback_query, state)

################## LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 LESSON_2 ##################

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
