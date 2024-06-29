import asyncio


# from user_app.models import UserData
from .models import Reward


# async def check_subscription(user_id):
#     chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
#     return False if chat_member.status in ['left', 'kicked'] else True


def check_subscription_sync(user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(check_subscription(user_id))


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

