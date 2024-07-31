import os
from user_app.models import UserData

from .models import Asset, ExchangePair


def is_exchange_pair_exists(asset_1_id: int, asset_2_id: int):
    try:
        exchange_pair = ExchangePair.objects.get(asset_1_id=asset_2_id, asset_2_id=asset_1_id)
    except ExchangePair.DoesNotExist:
        return False
    else:
        return True


def is_transfer_fee_correct(currency_amount, frontend_calculated_fee):
    backend_fee_percentage = float(os.environ.get("TRANSFER_FEE_PERCENTAGE"))
    backend_calculated_fee = round(currency_amount * (backend_fee_percentage / 100), 6)

    return False if float(frontend_calculated_fee) != backend_calculated_fee else True


def is_swap_fee_correct(amount_1, frontend_calculated_fee, exchange_pair: ExchangePair):
    backend_calculated_fee = round(amount_1 * (exchange_pair.fee_percentage / 100), 6)

    return False if round(float(frontend_calculated_fee), 6) != backend_calculated_fee else True


def is_swap_receive_amount_correct(amount_1, frontend_calculated_amount_2, exchange_pair: ExchangePair):
    backend_calculated_amount_2 = round(amount_1 / exchange_pair.rate, 6)

    print('backend_calculated_amount_2:')
    print(backend_calculated_amount_2)
    print('frontend_calculated_amount_2:')
    print(frontend_calculated_amount_2)

    return False if round(float(frontend_calculated_amount_2), 6) != backend_calculated_amount_2 else True




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
