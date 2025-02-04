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


async def yapp(id, question, delete_thread):
    print('day1_yapp triggered')
    if delete_thread:
        await remove_thread(id)
    try:
        response = await yapp_assistant(question, id, YAPP_SESH_ASSISTANT_ID)
        if response != "error":
            Iserror = False
            Jsoned = {
                    "extra": str(response)
                }
        elif response == "error":
            Iserror = True
            Jsoned = {
                    "error": str(response)
                }
        Final = json.dumps(
            {
                "IsError": str(Iserror),
                "Answer": Jsoned    
        })
        return Final, 201
    except Exception as e:
        return False