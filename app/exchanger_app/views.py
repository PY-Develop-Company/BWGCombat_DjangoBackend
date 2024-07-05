from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Swap, Transfer, Asset
from user_app.models import UserData, User
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from .utils import check_exchange_pair_existence, check_sufficiency


def exchanger_home(request):
    return HttpResponse("exchanger home")


@transaction.atomic
def execute_swap(request):
    user_id = request.data.get("userId")
    asset_1_id = request.data.get("asset1ID")
    asset_2_id = request.data.get("asset2ID")
    amount_1 = request.data.get("amount1")
    amount_2 = request.data.get("amount2")
    fee = request.data.get("fee")  # fee amount is tied to asset_1 amount

    checkpoint = transaction.savepoint()

    if not check_exchange_pair_existence(asset_1_id=asset_1_id, asset_2_id=asset_2_id):
        transaction.rollback()
        return JsonResponse({"result": "no such pair"}, status=status.HTTP_400_BAD_REQUEST)

    checkpoint = transaction.savepoint()

    user_data = UserData.objects.get(user_id=user_id)
    if not check_sufficiency(userdata=user_data, asset_id=asset_1_id, amount=amount_1, fee=fee):
        transaction.rollback()
        return JsonResponse({"result": "not enough balance"}, status=status.HTTP_200_OK)

    checkpoint = transaction.savepoint()

    if asset_1_id == 1 and asset_2_id == 2:
        user_data.remove_gold_coins(amount_1 + fee)
        checkpoint = transaction.savepoint()
        user_data.add_g_token_coins(amount_2)
    elif asset_1_id == 2 and asset_2_id == 1:
        user_data.remove_g_token_coins(amount_1 + fee)
        checkpoint = transaction.savepoint()
        user_data.add_gold_coins(amount_2)
    else:
        return JsonResponse({"result": "unexpected error while adding and/or removing coins"})

    user = User.objects.get(tg_id=user_id)
    asset_1 = Asset.objects.get(id=asset_1_id)
    asset_2 = Asset.objects.get(id=asset_2_id)

    swap = Swap(user=user, asset_1=asset_1, asset_2=asset_2, fee=fee, amount_1=amount_1, amount_2=amount_2)
    swap.save()

    return JsonResponse({"result": "ok"})
