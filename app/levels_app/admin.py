from django.contrib import admin

from .models import Rank, Reward, Stage, Task


class RankAdmin(admin.ModelAdmin):
    list_display = ("name", "reward_id")
    list_select_related = ("reward_id",)


class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "amount")


admin.site.register(Rank, RankAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Stage)
admin.site.register(Task)
