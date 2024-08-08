import random
from django.utils import timezone

from .models import FullscreenAdvert, AdView


def get_random_gold_reward(ad: FullscreenAdvert):
    random_reward = random.randint(ad.view_min_gold_reward.amount, ad.view_max_gold_reward.amount)
    return round(random_reward, -2)


def get_last_advert_view_time(user, advert):
    last_view = AdView.objects.filter(user=user, advert=advert).order_by('-time').first()

    if last_view:
        return last_view.time
    else:
        return None


def is_advert_displayable_for_user(user, advert):
    last_viewed_time = get_last_advert_view_time(user, advert)
    if not last_viewed_time:
        return True

    next_allowed_display_time = last_viewed_time + advert.display_period
    current_time = timezone.now()

    return current_time >= next_allowed_display_time
