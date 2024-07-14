from django.urls import path
from . import views


urlpatterns = [
    path("get_advert/", views.get_advert, name="get_advert")
]
