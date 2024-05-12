############################ (getText) #####################################

import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    
############################ (getText) #####################################
import httpx
from urllib.parse import urlsplit
#from .pastebins import nekobin
#from bot import TelegraphClient

def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.caption if message.caption else message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


################################### (paginate_models) ##############################################

from pyrogram.types import InlineKeyboardButton
from math import ceil

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_models(page_n: int, models: list,user_id) -> list:
    modules = sorted(
        [
            EqInlineKeyboardButton(
            x['name'],
            callback_data=f"d.{x['id']}.{user_id}"
                )
                for x in models
            ]
            )

    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 3

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "⬅️",
                    callback_data=f"d.left.{modulo_page}.{user_id}"
                ),
                EqInlineKeyboardButton(
                    "Cancel",
                    callback_data=f"d.-1.{user_id}"
                ),
                EqInlineKeyboardButton(
                    "➡️",
                    callback_data=f"d.right.{modulo_page}.{user_id}"
                ),
            )
        ]
    else:
        pairs += [[EqInlineKeyboardButton("Cancel", callback_data=f"d.-1.{user_id}")]]

    return pairs

###########################################  (ImageGeneration) ##########################################################
import asyncio,base64,mimetypes,os
from lexica import AsyncClient
from lexica.constants import languageModels

async def ImageGeneration(model,prompt):
    try:
        client = AsyncClient()
        output = await client.generate(model,prompt,"")
        if output['code'] != 1:
            return 2
        elif output['code'] == 69:
            return output['code']
        task_id, request_id = output['task_id'],output['request_id']
        await asyncio.sleep(20)
        tries = 0
        image_url = None
        resp = await client.getImages(task_id,request_id)
        while True:
            if resp['code'] == 2:
                image_url = resp['img_urls']
                break
            if tries > 15:
                break
            await asyncio.sleep(5)
            resp = await client.getImages(task_id,request_id)
            tries += 1
            continue
        return image_url
    except Exception as e:
        print(f"Failed to generate the image:",e)
    finally:
        await client.close()

async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path.
    """
    client = AsyncClient()
    content = await client.upscale(image)
    await client.close()
    upscaled_file_path = "upscaled.png"
    with open(upscaled_file_path, "wb") as output_file:
        output_file.write(content)
    return upscaled_file_path

async def ChatCompletion(prompt,model) -> tuple | str :
    modelInfo = getattr(languageModels,model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt,modelInfo)
    await client.close()
    if model == "bard":
        return output['content'], output['images'] if 'images' in output else []
    return output['content']

async def geminiVision(prompt,model,images) -> tuple | str :
    imageInfo = []
    for image in images:
        with open(image,"rb") as imageFile:
            data = base64.b64encode(imageFile.read()).decode("utf-8")
            mime_type,_= mimetypes.guess_type(image)
            imageInfo.append({
                "data": data,
                "mime_type": mime_type
            })
        os.remove(image)
    payload = {
        "images":imageInfo
    }
    modelInfo = getattr(languageModels,model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt,modelInfo,json=payload)
    return output['content']['parts'][0]['text']

async def ReverseImageSearch(img_url,search_engine) -> dict:
    client = AsyncClient()
    output = await client.ImageReverse(img_url,search_engine)
    await client.close()
    return output

async def SearchImages(query,search_engine) -> dict:
    client = AsyncClient()
    output = await client.SearchImages(query,0,search_engine)
    await client.close()
    return output

async def DownloadMedia(platform,url) -> dict:
    client = AsyncClient()
    output = await client.MediaDownloaders(platform,url)
    await client.close()
    return output

################################################ (Draw) ######################################################


from pyrogram import Client, filters, types as t
#from Utils import getText,paginate_models,getText
#from bot import Models

Database = {}

@Client.on_message(filters.command(["draw","imagine","dream"]))
async def draw(_: Client, m: t.Message):
    global Database
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("give something to create")
    user = m.from_user
    data = {'prompt':prompt,'reply_to_id':m.id}
    Database[user.id] = data
    btns = paginate_models(0,Models,user.id)
    await m.reply_text(
            text=f"Your prompt: `{prompt}`\n\nSelect a model",
            reply_markup=t.InlineKeyboardMarkup(btns)
            )

@Client.on_callback_query(filters.regex(pattern=r"^d.(.*)"))
async def selectModel(_:Client,query:t.CallbackQuery):
    global Database
    data = query.data.split('.')
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    if len(data) > 3:
        if data[1] == "right":
            next_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(next_page + 1,Models,auth_user)
                    )
                )
        elif data[1] == "left":
            curr_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(curr_page - 1,Models,auth_user)
                )
            )
        return
    modelId = int(data[1])
    if modelId == -1:
        del Database[auth_user]
        await query.message.delete()
        return
    await query.edit_message_text("Please wait, generating your image")
    promptData = Database.get(auth_user,None)
    if promptData is None:
        return await query.edit_message_text("Something went wrong.")
    img_url = await ImageGeneration(modelId,promptData['prompt'])
    if img_url is None or img_url == 2 or img_url ==1:
        return await query.edit_message_text("something went wrong!")
    elif img_url == 69:
        return await query.edit_message_text("NSFW not allowed!")
    images = []
    modelName = [i['name'] for i in Models if i['id'] == modelId]
    for i in img_url:
        images.append(t.InputMediaDocument(i))
    images[-1] = t.InputMediaDocument(img_url[-1],caption=f"Your prompt: `{promptData['prompt']}`\nModel: `{modelName[0]}`") # for caption
    await query.message.delete()
    try:
        del Database[auth_user]
    except KeyError:
        pass
    await _.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptData['reply_to_id']
    )

##############################################   (Modules)   ##################################################

import uvloop
uvloop.install()
import datetime,logging, sys
from pyrogram import Client
from lexica import Client as ApiClient
from lexica.constants import version
#from config import Config
#from Utils.telegraph import GraphClient

# Get logging configurations
logging.basicConfig(
    format="%(asctime)s - [BOT] - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

StartTime = datetime.datetime.now()
Models = ApiClient().models['models']['image']
LOGGER.info(f"Models Loaded: v{version}")

TelegraphClient = GraphClient(
    "LexicaAPI",
    "https://t.me/LexicaAPI",
    "LexicaAPI"
)
TelegraphClient.createAccount()

class Bot(Client):
    global StartTime,Models
    #print(Models)
    def __init__(self):
        super().__init__(
            "SDWaifuRobot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
        )
    async def start(self):
        await super().start()
        LOGGER.info("Bot Started")

    if Models is None:
        LOGGER.error("Models are empty!")
        sys.exit(1)

    async def stop(self):
        await super().stop()
        LOGGER.info("Stopped Services")

if __name__ == "__main__":
    Bot().run()

#################################### (GraphClient) ########################################
from httpx import Client,AsyncClient
import os,traceback,json
from .htmlParser import htmlToNodes

class GraphClient:
    def __init__(self,author_name,author_url,short_name,access_token=None):
        self.baseUrl = "https://api.graph.org/"
        self.client = Client(http2=True)
        self.access_token = access_token
        self.author_name = author_name
        self.author_url = author_url
        self.short_name = short_name
        self.headers = {
            "User-Agent":"SDWaifuRobot/1.0",
            "Content-Type":"application/json"
        }
    
    def createAccount(self,):
        url = self.baseUrl+"createAccount"
        data = {
            "author_name":self.author_name,
            "author_url":self.author_url,
            "short_name":self.short_name
        }
        resp = self.client.post(url,json=data,headers=self.headers)
        if resp.status_code != 200:
            return None
        resp = resp.json()
        if resp.get('ok'):
            self.access_token = resp['result']['access_token']
            return None
        raise Exception(resp['error'])
    
    def createPage(self,title,content):
        url = self.baseUrl+"createPage"
        content_json = json.dumps(htmlToNodes(content),separators=(',', ':'), ensure_ascii=False)
        data = {
            'access_token': self.access_token,
            'title': title,
            'author_name': self.author_name,
            'author_url':   self.author_url,
            'content': content_json,
            'return_content': False
        }
        resp = self.client.post(url,json=data,headers=self.headers)
        if resp.status_code != 200:
            return None
        resp = resp.json()
        if resp.get('ok'):
            return resp['result']['url']
        raise Exception(resp['error'])

  ################################################## (NEKOBIN) ########################################################################

import httpx

NEKOBIN = "https://nekobin.com/api/documents"
async def nekobin(data,extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    try:
        async with httpx.AsyncClient() as req:
            res = req.post(
                url=NEKOBIN,
                json={
                    "content":data,
                    "title": "data",
                    "author": "SDWaifuRobot"
                })
    except Exception as e:
        return {"error": str(e)}
    if res.ok:
        resp = res.json()
        purl = (
            f"nekobin.com/{resp['result']['key']}.{extension}"
            if extension
            else f"nekobin.com/{resp['result']['key']}"
        )
        return purl
    return {"error": "Unable to reach nekobin."}
