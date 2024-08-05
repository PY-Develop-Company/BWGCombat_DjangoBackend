import asyncio

import django.db
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView

from adrf.decorators import api_view as async_api_view

from .utils import get_gnome_reward
from .models import User, UserData, Fren, Link, LinkClick, Language

from levels_app.models import Rank
import json
from .serializers import UserDataSerializer, ClickSerializer, ReferralsSerializer, UserSettingsSerializer
from user_app.serializers import CustomTokenObtainPairSerializer

from redis import StrictRedis
from datetime import datetime
from tg_connection import get_fren_link


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def user_home(request):
    return HttpResponse("user home")


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_info(request):
    redis_db = StrictRedis('redis', 6379)
    user_id = request.query_params.get("userId")

    if not redis_db.exists(f"user_{user_id}"):
        print(redis_db.keys())
        user_data = get_object_or_404(UserData, user_id=user_id)
        redis_db.json().set(f"user_{user_id}", "$", UserDataSerializer(user_data).data)

    user_data = redis_db.json().get(f'user_{user_id}')
    delta = now() - datetime.fromisoformat(user_data["last_visited"])
    user_data['current_energy'] += round(min(delta.total_seconds() * user_data['energy_regeneration'], user_data['energy'] - user_data['current_energy']))

    income = user_data['gnome_amount']*get_gnome_reward()/24/3600 * delta.total_seconds()
    user_data['g_token'] += income

    redis_db.json().set(f"user_{user_id}", "$", user_data, xx=True)
    return Response({"info": user_data, 'passive_income': income}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@permission_classes([AllowAny])
def add_coins_to_user(request):
    total_clicks = request.data.get("totalClicks")
    user_id = request.data.get("userId")
    current_energy = request.data.get("currentEnergy")
    suspicious_activity = request.data.get("suspiciousActivity")

    if suspicious_activity:
        return JsonResponse({"result": "fail", "message": "suspicious activity has been detected"},
                            status=status.HTTP_400_BAD_REQUEST)

    user_data = get_object_or_404(UserData, user_id=user_id)
    user_data.add_gold_coins(total_clicks*user_data.multiclick_amount)
    user_data.current_energy = current_energy
    user_data.last_visited = now()

    user_data.save()
    info = ClickSerializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def remove_coins_from_user(request):
    coins = request.data.get("coins")
    user_id = request.data.get("user_id")

    user_data = get_object_or_404(UserData, user_id=user_id)
    user_data.remove_gold_coins(coins)
    info = UserDataSerializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def check_user_existence(request):
    try:
        data = json.loads(request.body)
        tg_id = data["tg_id"]
    except json.JSONDecodeError:
        return JsonResponse({"result": "Unexpected JSON error"})
    else:
        user_exists = User.objects.filter(tg_id=tg_id).exists()
        if user_exists:
            return JsonResponse({"result": "1"})
        else:
            return JsonResponse({"result": "0"})


@permission_classes([AllowAny])
@api_view(["POST"])
def add_user(request):
    try:
        data = json.loads(request.body)
        tg_id = data["tg_id"]
        #
        # user_exists = User.objects.filter(User, tg_id=tg_id).exists()
        # if user_exists:
        #     return JsonResponse({"result": "The user already exists"})

        tg_username = data["tg_username"]
        first_name = data["firstname"]
        last_name = data["lastname"]
        interface_lang = data["interface_lang_id"]
        is_admin = data["is_admin"]
        is_staff = is_admin  # temporarily
        password = data["password"] if "password" in data else None

    except json.JSONDecodeError:
        return JsonResponse({"result": "Unexpected JSON error"})

    try:
        user = User.objects.create(
            tg_username=tg_username,
            tg_id=tg_id,
            firstname=first_name,
            lastname=last_name,
            is_active=True,
            is_staff=is_staff,
            is_admin=is_admin,
            interface_lang_id=interface_lang
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

    except django.db.Error:
        return JsonResponse({"result": "Unexpected DB error"})

    return JsonResponse({"result": "The user has been registered successfully"})


@permission_classes([AllowAny])
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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_referrals(request):
    user_id = request.query_params.get("userId")

    user = get_object_or_404(User, tg_id = user_id)
    referrals = UserData.objects.filter(
        user_id__in=Fren.objects.filter(inviter_tg=user).values_list('fren_tg', flat=True)
    )
    serializer = ReferralsSerializer(referrals, many=True).data

    return JsonResponse({'referrals':serializer}, status=status.HTTP_200_OK)


def track_link_click(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    user_id = request.data.get("userId")
    user = User.objects.get(tg_id=user_id)
    LinkClick.objects.create(user=user, link=link)

    return redirect(link.url)


@permission_classes([AllowAny])
@api_view(["POST"])
def pick_character(request):
    user_id = request.data.get('userId')
    choice = request.data.get('gender')
    user_data = get_object_or_404(UserData, user_id=user_id)
    user_data.character_gender = int(choice)
    user_data.save()
    return JsonResponse(UserDataSerializer(user_data).data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(["POST"])
def change_language(request):
    user_id = request.data.get('userId')
    lang_code = request.data.get('languageCode')
    user_data = get_object_or_404(UserData, user_id=user_id)
    lang = get_object_or_404(Language, lang_code=lang_code)
    user_data.user.interface_lang = lang
    user_data.save()
    return JsonResponse(UserDataSerializer(user_data).data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(["GET"])
def get_user_settings(request):
    user_id = request.data.get("userId")

    user_data_obj = UserData.objects.get(user_id=user_id)
    settings_data = UserSettingsSerializer(user_data_obj).data

    return JsonResponse(settings_data)


@permission_classes([AllowAny])
@api_view(["POST"])
def update_user_settings(request):
    user_id = request.data.get("userId")
    language_code = request.data.get("languageCode")
    visual_effects = request.data.get("visualEffects")
    general_volume = request.data.get("generalVolume")
    effects_volume = request.data.get("effectsVolume")
    music_volume = request.data.get("musicVolume")

    user_data_obj = UserData.objects.get(user_id=user_id)
    user_obj = user_data_obj.user

    user_obj.interface_lang = Language.objects.get(lang_code=language_code)
    user_data_obj.visual_effects = visual_effects
    try:
        user_data_obj.general_volume = int(general_volume)
        user_data_obj.effects_volume = int(effects_volume)
        user_data_obj.music_volume = int(music_volume)
    except ValueError:
        return JsonResponse({"result": "updating volume failed as not-numbers passed as parameters"})
    else:
        user_obj.save()
        user_data_obj.save()

    return JsonResponse({"result": "ok"})


@permission_classes([AllowAny])
@async_api_view(["POST"])
async def async_get_fren_link(request):
    user_id = request.data.get("userId")
    task = asyncio.ensure_future(get_fren_link(user_id))
    link = await task
    return JsonResponse({"link": link})
