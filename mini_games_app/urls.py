from django.urls import path
from . import views


urlpatterns = [
    path('', views.get),
    path('fortune/start', views.fortune_start_game),
    path('fortune/result', views.fortune_get_game_result)
]
