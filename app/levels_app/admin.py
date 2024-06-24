from django.contrib import admin

from .models import Rank, Reward, Stage, Task


class RankAdmin(admin.ModelAdmin):
    list_display = ("name", "reward_id")
    list_select_related = ("reward_id",)

class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", 'reward_type')

class StageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "text", 'reward_id')


admin.site.register(Rank, RankAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Task, TaskAdmin)
