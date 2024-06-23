from .models import UserData


def add_gold_coins_to_user(user_data: UserData, coins: int):
    user_data.gold_balance = user_data.gold_balance + int(coins)
    user_data.save()
    return user_data


def remove_coin_from_user(user_data: UserData, coins: int):
    user_data.gold_balance = user_data.gold_balance - int(coins)
    user_data.save()
    return user_data
