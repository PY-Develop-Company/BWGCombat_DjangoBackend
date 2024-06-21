from .helper import add_gold_coins_to_user, remove_coin_from_user
from .models import UserData
from user_app.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import User_data_Serializer
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def get_user_info(request):
    user = request.user
    user_data = get_object_or_404(UserData, user_id=user.tg_id)
    serializer = User_data_Serializer(user_data)
    return Response({"info": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_coins_to_user(request):
    coins = request.data.get("clicks") ### multiply by coins_per_click
    user = request.user
    print(type(user))
    user_data = UserData.objects.filter(user_id=user).first()
    info = User_data_Serializer(add_gold_coins_to_user(user_data, coins)) 
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def remove_coins_from_user(request):
    coins = request.data.get("coins")
    user_id = request.data.get("user_id")
    user_data = UserData.objects.filter(user_id=user_id).first()
    info = User_data_Serializer(remove_coin_from_user(user_data, coins))
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


