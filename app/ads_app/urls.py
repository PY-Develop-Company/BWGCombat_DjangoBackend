from django.urls import path
from . import views


urlpatterns = [
    path("get_advert/", views.get_advert, name="get_advert"),
    path("get_fullscreen_advert/", views.get_fullscreen_advert, name="get_fullscreen_advert"),
    path("get_random_fullscreen_advert/", views.get_random_fullscreen_advert, name="get_random_fullscreen_advert"),
    path("all_banner_adverts/", views.get_all_banner_adverts, name="get_all_banner_adverts")
]
