from django.contrib import admin

from .models import (Rank, Reward, TaskTemplate, TaskRoute,
                     PartnersTasks, CompletedPartnersTasks, SocialTasks, CompletedSocialTasks,
                     Stage, StageTemplate)


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
admin.site.register(StageTemplate)
admin.site.register(Reward, RewardAdmin)
admin.site.register(TaskTemplate)
admin.site.register(TaskRoute)

admin.site.register(PartnersTasks)
admin.site.register(CompletedPartnersTasks)
admin.site.register(SocialTasks)
admin.site.register(CompletedSocialTasks)
