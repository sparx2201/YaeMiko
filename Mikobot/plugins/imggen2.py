# Credits: 
# @MyselfShuyaa
# @Not_Coding
# @SIAmKira
# @botsupportx


import requests
import time
import os
from pyrogram import filters
from Mikobot import app

# Command handler for /generate
@app.on_message(filters.command('create'))
async def generate_image(client, message):
    # Get the prompt from the command
    prompt = ' '.join(message.command[1:])

    # Send a message to inform the user to wait
    wait_message = await message.reply_text("Generating your image...")
    StartTime = time.time()


    # API endpoint URL
    url = 'https://ai-api.magicstudio.com/api/ai-art-generator'

    # Form data for the request
    form_data = {
        'prompt': prompt,
        'output_format': 'bytes',
        'request_timestamp': str(int(time.time())),
        'user_is_subscribed': 'false',
    }

    # Send a POST request to the API
    response = requests.post(url, data=form_data)

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
                await message.reply_document(destination_path, caption=f"Here's the generated image!\nTime Taken: {prompt}")

                # Delete the generated image after sending
                os.remove(destination_path)
            else:
                await wait_message.edit_text("Failed to generate the image.")
        except Exception as e:
            await wait_message.edit_text("Error: {}".format(e))
    else:
        await wait_message.edit_text("Error: {}".format(response.status_code))
