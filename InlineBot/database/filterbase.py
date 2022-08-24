# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

import pymongo
from . import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

filter_collection = database['filters']

async def add_filter(text, reply_text, btn, file, alert, msg_type, id):
    
    fdata = {'text': str(text)}
    
    button = str(btn)
    button = button.replace('pyrogram.types.InlineKeyboardButton', 'InlineKeyboardButton')
    found = filter_collection.find_one(fdata)
    if found:
        filter_collection.delete_one(fdata)
        
    data = {'_id': id, 'text':str(text), 'reply':str(reply_text), 'btn':str(button), 'file':str(file), 'alert':str(alert), 'type':str(msg_type)}
    filter_collection.insert_one(data)
    
async def delete_filter(message, text):
    
    query = {'text':text}
    
    found = filter_collection.find_one(query)
    
    if found:
        filter_collection.delete_one(query)
        await message.reply_text(
            f"<code>{text}</code>  deleted.",
            quote=True
        )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)

async def get_all_filters():
    texts = []
    query = filter_collection.find().sort('text', 1)
    try:
        for file in query:
            text = file['text']
            texts.append(text)
    except:
        pass
    return texts

async def count_filters():
    count = filter_collection.count_documents({})
    return count

async def del_all(message):
    
    if not await count_filters():
        await message.edit_text("Nothing to Delete.!")
        return

    try:
        filter_collection.remove()
        await message.edit_text("All filters deleted.!")
    except:
        await message.edit_text(f"Couldn't remove all of your filters")
        return

async def get_filters(text):
    if text == "":
        documents = filter_collection.find()
        doc_list = list(documents)
        doc_list.reverse()
        return doc_list[:50]
    else:
        regex = f"^{text}.*"
        query = {'text': {'$regex' : regex}}
        documents = filter_collection.find(query).sort('text', 1).limit(50)
        return documents

async def get_alerts(id):
    document = filter_collection.find_one({'_id': id})
    if not document:
        return False
    return document['alert']

async def get_data():
    documents = filter_collection.find().sort('text', 1)
    doc_list = list(documents)
    return str(doc_list)
    
async def import_data(data):
    filter_collection.insert_many(data)
    
async def get_status():
    filters = filter_collection.find()
    filters_no = 0
    text = 0
    photo = 0
    video = 0
    audio = 0
    document = 0
    animation = 0
    sticker = 0
    voice = 0 
    videonote = 0 
    
    for filter in filters:
        type = filter['type']
        if type == 'Text':
            text += 1 
        elif type == 'Photo':
            photo += 1 
        elif type == 'Video':
            video += 1 
        elif type == 'Audio':
            audio += 1 
        elif type == 'Document':
            document += 1
        elif type == 'Animation':
            animation += 1
        elif type == 'Sticker':
            sticker += 1 
        elif type == 'Voice':
            voice += 1
        elif type == 'Video Note':
            videonote += 1 

        filters_no += 1
    
    user_collection = database['users']
    no_users = user_collection.find().count()
    
    stats_text = f"""<b>Statistics</b>
    
Total users: {no_users}
Total filters: {filters_no}
Text filters: {text}
Photo filters: {photo}
Video filters: {video}
Audio filters: {audio}
Document filters: {document}
Animation filters: {animation}
Sticker filters: {sticker}
Voice filters: {voice}
Video Note filters: {videonote}"""

    return stats_text
