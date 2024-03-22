# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
    "https://graph.org/file/eacb152f1a9eff5b3e8ea.jpg",
    "https://graph.org/file/fba874b54ab87ed311aee.jpg",
    "https://graph.org/file/8b5aa3635bf0f615f1f8f.jpg",
    "https://graph.org/file/27b34bf275913b0e77dbc.jpg",
    "https://graph.org/file/aaff4b671ea8fb10ab886.jpg",

]

HEY_IMG = "https://graph.org/file/eacb152f1a9eff5b3e8ea.jpg"

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
        ib(text="Sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
        ib(text="Hᴇʟᴘ", callback_data="help_back"),
    ],
    [
        ib(
            text="Aᴅᴅ Mᴇ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """
×───   *𝘑𝘪𝘯𝙓*   ───×

Mᴀɪɴ Cᴏᴍᴍᴀɴᴅs
‣ /start : sᴛᴀʀᴛs ᴍᴇ 
‣ /help : ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏʀ ɪɴꜰᴏ ᴀʙᴏᴜᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴍᴏᴅᴜʟᴇs ​"""
