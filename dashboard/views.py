from django.shortcuts import render, get_object_or_404, redirect
from core.models import Tank, Log


def tank_dashboard(request):
    """
    Displays the dashboard with tanks, their temperatures, and valve states.
    """
    tanks = Tank.objects.select_related('sensor', 'valve').all()
    context = {
        'tanks': tanks,
    }
    return render(request, 'dashboard/tank_dashboard.html', context)


def log_view(request):
    """
    Displays a list of recent logs.
    """
    logs = Log.objects.select_related('tank').order_by('-timestamp')[:50]
    context = {
        'logs': logs,
    }
    return render(request, 'dashboard/logs.html', context)


def set_target_temperature(request, tank_name):
    """
    Allows the user to set the target temperature for a tank using its name.
    """
    tank = get_object_or_404(Tank, name=tank_name)
    if request.method == 'POST':
        target_temp = float(request.POST.get('target_temperature', tank.target_temperature))
        tank.target_temperature = target_temp
        tank.save()
        return redirect('tank_dashboard')
    context = {
        'tank': tank,
    }
    return render(request, 'dashboard/set_temperature.html', context)

