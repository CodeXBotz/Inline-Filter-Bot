# Copyright (C) @CodeXBotz - All Rights Reserved
# Licensed under GNU General Public License as published by the Free Software Foundation
# Written by Shahsad Kolathur <shahsadkpklr@gmail.com>, June 2021

import re
import os
import uuid
from typing import List
from telegraph import upload_file
from . import InlineKeyboardButton

BTN_URL_REGEX = r"(?:\[(.*)\]\((buttonurl|buttonalert):([^)]*)\))"

SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)

def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (text[0] == SMART_OPEN and text[counter] == SMART_CLOSE):
                break
            counter += 1
        else:
            return text.split(None, 1)

        key = remove_escapes(text[1:counter].strip())
        
        rest = text[counter + 1:].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    else:
        return text.split(None, 1)
        
def replace_href(text):
    regex = r"(.*)\[(.*)\]\((.*)\)(.*)"
    matches = re.search(regex, text, re.DOTALL)
    if matches:
        text = re.sub(regex,r"\1<a href='\3'>\2</a>\4",text)
        text = replace_href(text)
    return text
        
def remove_md(text):
    lists = {
        '__' : ['<u>','</u>'],
        '*' : ['<b>','</b>'],
        '`' : ['<code>','</code>'],
        '_' : ['<i>','</i>'],
        '~' : ['<s>','</s>']
    }
    for item, tag in lists.items():
        i = 2
        while i:
          text = text.replace(item,tag[i%2],1)
          i +=1
          if not (item in text):
              if i%2:
                  text = text[::-1].replace(tag[0][::-1],item[::-1],1)[::-1]
              text = text.replace(f"{tag[0]}{tag[1]}",f"{item}{item}")
              i = 0
    text = replace_href(text.replace('\n','\t')).replace('\t','\n')
    return text

def generate_button(text : str, id : str):
    btns = []
    if not text:
        return None
    matches = re.finditer(BTN_URL_REGEX, text, re.MULTILINE)
    if not matches:
        return None
    i = 0
    j = 0
    datalist = []
    for match in matches:
        button_text = match.group(1)
        for x in ['b', 'i', 'code', 'u', 's']:
            button_text = button_text.replace(f'<{x}>', '').replace(f'</{x}>', '')
        if bool(match.group(2) == 'buttonurl') & bool(' ' not in match.group(3)):
            if match.group(3).endswith(':same'):
                btnurl = match.group(3)[:-5]
                if i == 0:
                    btns.append([
                        InlineKeyboardButton(text=button_text, url=btnurl)
                    ])
                else:
                    btns[-1].append(
                        InlineKeyboardButton(text=button_text, url=btnurl)
                    )
            else:
                btns.append([
                    InlineKeyboardButton(text=button_text, url=match.group(3))
                ])
        elif match.group(2) == 'buttonalert':
            if match.group(3).endswith(':same'):
                if len(match.group(3)[:-5]) >= 200:
                    continue
                cdata = match.group(3)[:-5]
                datalist.append(cdata)
                if i == 0:
                    btns.append([
                        InlineKeyboardButton(text=button_text, callback_data=f"alertmessage:{j}:{id}")
                    ])
                else:
                    btns[-1].append(
                        InlineKeyboardButton(text=button_text, callback_data=f"alertmessage:{j}:{id}")
                    )
            else:
                if len(match.group(3)) >= 200:
                    continue
                datalist.append(match.group(3))
                btns.append([
                    InlineKeyboardButton(text=button_text, callback_data=f"alertmessage:{j}:{id}")
                ])
            j += 1
        i += 1
    new_text = re.sub(BTN_URL_REGEX, '', text, re.MULTILINE)
    text = remove_md(new_text)
    return text,btns,datalist

def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res

async def upload_photo(message):
    msg = await message.reply_text("<code>Please wait..</code>")
    _T_LIMIT = 5242880
    if not (bool(message.photo) and bool(message.photo.file_size <= _T_LIMIT)):
        await msg.edit("<i>Sorry this Photo is not supported..</i>")
        return False
    dl_loc = await message.download()
    try:
        response = upload_file(dl_loc)
    except Exception as t_e:
        await msg.edit_text(t_e)
        link = False
    else:
        link = f'https://telegra.ph{response[0]}'
        await msg.delete()
    finally:
        os.remove(dl_loc)
        
    return  link

def make_dict(data_list : List[dict], keywords : List[str]):
    dict_list = []
    for i in range(len(data_list)):
        if data_list[i]['text'] in keywords:
            continue

        new_id = str(uuid.uuid4())
        old_id = data_list[i]['_id']

        new_data = {'_id': new_id}
        new_data['text'] = data_list[i]['text']
        new_data['reply'] = data_list[i]['reply']
        new_data['file'] = data_list[i]['file']
        new_data['alert'] = data_list[i]['alert']
        new_data['type'] = data_list[i]['type']

        button_text = data_list[i]['btn']
        new_data['btn'] = button_text.replace(old_id, str(new_id))
        
        dict_list.append(new_data)

    return dict_list
