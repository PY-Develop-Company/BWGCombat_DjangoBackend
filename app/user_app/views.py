import django.db
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
import json


def user_home(request):
    return HttpResponse('user home')


@method_decorator(csrf_exempt, name='dispatch')
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tg_username = data['tg_username']
            tg_id = data['tg_id']
            first_name = data['firstname']
            last_name = data['lastname']
            interface_lang = data['interface_lang_id']

            # Додавання користувача до бази даних
            user = User.objects.create(
                tg_username=tg_username,
                tg_id=tg_id,
                firstname=first_name,
                lastname=last_name,
                # костиль, пароль треба допускати як nullable
                password='123',
                is_active=True,
                is_staff=False,
                is_admin=False,
                interface_lang_id=interface_lang
            )
            user.save()

            return HttpResponse('The user has been registered successfully')

        except django.db.IntegrityError:
            # костиль, треба нормальна перевірка перед спробою виконання INSERT INTO
            return HttpResponse('The user already exists and successfully found')

        except KeyError:
            print('error key')
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        except json.JSONDecodeError:
            print('error decode')
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    else:
        print('wrong method')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
