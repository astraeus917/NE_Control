from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('list/', views.list, name='list'),
    path('show/', views.show, name='show'),
]


