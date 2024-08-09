from rest_framework import serializers
from .models import LevelInfo
from django.db import models


class LevelInfoSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    name = serializers.CharField()

    # загальна кількість можливих варіантів
    total_count = serializers.IntegerField()
    # сума яку можна виграти
    win = serializers.IntegerField()
    # мінімальна кількість сум виграш
    win_count_min = serializers.IntegerField()
    # сума яку можна програти
    lost = serializers.IntegerField()
    # мінімальна кількість сум прогаш
    lost_count_min = serializers.IntegerField()
    # проставлення якщо не вистачає True - виграш, False - програш
    if_not_enough = serializers.BooleanField()
    # сума спроби
    amount_attempted = serializers.IntegerField()

    # for gnome
    gnome_chance = serializers.IntegerField()
    gnome_chance_max = serializers.IntegerField()

    class Meta:
        model = LevelInfo
        fields = "__all__"
