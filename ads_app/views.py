from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

import random

from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q

from .models import BannerAdvert, FullscreenAdvert, AdView, BannerAdLinkClick, FullscreenAdLinkClick, AdSet
from .serializers import BannerAdvertSerializer, FullscreenAdvertSerializer
from .utils import get_random_gold_reward


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

    ad_set = AdSet.objects.get(fullscreen=advert)
    if not ad_set.is_active:
        return JsonResponse({"result": "the ad set which the requested ad belongs to is disabled, "
                                       "most commonly because of reaching clicks goal"})

    advert_data = FullscreenAdvertSerializer(advert).data
    advert_data['random_gold_reward'] = get_random_gold_reward(advert)

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_random_fullscreen_advert(request):
    fullscreen_ads_ids = FullscreenAdvert.objects.filter().all().values_list('id', flat=True)


    try:
        advert = FullscreenAdvert.objects.get(id=random.choice(fullscreen_ads_ids))
    except FullscreenAdvert.DoesNotExist:
        return JsonResponse({"result": "unexpected absence of the advert"})

    advert_data = FullscreenAdvertSerializer(advert).data
    advert_data['random_gold_reward'] = get_random_gold_reward(advert)

    return JsonResponse(advert_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_banner_adverts(request):
    adverts = BannerAdvert.objects.all()
    adverts_data = BannerAdvertSerializer(adverts, many=True).data

    return JsonResponse({"banner_adverts": adverts_data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_active_banner_adverts(request):
    active_adverts = BannerAdvert.objects.filter(adset__is_active=True)
    active_adverts_data = BannerAdvertSerializer(active_adverts, many=True).data
    return JsonResponse({"active_banner_adverts": active_adverts_data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_fullscreen_adverts(request):
    adverts = FullscreenAdvert.objects.all()
    adverts_data = FullscreenAdvertSerializer(adverts, many=True).data

    return JsonResponse({"banner_adverts": adverts_data})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_active_fullscreen_adverts(request):
    active_adverts = FullscreenAdvert.objects.filter(adset__is_active=True)
    active_adverts_data = FullscreenAdvertSerializer(active_adverts, many=True).data
    return JsonResponse({"active_banner_adverts": active_adverts_data})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_adview(request):
    user_id = request.data.get("userId")
    advert_id = request.data.get("adId")

    AdView.objects.create(user_id=user_id, advert_id=advert_id)

    return JsonResponse({"result": "ok"})


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register_fullscreen_adclick(request, ad_id):
    user_id = request.data.get("userId")
    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    fullscreen_advert = FullscreenAdvert.objects.get(id=ad_id)
    FullscreenAdLinkClick.objects.create(user_id=user_id, advert=fullscreen_advert)

    ad_set = AdSet.objects.get(fullscreen=fullscreen_advert)
    ad_set.current_clicks_number += 1
    ad_set.save()
    ad_set.disable_if_goal_reached()

    return redirect(fullscreen_advert.link.url)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register_banner_adclick(request, ad_id):
    user_id = request.data.get("userId")
    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    banner_advert = BannerAdvert.objects.get(id=ad_id)
    BannerAdLinkClick.objects.create(user_id=user_id, advert=banner_advert)

    ad_set = AdSet.objects.get(banner=banner_advert)
    ad_set.current_clicks_number += 1
    ad_set.save()
    ad_set.disable_if_goal_reached()

    return redirect(banner_advert.link.url)
