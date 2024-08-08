from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from links_app.models import Link, LinkClick


def links_home(request):
    return HttpResponse("links home")


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def track_link_click(request, link_id):
    user_id = request.data.get("userId")
    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    link = get_object_or_404(Link, id=link_id)
    LinkClick.objects.create(user_id=user_id, link=link)

    return redirect(link.url)
