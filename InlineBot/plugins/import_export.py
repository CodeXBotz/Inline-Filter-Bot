# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

import io
import os

from InlineBot import (
    CodeXBotz,
    filters,
    Message
)
from InlineBot.database import(
    get_data,
    count_filters,
    import_data,
    get_all_filters
)
from InlineBot.helper_funcs import make_dict

@CodeXBotz.on_message(filters.private & filters.command('export') & filters.admins)
async def export_data(client: CodeXBotz, message: Message):
    sts_msg = await message.reply('<i>Please Wait..!</i>')
    
    if await count_filters() == 0:
        await sts_msg.edit('You have no filters to Export')
        return
    data = await get_data()
    with io.BytesIO(str.encode(data)) as keyword_file:
            keyword_file.name = "export_data.txt"
            await message.reply_document(
                document=keyword_file
            )
    await sts_msg.delete()
    
@CodeXBotz.on_message(filters.private & filters.command('import') & filters.reply & filters.owner)
async def import_datas(client: CodeXBotz, message: Message):
    replied = message.reply_to_message
    if not replied.document:
        return
    elif not replied.document.file_name.endswith('.txt'):
        return
    sts_msg = await message.reply('<i>Please Wait..!</i>')
    dl_loc = await replied.download()
    with open(dl_loc, 'r') as f:
        data_text = f.read()
    try:
        os.remove(dl_loc)
    except:
        pass
    
    exst_keywords = await get_all_filters()

    try:
        data_list = make_dict(eval(data_text), exst_keywords)
    except Exception as e:
        await sts_msg.edit('Invalid File.!')
        return
    if len(data_list) == 0:
        await sts_msg.edit("Can't import any filters.!")
        return
    await import_data(data_list)
    await sts_msg.edit(f'Imported {len(data_list)} filters')
