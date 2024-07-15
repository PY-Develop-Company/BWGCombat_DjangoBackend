from rest_framework import serializers
from .models import Rank, Task, Reward, SocialMedia
from user_app.models import User, UsersTask


class SocialMediaTasksSerializer(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj:SocialMedia):
        return obj.id in self.context.get('completed_tasks')

    def get_amount(self, obj:SocialMedia):
        return obj.reward_amount
    

    class Meta:
        model = SocialMedia
        fields = ('name', 'link', 'amount', 'is_completed')


class RewardSerializer(serializers.ModelSerializer):
    reward_type = serializers.SerializerMethodField()

    def get_reward_type(self, obj):
        return obj.get_reward_type_display()

    class Meta:
        model = Reward
        fields = "__all__"


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


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


class TaskWithStatus(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj: Task):
        return UsersTasks.objects.filter(user_id=self.context['user_id'], task=obj).exists()

    class Meta:
        model = Task
        fields = ['id', 'name', 'is_completed']


class RankInfoSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = ['id', 'name', 'description', 'tasks']

    def get_tasks(self, obj):
        tasks = []
        initial_tasks = Task.objects.filter(rank=obj, initial=True).all()

        for i in initial_tasks:
            current_task = i
            temp_tasks = []
            while current_task:
                temp_tasks.append(TaskWithStatus(current_task, context=self.context).data)
                current_task = current_task.next_task
            tasks.append(temp_tasks)
        return tasks
