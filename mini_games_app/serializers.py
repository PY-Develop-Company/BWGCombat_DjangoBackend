from rest_framework import serializers
from .models import LevelInfo
from django.db import models


class LevelInfoSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = LevelInfo
        fields = "__all__"
