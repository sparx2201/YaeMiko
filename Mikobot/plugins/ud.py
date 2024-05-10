import requests
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from Mikobot import dispatcher
from Mikobot.plugins.disable import DisableAbleCommandHandler

import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram.helpers import mention_html

import Database.sql.approve_sql as sql
from Mikobot import DRAGONS, dispatcher

from Mikobot.plugins.helper_funcs.chat_status import check_admin
from Mikobot.plugins.helper_funcs.extraction import extract_user
from Mikobot.plugins.log_channel import loggable


async def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len("/ud ") :]
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    await message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


UD_HANDLER = DisableAbleCommandHandler("ud", ud, block=False)

dispatcher.add_handler(UD_HANDLER)

__help__ = """
» /ud (text) *:* sᴇᴀʀᴄʜs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴜʀʙᴀɴ ᴅɪᴄᴛɪᴏɴᴀʀʏ ᴀɴᴅ sᴇɴᴅs ʏᴏᴜ ᴛʜᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
"""
__mod_name__ = "Uʀʙᴀɴ"

__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]
