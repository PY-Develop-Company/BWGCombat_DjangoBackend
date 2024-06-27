from user_app.models import UserData
from .models import Reward


def add_reward(user_data: UserData, reward: Reward):
    reward_type = int(reward.reward_type)
    reward_amount = int(reward.amount)
    match reward_type:
        case 1:
            user_data.add_gold_coins(reward_amount)
        case 2:
            user_data.add_multiplier_coins(reward_amount)
        case 3:
            pass  ### add for another type of reward
        case _:
            return "No such type reward"
