from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import random

from django.http import JsonResponse
from django.db.models import Q

from .models import Advert
from .serializers import AdvertSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_advert(request):
    advert_id = request.data.get("adId")

    try:
        advert = Advert.objects.get(id=advert_id)
    except Advert.DoesNotExist:
        return JsonResponse({"result": "advert with such id does not exist"})

    advert_data = AdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_fullscreen_advert(request):
    advert_id = request.data.get("adId")

    try:
        advert = Advert.objects.get(id=advert_id)
    except Advert.DoesNotExist:
        return JsonResponse({"result": "advert with such id does not exist"})

    if not advert.is_fullscreen():
        return JsonResponse({"result": "requested advert is only for banners"})

    advert_data = AdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_random_fullscreen_advert(request):
    fullscreen_ads_ids = Advert.objects.filter(Q(show_place=Advert.ShowPlace.FAIRY) |
                                               Q(show_place=Advert.ShowPlace.CHEST)).all().values_list('id', flat=True)

    print('fullscreen_ads_ids:')
    print(fullscreen_ads_ids)

    try:
        advert = Advert.objects.get(id=random.choice(fullscreen_ads_ids))
    except Advert.DoesNotExist:
        return JsonResponse({"result": "unexpected absence of the advert"})

    advert_data = AdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_banner_adverts(request):
    adverts = Advert.objects.all()
    adverts_data = AdvertSerializer(adverts, many=True).data

    return JsonResponse({"adverts": adverts_data})
