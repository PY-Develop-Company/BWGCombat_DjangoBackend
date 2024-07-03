from .models import User, Language
from django.contrib import admin
from .models import UserData, UsersTasks, Fren


class UserDataAdmin(admin.ModelAdmin):
    list_display = ("user_id", "gold_balance", "g_token", "rank")
    list_select_related = ("rank",)


class UserTasksAdmin(admin.ModelAdmin):
    list_display = ("user", "task")


class FrenAdmin(admin.ModelAdmin):
    list_display = ("inviter_tg", "fren_tg")


admin.site.register(User)
admin.site.register(Language)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(UsersTasks, UserTasksAdmin)
admin.site.register(Fren, FrenAdmin)
