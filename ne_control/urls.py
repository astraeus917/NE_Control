from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.import_csv, name='import'),
    path('general-list/', views.general_list, name='general-list'),
    path('list/', views.list, name='list'),
    path('show/<str:pk>/', views.show, name='show'),
]


