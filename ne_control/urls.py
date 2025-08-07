from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage, name='manage'),
    path('general-list/', views.general_list, name='general-list'),
    path('list/', views.list, name='list'),
    path('show/<str:pk>/', views.show, name='show'),
]


