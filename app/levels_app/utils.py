import asyncio

from user_app.models import UserData, Fren, Link
from django.shortcuts import get_object_or_404
from .models import Reward


# async def check_subscription(user_id):
#     chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
#     return False if chat_member.status in ['left', 'kicked'] else True
#
#
# def check_subscription_sync(user_id):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(check_subscription(user_id))


def give_reward_to_inviter(fren_id):
    try:
        inviter_id = Fren.objects.get(fren_id=fren_id)
    except Fren.DoesNotExist:
        return
    userdata = get_object_or_404(UserData, user_id=inviter_id)

    reward = userdata.rank.inviter_reward

    userdata.receive_reward(reward)
    userdata.save()


def check_if_link_is_telegram(link: Link):
    telegram_link_starts = ('t.me/', 'https://t.me/')
    index = link.url.find(telegram_link_starts[1])
    if index == -1:
        index = link.url.find(telegram_link_starts[0])
        return index != -1

    return True


def set_rewards_for_user_tasks(user_id: int, stage: int):
    pass
