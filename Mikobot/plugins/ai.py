# CREATED BY: https://t.me/O_oKarma
# API CREDITS: @Qewertyy
# PROVIDED BY: https://github.com/Team-ProjectCodeX

# <============================================== IMPORTS =========================================================>
import base64
import re
import logging 
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from Mikobot import LOGGER as logger
from Mikobot import function
from Mikobot.state import state

# <=======================================================================================================>

# <================================================ CONSTANTS =====================================================>
API_URL = "https://lexica.qewertyy.dev/models"
PALM_MODEL_ID = 0
GPT_MODEL_ID = 5

# <================================================ FUNCTIONS =====================================================>


async def get_api_response(model_id, api_params, api_url):
    try:
        response = await state.post(api_url, params=api_params)
        if response.status_code == 200:
            data = response.json()
            return data.get(
                "content", f"Error: Empty response received from the {model_id} API."
            )
        else:
            return f"Error: Request failed with status code {response.status_code}."
    except state.RequestError as e:
        return f"Error: An error occurred while calling the {model_id} API. {e}"


async def palm_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: Missing input text after /palm command.",
        )
        return

    input_text = " ".join(args)

    result_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="🌴"
    )

    api_params = {"model_id": PALM_MODEL_ID, "prompt": input_text}
    api_response = await get_api_response("PALM", api_params, API_URL)

    await result_msg.delete()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=api_response)



async def gpt_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the message text starts with "Jinx" (case insensitive)
    if update.message.text.lower().startswith("jinx"):
        # Extract the text after "Jinx"
        input_text = update.message.text[len("Jinx"):].strip()
        context.args = input_text.split()  # Update context.args with the extracted text as arguments
        await ask(update, context)  # Call the ask function (or your equivalent) with modified arguments
    else:
        # If "Jinx" is not at the start of the message text, proceed with normal GPT processing
        args = context.args
        input_text = " ".join(args)

        if not args:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Error: Missing input text after /ask command.",
            )
            return

        result_msg = await context.bot.send_message(
            chat_id=update.effective_chat.id, text="💬"
        )

        api_params = {"model_id": GPT_MODEL_ID, "prompt": input_text}
        api_response = await get_api_response("GPT", api_params, API_URL)

        await result_msg.delete()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=api_response)


# Define the upscale_image function
async def upscale_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Check if the replied message contains a photo
        if update.message.reply_to_message and update.message.reply_to_message.photo:
            # Send a message indicating upscaling is in progress
            progress_msg = await update.message.reply_text(
                "Upscaling your image, please wait..."
            )

            # Access the image file_id from the replied message
            image = await update.message.reply_to_message.photo[-1].get_file()

            # Download the image and save it
            image_path = await image.download_to_drive()

            with open(image_path, "rb") as image_file:
                f = image_file.read()

            b = base64.b64encode(f).decode("utf-8")

            response = await state.post(
                "https://lexica.qewertyy.dev/upscale",
                data={"image_data": b},
            )

            # Save the upscaled image
            upscaled_file_path = "upscaled_image.png"
            with open(upscaled_file_path, "wb") as output_file:
                output_file.write(response.content)

            # Delete the progress message
            await context.bot.delete_message(
                chat_id=update.message.chat_id, message_id=progress_msg.message_id
            )

            # Send the upscaled image as a PNG file
            await update.message.reply_document(
                document=open(upscaled_file_path, "rb"),
                caption=f"<b>Upscaled your image.</b>\n<b>Generated By:</b> @{context.bot.username}",
                parse_mode=ParseMode.HTML,
            )
        else:
            await update.message.reply_text("Please reply to an image to upscale it.")

    except Exception as e:
        logger.error(f"Failed to upscale the image: {e}")
        await update.message.reply_text(
            "Failed to upscale the image. Please try again later."
        )


# <================================================ HANDLER =======================================================>
# Register the upscale_image command handler
function(CommandHandler("upscale", upscale_image, block=False))
function(CommandHandler("palm", palm_chatbot, block=False))
function(CommandHandler("ask", gpt_chatbot, block=False))
# <================================================ END =======================================================>
