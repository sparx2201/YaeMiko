from inspect import getfullargspec
from io import BytesIO
from telegram import Message, Update, User
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, Updater 
from telegram.error import TelegramError
import logging
import asyncio
import logging
import os
import sys
import base64
import io
import telegram

from Mikobot import app
from Mikobot import aiohttpsession as session
from Mikobot import dispatcher

API_URL = "https://webscreenshot.vercel.app/api"

async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
    return data

async def take_screenshot(url: str, full: bool = False):
    url = f"https://{url}" if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1920,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(API_URL, json=payload)
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(base64.b64decode(b))
    file.name = "webss.jpg"
    return file

async def eor(message: Message, **kwargs):
    return await message.edit(**kwargs)

@app.on_message(filters.command(["webshot", "screenshot", "ss", "webss"], prefixes=["/"]))
async def take_ss(client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await eor(message, text="Usage: /webshot [URL] (yes|no)")
    if len(args) == 2:
        url = args[1]
        full = False
    elif len(args) == 3:
        url = args[1]
        full = args[2].lower().strip() in ["yes", "y", "1", "true"]
    else:
        return await eor(message, text="Invalid arguments.")

    m = await eor(message, text="Capturing screenshot...")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("Failed to take screenshot.")

        m = await m.edit("Uploading...")

        await message.reply_photo(photo)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))





__mod_name__ = "𝐖ᴇʙsʜᴏᴛ"
__help__ = """
» /webss *:* Sᴇɴᴅs ᴛʜᴇ sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴜʀʟ.
"""


#from base64 import b64decode
#from io import BytesIO
#from inspect import getfullargspec
#import requests
#from telegram.ext import filters, CommandHandler, MessageHandler
##from telegram.utils.request import Request
#from Mikobot import dispatcher, function
#from Mikobot import tbot as app
#from Mikobot.utils.post import post

#async def take_screenshot(url: str, full: bool = False):
#    url = "https://" + url if not url.startswith("http") else url
#    payload = {
#        "url": url,
#        "width": 1920,
#        "height": 1080,
#        "scale": 1,
#        "format": "jpeg",
#    }
#    if full:
#        payload["full"] = True
#    data = await post(
#        "https://webscreenshot.vercel.app/api",
#        data=payload,
#    )
#    if "image" not in data:
#        return None
#    b = data["image"].replace("data:image/jpeg;base64,", "")
#    file = BytesIO(b64decode(b))
#    file.name = "webss.jpg"
#    return file

#async def eor(update, context, **kwargs):
#    if update.message:
#        func = update.message.edit_text if update.message.from_user.is_self else update.message.reply_text
#    else:
#        func = update.callback_query.message.reply_text
#    spec = getfullargspec(func.__wrapped__).args
#    return await func(**{k: v for k, v in kwargs.items() if k in spec})

#async def take_ss(update, context):
#    if len(context.args) < 1:
#        return await eor(update, context, text="ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.")

#    url = context.args[0]
#    full = False
#    if len(context.args) > 1:
#        full = context.args[1].lower().strip() in ["yes", "y", "1", "true"]

#    m = await eor(update, context, text="ᴄᴀᴘᴛᴜʀɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ...")

#    try:
#        photo = await take_screenshot(url, full)
#        if not photo:
#            return await m.edit("ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.")

#        m = await m.edit("ᴜᴘʟᴏᴀᴅɪɴɢ...")

#        if not full:
#            await update.message.reply_document(photo)
#        else:
#            await update.message.reply_document(photo)
#        await m.delete()
#    except Exception as e:
#        await m.edit(str(e))

#take_ss_handler = CommandHandler(["webss", "ss", "webshot"], take_ss, block=False)
#function(take_ss_handler)

#__help__ = """
#» /webss *:* Sᴇɴᴅs ᴛʜᴇ sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴜʀʟ.
#"""
#__mod_name__ = "Wᴇʙsʜᴏᴛ"
