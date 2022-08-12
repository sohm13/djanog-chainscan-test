from django.urls import path

from . import views

app_name = "blockchains"

urlpatterns = [
    path('', views.index, name='index'),
    path("compare/", views.compare_view, name='compare-view'),
    path("bsc/", views.BscListView.as_view(), name='bsc-list'),
    path('bsc/<int:pk>/', views.bsc_pair_detail, name='bsc-detail'),

]