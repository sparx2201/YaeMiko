# Credits: 
# @MyselfShuyaa
# @Not_Coding
# @SIAmKira
# @botsupportx





import requests
import time
import os
from Mikobot.utils.can_restrict import can_restrict
from pyrogram import filters
from Mikobot import app
from Mikobot.plugins.disable import DisableAbleCommandHandler
from Mikobot import dispatcher
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from Mikobot import BOT_USERNAME
from Database.mongodb.toggle_mongo import is_create_on, create_on, create_off
#"Sex",
#"Sexual",

blacklisted_words = [
"Pornography",
"Nude",
"Naked",
"Explicit",
"XXX",
"Erotic",
"Obscene",
"Hardcore",
"NSFW",
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
"fucking", "fucked", "pussy",]



# Command handler for /generate
@app.on_message(filters.command('create'))
async def generate_image(client, message):
#async def generate_image(client, update: Update, context: ContextTypes.DEFAULT_TYPE):
   # message = update.effective_message  # Extract the Message object from the CallbackContext object
    
    if not await is_create_on(message.chat.id):
        await message.reply_text("Create Command is Disabled in this chat\nUse '/createMode on' to enable it")
        return
    
    #if message.reply_to_message:
       # user_id = message.reply_to_message.from_user.id
       # user = await client.get_users(user_id)
   # else:
        # If it's not a reply, use the sender of the command
    user = await client.get_users(message.from_user.id)
        
    # Get the prompt from the command
    prompt = ' '.join(message.command[1:])

    if any(word.lower() in prompt.lower() for word in blacklisted_words):
        await message.reply_text("Warning: Your prompt contains a blacklisted useless word.")
        return

    # Send a message to inform the user to wait
    wait_message = await message.reply_text("Generating your image...")
    StartTime = time.time()


    # API endpoint URL
#    url = 'https://ai-api.magicstudio.com/api/ai-art-generator'

    # Form data for the request
 #   form_data = {
  #      'prompt': prompt,
  #      'output_format': 'bytes',
  #      'request_timestamp': str(int(time.time())),
  #      'user_is_subscribed': 'false',
   # }

    # Send a POST request to the API
    #response = requests.post(url, data=form_data)

    url = 'https://fumes-api.onrender.com/sdxl-api'
    payload = {'prompt': 'car',
            "apply_watermark": False,
            "negative_prompt": '',
            "image": None,
            "mask": None,
            "width": 1024,
            "height": 1024,
            "num_outputs": 1,
            "scheduler": 'DDIM',
            "num_inference_steps": 40,
            "guidance_scale": 8,
            "prompt_strength": 0.8,
            "seed": 69,
            "refine": "no_refiner",
            "high_noise_frac": 1,
            "refine_steps": None,}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        try:
            if response.content:
                destination_dir = ''
                destination_path = os.path.join(destination_dir, 'img_gen_byJinx.jpg')

                # Save the image to the destination path
                with open(destination_path, 'wb') as f:
                    f.write(response.content)

                # Delete the wait message
                await wait_message.delete()

                # Send the generated image
             
                await message.reply_photo(destination_path, caption=f"**Generated By** : {user.mention()}\n**Powered By** : @JinX_UBot\n**Prompt** : `{prompt}`")
                await message.delete()

                # Delete the generated image after sending
                os.remove(destination_path)
            else:
                await wait_message.edit_text("Failed to generate the image.")
        except Exception as e:
            await wait_message.edit_text("Error: {}".format(e))
    else:
        await wait_message.edit_text("Error: bruhhh prompt?")

########################################################################################################

@app.on_message(
    filters.command(["createMode", f"createMode@{BOT_USERNAME}"]) & ~filters.private
)
@can_restrict
async def create_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("Use /createMode [on/off] to enable or disable create command\n")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status in ("on", "yes"):
        if await is_create_on(chat_id):
            await message.reply_text("**Create Mode is already enabled!**\nUse '/create' to Generate Image")
            return
        await create_on(chat_id)
        await message.reply_text("**Enabled Create Mode!**\nNow anyone can use '/create' to \nGenerate Image")
            
    elif status in ("off", "no"):
        if not await is_create_on(chat_id):
            await message.reply_text("**Create Mode is already Disabled!**\nCan't use '/create' to Generate Image")
            return
            
        await create_off(chat_id)
        await message.reply_text("**Disabled Create Mode!**\nNow no-one can use '/create' to \nGenerate Image")
    else:
        await message.reply_text("Use /createMode [on/off] to enable or disable create command \nand Use '/create' to Generate Image")
