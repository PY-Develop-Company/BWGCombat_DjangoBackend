from django.contrib import admin

from .models import Rank, Reward, Task, EnergyLevel, MultiplierLevel, PassiveIncomeLevel, SocialMedia, CompletedSocialTasks


class RankAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # list_select_related = ("rewards",)


class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "reward_type")


class StageAdmin(admin.ModelAdmin):
    list_display = ("name",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "text")


admin.site.register(Rank, RankAdmin)
admin.site.register(Reward, RewardAdmin)
# admin.site.register(Stage, StageAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(EnergyLevel)
admin.site.register(MultiplierLevel)
admin.site.register(PassiveIncomeLevel)
admin.site.register(SocialMedia)
admin.site.register(CompletedSocialTasks)