from django.urls import path
from . import views


urlpatterns = [
    path('', views.tank_dashboard, name='tank_dashboard'),
    path('logs/', views.log_view, name='log_view'),
    path('set-temperature/<str:tank_name>/', views.set_target_temperature, name='set_target_temperature'),
]
