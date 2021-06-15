# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

import os

API_HASH = os.environ.get("API_HASH", "")
APP_ID = int(os.environ.get("APP_ID", ""))
DB_URI = os.environ.get("DATABASE_URL", "")
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_BOT_WORKERS = int(os.environ.get("BOT_WORKERS", '4'))
DB_NAME = os.environ.get("DATABASE_NAME", "InlineFilterBot")
thumb = os.environ.get('THUMBNAIL_URL', 'https://telegra.ph/file/516ca261de9ebe7f4ffe1.jpg')
OWNER_ID = int(os.environ.get('OWNER_ID'))
CUSTOM_START_MESSAGE = os.environ.get('START_MESSAGE','')
FILTER_COMMAND = os.environ.get('FILTER_COMMAND', 'add')
DELETE_COMMAND = os.environ.get('DELETE_COMMAND', 'del')
IS_PUBLIC = True if os.environ.get('IS_PUBLIC', 'True').lower() != 'false' else False
try:
    ADMINS=[OWNER_ID]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#---------- ---------- ---------- ----------

import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = "codexbotz.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

#---------- ---------- ---------- ----------
from pyrogram import Client

class CodeXBotz(Client):
    def __init__(self):
        super().__init__(
            "bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "InlineBot/plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        self.LOGGER(__name__).info(f"@{bot_details.username}  started!")
        self.LOGGER(__name__).info("Created by 𝘾𝙤𝙙𝙚 𝕏 𝘽𝙤𝙩𝙯\nhttps://t.me/CodeXBotz")
        self.bot_details = bot_details

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
        
#---------- ---------- ---------- ----------

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedDocument
)

def is_owner(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if user_id == OWNER_ID:
        return True
    else:
        return False

def is_admin(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if user_id in ADMINS:
        return True
    else:
        return False
def check_inline(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if IS_PUBLIC:
        return True
    elif user_id in ADMINS:
        return True
    else:
        return False

filters.admins = filters.create(is_admin)
filters.owner = filters.create(is_owner)
filters.inline = filters.create(check_inline)

#---------- ---------- ---------- ----------
