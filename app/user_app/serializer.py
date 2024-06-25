from rest_framework import serializers
from .models import UserData
from levels_app.models import Rank, Stage, Task, Reward
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['tg_username'] = user.tg_username
        token['tg_id'] = user.tg_id

        return token



class RewardRelatedField(serializers.RelatedField):
    def to_representation(self, obj:Reward):
        return obj.amount


class User_data_Serializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()

    def get_rank(self, obj:UserData):
        return RankingSerializer(obj.rank_id).data
    
    def get_stage(self, obj:UserData):
        return StageSerializer(obj.stage_id).data

    class Meta:
        model = UserData
        fields = (
            "user_id",
            "gold_balance",
            "g_token",
            "last_visited",
            "rank",
            "stage",
            "click_multiplier",
            "energy"
        )



class RankingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank
        fields = "__all__"


class StageSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()


    def get_tasks(self, obj:Stage):
        return TaskSerializer(obj.tasks_id, many=True).data

    class Meta:
        model = Stage
        fields = ['name', 'next_rank', 'tasks']


class TaskSerializer(serializers.ModelSerializer):
    reward_id = RewardRelatedField(read_only = True)

    class Meta:
        model = Task
        fields = ['name', 'text', 'reward_id']
