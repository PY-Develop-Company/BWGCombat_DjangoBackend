from .models import User, Language
from django.contrib import admin
from .models import UserData


class UserDataAdmin(admin.ModelAdmin):
    list_display = ("user_id", "gold_balance", "g_token", "rank_id", "stage_id")
    list_select_related = ("rank_id",)


admin.site.register(User)
admin.site.register(Language)
admin.site.register(UserData, UserDataAdmin)

