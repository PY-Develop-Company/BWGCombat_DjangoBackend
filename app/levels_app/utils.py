import asyncio


from user_app.models import UserData, Fren, Link
from django.shortcuts import get_object_or_404
from .models import Reward


# async def check_subscription(user_id):
#     chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
#     return False if chat_member.status in ['left', 'kicked'] else True


def check_subscription_sync(user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(check_subscription(user_id))


def give_reward_to_inviter(fren_id):
    inviter_id = get_object_or_404(Fren, fren_id=fren_id)
    userdata = get_object_or_404(UserData, user_id=inviter_id)

    reward = get_object_or_404(Reward, name="Referral's rank 1")

    userdata.receive_reward(reward)
    userdata.save()


def check_if_link_is_telegram(link):  # will be changed on 05.05.2024
    if isinstance(link, Link):
        link_str = link.url
    elif isinstance(link, str):
        link_str = link

    telegram_link_starts = ('t.me/', 'https://t.me/')
    index = link_str.find(telegram_link_starts[1])
    if index == -1:
        index = link_str.find(telegram_link_starts[0])
        return False if index == -1 else True
    else:
        return True


# def add_reward(user_data: UserData, reward: Reward):
"""
Метод перенесено у levels.app/views
"""
#     reward_type = int(reward.reward_type)
#     reward_amount = int(reward.amount)
#     match reward_type:
#         case 1:
#             user_data.add_gold_coins(reward_amount)
#         case 2:
#             user_data.add_multiplier_coins(reward_amount)
#         case 3:
#             pass  ### add for another type of reward
#         case _:
#             return "No such type reward"

