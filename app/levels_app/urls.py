from django.urls import path
from . import views


urlpatterns = [
    path("", views.levels_home),
    path("next_rank/", views.go_to_next_rank, name="move_to_other_rank"),
    path('get_rank_info/', views.get_rank_info, name='rank_information'),
    path('sm_ts/', views.get_social_media_tasks, name='get_social_media_tasks'),
]
