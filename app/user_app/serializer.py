from rest_framework import serializers
from .models import UserData
from levels_app.models import Rank, Task, Reward, MaxEnergyLevel, MulticlickLevel
from levels_app.serializer import RankInfoSerializer, RankingSerializer, RewardSerializer, TaskSerializer
from user_app.models import User, UsersTasks
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


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
    passive_income = serializers.SerializerMethodField()
    is_picked_gender = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    lang_code = serializers.SerializerMethodField()



    def get_click_multiplier(self, obj:UserData):
        return MultiplierSerializer(obj.multiclick_level).data

    def get_passive_income(self, obj:UserData):
        return EnergySerializer(obj.passive_income_level).data

    def get_energy(self, obj:UserData):
        return EnergySerializer(obj.max_energy_level).data

    def get_rank(self, obj: UserData):
        return RankingSerializer(obj.rank).data

    def get_username(self, obj: UserData):
        return User.objects.get(tg_id=obj.user_id.tg_id).tg_username
    
    def get_is_picked_gender(self, obj:UserData):
        return obj.character_gender is not None
    
    def get_gender(self, obj: UserData):
        return obj.character_gender
    
    def get_lang_code(self, obj: UserData):
        return obj.user_id.interface_lang.lang_code
    


    class Meta:
        model = UserData
        fields = (
            "user_id",
            "is_picked_gender",
            "gender",
            "lang_code",
            "username",
            "gold_balance",
            "g_token",
            "last_visited",
            "rank",
            # "stage",
            "click_multiplier",
            "energy",
            "energy_regeneration",
            "current_energy",
            "passive_income",
        )

class ClickSerializer(serializers.ModelSerializer):

    click_multiplier = serializers.SerializerMethodField()
    energy = serializers.SerializerMethodField()
    passive_income = serializers.SerializerMethodField()

    def get_click_multiplier(self, obj:UserData):
        return MultiplierSerializer(obj.multiclick_level).data

    def get_passive_income(self, obj:UserData):
        return EnergySerializer(obj.passive_income_level).data

    def get_energy(self, obj:UserData):
        return EnergySerializer(obj.max_energy_level).data


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

    def get_tg_username(self, obj:UserData):
        return obj.user_id.tg_username
    
    def get_passive_income(self, obj:UserData):
        return obj.passive_income_level.amount
        
    
    class Meta:
        model = UserData
        fields = ('tg_username', 'g_token', 'rank', 'passive_income', 'character_gender')