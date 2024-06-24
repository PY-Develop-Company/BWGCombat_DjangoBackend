import django.db
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import User, UserData, Fren

# from aiogram import Bot
# from aiogram.utils.deep_linking import create_start_link

import json
from .serializer import User_data_Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user_app.serializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


def user_home(request):
    return HttpResponse('user home')



@api_view(["GET"])
def get_user_info(request):
    user = request.user
    user_data = get_object_or_404(UserData, user_id=user.tg_id)
    serializer = User_data_Serializer(user_data)
    return Response({"info": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_coins_to_user(request):
    coins = request.data.get("clicks") ### multiply by coins_per_click
    user_id = request.data.get("user_id")

    user_data = UserData.objects.filter(user_id=user_id).first()
    user_data.add_gold_coins(coins)
    info = User_data_Serializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def remove_coins_from_user(request):
    coins = request.data.get("coins")
    user_id = request.data.get("user_id")

    user_data = UserData.objects.filter(user_id=user_id).first()
    user_data.remove_coins(coins)
    info = User_data_Serializer(user_data)
    return Response({"user_info": info.data}, status=status.HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
def add_user(request):
    try:
        data = json.loads(request.body)
        tg_username = data['tg_username']
        tg_id = data['tg_id']
        first_name = data['firstname']
        last_name = data['lastname']
        interface_lang = data['interface_lang_id']
        is_admin = data['is_admin']
        is_staff = is_admin
        password = data['password'] if 'password' in data else None

        # Додавання користувача до бази даних
        user = User.objects.create(
            tg_username=tg_username,
            tg_id=tg_id,
            firstname=first_name,
            lastname=last_name,
            # password=password,
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

        return HttpResponse('The user has been registered successfully')
    except django.db.IntegrityError:
        # резервна перевірка
        return HttpResponse('The user already exists and successfully found')

    except KeyError as ke:
        print(ke)
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    except json.JSONDecodeError:
        print('error decode')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})


@csrf_exempt
@require_POST
def add_referral(request):
    try:
        data = json.loads(request.body)
        fren_tg_id = int(data['fren_tg_id'])
        inviter_tg_id = int(data['inviter_tg_id'])

        inviter_user = User.objects.get(tg_id=inviter_tg_id)

        # Додавання реферала до бази даних
        fren = Fren(fren_tg_id=fren_tg_id, inviter_tg_id=inviter_user)
        fren.save()

        return HttpResponse('The user has been registered successfully')
    except django.db.IntegrityError:
        # резервна перевірка
        return HttpResponse('Database Integrity error')

    except KeyError as ke:
        print(ke)
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    except json.JSONDecodeError:
        print('error decode')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})


@api_view(["GET"])
def get_user_referrals(request):
    tg_id = request.data.get("tg_id")

    print(request.data)
    print(request.body)

    # print('json.loads(request.body)')
    # print(data)

    print()
    print(1)
    print(tg_id)
    print(1)
    print()
    user = User.objects.get(tg_id=tg_id)
    referrals = user.referrals.all()

    for referral in referrals:
        print(referral)

    return HttpResponse(referrals)


    
