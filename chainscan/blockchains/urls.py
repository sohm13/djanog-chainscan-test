from django.urls import path

from . import views

app_name = "blockchains"

urlpatterns = [
    path('', views.index, name='index'),
    path("bsc/", views.BscListView.as_view(), name='bsc-list'),
    path("bsc/pair-balances/", views.pair_balances, name='pair-balances'),
    path('bsc/<int:pk>/', views.BscDetailView.as_view(), name='bsc-detail'),
    path('bsc/pair-filter/', views.pair_balances, name='pair-filter'),

]