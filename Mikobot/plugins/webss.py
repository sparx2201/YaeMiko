from inspect import getfullargspec
from io import BytesIO
from telegram import Message, Update, User
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from Mikobot import tbot as app
from Mikobot import aiohttpsession as session
from Mikobot import dispatcher

async def post(url: str, *args, **kwargs):
    async with session.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

async def take_screenshot(url: str, full: bool = False):
    url = url if url.startswith("http") else f"https://{url}"
    payload = {
        "url": url,
        "width": 1920,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(
        "https://webscreenshot.vercel.app/api",
        data=payload,
    )
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file

def get_reply_to(message: Message):
    try:
        return message.reply_to_message.message_id
    except AttributeError:
        try:
            return message.reply_to_message_id
        except AttributeError:
            return None

async def eor(msg: Message, **kwargs):
    reply_to = get_reply_to(msg)

    func = (
        (msg.edit_text if reply_to == msg else msg.reply_text)
        if msg.from_user
        else msg.reply_text
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

async def take_ss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None:
        return

    ctx_args = context.args
    if len(ctx_args) < 1:
        return await eor(message, text="ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.")

    if len(ctx_args) == 1:
        url = ctx_args[0]
        full = False
    elif len(ctx_args) == 2:
        url = ctx_args[0]
        full = ctx_args[1].lower().strip() in ["yes", "y", "1", "true"]
    else:
        return await eor(message, text="ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ.")

    m = await eor(message, text="ᴄᴀᴘᴛᴜʀɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ...")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.")

        m = await m.edit("ᴜᴘʟᴏᴀᴅɪɴɢ...")

        await message.reply_document(photo)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))

dispatcher.add_handler(CommandHandler(["webss", "ss", "webshot"], take_ss, block=False))



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
