from django.urls import path
from . import views

urlpatterns = [
    path('', views.empty_view, name='empty_view'),
    path('first/', views.first_view, name='first_view'),
    path('second/', views.second_view, name='second_view'),
    path('hello/', views.hello_view, name='hello_view'),
]