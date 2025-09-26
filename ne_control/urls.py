from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage, name='manage'),
    path('list/', views.list, name='list'),
    path('control/', views.control, name='control'),
    path('show/<str:pk>/', views.show, name='show'),
    path('user/edit/<str:pk>', views.user_edit, name='user-edit'),
    path('workplace/edit/<str:pk>', views.workplace_edit, name='workplace-edit'),
]


