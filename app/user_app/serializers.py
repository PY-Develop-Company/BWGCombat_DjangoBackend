from rest_framework import serializers
from .models import UserData
from levels_app.models import Rank, TaskTemplate, TaskRoutes, Reward, MaxEnergyLevel, MulticlickLevel
from levels_app.serializer import RankInfoSerializer, RankingSerializer, RewardSerializer, TaskSerializer
from user_app.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_app.utils import get_gnome_reward


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class EnergySerializer(serializers.ModelSerializer):

    class Meta: 
        model = MaxEnergyLevel
        fields = ('id', 'amount')


class MultiplierSerializer(serializers.ModelSerializer):

    class Meta: 
        model = MaxEnergyLevel
        fields = ('id', 'amount')


class UserDataSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    # stage = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    click_multiplier = serializers.SerializerMethodField()
    energy = serializers.SerializerMethodField()
    is_picked_gender = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    lang_code = serializers.SerializerMethodField()

    def get_click_multiplier(self, obj: UserData):
        return obj.multiclick_amount

    def get_energy(self, obj: UserData):
        return obj.max_energy_amount

    def get_rank(self, obj: UserData):
        return RankingSerializer(obj.rank).data

    def get_username(self, obj: UserData):
        return User.objects.get(tg_id=obj.user.tg_id).tg_username

    def get_is_picked_gender(self, obj: UserData):
        return obj.character_gender is not None

    def get_gender(self, obj: UserData):
        return obj.character_gender

    def get_lang_code(self, obj: UserData):
        return obj.user.interface_lang.lang_code

    class Meta:
        model = UserData
        fields = (
            "user_id",
            "is_picked_gender",
            "gender",
            "username",
            "gold_balance",
            "g_token",
            "last_visited",
            "rank",
            "current_stage",
            "click_multiplier",
            "energy",
            "energy_regeneration",
            "current_energy",
            "gnome_amount",
            "lang_code",
            "visual_effects",
            "general_volume",
            "effects_volume",
            "music_volume"
        )


class UserSettingsSerializer(serializers.ModelSerializer):
    lang_code = serializers.SerializerMethodField()

    def get_lang_code(self, obj: UserData):
        return obj.user.interface_lang.lang_code

    class Meta:
        model = UserData
        fields = (
            "lang_code",
            "visual_effects",
            "general_volume",
            "effects_volume",
            "music_volume"
        )


class ClickSerializer(serializers.ModelSerializer):

    click_multiplier = serializers.SerializerMethodField()
    energy = serializers.SerializerMethodField()
    passive_income = serializers.SerializerMethodField()

    def get_click_multiplier(self, obj: UserData):
        return obj.multiclick_amount

    def get_passive_income(self, obj: UserData):
        return obj.gnome_amount
    
    def get_energy(self, obj: UserData):
        return obj.max_energy_amount

    class Meta:
        model = UserData
        fields = (
            "user_id",
            "gold_balance",
            "g_token",
            "click_multiplier",
            "energy",
            "energy_regeneration",
            "current_energy",
            "passive_income",
            )


class ReferralsSerializer(serializers.ModelSerializer):
    tg_username = serializers.SerializerMethodField()
    passive_income = serializers.SerializerMethodField()

    def get_tg_username(self, obj: UserData):
        return obj.user.tg_username
    
    def get_passive_income(self, obj: UserData):
        return obj.gnome_amount * get_gnome_reward()
    
    class Meta:
        model = UserData
        fields = ('tg_username', 'g_token', 'rank', 'passive_income', 'character_gender')