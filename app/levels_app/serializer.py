from rest_framework import serializers
from user_app.models import UsersTasks

from .models import Rank, TaskTemplate, TaskRoutes, Reward, SocialMedia


class SocialMediaTasksSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj: SocialMedia):
        return obj.id in self.context.get('completed_tasks')

    def get_amount(self, obj: SocialMedia):
        return obj.reward_amount

    class Meta:
        model = SocialMedia
        fields = ('name', 'link', 'amount', 'is_completed')


class RewardSerializer(serializers.ModelSerializer):
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
        model = TaskTemplate
        fields = ["name", "text", "rewards"]


class TaskForPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ('name', 'text')


class TaskWithStatus(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj: TaskTemplate):
        return UsersTasks.objects.filter(user_id=self.context['user_id'], task=obj).exists()

    class Meta:
        model = TaskTemplate
        fields = ['id', 'name', 'is_completed']


class ClosedRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ('id', 'name', 'description', 'gold_required')


class RankInfoSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = ['id', 'name', 'description', 'tasks']

    def get_tasks(self, obj):
        tasks = []
        initial_tasks = TaskTemplate.objects.filter(rank=obj, initial=True).all()

        for i in initial_tasks:
            current_task = i
            temp_tasks = []
            while current_task:
                temp_tasks.append(TaskWithStatus(current_task, context=self.context).data)
                current_task = current_task.next_task
            tasks.append(temp_tasks)
        return tasks


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRoutes


class TaskCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRoutes
        fields = ('coord_x', 'coord_y')


class TasksSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    x = serializers.SerializerMethodField()
    y = serializers.SerializerMethodField()
    rewards = serializers.SerializerMethodField()
    routes = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_name(self, obj: UsersTasks):
        return obj.task.template.name

    def get_x(self, obj: UsersTasks):
        return obj.task.coord_x

    def get_y(self, obj: UsersTasks):
        return obj.task.coord_y

    def get_type(self, obj):
        return obj.task.template.get_task_type_display()

    def get_rewards(self, obj: UsersTasks):
        return RewardSerializer(obj.rewards, many=True).data

    def get_status(self, obj: UsersTasks):
        return obj.get_status_display()

    def get_routes(self, obj: UsersTasks):
        if obj.status == UsersTasks.Status.COMPLETED:
            tsks = obj.task.get_subtasks()
            return TaskCoordinatesSerializer(tsks, many=True).data

    class Meta:
        model = UsersTasks
        fields = ('id', 'name', 'x', 'y', 'type', 'status', 'rewards', 'routes')
