from django.shortcuts import render, get_object_or_404, redirect
from core.models import Tank, Log, DigitalInput, Relay
from api.evok_client import EvokClient
import plotly.graph_objects as go


def temperature_graph(request, tank_name):
    """
    Generates a temperature history graph for the given tank.
    """
    tank = Tank.objects.get(name=tank_name)
    logs = Log.objects.filter(tank=tank).order_by('timestamp')

    timestamps = [log.timestamp for log in logs]
    temperatures = [log.temperature for log in logs if log.temperature is not None]

    # Create Plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=temperatures,
        mode='lines+markers',
        name='Temperature'
    ))
    fig.update_layout(
        title=f"Temperature History for {tank.name}",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        template="plotly_white"
    )

    # Render the graph as a div
    graph_div = fig.to_html(full_html=False)

    return render(request, 'dashboard/temperature_graph.html', {
        'tank': tank,
        'graph_div': graph_div
    })


def tank_dashboard(request):
    """
    Displays the tank dashboard with current temperature data.
    """
    tanks = Tank.objects.select_related('sensor').all()
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


def system_status(request):
    """
    Displays the current status of the system (digital inputs and relays).
    Displays the current status of the system, including alarm state.
    """
    inputs = DigitalInput.objects.all()
    relays = Relay.objects.all()
    # Get the state of Total Stop
    total_stop = DigitalInput.objects.get(name="Total_Stop_DI").state
    # Get the alarm state
    alarm_relay = Relay.objects.get(name="Alarm_Relay")
    alarm_active = alarm_relay.is_active
    context = {
        'inputs': inputs,
        'relays': relays,
        'total_stop': total_stop,
        'alarm_active': alarm_active,
    }
    return render(request, 'dashboard/system_status.html', context)


def deactivate_alarm(request):
    """
    Deactivates the alarm manually.
    """
    if request.method == "POST":
        alarm_relay = Relay.objects.get(name="Alarm_Relay")
        alarm_relay.is_active = False
        alarm_relay.save()

        client = EvokClient()
        client.set_relay(alarm_relay.circuit, 0)  # Turn off alarm relay

        Log.objects.create(message="Alarm manually deactivated.")
    return redirect('system_status')



