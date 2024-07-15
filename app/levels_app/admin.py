from django.contrib import admin

from .models import Rank, Reward, TaskTemplate, TaskRoutes, MaxEnergyLevel, MulticlickLevel, PassiveIncomeLevel, SocialMedia, CompletedSocialTasks, Stage, StageTemplate


class RankAdmin(admin.ModelAdmin):
    list_display = ("name",)


class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "reward_type")


class StageAdmin(admin.ModelAdmin):
    list_display = ("name",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "text")


admin.site.register(Rank, RankAdmin)
admin.site.register(Stage)
admin.site.register(Reward, RewardAdmin)
admin.site.register(TaskTemplate)
admin.site.register(TaskRoutes)
admin.site.register(MaxEnergyLevel)
admin.site.register(MulticlickLevel)
admin.site.register(PassiveIncomeLevel)
admin.site.register(SocialMedia)
admin.site.register(CompletedSocialTasks)
admin.site.register(StageTemplate)