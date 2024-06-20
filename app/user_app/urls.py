from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_home),
    path('home/', views.user_home),
    path('add_user/', views.add_user, name='add_user'),
]
