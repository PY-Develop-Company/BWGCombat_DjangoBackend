from rest_framework import serializers
from .models import UserData
from levels_app.models import Rank, Stage, Task, Reward
from user_app.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class RewardSerializer(serializers.ModelSerializer):
    reward_type = serializers.SerializerMethodField()

    def get_reward_type(self, obj):
        return obj.get_reward_type_display()

    class Meta:
        model = Reward
        fields = "__all__"


class User_data_Serializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_rank(self, obj: UserData):
        return RankingSerializer(obj.rank_id).data

    def get_stage(self, obj: UserData):
        return StageSerializer(obj.stage_id).data

    def get_username(self, obj: UserData):
        return User.objects.get(tg_id=obj.user_id.tg_id).tg_username

    class Meta:
        model = UserData
        fields = (
            "user_id",
            "username",
            "gold_balance",
            "g_token",
            "last_visited",
            "rank",
            "stage",
            "click_multiplier",
            "energy",
        )


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class StageSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj: Stage):
        return TaskSerializer(obj.tasks_id, many=True).data

    class Meta:
        model = Stage
        fields = ["name", "tasks"]


class TaskSerializer(serializers.ModelSerializer):
    reward = serializers.SerializerMethodField()

    def get_reward(self, obj: Stage):
        return RewardSerializer(obj.reward_id).data

    class Meta:
        model = Task
        fields = ["name", "text", "reward"]
