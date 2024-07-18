from django.urls import path
from . import views


urlpatterns = [
    path("get_advert/", views.get_advert, name="get_advert"),
    path("all_adverts/", views.get_all_adverts, name="get_all_adverts")
]
