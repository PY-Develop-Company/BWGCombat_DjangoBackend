from rest_framework import serializers
from .models import UserData


class User_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = (
            "user_id",
            "gold_balance",
            "g_token",
            "last_visited",
            "rank_id",
            "stage_id",
        )
