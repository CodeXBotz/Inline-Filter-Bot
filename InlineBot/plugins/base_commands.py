# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

from InlineBot import CodeXBotz, ADMINS, filters, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from InlineBot.strings import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, MARKDOWN_HELP
from InlineBot.database import present_in_userbase, add_to_userbase

start_keyboard = [
    [
        InlineKeyboardButton(text = '🤔 Help', callback_data = "help"),
        InlineKeyboardButton(text = '🤖 About', callback_data = "about")
    ],
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close")
    ]
]

start_keyboard_c = [
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = "about"),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close")
    ],
    [
        InlineKeyboardButton(text = 'Search Here', switch_inline_query_current_chat = '')
    ]
]

help_keyboard = [
    [
        InlineKeyboardButton(text = '✏️ Markdown Helper ✏️', callback_data = 'markdownhelper')
    ],
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = 'about'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard = [
     [
        InlineKeyboardButton(text = '🤔 Help', callback_data = 'help'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard_c = [
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

markdown_keyboard = [
    [
        InlineKeyboardButton(text = '🔙 Back', callback_data = 'help')
    ]
]

@CodeXBotz.on_message(filters.command('start') & filters.private)
async def start_msg_admins(client: CodeXBotz, message: Message):
    if message.from_user.id in ADMINS:
        reply_markup = InlineKeyboardMarkup(start_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(start_keyboard_c)
    text = START_MESSAGE.format(
        mention = message.from_user.mention,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name,
        user_id = message.from_user.id,
        username = '' if message.from_user.username == None else '@'+message.from_user.username
    )

    await message.reply(
        text = text,
        quote = True,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )
    if not await present_in_userbase(message.from_user.id):
        await add_to_userbase(message.from_user.id)
    
@CodeXBotz.on_message(filters.command('help') & filters.private & filters.admins)
async def help_msg(client: CodeXBotz, message: Message):
    await message.reply(
        text = HELP_MESSAGE,
        quote = True,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )

@CodeXBotz.on_message(filters.command('about') & filters.private)
async def about_msg(client: CodeXBotz, message: Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await message.reply(
        text = ABOUT_MESSAGE,
        quote = True,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )

@CodeXBotz.on_callback_query(filters.regex(r'^close$'))
async def close_cbb(client: CodeXBotz, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass

@CodeXBotz.on_callback_query(filters.regex(r'^help$') & filters.admins)
async def help_cbq(client: CodeXBotz, query: CallbackQuery):
    await query.edit_message_text(
        text = HELP_MESSAGE,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )
    
@CodeXBotz.on_callback_query(filters.regex('^about$'))
async def about_cbq(client: CodeXBotz, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id in ADMINS:
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await query.edit_message_text(
        text = ABOUT_MESSAGE,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )
    
@CodeXBotz.on_callback_query(filters.regex('^markdownhelper$') & filters.admins)
async def md_helper(client: CodeXBotz, query: CallbackQuery):
    await query.edit_message_text(
        text = MARKDOWN_HELP,
        reply_markup = InlineKeyboardMarkup(markdown_keyboard),
        disable_web_page_preview = True,
        parse_mode = 'html'
    )
