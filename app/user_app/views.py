import django.db
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.core.exceptions import ValidationError


from .models import User, UserData, Fren, Link, LinkClick
from levels_app.models import Rank

# from aiogram import Bot
# from aiogram.utils.deep_linking import create_start_link

import json
from .serializer import UserDataSerializer, RankInfoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user_app.serializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


def user_home(request):
    data = json.loads(request.body)
    if data:
        fren_id = data["fren_id"]
    return HttpResponse("user home")


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_info(request):
    user_id = request.query_params.get("userId")
    user_data = get_object_or_404(UserData, user_id=user_id)
    serializer = UserDataSerializer(user_data)
    return Response({"info": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_coins_to_user(request):
    coins = request.data.get("totalClicks")
    user_id = request.data.get("userId")

    user_data = UserData.objects.get(user_id=user_id)
    user_data.add_gold_coins(coins)
    user_data.save()
    info = UserDataSerializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def remove_coins_from_user(request):
    coins = request.data.get("coins")
    user_id = request.data.get("user_id")

    user_data = UserData.objects.filter(user_id=user_id).first()
    user_data.remove_gold_coins(coins)
    info = UserDataSerializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def add_user(request):
    try:
        data = json.loads(request.body)
        tg_username = data["tg_username"]
        tg_id = data["tg_id"]
        first_name = data["firstname"]
        last_name = data["lastname"]
        interface_lang = data["interface_lang_id"]
        is_admin = data["is_admin"]
        is_staff = is_admin
        password = data["password"] if "password" in data else None

        # Додавання користувача до бази даних
        user = User.objects.create(
            tg_username=tg_username,
            tg_id=tg_id,
            firstname=first_name,
            lastname=last_name,
            is_active=True,
            is_staff=is_staff,
            is_admin=is_admin,
            interface_lang_id=interface_lang,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        return JsonResponse({"result": "The user has been registered successfully"})
    except django.db.IntegrityError:
        return JsonResponse({"result": "The user already exists"})


@csrf_exempt
@api_view(["POST"])
def add_referral(request):
    try:
        fren_tg = request.data.get("fren_tg")
        inviter_tg = request.data.get("inviter_tg")

        # Додавання реферала до бази даних
        fren = Fren.objects.create(fren_tg_id=fren_tg, inviter_tg_id=inviter_tg)
        fren.save()

        return HttpResponse("The user has been registered successfully")
    except django.db.IntegrityError:
        return HttpResponse("Database Integrity error")

    except KeyError as ke:
        return JsonResponse({"status": "error", "message": "Invalid data"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"})


@csrf_exempt
@api_view(["GET"])
def get_user_referrals(request):
    data = json.loads(request.body)

    user = User.objects.get(tg_id=data["tg_id"])
    referrals = user.referrals.all()

    for referral in referrals:
        print(referral)

    return HttpResponse(referrals)


def track_link_click(request, link_id):
    link = get_object_or_404(Link, id=link_id)

    user_id = request.data.get("userId")

    user = User.objects.get(tg_id=user_id)

    LinkClick.objects.create(user=user, link=link)

    return redirect(link.url)


@api_view(["POST"])
def get_rank_info(request):
    user_id = request.data.get('userId')
    rank_id = request.data.get('rankId')
    user_data = get_object_or_404(UserData, user_id=user_id)
    rank_info = get_object_or_404(Rank, id=rank_id)
    if user_data.rank_id == rank_info:
        serializer = RankInfoSerializer(rank_info, context = {'user_id':user_data.user_id_id, 'stage_id': user_data.stage_id_id})
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"rank_id": rank_info.id, "name": rank_info.name, 'description': rank_info.description}, status=status.HTTP_200_OK)


    

