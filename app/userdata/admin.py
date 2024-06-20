from django.contrib import admin
from .models import UserData, Rank, Reward, Stage, Task

# Register your models here.


class UserDataAdmin(admin.ModelAdmin):
    list_display = ("user_id", "gold_balance", "g_token", "rank_id", "stage_id")
    list_select_related = ("rank_id",)


class RankAdmin(admin.ModelAdmin):
    list_display = ("name", "reward_id")
    list_select_related = ("reward_id",)


class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "amount")


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Stage)
admin.site.register(Task)
