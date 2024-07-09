from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Advert


@api_view(["GET"])
@permission_classes([AllowAny])
def get_advert(request):
    advert_id = request.data.get("adId")

    advert = Advert.objects.get(id=advert_id)

    return JsonResponse({"advert_id": advert.id,
                         "name": advert.name,
                         "description": advert.description,
                         "image": advert.img_path})
