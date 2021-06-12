# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

import io
import re
import uuid

from InlineBot import (
    CodeXBotz,
    Message,
    filters,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from InlineBot.helper_funcs import (
    generate_button,
    upload_photo,
    split_quotes
)  
from InlineBot.database import (
    del_all,
    add_filter,
    delete_filter,
    count_filters,
    get_all_filters
)
from InlineBot import FILTER_COMMAND, DELETE_COMMAND

@CodeXBotz.on_message(filters.command(FILTER_COMMAND) & filters.admins)
async def new_filter(client: CodeXBotz, message: Message):

    strid = str(uuid.uuid4())
    args = message.text.html.split(None, 1)
    
    if len(args) < 2:
        await message.reply_text("Use Correct format 😐", quote=True)
        return
    
    extracted = split_quotes(args[1])
    text = extracted[0].lower()
    msg_type = 'Text'
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = generate_button(extracted[1], strid)
        fileid = None
        if not reply_text:
            await message.reply_text("You cannot have buttons alone, give some text to go with it!", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        reply_text = ""
        btn = []
        fileid = None
        alert = None
        msg_type = 'Text'
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            replied = message.reply_to_message
            msg = replied.document or replied.video or replied.audio or replied.animation or replied.sticker or replied.voice or replied.video_note or None
            if msg:
                fileid = msg.file_id
                if replied.document:
                    msg_type = 'Document'
                elif replied.video:
                    msg_type = 'Video'
                elif replied.audio:
                    msg_type = 'Audio'
                elif replied.animation:
                    msg_type = 'Animation'
                elif replied.sticker:
                    msg_type = 'Sticker'
                elif replied.voice:
                    msg_type = 'Voice'
                elif replied.video_note:
                    msg_type = 'Video Note'

                reply_text = message.reply_to_message.caption.html
            
            elif replied.photo:
                fileid = await upload_photo(replied)
                msg_type = 'Photo'
                if not fileid:
                    return
                reply_text = message.reply_to_message.caption.html
            
                    
            elif replied.text:
                reply_text = message.reply_to_message.text.html
                msg_type = 'Text'
                fileid = None
            else:
                await message.reply('Not Supported..!')
                return
            alert = None
        except:
            pass
            

    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = await upload_photo(message.reply_to_message)
            if not fileid:
                return
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Photo'

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Video'

    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Audio'
   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Document'

    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Animation'

    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert =  generate_button(extracted[1], strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Sticker'

    elif message.reply_to_message and message.reply_to_message.voice:
        try:
            fileid = message.reply_to_message.voice.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Voice'
    elif message.reply_to_message and message.reply_to_message.video_note:
        try:
            fileid = message.reply_to_message.video_note.file_id
            reply_text, btn, alert = generate_button(extracted[1], strid)
        except Exception as a:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Video Note'
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = generate_button(message.reply_to_message.text.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
    else:
        await message.reply('Not Supported..!')
        return
    
    try:
        if fileid:
            if msg_type == 'Photo':
                await message.reply_photo(
                    photo = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
            else:
                await message.reply_cached_media(
                    file_id = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
        else:
            await message.reply(
                text = reply_text,
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
            )
    except Exception as a:
        try:
            await message.reply(text = f"<b>❌ Error</b>\n\n{str(a)}\n\n<i>Join @CodeXBotzSupport for Support</i>")
        except:
            pass
        return

    await add_filter(text, reply_text, btn, fileid, alert, msg_type, strid)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text = 'Share filter', switch_inline_query = text),
                InlineKeyboardButton(text = 'Try Here', switch_inline_query_current_chat = text)
            ]
        ]
    )
    await message.reply_text(f"<code>{text}</code> Added", quote = True, reply_markup = reply_markup)

@CodeXBotz.on_message(filters.command(DELETE_COMMAND) & filters.admins)
async def del_filter(client: CodeXBotz, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n"
            f"<code>/{DELETE_COMMAND.lower()} filtername</code>\n\n"
            "Use /filters to view all available filters",
            quote=True
        )
        return

    query = text.lower()
    await delete_filter(message, query)
    
@CodeXBotz.on_message(filters.command('filters') & filters.admins)
async def get_all(client: CodeXBotz, message: Message):
    texts = await get_all_filters()
    count = await count_filters()
    if count:
        filterlist = f"<b>Bot have total {count} filters</b>\n\n"

        for text in texts:
            keywords = f" ○  <code>{text}</code>\n"
            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("<code>", "").replace("</code>","").replace('<b>', '').replace('</b>', ''))) as keyword_file:
                sts = await message.reply('<i>Please wait..</i>')
                keyword_file.name = "filters.txt"
                await message.reply_document(
                    document=keyword_file
                )
                await sts.delete()
            return
    else:
        filterlist = f"<b>Bot have no filters.!</b>"

    await message.reply_text(
        text=filterlist,
        quote=True
    )
    
@CodeXBotz.on_message(filters.command('delall') & filters.owner)
async def delallconfirm(client, message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Yes', callback_data = 'delall'),
                InlineKeyboardButton('No', callback_data = 'delallclose')
            ]
        ]
    )
    await message.reply_text(
        f"This will delete all of your filters.\nAre you sure you want do this.?",
        reply_markup = reply_markup,
        quote=True
    )
    
@CodeXBotz.on_callback_query(filters.regex("^delall$") & filters.owner)
async def delall(client: CodeXBotz, query: CallbackQuery):
    await del_all(query.message)

@CodeXBotz.on_callback_query(filters.regex("^delallclose$") & filters.owner)
async def delcancel(client: CodeXBotz, query: CallbackQuery):
    await query.edit_message_text(
        text = 'Process Cancelled',
        reply_markup = None
    )
    return
