from django.urls import path
from . import views
from .views import LevelInfoAPIView


urlpatterns = [
    path('', LevelInfoAPIView.as_view()),
    path('fortune/start', views.fortune_start_game),
    path('fortune/result', views.fortune_get_game_result)
]
