from datetime import datetime
import os
import uuid

from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import Message
from aiogram.dispatcher.filters import Filter
from async_lru import alru_cache
import urllib

import carbon
import requests
import utility

bot_token = os.getenv('CODEIMAGINEBOT_TELEGRAM_TOKEN')
influx_query_url = os.getenv('CODEIMAGINEBOT_INFLUX_QUERY')


def influx_query(query_str: str):
    if influx_query_url:
        try:
            url = influx_query_url
            headers = {'Content-Type': 'application/Text'}

            x = requests.post(url, data=query_str.encode('utf-8'), headers=headers)
        except Exception as e:
            print(e)


bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher(bot)

class ignore_old_messages(Filter):
    async def check(self, message: Message):
        return (datetime.now() - message.date).seconds < 30


@dp.message_handler(ignore_old_messages(), commands=['start'])
async def start(message: Message):
    reply_text = "Привет, напиши мне код, а я тебе отдам картинку"
    msg = await bot.send_message(message.chat.id, text=reply_text, reply_to_message_id=message.message_id, parse_mode=ParseMode.MARKDOWN)


@alru_cache(maxsize=3200)
async def get_image_path_from_code(code: str) -> str:
    code = urllib.parse.quote_plus(code)

    body = {
        "backgroundColor": "rgba(57, 132, 95, 100)",
        "code": code,
        "theme": "dracula"
    }

    validatedBody = utility.validateBody(body)

    carbonURL = utility.createURLString(validatedBody)
    path = os.getcwd() + f'/images/{uuid.uuid4()}.png'

    await carbon.get_response(carbonURL, path)

    return path


@dp.message_handler(ignore_old_messages(), content_types=types.ContentType.TEXT)
async def code_handle(message: Message):
    # Work always in private messages
    if message.chat.type == 'private':
        text = message.text
        reply_to_message_id = message.message_id
    # Work in chat only by replying
    elif message.reply_to_message and message.reply_to_message.text and message.text == 'cute':
        text = message.reply_to_message.text
        reply_to_message_id = message.reply_to_message.message_id
    else:
        return

    await message.answer_chat_action('upload_photo')
    user_id = message.from_user.id
    user_name = message.from_user.mention
    user_fullname = message.from_user.full_name.replace(' ', '\ ').replace('=', '\=')
    chat_id = message.chat.id
    if message.chat.title:
        chat_title = message.chat.title.replace(' ', '\ ').replace('=', '\=')
    else:
        chat_title = user_fullname

    print(f'bots,botname=codeimaginebot,chatname={chat_title},chat_id={chat_id},user_id={user_id},user_name={user_name},user_fullname={user_fullname} image=1')
    influx_query(f'bots,botname=codeimaginebot,chatname={chat_title},chat_id={chat_id},user_id={user_id},user_name={user_name},user_fullname={user_fullname} image=1')

    chat_id = message.chat.id

    path = await get_image_path_from_code(text)

    with open(path, 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, reply_to_message_id=reply_to_message_id, photo=open(path, 'rb'))


if __name__ == '__main__':
    dp.bind_filter(ignore_old_messages)
    executor.start_polling(dp, on_startup=print(f"Bot is started."))
