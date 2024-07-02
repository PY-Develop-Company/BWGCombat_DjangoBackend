from django.urls import path
from . import views


urlpatterns = [
    path("", views.levels_home),
    path("next_rank/", views.go_to_next_rank, name="move_to_other_rank"),
    path("next_stage/", views.go_to_next_stage, name="go_to_next_stage"),
]
