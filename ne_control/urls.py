from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.import_csv, name='import'),
    path('list/', views.list, name='list'),
    path('show/<str:pk>/', views.show, name='show'),
]


