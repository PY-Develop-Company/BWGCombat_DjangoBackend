from rest_framework import serializers
from .models import Swap, Transfer, ExchangePair
from user_app.models import User, UserData


class SwapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swap
        fields = "__all__"


class TransferSerializer(serializers.ModelSerializer):
    receiver_username = serializers.SerializerMethodField()
    receiver_gender = serializers.SerializerMethodField()

    def get_receiver_username(self, obj: Transfer):
        return obj.user_2.tg_username

    def get_receiver_gender(self, obj: Transfer):
        userdata = UserData.objects.get(user_id=obj.user_2.tg_id)
        return userdata.character_gender

    class Meta:
        model = Transfer
        fields = ("user_1", "user_2", "asset", "fee", "amount", "time",
                  "receiver_username", "receiver_gender")


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangePair
        fields = "__all__"
