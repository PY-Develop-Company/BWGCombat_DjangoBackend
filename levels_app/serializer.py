from rest_framework import serializers
from user_app.models import UsersTasks

from .models import Rank, TaskTemplate, TaskRoute, Reward, PartnersTask, SocialTask, Stage
from links_app.serializer import LinkModelSerializer


class SocialTasksSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_name(self, obj: SocialTask):
        user_language = self.context.get('user_language')
        if user_language == 'en':
            return obj.name_en
        elif user_language == 'de':
            return obj.name_de
        elif user_language == 'fr':
            return obj.name_fr
        elif user_language == 'ru':
            return obj.name_ru
        elif user_language == 'uk':
            return obj.name_uk
        elif user_language == 'zh':
            return obj.name_zh
        raise TypeError("Unknown language: %s" % user_language)

    def get_is_completed(self, obj: SocialTask):
        return obj.id in self.context.get('completed_tasks')

    def get_amount(self, obj: SocialTask):
        return obj.reward_amount

    def get_link(self, obj: SocialTask):
        return LinkModelSerializer(obj.link).data

    class Meta:
        model = SocialTask
        fields = ('id', 'name', 'link', 'amount', 'is_completed')


class PartnersTasksSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    button_type = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_is_completed(self, obj: PartnersTask):
        return obj.id in self.context.get('completed_tasks')

    def get_amount(self, obj: PartnersTask):
        return obj.reward_amount

    def get_button_type(self, obj: PartnersTask):
        user_language = self.context.get('user_language')
        if user_language == 'en':
            return obj.button_type.name_en
        elif user_language == 'de':
            return obj.button_type.name_de
        elif user_language == 'fr':
            return obj.button_type.name_fr
        elif user_language == 'ru':
            return obj.button_type.name_ru
        elif user_language == 'uk':
            return obj.button_type.name_uk
        elif user_language == 'zh':
            return obj.button_type.name_zh
        raise TypeError("Unknown language: %s" % user_language)

    def get_link(self, obj: SocialTask):
        return LinkModelSerializer(obj.link).data

    class Meta:
        model = PartnersTask
        fields = ('id', 'name', 'button_type', 'link', 'amount', 'is_completed')


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "instrument", "drink"]


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


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRoute


class TaskCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRoute
        fields = ('coord_x', 'coord_y')


class TasksSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    x = serializers.SerializerMethodField()
    y = serializers.SerializerMethodField()
    rewards = serializers.SerializerMethodField()
    routes = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

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
        if obj.status == UsersTasks.Status.CLAIMED:
            tsks = obj.task.get_subtasks()
            return TaskCoordinatesSerializer(tsks, many=True).data

    def get_price(self, obj: UsersTasks):
        return obj.task.template.price

    class Meta:
        model = UsersTasks
        fields = ('id', 'name', 'x', 'y', 'type', 'price', 'status', 'rewards', 'routes')
