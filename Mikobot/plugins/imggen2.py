# Credits: 
# @MyselfShuyaa
# @Not_Coding
# @SIAmKira
# @botsupportx

import html
import requests
import time
import os
from pyrogram import filters
from Mikobot import app
from Mikobot.plugins.disable import DisableAbleCommandHandler
from Mikobot import dispatcher
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from telegram import User
from telegram.constants import ParseMode
from telegram.helpers import mention_html

blacklisted_words = [
"Pornography",
"Nude",
"Naked",
"Explicit",
"XXX",
"Sex",
"Erotic",
"Obscene",
"Hardcore",
"NSFW",
"Sexual",
"Intimate",
"Sensual",
"Racy",
"Provocative",
"Lewd",
"Indecent",
"Steamy",
"Vulgar",
"Salacious",
"Naughty",
"Titillating",
"X-rated",
"Suggestive",
"Raunchy",
"Carnal",
"Prurient",
"Dirty",
"Smutty",
"Filthy",
"Nudity",
"Undressed",
"Exposed",
"Unclad",
"Bare",
"Flesh",
"Eroticized",
"Kinky",
"Fetish",
"Perversion",
"Taboo",
"Deviant",
"Degenerate",
"Debauchery",
"Libertine",
"Whore",
"Slut",
"Prostitute",
"Escort",
"Brothel",
"Pimp",
"Orgy",
"Threesome",
"Gangbang",
"Swinger",
"Voyeur",
"Exhibitionist",
"Masturbation",
"Spank",
"BDSM",
"Bondage",
"Discipline",
"Submission",
"Sadism",
"Masochism",
"Fornication",
"Copulation",
"Intercourse",
"Coitus",
"Penetration",
"Ejaculation",
"Sperm",
"Cum",
"Oral",
"Blowjob",
"Cunnilingus",
"Anal",
"Butt",
"Ass",
"Tits",
"Boobs",
"Breasts",
"Genitals",
"Vagina",
"Vulva",
"Clitoris",
"Penis",
"Testicles",
"Scrotum",
"Labia",
"Anus",
"Buttocks",
"Pubic",
"fucking", "fucked",
]

# Command handler for /generate
#@app.on_message(filters.command('create'))
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    # Extract the Message object from the Update object
    message = update.message

    # Get the user who sent the command
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user = await context.bot.get_chat_member(message.chat_id, user_id)
    else:
        user = await context.bot.get_chat_member(message.chat_id, message.from_user.id)
    
    # Get the prompt from the command
    prompt = ' '.join(message.text.split()[1:])

    # Check if the prompt contains any blacklisted words
    if any(word.lower() in prompt.lower() for word in blacklisted_words):
        await message.reply_text("Warning: Your prompt contains a blacklisted word.")
        return

    # Send a message to inform the user to wait
    wait_message = await message.reply_text("Generating your image...")

    # API endpoint URL
    url = 'https://ai-api.magicstudio.com/api/ai-art-generator'

    # Form data for the API request
    form_data = {
        'prompt': prompt,
        'output_format': 'bytes',
        'request_timestamp': str(int(time.time())),
        'user_is_subscribed': 'false',
    }

    # Send the API request
    try:
        response = requests.post(url, data=form_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error: Prompt missing")
        await wait_message.delete()
        return

    # Get the generated image from the API response
    image_bytes = response.content

    # Save the generated image to a file
    file_name = f"img_gen_byJinx.png"
    file_path = os.path.join("generated_images", file_name)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    # Send the generated image to the user with a caption
    caption = f"*Generated By* : {user.user.mention_html(user.id, user.first_name)} \n*Powered By* : @JinX_UBot\n*Prompt* : ``{prompt}``"
#
    try:
        await context.bot.send_photo(chat_id=message.chat_id, photo=file_path, caption=caption, parse_mode=ParseMode.HTML)
    except BadRequest as e:
        await message.reply_text(f"Error: Prompt missing")
        await wait_message.delete()
        return

    # Delete the wait message
    await wait_message.delete()
    
##########################################################3
GEN_HANDLER = DisableAbleCommandHandler("create", generate_image, block=False)
dispatcher.add_handler(GEN_HANDLER)
