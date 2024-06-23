from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_home),
    path('home/', views.user_home, name='user_home'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_referal/', views.add_referral, name='add_referral'),
    path('get_user_referrals/', views.get_user_referrals, name='get_user_referrals')
]
