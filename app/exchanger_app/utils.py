from .models import Asset, ExchangePair
from user_app.models import UserData


def check_exchange_pair_existence(asset_1_id: int, asset_2_id: int):
    try:
        exchange_pair = ExchangePair.objects.get(asset_1_id=asset_1_id, asset_2_id=asset_2_id)
    except ExchangePair.DoesNotExist:
        return False
    else:
        return True


def check_sufficiency(userdata: UserData, asset_id: int, amount: float | int, fee: float | int):
    if asset_id == 1:
        return True if userdata.gold_balance >= amount+fee else False
    elif asset_id == 2:
        return True if userdata.g_token >= amount+fee else False
    else:
        return Asset.DoesNotExist
