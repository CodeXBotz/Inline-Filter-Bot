# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

from pyrogram import __version__
from InlineBot import (
    OWNER_ID,
    FILTER_COMMAND,
    DELETE_COMMAND,
    CUSTOM_START_MESSAGE
)

if CUSTOM_START_MESSAGE:
    START_MESSAGE = CUSTOM_START_MESSAGE
else:
    START_MESSAGE = """<b>Hello {mention},

I am an Inline Saver Bot, you can save inline filters and It can be use in any of your chats easily, Click help for more details</b> 
"""

HELP_MESSAGE = f"""<b><u>This Is Not For You‼️</u></b>

"""

MARKDOWN_HELP = """<b><u>This Is Not For You‼️</u></b>

"""
