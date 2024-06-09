
# <============================================== IMPORTS =========================================================>
import asyncio

from pyrogram import filters

from Database.mongodb.karma_mongo import *
from Mikobot import OWNER_ID, app
from Mikobot.utils.can_restrict import can_restrict
from Mikobot.utils.errors import capture_err

# <=======================================================================================================>

karma_positive_group = 3
karma_negative_group = 4


# <================================================ FUNCTION =======================================================>
@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(
        r"^(\+|\+\+|\+\+\+|\+\+\+\+|\+\+\+\+\+|thnx|\+1|thx|tnx|ty|tq|thank you|thanx|thanks|pro|cool|good|agree|makasih|Thnx|Thx|Tnx|Ty|Tq|Thank you|Thanx|Thanks|Pro|Cool|Good|Agree|Makasih|👍|👍👍|👍👍👍|❤️|❤️❤️|❤️❤️❤️|Arigatou gozaimasu|Arigatou Gozaimasu|arigatou gozaimasu|Arigatou|arigatou|spaseebah|SpaSeeBah|Spaseebah|\+\+ .+)$"
    )
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
@capture_err
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    reply_user = message.reply_to_message.from_user
    current_user = message.from_user
    if not (reply_user and current_user):
        return
    if reply_user.id == OWNER_ID:
        await message.reply_text("Wᴇʟʟ! ᴛʜᴀᴛ's ᴍʏ ᴍᴀɴ ᴀɴᴅ ʜᴇ's ᴀʟᴡᴀʏs ʀɪɢʜᴛ ✨ ")
        return
    if reply_user.id == current_user.id:
        return

    chat_id = message.chat.id
    user_id = reply_user.id
    user_mention = reply_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    karma = current_karma["karma"] + 1 if current_karma else 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Iɴᴄʀᴇᴍᴇɴᴛᴇᴅ Kᴀʀᴍᴀ ᴏғ\n{user_mention} ʙʏ 1\n\n**✨ Tᴏᴛᴀʟ Pᴏɪɴᴛs :** {karma}"
    )


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(r"^(-|--|-1|not cool|disagree|worst|bad|Not Cool|Not cool|Disagree|Worst|Bad|👎|👎👎|👎👎👎|-- .+)$")
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
@capture_err
async def downvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    reply_user = message.reply_to_message.from_user
    current_user = message.from_user
    if not (reply_user and current_user):
        return
    if reply_user.id == OWNER_ID:
        await message.reply_text("I know him, so I'm not gonna do that, baby.")
        return
    if reply_user.id == current_user.id:
        return

    user_id = reply_user.id
    user_mention = reply_user.mention
    current_karma = await get_karma(message.chat.id, await int_to_alpha(user_id))
    karma = current_karma["karma"] - 1 if current_karma else 0
    new_karma = {"karma": karma}
    await update_karma(message.chat.id, await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Dᴇᴄʀᴇᴍᴇɴᴛᴇᴅ Kᴀʀᴍᴀ ᴏғ\n{user_mention} ʙʏ 1\n\n**✨ Tᴏᴛᴀʟ Pᴏɪɴᴛs :** {karma}"
    )


@app.on_message(filters.command("karmastat") & filters.group)
@capture_err
async def karma(_, message):
    if not message.reply_to_message:
        m = await message.reply_text("Analyzing karma... This may take a while.")
        karma = await get_karmas(message.chat.id)
        if not karma:
            await m.edit_text("No karma in the database for this chat.")
            return
        msg = f"**🎖 Karma List of {message.chat.title} :**\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True)
            )
        if not karma_dicc:
            await m.edit_text("No karma in the database for this chat.")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await _.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            msg += f"`{karma_count}`  {(first_name[0:12] + '...') if len(first_name) > 12 else first_name}\n"
            limit += 1
        await m.edit_text(msg)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(message.chat.id, await int_to_alpha(user_id))
        karma = karma["karma"] if karma else 0
        await message.reply_text(f"**✨ Tᴏᴛᴀʟ Pᴏɪɴᴛs:** {karma}")


@app.on_message(filters.command("karma"))
@can_restrict
async def karma_toggle_xd(_, message):
    usage = "**Usage:**\n/karma [ON|OFF]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip().lower()

    if state == "on":
        disabled = karmadb.find_one({"chat_id_toggle": chat_id})
        if disabled:
            karmadb.delete_one({"chat_id_toggle": chat_id})
            await message.reply_text("Enabled the Karma System.")
        else:
            await message.reply_text("Karma System is already enabled.")
    elif state == "off":
        disabled = karmadb.find_one({"chat_id_toggle": chat_id})
        if disabled:
            await message.reply_text("Karma System is already disabled.")
        else:
            karmadb.insert_one({"chat_id_toggle": chat_id})
            await message.reply_text("Disabled the Karma System.")
    else:
        await message.reply_text(usage)


# <=================================================== HELP ====================================================>


__mod_name__ = "Kᴀʀᴍᴀ"
__help__ = """

❍ *Uᴘᴠᴏᴛᴇ* -  ᴜsᴇ ᴜᴘᴠᴏᴛᴇ ᴋᴇʏᴡᴏʀᴅs 
ʟɪᴋᴇ "+", "+1", "Thanks", ᴇᴛᴄ. ᴛᴏ ᴜᴘᴠᴏᴛᴇ ᴀ ᴍᴇssᴀɢᴇ.

❍ *Dᴏᴡɴᴠᴏᴛᴇ* - ᴜsᴇ ᴅᴏᴡɴᴠᴏᴛᴇ ᴋᴇʏᴡᴏʀᴅs 
ʟɪᴋᴇ "-", "-1", ᴇᴛᴄ. ᴛᴏ ᴅᴏᴡɴᴠᴏᴛᴇ ᴀ ᴍᴇssᴀɢᴇ.

*Commands*

▸ /karmastat:- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴀᴛ ᴜsᴇʀ's  ᴋᴀʀᴍᴀ ᴘᴏɪɴᴛs

▸ /karmastat:- sᴇɴᴅ ᴡɪᴛʜᴏᴜᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴋᴀʀᴍᴀ ᴘᴏɪɴᴛ ʟɪsᴛ ᴏғ ᴛᴏᴘ 10

▸ /karma [off|on] - ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴋᴀʀᴍᴀ sʏsᴛᴇᴍ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
"""
# <================================================ END =======================================================>
