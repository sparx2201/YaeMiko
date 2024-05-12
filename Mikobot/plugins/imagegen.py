import asyncio
import aiohttp
from telethon import events

from Mikobot import tbot as client

BASE_URL = "https://lexica.qewertyy.dev"
SESSION_HEADERS = {"Host": "lexica.qewertyy.dev"}

class AsyncClient:
    def __init__(self):
        self.url = BASE_URL
        self.session = aiohttp.ClientSession()

    async def generate(self, model_id, prompt, negative_prompt=""):
        data = {
            "model_id": model_id,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_images": 1,
            "width": 256,
            "height": 256,
        }

        async with self.session.post(
            f"{self.url}/models/inference", data=data, headers=SESSION_HEADERS
        ) as resp:
            return await resp.json()

    async def get_images(self, task_id, request_id):
        data = {"task_id": task_id, "request_id": request_id}

        async with self.session.post(
            f"{self.url}/models/inference/task", data=data, headers=SESSION_HEADERS
        ) as resp:
            return await resp.json()

    async def close(self):
        await self.session.close()

async def generate_image_handler(event, model_id):
    command_parts = event.text.split(" ", 1)

    if len(command_parts) < 2:
        await event.reply("Please provide a prompt.")
        return

    prompt = command_parts[1]
    negative_prompt = ""

    reply_message = await event.reply("Generating your image...")

    client = AsyncClient()

    tasks = []

    response = await client.generate(model_id, prompt, negative_prompt)
    task_id = response["task_id"]
    request_id = response["request_id"]

    tasks.append(asyncio.create_task(client.get_images(task_id, request_id)))

    timeout_seconds = 180

    while True:
        done, _ = await asyncio.wait(tasks, timeout=180)

        for task in done:
            generated_images = task.result()

            if "img_urls" in generated_images:
                for img_url in generated_images["img_urls"]:
                    await reply_message.delete()
                    await event.reply(file=img_url)
                break

            if timeout_seconds <= 0:
                await reply_message.edit("Image generation timed out.")
                break

            timeout_seconds -= 180

        if not tasks:
            break

    await client.close()

@client.on(events.NewMessage(pattern=r"/create"))
async def creative_handler(event):
    await generate_image_handler(event, model_id=16)
