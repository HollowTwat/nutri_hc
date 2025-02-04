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


from functions import *

debug = 1


async def yapp(id, question, new_thread):
    print('day1_yapp triggered')
    
    if new_thread:
        await remove_thread(id)
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