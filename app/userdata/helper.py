from .models import UserData
from django.contrib.auth.models import User  ### replace with custom user


def add_gold_coins_to_user(user_data: UserData, coins: int):
    user_data.gold_balance = user_data.gold_balance + int(coins)
    user_data.save()
