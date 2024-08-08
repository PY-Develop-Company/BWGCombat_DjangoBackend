from django.urls import path
from . import views


urlpatterns = [
    path("", views.levels_home),
    path("next_rank/", views.go_to_next_rank, name="move_to_other_rank"),
    path("next_stage/", views.go_to_next_stage, name='move_to_next_stage'),

    path('get_user_current_stage_info/', views.get_user_current_stage_info, name='stage_tasks'),
    path('buy_task/', views.buy_task_view, name='buy_task'),
    path('claim_task/', views.claim_task_rewards_view, name='claim_task'),

    path('social_tasks/', views.get_social_tasks, name='get_social_media_tasks'),
    path('partner_tasks/', views.get_partner_tasks, name='get_social_media_tasks'),
    path('check_social_task/', views.complete_social_task, name='get_social_media_tasks'),
    path('check_partner_task/', views.complete_partner_task, name='get_social_media_tasks'),
]
