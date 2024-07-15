from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .models import Advert


@api_view(["GET"])
@permission_classes([AllowAny])
def get_advert(request):
    advert_id = request.data.get("adId")

    advert = Advert.objects.get(id=advert_id)

    return JsonResponse({"advert_id": advert.id,
                         "name": advert.name,
                         "description": advert.description,
                         "image": advert.image_path})
