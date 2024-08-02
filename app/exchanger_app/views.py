import logging
import os

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import SwapSerializer, TransferSerializer, RateSerializer
from .utils import (is_exchange_pair_exists, is_asset_exists, is_sufficient,
                    is_transfer_fee_correct, is_swap_fee_correct, is_swap_receive_amount_correct)

from .models import Swap, Transfer, Asset, ExchangePair
from user_app.models import UserData, User

from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


def exchanger_home(request):
    return HttpResponse("exchanger home")


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def execute_swap(request):
    user_id = request.data.get("userId")
    asset_1_id = request.data.get("asset1Id")
    asset_2_id = request.data.get("asset2Id")
    amount_1 = request.data.get("amount1")
    amount_2 = request.data.get("amount2")
    fee = request.data.get("fee")  # fee amount is tied to asset_1 amount

    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # BE CAREFUL! Assets inversion!!!
        exchange_pair = ExchangePair.objects.get(asset_1_id=asset_2_id, asset_2_id=asset_1_id)
    except ExchangePair.DoesNotExist:
        return JsonResponse({"result": "no such pair"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_swap_fee_correct(amount_1, fee, exchange_pair):
        return JsonResponse({"result": "fee is incorrect or irrelevant",
                            "hint": "try erasing and entering value again"},
                            status=status.HTTP_423_LOCKED)

    if not is_swap_receive_amount_correct(amount_1, amount_2, exchange_pair):
        return JsonResponse({"result": "receive amount is incorrect or irrelevant",
                            "hint": "try erasing and entering value again"},
                            status=status.HTTP_423_LOCKED)

    try:
        user_data = UserData.objects.get(user_id=user_id)
    except UserData.DoesNotExist:
        return JsonResponse({"result": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not is_sufficient(userdata=user_data, asset_id=asset_1_id, amount=amount_1, fee=fee):
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    if asset_1_id == 1:
        swap_limit_on_rank = user_data.rank.swap_limit
        g_tokens_swapped_on_rank = sum(Swap.objects.filter(user_id=user_id, user_rank=user_data.rank,
                                                           asset_1_id=1).values_list("amount_1", flat=True))
        if not g_tokens_swapped_on_rank:
            g_tokens_swapped_on_rank = 0

        if g_tokens_swapped_on_rank + amount_1 > swap_limit_on_rank:
            return JsonResponse({"result": "g_tokens swap limit on rank exceeded"}, status=status.HTTP_200_OK)

    # print(amount_1 + fee)
    try:
        if asset_1_id == 1 and asset_2_id == 2:
            user_data.remove_g_token_coins(amount_1 + fee)
            user_data.add_gold_coins(amount_2)
        elif asset_1_id == 2 and asset_2_id == 1:
            user_data.remove_gold_coins(amount_1 + fee)
            user_data.add_g_token_coins(amount_2)
        elif asset_1_id == 1 and asset_2_id == 3:
            user_data.remove_g_token_coins(amount_1 + fee)
            user_data.add_gnomes(amount_2)
        elif asset_1_id == 3 and asset_2_id == 1:
            user_data.remove_gnomes(amount_1 + fee)
            user_data.add_g_token_coins(amount_2)
        else:
            return JsonResponse({"result": "no such exchange pair"})

        user = User.objects.get(tg_id=user_id)
        asset_1 = Asset.objects.get(id=asset_1_id)
        asset_2 = Asset.objects.get(id=asset_2_id)

        swap = Swap(user=user, user_rank=user_data.rank,
                    asset_1=asset_1, asset_2=asset_2,
                    fee=fee, amount_1=amount_1, amount_2=amount_2)
        swap.save()

        user_data.save()
    except Exception as e:
        logging.error(e)
        raise
        # transaction rollback

    return JsonResponse({"result": "ok",
                         "new_user_gold_balance": user_data.gold_balance,
                         "new_user_g-token_balance": user_data.g_token,
                         "new_user_gnome_balance": user_data.gnome_amount})


@csrf_exempt
@api_view(["POST"])
@transaction.atomic
def execute_transfer(request):
    user_1_id = request.data.get("user1Id")
    user_2_id = request.data.get("user2Id")
    asset_id = request.data.get("assetId")
    amount = request.data.get("amount")
    fee = request.data.get("fee")

    if not user_1_id or not user_2_id:
        return JsonResponse({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_asset_exists(asset_id=asset_id):
        return JsonResponse({"result": "no such asset"}, status=status.HTTP_400_BAD_REQUEST)

    if not is_transfer_fee_correct(amount, fee):
        return JsonResponse({"result": "fee is incorrect or irrelevant",
                            "hint": "try erasing and entering value again"},
                            status=status.HTTP_423_LOCKED)

    sender_data = UserData.objects.get(user_id=user_1_id)
    if not is_sufficient(userdata=sender_data, asset_id=asset_id, amount=amount, fee=fee):
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    try:
        receiver_data = UserData.objects.get(user_id=user_2_id)
    except UserData.DoesNotExist:
        return JsonResponse({"result": "user does not exist"})

    try:
        if asset_id == 1:
            sender_data.remove_g_token_coins(amount + fee)
            receiver_data.add_g_token_coins(amount)
        elif asset_id == 2:
            sender_data.remove_gold_coins(amount + fee)
            receiver_data.add_gold_coins(amount)
        else:
            return JsonResponse({"result": "no such currency"})

        sender = User.objects.get(tg_id=user_1_id)
        receiver = User.objects.get(tg_id=user_2_id)

        asset = Asset.objects.get(id=asset_id)

        transfer = Transfer(user_1=sender, user_2=receiver, asset=asset, fee=fee, amount=amount)
        transfer.save()

        sender_data.save()
        receiver_data.save()
    except Exception as e:
        logging.error(e)
        raise
        # transaction rollback

    if asset_id == 1:
        sender_balance = sender_data.g_token
        receiver_balance = receiver_data.g_token
    elif asset_id == 2:
        sender_balance = sender_data.gold_balance
        receiver_balance = receiver_data.gold_balance
    else:
        raise

    return JsonResponse({"result": "ok",
                         "new_sender_balance": sender_balance,
                         "new_receiver_balance": receiver_balance})


@api_view(["POST"])
def get_all_transactions(request):
    user_id = request.data.get('userId')

    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    swaps = Swap.objects.filter(user=user)
    swap_data = SwapSerializer(swaps, many=True).data

    transfers = Transfer.objects.filter(user_1=user) | Transfer.objects.filter(user_2=user)
    transfer_data = TransferSerializer(transfers, many=True).data

    return JsonResponse({"swaps": swap_data, 'transfers': transfer_data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_rates(request):
    rates = ExchangePair.objects.all()
    rates_data = RateSerializer(rates, many=True).data

    return JsonResponse({"rates": rates_data})


@api_view(["POST"])
@permission_classes([AllowAny])
def get_exchange_rate(request):
    asset_1_id = request.data.get("asset1Id")
    asset_2_id = request.data.get("asset2Id")
    amount_1 = request.data.get("amount1")

    try:
        # BE CAREFUL! Assets INVERSION!
        exchange_pair = ExchangePair.objects.get(asset_1_id=asset_2_id, asset_2_id=asset_1_id)
    except ExchangePair.DoesNotExist:
        return JsonResponse({"result": "no such exchange pair"})

    amount_2 = amount_1 / exchange_pair.rate

    if not exchange_pair.fee_percentage:
        fee_amount = 0
    else:
        fee_amount = amount_1 * (exchange_pair.fee_percentage / 100)

    return JsonResponse({"exchange_rate": round(1/exchange_pair.rate, 6),
                         "fee_percentage": exchange_pair.fee_percentage,
                         "fee_amount": round(fee_amount, 6),
                         "amount_1": amount_1,
                         "amount_2": round(amount_2, 6)})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_transfer_fee(request):
    transfer_fee = float(os.environ.get("TRANSFER_FEE_PERCENTAGE"))
    return JsonResponse({"transfer_fee": transfer_fee})


@api_view(["POST"])
@transaction.atomic()
def buy_vip(request):
    user_id = request.data.get('userId')

    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=400)

    # vip price temp
    vip_price = 10

    try:
        user_data = UserData.objects.get(pk=user_id)
    except UserData.DoesNotExist:
        return JsonResponse({"result": "user does not exist"})

    if user_data.is_vip:
        return JsonResponse({"result": "user is already vip"}, status=status.HTTP_200_OK)

    if not is_sufficient(userdata=user_data, asset_id=1, amount=vip_price, fee=0):
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    try:
        user_data.remove_g_token_coins(vip_price)
        user_data.make_vip()
        user_data.save()
    except Exception as e:
        logging.error(e)
        raise
        # transaction rollback

    return JsonResponse({"result": "ok"})
