from django.urls import path

from . import views

app_name = "blockchains"

urlpatterns = [
    path('', views.index, name='index'),
    path("compare/", views.compare_view, name='compare-view'),
    path("bsc/", views.BscListView.as_view(), name='bsc-list'),
    path('bsc/<int:pk>/', views.bsc_pair_detail, name='bsc-detail'),

    path("aurora/", views.AuroraListView.as_view(), name='aurora-list'),
    path('aurora/<int:pk>/', views.aurora_pair_detail, name='aurora-detail'),

]