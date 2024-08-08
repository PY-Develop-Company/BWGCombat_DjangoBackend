from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.links_home),
    path('track/<int:link_id>/', views.track_link_click, name='track_link_click')
]