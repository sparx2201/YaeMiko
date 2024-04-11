# <============================================== IMPORTS =========================================================>
import html
import random
from datetime import datetime

import humanize
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, MessageHandler, filters

from Database.sql import afk_sql as sql
from Mikobot import LOGGER, function
from Mikobot.plugins.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from Mikobot.plugins.users import get_user_id

# <=======================================================================================================>

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


# <================================================ FUNCTION =======================================================>
async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text:
        args = update.effective_message.text.split(None, 1)
    else:
        return
    user = update.effective_user

    if not user:  # ignore channels
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    try:
        if reason:
            await update.effective_message.reply_text(
                f" {fname} ɪs ɴᴏᴡ ᴀᴡᴀʏ!",
                parse_mode="html",
            )
        else:
            await update.effective_message.reply_text(
                " {} ɪs ɴᴏᴡ ᴀᴡᴀʏ!{}".format(fname, notice),
            )
    except BadRequest:
        pass


async def no_longer_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    if sql.is_afk(user.id):
        afk_user = sql.check_afk_status(user.id)

        time = humanize.naturaldelta(datetime.now() - afk_user.time)

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                " {} ɪs ʜᴇʀᴇ!",
                " {} ɪs ʙᴀᴄᴋ!",
                " {} ɪs ɴᴏᴡ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ!",
                " {} ɪs ᴀᴡᴀᴋᴇ!",
                " {} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!",
                " {} ɪs ғɪɴᴀʟʟʏ ʜᴇʀᴇ!",
                " Wᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ! {}",
            ]
            chosen_option = random.choice(options)
            await update.effective_message.reply_text(
                chosen_option.format(firstname)
                + f"\nYᴏᴜ ᴡᴇʀᴇ Aғᴋ ғᴏʀ: {time}",
                parse_mode="html",
            )
        except:
            return


async def reply_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = await get_user_id(
                message.text[ent.offset : ent.offset + ent.length],
            )
            if not user_id:
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = await bot.get_chat(user_id)
            except BadRequest:
                LOGGER.error(
                    "Error: Could not fetch userid {} for AFK module".format(user_id)
                )
                return
            fst_name = chat.first_name

            await check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        await check_afk(update, context, user_id, fst_name, userc_id)


async def check_afk(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    fst_name: str,
    userc_id: int,
):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)

        if int(userc_id) == int(user_id):
            return

        time = humanize.naturaldelta(datetime.now() - user.time)

        if not user.reason:
            res = "{} ɪs Aғᴋ.\nSɪɴᴄᴇ: {}.".format(
                fst_name,
                time,
            )
            await update.effective_message.reply_text(res)
        else:
            res = (
                "{} ɪs Aғᴋ.\nSɪɴᴄᴇ: {}\nRᴇᴀsᴏɴ: {}".format(
                    html.escape(fst_name),
                    time, 
                    html.escape(user.reason),
                )
            )
            await update.effective_message.reply_text(res, parse_mode="html")


# <=================================================== HELP ====================================================>


__help__ = """
‣ /afk, brb, !afk <reason>*:* ᴍᴀʀᴋ ʏᴏᴜʀsᴇʟғ ᴀs Aғᴋ (ᴀᴡᴀʏ ғʀᴏᴍ ᴋᴇʏʙᴏᴀʀᴅ).

Wʜᴇɴ ᴍᴀʀᴋᴇᴅ ᴀs Aғᴋ, ᴀɴʏ ᴍᴇɴᴛɪᴏɴs ᴡɪʟʟ ʙᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴡɪᴛʜ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴀʏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ!
"""

# <================================================ HANDLER =======================================================>
AFK_HANDLER = DisableAbleCommandHandler("afk", afk, block=False)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    filters.Regex(r"^(?i:(brb|!afk))( .*)?$"), afk, friendly="afk", block=False
)
NO_AFK_HANDLER = MessageHandler(
    filters.ALL & filters.ChatType.GROUPS, no_longer_afk, block=False
)
AFK_REPLY_HANDLER = MessageHandler(
    filters.ALL & filters.ChatType.GROUPS, reply_afk, block=False
)

function(AFK_HANDLER, AFK_GROUP)
function(AFK_REGEX_HANDLER, AFK_GROUP)
function(NO_AFK_HANDLER, AFK_GROUP)
function(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "Aғᴋ"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
# <================================================ END =======================================================>
