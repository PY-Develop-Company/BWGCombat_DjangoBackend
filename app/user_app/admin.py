from .models import User, Language
from django.contrib import admin
from .models import UserData, User_tasks, Fren


class UserDataAdmin(admin.ModelAdmin):
    list_display = ("user_id", "gold_balance", "g_token", "rank_id", "stage_id")
    list_select_related = ("rank_id",)


class UserTasksAdmin(admin.ModelAdmin):
    list_display = ("user", "task")


class FrenAdmin(admin.ModelAdmin):
    list_display = ("inviter_tg", "fren_tg")


admin.site.register(User)
admin.site.register(Language)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(User_tasks, UserTasksAdmin)
admin.site.register(Fren, FrenAdmin)
