from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import SwapSerializer, TransferSerializer
from .utils import is_exchange_pair_exists, is_asset_exists, is_sufficient

from .models import Swap, Transfer, Asset
from user_app.models import UserData, User

from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt


def exchanger_home(request):
    return HttpResponse("exchanger home")


@csrf_exempt
@api_view(["POST"])
# @transaction.atomic
@permission_classes([AllowAny])
def execute_swap(request):
    user_id = request.data.get("userId")
    asset_1_id = request.data.get("asset1Id")
    asset_2_id = request.data.get("asset2Id")
    amount_1 = request.data.get("amount1")
    amount_2 = request.data.get("amount2")
    fee = request.data.get("fee")  # fee amount is tied to asset_1 amount

    checkpoint = transaction.savepoint()

    if not is_exchange_pair_exists(asset_1_id=asset_1_id, asset_2_id=asset_2_id):
        transaction.rollback()
        return JsonResponse({"result": "no such pair"}, status=status.HTTP_400_BAD_REQUEST)

    checkpoint = transaction.savepoint()

    user_data = UserData.objects.get(user_id=user_id)
    if not is_sufficient(userdata=user_data, asset_id=asset_1_id, amount=amount_1, fee=fee):
        transaction.rollback()
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    checkpoint = transaction.savepoint()

    print(amount_1 + fee)
    if asset_1_id == 1 and asset_2_id == 2:
        user_data.remove_g_token_coins(amount_1 + fee)
        checkpoint = transaction.savepoint()
        user_data.add_gold_coins(amount_2)
    elif asset_1_id == 2 and asset_2_id == 1:
        user_data.remove_gold_coins(amount_1 + fee)
        checkpoint = transaction.savepoint()
        user_data.add_g_token_coins(amount_2)
    else:
        return JsonResponse({"result": "unexpected error while adding and/or removing coins"})

    user = User.objects.get(tg_id=user_id)
    asset_1 = Asset.objects.get(id=asset_1_id)
    asset_2 = Asset.objects.get(id=asset_2_id)

    swap = Swap(user=user, asset_1=asset_1, asset_2=asset_2, fee=fee, amount_1=amount_1, amount_2=amount_2)
    swap.save()

    user_data.save()

    return JsonResponse({"result": "ok"})


@csrf_exempt
@api_view(["POST"])
# @transaction.atomic
def execute_transfer(request):
    user_1_id = request.data.get("user1Id")
    user_2_id = request.data.get("user2Id")
    asset_id = request.data.get("assetId")
    amount = request.data.get("amount")
    fee = request.data.get("fee")

    checkpoint = transaction.savepoint()

    if not is_asset_exists(asset_id=asset_id):
        transaction.rollback()
        return JsonResponse({"result": "no such asset"}, status=status.HTTP_400_BAD_REQUEST)

    sender_data = UserData.objects.get(user_id=user_1_id)
    if not is_sufficient(userdata=sender_data, asset_id=asset_id, amount=amount, fee=fee):
        transaction.rollback()
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    checkpoint = transaction.savepoint()

    receiver_data = UserData.objects.get(user_id=user_2_id)

    if asset_id == 1:
        sender_data.remove_g_token_coins(amount + fee)
        checkpoint = transaction.savepoint()
        receiver_data.add_g_token_coins(amount)
    elif asset_id == 2:
        sender_data.remove_gold_coins(amount + fee)
        checkpoint = transaction.savepoint()
        receiver_data.add_gold_coins(amount)

    else:
        return JsonResponse({"result": "unexpected error while adding and/or removing coins"})

    sender = User.objects.get(tg_id=user_1_id)
    receiver = User.objects.get(tg_id=user_2_id)

    asset = Asset.objects.get(id=asset_id)

    transfer = Transfer(user_1=sender, user_2=receiver, asset=asset, fee=fee, amount=amount)
    transfer.save()

    sender_data.save()
    receiver_data.save()

    return JsonResponse({"result": "ok"})


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
