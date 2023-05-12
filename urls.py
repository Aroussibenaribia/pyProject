from django.urls import path
from . import views

urlpatterns = [
    path('smartphones/', views.smartphone_list, name='smartphone_list'),
]
