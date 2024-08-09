from django.contrib import admin

from .models import LevelInfo, GameResults, GameStarted

admin.site.register(LevelInfo)
admin.site.register(GameResults)
admin.site.register(GameStarted)