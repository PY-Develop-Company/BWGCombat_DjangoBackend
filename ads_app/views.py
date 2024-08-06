from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import random

from django.http import JsonResponse
from django.db.models import Q

from .models import BannerAdvert, FullscreenAdvert, AdView
from .serializers import BannerAdvertSerializer, FullscreenAdvertSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_banner_advert(request):
    advert_id = request.data.get("adId")

    try:
        advert = BannerAdvert.objects.get(id=advert_id)
    except BannerAdvert.DoesNotExist:
        return JsonResponse({"result": "advert with such id does not exist or it is not a banner advert"})

    advert_data = BannerAdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_fullscreen_advert(request):
    advert_id = request.data.get("adId")

    try:
        advert = FullscreenAdvert.objects.get(id=advert_id)
    except FullscreenAdvert.DoesNotExist:
        return JsonResponse({"result": "advert with such id does not exist or it is not a fullscreen advert"})

    # if not advert.is_fullscreen():
    #     return JsonResponse({"result": "requested advert is only for banners"})

    advert_data = FullscreenAdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_random_fullscreen_advert(request):
    fullscreen_ads_ids = FullscreenAdvert.objects.all().values_list('id', flat=True)

    print('fullscreen_ads_ids:')
    print(fullscreen_ads_ids)

    try:
        advert = FullscreenAdvert.objects.get(id=random.choice(fullscreen_ads_ids))
    except FullscreenAdvert.DoesNotExist:
        return JsonResponse({"result": "unexpected absence of the advert"})

    advert_data = FullscreenAdvertSerializer(advert).data

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_banner_adverts(request):
    adverts = BannerAdvert.objects.all()
    adverts_data = BannerAdvertSerializer(adverts, many=True).data

    return JsonResponse({"banner_adverts": adverts_data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_fullscreen_adverts(request):
    adverts = FullscreenAdvert.objects.all()
    adverts_data = FullscreenAdvertSerializer(adverts, many=True).data

    return JsonResponse({"banner_adverts": adverts_data})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_adview(request):
    user_id = request.data.get("userId")
    advert_id = request.data.get("adId")

    AdView.objects.create(user_id=user_id, advert_id=advert_id)

    return JsonResponse({"result": "ok"})