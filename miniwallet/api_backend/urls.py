from django.urls import path,include
from . import views

urlpatterns = [
    path('init', views.Main_class.as_view()),
    path('wallet', views.Wallet_view.as_view()),
    path('deposits', views.Topup_view.as_view()),
    path('withdrawals', views.Transfer_view.as_view())
]