from django.urls import path
from dashboard.views import (
    tank_dashboard,
    temperature_graph,
    log_view,
    set_target_temperature,
    system_status,
    deactivate_alarm,
)

urlpatterns = [
    path('', tank_dashboard, name='tank_dashboard'),  # Root dashboard
    path('logs/', log_view, name='log_view'),
    path('set-temperature/<str:tank_name>/', set_target_temperature, name='set_target_temperature'),
    path('system-status/', system_status, name='system_status'),
    path('deactivate-alarm/', deactivate_alarm, name='deactivate_alarm'),
    path('dashboard/graph/<str:tank_name>/', temperature_graph, name='temperature_graph'),
]