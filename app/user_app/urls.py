from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.user_home),
    path("home/", views.user_home, name="user_home"),
    path("add_user/", views.add_user, name="add_user"),
    path("get_info/", views.get_user_info, name="get_user_info"),
    path("add_coins/", views.add_coins_to_user, name="add_coins"),
    path("rem_coins/", views.remove_coins_from_user, name="rem_coins"),
    path('add_referral/', views.add_referral, name='add_referral'),
    path('get_user_referrals/', views.get_user_referrals, name='get_user_referrals')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
