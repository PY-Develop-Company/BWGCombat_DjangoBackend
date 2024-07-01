from django.urls import path
from . import views


urlpatterns = [
    path("", views.levels_home),
    path("next_stage/", views.go_to_next_rank, name="move_to_other_stage"),
    path("task_submission/", views.request_task_submission, name='task_submission')
]
