from django.shortcuts import render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from .games_handlers.GameFortune import GameFortune
from .models import LevelInfo, GameResults
from user_app.models import User, UserData
from .serializers import LevelInfoSerializer
from rest_framework.views import APIView

from rest_framework.decorators import api_view, permission_classes

from random import shuffle, randint


class LevelInfoAPIView(APIView):

    def get(self, request):
        w = LevelInfo.objects.all().values()
        return Response({'posts': LevelInfoSerializer(w, many=True).data})


# Fortune Level 1
@api_view(["GET"])
def fortune_start_game(request):
    return GameFortune().start(request.data.get('tg_user_id'))


@api_view(["GET"])
def fortune_get_game_result(request):
    return GameFortune().get(request.data.get("game_started_id"))
