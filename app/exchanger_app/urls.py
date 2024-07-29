from django.urls import path
from . import views


urlpatterns = [
    path("", views.exchanger_home),
    path("execute_swap/", views.execute_swap, name="execute_swap"),
    path("execute_transfer/", views.execute_transfer, name="execute_transfer"),
    path("buy_vip/", views.buy_vip, name="buy_vip"),
    path("all_transactions/", views.get_all_transactions, name="all_transactions"),
    path("add_gnome/", views.buy_gnome, name='buy gnome')
]
