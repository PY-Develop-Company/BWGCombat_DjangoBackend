from django.urls import path
from . import views


urlpatterns = [path("", views.clicker_home)]
