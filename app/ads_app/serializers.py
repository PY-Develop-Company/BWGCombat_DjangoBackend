from rest_framework import serializers
from .models import Advert
# from app.user_app.models import Link


class AdvertSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj: Advert):
        return obj.link.url

    class Meta:
        model = Advert
        fields = ("id", "name", "url", "file_path")
