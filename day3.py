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

IMG1 = "AgACAgIAAxkBAANAZ6Izhb3-oRwlYaP2VqDUaNj2B40AAr3sMRundBFJUR0CTkcujnEBAAMCAAN5AAM2BA"
IMG2 = "AgACAgIAAxkBAANEZ6Izix5un3K9FJFIkhnYohD1ndoAAr7sMRundBFJIg8zZa_LlZ4BAAMCAAN5AAM2BA"

IMG3 = "AgACAgIAAxkBAAMWZ6EeHHZlQuvULWbsJ0pM73-eQGUAAuL2MRundAlJ1lkQgI65WD8BAAMCAAN5AAM2BA"
IMG4 = "AgACAgIAAxkBAAMaZ6EeInSKWO2MV5QgfFFTinbKz78AAuP2MRundAlJraM0a_v0fWoBAAMCAAN5AAM2BA"

IMG5 = "AgACAgIAAxkBAAMcZ6EeY6Cpo88iEVUuKp94QnS3IoMAAuj2MRundAlJCB5-3Qoyr9YBAAMCAAN5AAM2BA"

IMG6 = "AgACAgIAAxkBAANrZ6JDsUQ0O6MqJSTe_sw2bfW_XFUAAl_tMRundBFJNj-RlQaUXkwBAAMCAAN5AAM2BA"
IMG7 = "AgACAgIAAxkBAAN9Z6JFxnoDL4z0AzUvijv5XOdITaQAAnrtMRundBFJr0YsPvhWHfYBAAMCAAN5AAM2BA"
IMG8 = "AgACAgIAAxkBAAOBZ6JFzb1SlgGI5Lw8FElb8CH9v5kAAnvtMRundBFJYRsH9-KY4wABAQADAgADeQADNgQ"
IMG9 = "AgACAgIAAxkBAAOFZ6JF0gyVWUX0JLcdG8CHPhCrRLYAAnztMRundBFJKxmWswABEVhGAQADAgADeQADNgQ"
IMG10 = "AgACAgIAAxkBAAOJZ6JF25nDe-gpt_IDLtxxfaHDhggAAn3tMRundBFJ_tZtghfiAzgBAAMCAAN5AAM2BA"



class LessonStates3(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_11 = State()
    step_12 = State()
    step_13 = State()
    step_14 = State()
    step_15 = State()
    step_16 = State()