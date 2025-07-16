from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.index, name='import'),
    path('list/', views.list, name='list'),
    path('show/', views.show, name='show'),
]


