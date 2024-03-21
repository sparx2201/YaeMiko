# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
    "https://graph.org/file/ef4ebe4f2e88d521678bb.jpg",
    "https://graph.org/file/5a792a93f1944f8dd64e9.jpg",
    "https://graph.org/file/5bfee7b85968dc552db68.jpg",
    "https://graph.org/file/ce3457d3fdbd17c3e015d.jpg",
]

HEY_IMG = "https://graph.org/file/99bee7df6e46e62a20fa4.jpg"

ALIVE_ANIMATION = [
    "https://telegra.ph//file/f9e2b9cdd9324fc39970a.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/c4c2759c5fc04cefd207a.mp4",
    "https://telegra.ph//file/b1fa6609b1c4807255927.mp4",
    "https://telegra.ph//file/f3c7147da6511fbe27c25.mp4",
    "https://telegra.ph//file/39071b73c02e3ff5945ca.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/6efdd8e28756bc2f6e53e.mp4",
]

FIRST_PART_TEXT = "*ʜᴇʏ* `{}` . . ."

PM_START_TEXT = "ɪ ᴀᴍ *𝘑𝘪𝘯𝙓* \n──────────────×\n ᴀ ᴍᴏꜱᴛ ᴘᴏᴡᴇʀꜰᴜʟ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ᴍᴏᴅᴜʟᴇꜱ ᴀɴᴅ ꜰᴇᴀᴛᴜʀᴇs\n────────────────────────×\nɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ᴡʜɪᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪɴᴛᴏ ꜱʜᴀᴘᴇ ꜱᴏ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴏᴍᴍᴀɴᴅ, ᴀɴᴅ ʟᴇᴛꜱ ɢᴇᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪɴ ʟɪɴᴇ."

START_BTN = [
    [
        InlineKeyboardButton(
            text="Aᴅᴅ Mᴇ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="Aʙᴏᴜᴛ", callback_data="Miko_"),
        InlineKeyboardButton(text="Aɪ", callback_data="ai_handler"),
       ],
    [
        InlineKeyboardButton(text="Cᴏᴍᴍᴀɴᴅs", callback_data="help_back"),
    ],
]

GROUP_START_BTN = [
    [
        InlineKeyboardButton(text="Aᴅᴅ Mᴇ",url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
]

ALIVE_BTN = [
    [
        InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="Hᴇʟᴘ", callback_data="help_back"),
    ],
    [
        ib(
            text="Aᴅᴅ Mᴇ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """×─── *𝘑𝘪𝘯*𝙓 ───×\nMᴀɪɴ Cᴏᴍᴍᴀɴᴅs\n ‣ /start : sᴛᴀʀᴛꜱ ᴍᴇ \n ‣ /help : ​🇹​​🇴​ ​🇬​​🇪​​🇹​ ​🇭​​🇪​​🇱​​🇵​ ​🇴​​🇷​ ​🇮​​🇳​​🇫​​🇴​ ​🇦​​🇧​​🇴​​🇺​​🇹​ ​🇦​​🇱​​🇱​ ​🇨​​🇴​​🇲​​🇲​​🇦​​🇳​​🇩​​🇸​ ​🇦​​🇳​​🇩​ ​🇲​​🇴​​🇩​​🇺​​🇱​​🇪​​🇸​"""
