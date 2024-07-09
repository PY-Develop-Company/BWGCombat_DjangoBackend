from django.urls import path
from . import views


urlpatterns = [
    path("", views.exchanger_home),
    path("execute_swap/", views.execute_swap, name="execute_swap"),
]