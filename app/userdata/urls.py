from django.urls import path

from . import views


urlpatterns = [   
    path("get_info/", views.get_user_info, name="get_user_info"),
    path("add_coins/", views.add_coins_to_user, name="add-coins"),
]