from django.urls import path
from . import views

urlpatterns = [
    path('', views.tank_dashboard, name='tank_dashboard'),
]