from .helper import add_gold_coins_to_user
from .models import UserData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import User_data_Serializer
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def get_user_info(request):
    user = request.user
    user_data = get_object_or_404(UserData, user_id=user.id)
    serializer = User_data_Serializer(user_data)
    return Response({"info": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_coins_to_user(request):
    coins = request.data.get("clicks")
    user = request.user
    user_data = UserData.objects.filter(user_id=user.id).first()
    add_gold_coins_to_user(user_data, coins) ### add multiplier for clicks
    return Response({"coins": coins}, status=status.HTTP_200_OK)
