from django.shortcuts import render
from core.models import Tank

def tank_dashboard(request):
    """
    Displays the dashboard with tanks, their temperatures, and valve states.
    """
    tanks = Tank.objects.select_related('sensor', 'valve').all()
    context = {
        'tanks': tanks,
    }
    return render(request, 'dashboard/tank_dashboard.html', context)
