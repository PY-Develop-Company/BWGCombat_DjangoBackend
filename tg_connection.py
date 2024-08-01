from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
import os


TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(TOKEN)


async def is_subscribed_to_channel(user_id, channel_id):
    chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    return chat_member.status not in ['left', 'kicked']


async def get_fren_link(user_id):
    link = await create_start_link(bot, f'fren_id{user_id}')
    return link
