from rest_framework import serializers
from .models import UserData
from levels_app.models import Rank, Task, Reward, EnergyLevel, MultiplierLevel
from user_app.models import User, UsersTasks
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


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

class EnergySerializer(serializers.ModelSerializer):

    class Meta: 
        model = EnergyLevel
        fields = ('id', 'amount')


class MultiplierSerializer(serializers.ModelSerializer):

    class Meta: 
        model = EnergyLevel
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



    def get_click_multiplier(self, obj:UserData):
        return MultiplierSerializer(obj.click_multiplier).data

    def get_passive_income(self, obj:UserData):
        return EnergySerializer(obj.passive_income).data

    def get_energy(self, obj:UserData):
        return EnergySerializer(obj.max_energy).data

    def get_rank(self, obj: UserData):
        return RankingSerializer(obj.rank_id).data

    # def get_stage(self, obj: UserData):
    #     return StageSerializer(obj.stage_id, context = {"user_id": obj.user_id}).data

    def get_username(self, obj: UserData):
        return User.objects.get(tg_id=obj.user_id.tg_id).tg_username
    
    def get_is_picked_gender(self, obj:UserData):
        return obj.character_gender is not None
    
    def get_gender(self, obj: UserData):
        return obj.character_gender
    


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
            # "stage",
            "click_multiplier",
            "energy",
            "energy_regeneration",
            "current_energy",
            "passive_income",
        )


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


# class StageSerializer(serializers.ModelSerializer):
#     tasks = serializers.SerializerMethodField()
#
#     def get_tasks(self, obj: Stage):
#         user = self.context['user_id']
#         completed_tasks_ids = UsersTasks.objects.filter(user_id=user, task__in=obj.tasks_id.all()).values_list('task_id', flat=True)
#         incomplete_tasks = obj.tasks_id.exclude(id__in=completed_tasks_ids)
#         return TaskSerializer(incomplete_tasks, many=True).data
#
#     class Meta:
#         model = Stage
#         fields = ["id", "name", "tasks", 'next_stage']


class TaskSerializer(serializers.ModelSerializer):
    rewards = serializers.SerializerMethodField()

    def get_rewards(self):
        return RewardSerializer(self.rewards, many=True).data

    class Meta:
        model = Task
        fields = ["name", "text", "rewards"]


class TaskForPreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'text')


# class StageInfo(serializers.ModelSerializer):
#     completed_tasks = serializers.SerializerMethodField()
#     incompleted_tasks = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Stage
#         fields = ('name', 'completed_tasks', 'incompleted_tasks')
#
#     def get_completed_tasks(self, obj):
#         user_id = self.context['user_id']
#         completed_tasks_ids = UsersTasks.objects.filter(user_id=user_id, task__in=obj.tasks_id.all()).values_list('task_id', flat=True)
#         completed_tasks = Task.objects.filter(id__in=completed_tasks_ids)
#         return TaskForPreviewSerializer(completed_tasks, many=True).data
#
#     def get_incompleted_tasks(self, obj):
#         user_id = self.context['user_id']
#         completed_tasks_ids = UsersTasks.objects.filter(user_id=user_id, task__in=obj.tasks_id.all()).values_list('task_id', flat=True)
#         incomplete_tasks = obj.tasks_id.exclude(id__in=completed_tasks_ids)
#         return TaskForPreviewSerializer(incomplete_tasks, many=True).data


class RankInfoSerializer(serializers.ModelSerializer):
    # stage = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = ('name', 'description', 'gold_required')

#     def get_stage(self, obj):
#         print(self.context.get('stage_id'))
#         stage = get_object_or_404(Stage, id = self.context.get('stage_id'))
#         return StageInfo(stage, context=self.context).data
    

class ClickSerializer(serializers.ModelSerializer):

    click_multiplier = serializers.SerializerMethodField()
    energy = serializers.SerializerMethodField()
    passive_income = serializers.SerializerMethodField()

    def get_click_multiplier(self, obj:UserData):
        return MultiplierSerializer(obj.click_multiplier).data

    def get_passive_income(self, obj:UserData):
        return EnergySerializer(obj.passive_income).data

    def get_energy(self, obj:UserData):
        return EnergySerializer(obj.max_energy).data


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
