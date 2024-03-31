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
       "https://graph.org/file/c10e465f7d3373260ba24.mp4",
       "https://graph.org/file/264868629a93976c6f552.mp4",
       "https://graph.org/file/c224bd65cdd029853dc64.mp4",
       "https://graph.org/file/b7d566bc89568f76ae8a6.mp4",
       "https://graph.org/file/9ac63bf5f2775ecac0081.mp4",
       "https://graph.org/file/6f0afd144edacfae3ec80.mp4",
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
    ],
]

ALIVE_BTN = [
    [
       ib(text="Aᴅᴅ Mᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ib(text="Hᴇʟᴘ", url="https://t.me/{BOT_USERNAME}?start=help"),
    ]
]

HELP_STRINGS = """
×───   *𝘑𝘪𝘯𝙓*   ───×

Mᴀɪɴ Cᴏᴍᴍᴀɴᴅs
‣ /start : sᴛᴀʀᴛs ᴍᴇ 
‣ /help : ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏʀ ɪɴꜰᴏ ᴀʙᴏᴜᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴍᴏᴅᴜʟᴇs ​"""
