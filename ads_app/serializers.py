from rest_framework import serializers
from .models import BannerAdvert, FullscreenAdvert, AdView
# from app.user_app.models import Link


class BannerAdvertSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj: BannerAdvert):
        return obj.link.url

    class Meta:
        model = BannerAdvert
        fields = ("id", "name", "url", "relevant_region", "file_path")


class FullscreenAdvertSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    view_max_gold_reward = serializers.SerializerMethodField()
    view_min_gold_reward = serializers.SerializerMethodField()

    def get_url(self, obj: FullscreenAdvert):
        return obj.link.url

    def get_view_max_gold_reward(self, obj: FullscreenAdvert):
        return int(obj.view_max_gold_reward.amount)

    def get_view_min_gold_reward(self, obj: FullscreenAdvert):
        return int(obj.view_min_gold_reward.amount)


    class Meta:
        model = FullscreenAdvert
        fields = ("id", "name", "url", "is_video", "relevant_region", "file_path",
                  "view_max_gold_reward", "view_min_gold_reward", "view_gnome_reward", "gnome_probability")


class AdViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdView
        fields = "__all__"
