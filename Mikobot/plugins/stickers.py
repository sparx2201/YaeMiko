import math
import os
import urllib.request as urllib
from html import escape
import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.helpers import mention_html

from Mikobot import dispatcher
from Mikobot.plugins.disable import CommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="

async def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
       await update.effective_message.reply_text(
            "Hey "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )


async def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        await msg.reply_text("Provide some name to search for pack.")
        return

    combot_stickers_url = "https://combot.org/telegram/stickers?q="
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, "html.parser")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")

    if not results:
        await msg.reply_text("No results found :(.")
        return

    reply = f"Stickers for *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    
    await msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

async def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id

    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = await bot.download_file(new_file.file_path, "sticker.png")
        await new_file.download("sticker.png")
        with open("sticker.png", "rb") as sticker_file:
            await bot.send_document(chat_id, document=sticker_file)
        os.remove("sticker.png")
    else:
        await update.effective_message.reply_text(
            "Please reply to a sticker for me to upload its PNG."
        )

async def kang(update: Update, context: CallbackContext):
    msg = update.effective_message
    user = update.effective_user
    packnum = 0
    packname = f"a{user.id}_by_{context.bot.username}"
    max_stickers = 120
    
    while packnum <= max_stickers:
        try:
            stickerset = await context.bot.get_sticker_set(packname)
            packnum = len(stickerset.stickers)
            if packnum >= max_stickers:
                packname = f"a{user.id}_{packnum+1}_by_{context.bot.username}"
        except BadRequest as e:
            if e.message == "Stickerset_invalid":
                break

    is_animated = False
    file_id = ""

    if msg.reply_to_message and msg.reply_to_message.sticker:
        sticker = msg.reply_to_message.sticker
        file_id = sticker.file_id
        is_animated = sticker.is_animated

    if not file_id:
        await msg.reply_text("Please reply to a sticker to kang it.")
        return

    kang_file = await context.bot.get_file(file_id)

    sticker_format = "static" if not is_animated else "animated"
    download_path = f"kangsticker.{sticker_format}"

    try:
        await kang_file.download_to_drive(download_path)
    except Exception as e:
        print(f"Error downloading sticker: {e}")
        await msg.reply_text("Failed to download the sticker.")
        return

    sticker_emoji = "🤔"  # Default emoji

    if msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
        sticker_emoji = msg.reply_to_message.sticker.emoji

    # Add sticker to set
    await context.bot.add_sticker_to_set(
        user_id=user.id,
        name=packname,
        sticker=open(download_path, "rb"),
    )

    await makepack_internal(
        update,
        context,
        msg,
        user,
        sticker_emoji,
        packname,
        packnum,
        download_path,
    )

    # Remove the temporary file
    try:
        if os.path.isfile(download_path):
            os.remove(download_path)
    except Exception as e:
        print(f"Error removing temporary file: {e}")

async def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    sticker_path,
):
    name = user.first_name[:50]
    extra_version = "" if packnum <= 0 else f" {packnum}"
    try:
        success = await context.bot.create_new_sticker_set(
            user_id=user.id,
            name=packname,
            title=f"{name}'s kang pack{extra_version}",
            stickers=[sticker_path],
        )
    except BadRequest as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            await msg.reply_text(
                f"Your pack can be found [here](t.me/addstickers/{packname})",
                parse_mode=ParseMode.MARKDOWN,
            )
        elif e.message in ("Peer_id_invalid", "bot was blocked by the user"):
            await msg.reply_text(
                "Contact me in PM first.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Start", url=f"t.me/{context.bot.username}")]]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            await msg.reply_text(
                f"Sticker pack successfully created. Get it [here](t.me/addstickers/{packname})",
                parse_mode=ParseMode.MARKDOWN,
            )
        return

    if success:
        await msg.reply_text(
            f"Sticker pack successfully created. Get it [here](t.me/addstickers/{packname})",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")



__help__ = """
 ❍ /stickerid*:* reply to a sticker to me to tell you its file ID.
 ❍ /getsticker*:* reply to a sticker to me to upload its raw PNG file.
 ❍ /kang*:* reply to a sticker to add it to your pack.
 ❍ /stickers*:* Find stickers for given term on combot sticker catalogue
"""

__mod_name__ = "Sᴛɪᴄᴋᴇʀ"

STICKERID_HANDLER = CommandHandler("stickerid", stickerid, )
GETSTICKER_HANDLER = CommandHandler("getsticker", getsticker, )
KANG_HANDLER = CommandHandler("kang", kang, )
STICKERS_HANDLER = CommandHandler("stickers", cb_sticker, )

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
