import random
from .models import FullscreenAdvert


def get_random_gold_reward(ad: FullscreenAdvert):
    random_reward = random.randint(ad.view_min_gold_reward.amount, ad.view_max_gold_reward.amount)
    return round(random_reward, -2)
