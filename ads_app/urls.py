from django.urls import path
from . import views


urlpatterns = [
    path("get_banner_advert/", views.get_banner_advert, name="get_banner_advert"),
    path("get_fullscreen_advert/", views.get_fullscreen_advert, name="get_fullscreen_advert"),
    path("get_random_fullscreen_advert/", views.get_random_fullscreen_advert, name="get_random_fullscreen_advert"),
    path("all_banner_adverts/", views.get_all_banner_adverts, name="get_all_banner_adverts"),
    path("all_fullscreen_adverts/", views.get_all_fullscreen_adverts, name="all_fullscreen_adverts"),
    path("register_adview/", views.register_adview, name="register_adview"),
    path("track_fullscreen_ad/<int:ad_id>/", views.register_fullscreen_adclick, name="register_fullscreen_adclick"),
    path("track_banner_ad/<int:ad_id>/", views.register_banner_adclick, name="register_banner_adclick")
]
