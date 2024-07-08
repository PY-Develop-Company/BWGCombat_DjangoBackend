from rest_framework import serializers
from .models import Rank, Task, Reward, SocialMedia
from user_app.models import User, UsersTasks

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