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
# from stickerlist import STICKERLIST
import shelve
import json

from functions import *
from functions2 import *
from menu_functions import *
from day1 import *
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

@router.message(Command('lesson_1'))
async def start_lesson(message: types.Message, state: FSMContext):
    await state.set_state(LessonStates.step_1)
    await message.answer(
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

################## QUESTIONNAIRE  QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE QUESTIONNAIRE ##################

@router.message(Command('questionaire'))
async def main_rerty_mail(message: Message, state: FSMContext):
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
    await process_mail(message, state)
    await state.set_state(Questionnaire.name)

@router.message(StateFilter(Questionnaire.name))
async def main_process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await process_name(message, state)
    await state.set_state(Questionnaire.gender)

@router.callback_query(StateFilter(Questionnaire.gender), lambda c: True)
async def main_process_gender(callback_query: types.CallbackQuery, state: FSMContext):
    gender = callback_query.data
    print(gender)
    if gender == "female":
        await process_gender(callback_query.message, state)
        await state.set_state(Questionnaire.f_preg)
    elif gender == "male":
        await process_f_breastfeed(callback_query.message, state)
        await state.set_state(Questionnaire.height)
    else: 
        await callback_query.message.answer("Что-то не так с полом")
@router.callback_query(StateFilter(Questionnaire.f_preg), lambda c: True)
async def main_process_f_preg(callback_query: types.CallbackQuery, state: FSMContext):
    await process_f_preg(callback_query.message, state)
    await state.set_state(Questionnaire.f_breastfeed)

@router.callback_query(StateFilter(Questionnaire.f_breastfeed), lambda c: True)
async def main_process_f_breastfeed(callback_query: types.CallbackQuery, state: FSMContext):
    await process_f_breastfeed(callback_query.message, state)
    await state.set_state(Questionnaire.height)

@router.message(StateFilter(Questionnaire.height))
async def main_process_geight(message: Message, state: FSMContext):
    await process_height(message, state)

@router.message(StateFilter(Questionnaire.weight))
async def main_process_weight(message: Message, state: FSMContext):
    await process_weight(message, state)

@router.message(StateFilter(Questionnaire.age))
async def main_process_age(message: Message, state: FSMContext):
    await process_age(message, state)

@router.callback_query(StateFilter(Questionnaire.water), lambda c: True)
async def main_process_water(callback_query: types.CallbackQuery, state: FSMContext):
    await process_water(callback_query.message, state)

@router.callback_query(StateFilter(Questionnaire.booze), lambda c: True)
async def main_process_booze(callback_query: types.CallbackQuery, state: FSMContext):
    await process_booze(callback_query.message, state)

@router.callback_query(StateFilter(Questionnaire.meals), lambda c: True)
async def main_process_meals(callback_query: types.CallbackQuery, state: FSMContext):
    await process_meals(callback_query.message, state)

@router.message(StateFilter(Questionnaire.meals_extra))
@router.callback_query(StateFilter(Questionnaire.meals_extra))
async def main_process_meals_extra(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message_or_callback, types.Message):
        await process_meals_extra(message_or_callback, state)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await process_meals_extra(message_or_callback.message, state)

@router.message(StateFilter(Questionnaire.allergies))
@router.callback_query(StateFilter(Questionnaire.allergies))
async def main_process_allergies(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message_or_callback, types.Message):
        await process_allergies(message_or_callback, state)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await process_allergies(message_or_callback.message, state)

@router.callback_query(StateFilter(Questionnaire.part3), lambda c: True)
async def main_process_part3(callback_query: types.CallbackQuery, state: FSMContext):
    await process_part3(callback_query.message, state)

@router.message(StateFilter(Questionnaire.jogging))
async def main_process_jogging(message: Message, state: FSMContext):
    await process_jogging(message, state)

@router.message(StateFilter(Questionnaire.lifting))
async def main_process_lifting(message: Message, state: FSMContext):
    await process_lifting(message, state)

@router.callback_query(StateFilter(Questionnaire.stress), lambda c: True)
async def main_process_stress(callback_query: types.CallbackQuery, state: FSMContext):
    await process_stress(callback_query.message, state)

@router.callback_query(StateFilter(Questionnaire.sleep), lambda c: True)
async def main_process_sleep(callback_query: types.CallbackQuery, state: FSMContext):
    await process_sleep(callback_query.message, state)

@router.callback_query(StateFilter(Questionnaire.goal), lambda c: True)
async def main_process_goal(callback_query: types.CallbackQuery, state: FSMContext):
    await process_goal(callback_query.message, state)

@router.callback_query(StateFilter(Questionnaire.w_loss), lambda c: True)
async def main_process_w_loss(callback_query: types.CallbackQuery, state: FSMContext):
    await process_w_loss(callback_query.message, state)

@router.message(StateFilter(Questionnaire.w_loss_amount))
async def main_process_w_loss_amount(message: Message, state: FSMContext):
    await process_w_loss_amount(message, state)

@router.message(StateFilter(Questionnaire.city))
async def main_process_city(message: Message, state: FSMContext):
    await process_city(message, state)

@router.message(StateFilter(Questionnaire.morning_ping))
async def main_process_morning_ping(message: Message, state: FSMContext):
    await process_morning_ping(message, state)

@router.message(StateFilter(Questionnaire.evening_ping))
async def main_process_evening_ping(message: Message, state: FSMContext):
    await process_evening_ping(message, state)

@router.message(StateFilter(Questionnaire.community_invite))
async def main_process_community_invite(message: Message, state: FSMContext):
    await process_community_invite(message, state)

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
