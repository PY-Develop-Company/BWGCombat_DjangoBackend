import django.db
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view

from .models import User, Fren

# from aiogram import Bot
# from aiogram.utils.deep_linking import create_start_link

import json


def user_home(request):
    return HttpResponse('user home')


@csrf_exempt
@require_POST
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
