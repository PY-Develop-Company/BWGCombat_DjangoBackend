from django.urls import path
from . import views


urlpatterns = [
    path("", views.levels_home),
    path("next_rank/", views.go_to_next_rank, name="move_to_other_rank"),
    path("next_stage/", views.go_to_next_stage, name='move_to_next_stage'),
    path('get_user_current_stage_info/', views.get_user_current_stage_info, name='stage_tasks'),
    path('social_tasks/', views.get_social_media_tasks, name='get_social_media_tasks'),
    path('partner_tasks/', views.get_partner_tasks, name='get_social_media_tasks'),
    path('social_task_checker/', views.complete_partner_task, name='get_social_media_tasks'),
    path('check_task/', views.check_task_completion, name='check_task_state'),
]
