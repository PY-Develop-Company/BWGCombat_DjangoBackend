from django.contrib import admin

from .models import (Rank, Reward, TaskTemplate, TaskRoute,
                     PartnersTask, CompletedPartnersTask, SocialTask, CompletedSocialTask,
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

admin.site.register(PartnersTask)
admin.site.register(CompletedPartnersTask)
admin.site.register(SocialTask)
admin.site.register(CompletedSocialTask)
