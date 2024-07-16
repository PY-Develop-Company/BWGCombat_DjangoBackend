from user_app.models import UserData

from .models import Asset, ExchangePair


def is_exchange_pair_exists(asset_1_id: int, asset_2_id: int):
    try:
        exchange_pair = ExchangePair.objects.get(asset_1_id=asset_1_id, asset_2_id=asset_2_id)
    except ExchangePair.DoesNotExist:
        return False
    else:
        return True


def is_asset_exists(asset_id: int):
    try:
        asset = Asset.objects.get(id=asset_id)
    except ExchangePair.DoesNotExist:
        return False
    else:
        return True


def is_sufficient(userdata: UserData, asset_id: int, amount: float | int, fee: float | int):
    if asset_id == 1:
        return userdata.g_token >= amount + fee
    elif asset_id == 2:
        return userdata.gold_balance >= amount + fee
    else:
        return Asset.DoesNotExist
