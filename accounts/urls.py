from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.access_login, name='access_login'),
    path('register/user', views.register_user, name='register_user'),
    path('logout/', views.logout, name='logout'),
]


