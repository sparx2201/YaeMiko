
# Created by : AJ
# @JinX_Ubot

# ============================================== IMPORTS =========================================================
from os import remove

from pyrogram import filters

from Database.mongodb.toggle_mongo import is_nsfw_on, nsfw_off, nsfw_on, nsfw_warn_on, nsfw_warn_off, is_nsfw_warn_on
from Mikobot import BOT_USERNAME, DRAGONS, app
from Mikobot.state import arq
from Mikobot.utils.can_restrict import can_restrict
from Mikobot.utils.errors import capture_err

# =================================================== Fuction ====================================================

##########################################(basic)##############################

async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id

##########################################(Auto Detect for Anti-Nsfw)###########################

@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
@capture_err
async def detect_nsfw(_, message):
    if not await is_nsfw_on(message.chat.id):
        return
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await _.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if message.from_user.id in DRAGONS:
        return
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
───────────────────
⚠️ **NSFW Image Detected & 
 Deleted  Successfully!**
────────────────
 **User** : {message.from_user.mention} [{message.from_user.id}]
┈┈┈┈┈┈┈┈┈┈┈┈┈┈
▸ __Safe__ : `{results.neutral} %`
▸ __Porn__ : `{results.porn} %`
▸ __Hentai__ : `{results.hentai} %`
▸ __Sexy__ : `{results.sexy} %`
▸ __Drawings__ : `{results.drawings} %`
────────────────────
"""
    )

##########################################(Anti-Nsfw)#####################################

@app.on_message(
    filters.command(["antinsfw", f"antinsfw@{BOT_USERNAME}"]) & ~filters.private
)
@can_restrict
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("Lol! Use /antinsfw [on/off] Bruhh")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status in ("on", "yes"):
        if await is_nsfw_on(chat_id):
            await message.reply_text("**AntiNsfw is already enabled!**\nʜɪʜɪ ᴀɴᴅ ᴡᴏʀᴋɪɴɢ Pʀᴏᴘᴇʀʟʏ sᴏ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ")
            return
        await nsfw_on(chat_id)
        await message.reply_text("**Enabled AntiNsfw System!**\n\nNᴏᴡ I ᴡɪʟʟ Dᴇᴛᴇᴄᴛ ᴀɴᴅ Dᴇʟᴇᴛᴇ Nsғᴡ \nCᴏɴᴛᴇɴᴛ sᴏ ɴᴏ-ᴏɴᴇ ᴄᴀɴ ʙᴇᴄᴏᴍᴇ \nᴍᴏʀᴇ ʙᴀᴅ ᴛʜᴀɴ ᴍᴇ")
            
    elif status in ("off", "no"):
        if not await is_nsfw_on(chat_id):
            await message.reply_text("**AntiNsfw is already Disabled!**\nsᴏ ᴡʜᴏʟᴇ ᴄʜᴀᴛ ғʀᴇᴇ ᴛᴏ sᴇɴᴅ ᴀɴʏᴛʜɪɴɢ")
            return
            
        await nsfw_off(chat_id)
        await message.reply_text("**Disabled AntiNSFW System!**\nʙᴛᴡ ɪᴛ's ʙᴀᴅ ᴍᴀɴɴᴇʀs ɴᴏᴡ ᴄʜᴀᴛ \nɪs ғʀᴇᴇ ғʀᴏᴍ ᴍʏ ʜᴀɴᴅs ɴᴏᴡ")
    else:
        await message.reply_text("Lol! Only Use /antinsfw [on/off] Bruhh")


###########################################(scan)######################################

@app.on_message(filters.command(["nsfwscan", f"nsfwscan@{BOT_USERNAME}"]))
@capture_err
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    m = await message.reply_text("Scanning")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Something wrong happened.")
    file = await _.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
────────────────
 **Scan Sucessefully!**
──────────────
▸ __Neutral__ : `{results.neutral} %`
▸ __Porn__ : `{results.porn} %`
▸ __Hentai__ : `{results.hentai} %`
▸ __Sexy__ : `{results.sexy} %`
▸ __Drawings__ : `{results.drawings} %`
┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 **NSFW** : `{results.is_nsfw}`
───────────────
"""
    )
    
##########################################(Anti-Nsfw + Warn)####################################

# @app.on_message(
#     filters.command(["warnnsfw", f"warnnsfw@{BOT_USERNAME}"]) & ~filters.private
# )
# @can_restrict
# async def nsfw_warn_enable_disable(_, message):
#     
#     if not await is_nsfw_on(message.chat.id):
#         await message.reply_text("Enable Antinsfw System First!")
#         return
#     
#     if len(message.command) != 2:
#         await message.reply_text("Usage: /warnnsfw [on/off]")
#         return
#     status = message.text.split(None, 1)[1].strip()
#     status = status.lower()
#     chat_id = message.chat.id
#     if status in ("on", "yes"):
#         if await is_nsfw_warn_on(chat_id):
#             await message.reply_text("Warn is already enabled on Nsfw content.")
#             return
#         await nsfw_warn_on(chat_id)
#         await message.reply_text("Enabled Warn System on Nsfw content.")
# 
#     
#     elif status in ("off", "no"):
#         if not await is_nsfw_warn_on(chat_id):
#             await message.reply_text("Warn is already disabled on Nsfw content.")
#             return
#         await nsfw_warn_off(chat_id)
#         await message.reply_text("Disabled Warn System on Nsfw content.")
#     else:
#         await message.reply_text("Unknown Suffix, Use /antinsfw [on/off]")




# =================================================== Help ====================================================


__mod_name__ = "Aɴᴛɪ-Nsғᴡ"

__help__ = """
*🔞 Dᴇᴛᴇᴄᴛ NSFW ᴍᴀᴛᴇʀɪᴀʟ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ɪᴛ ᴛᴏ 
     ᴘʀᴇᴠᴇɴᴛ Tʜᴇ Gʀᴏᴜᴘ ғʀᴏᴍ ɢᴇᴛᴛɪɴɢ ʙᴀɴɴᴇᴅ.*.

 *Commands:*

▸ /antinsfw [on/off]: Eɴᴀʙʟᴇs Aɴᴛɪ-Nsғᴡ sʏsᴛᴇᴍ.
   ᴛᴏ ᴀᴜᴛᴏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ Nsғᴡ (18+) Cᴏɴᴛᴇɴᴛ

▸ /nsfwscan <reply to message>: Sᴄᴀɴs ᴛʜᴇ ғɪʟᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ.
"""
# =============================================== END =======================================================>
