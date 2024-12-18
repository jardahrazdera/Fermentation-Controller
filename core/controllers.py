from api.evok_client import EvokClient
from core.models import Sensor, Valve, Tank, Log
from django.utils import timezone


def regulate_temperature():
    """
    Automatically regulates the temperature of each tank by controlling valves.
    Logs all events such as temperature updates and valve state changes.
    """
    client = EvokClient()
    tanks = Tank.objects.select_related('sensor', 'valve').all()

    for tank in tanks:
        if tank.sensor and tank.valve:
            # Read the current temperature
            current_temp = client.get_temperature(tank.sensor.circuit)
            if current_temp is None:
                Log.objects.create(
                    tank=tank,
                    event=f"Failed to read temperature for sensor '{tank.sensor.name}'.",
                    temperature=None,
                )
                print(f"Failed to read temperature for sensor '{tank.sensor.name}'.")
                continue

            # Log temperature reading
            Log.objects.create(
                tank=tank,
                event="Temperature updated.",
                temperature=current_temp,
            )
            print(f"Tank '{tank.name}': Current Temp = {current_temp} °C, Target Temp = {tank.target_temperature} °C")

            # Check if valve needs to be opened or closed
            if current_temp > tank.target_temperature and not tank.valve.is_open:
                client.set_relay(tank.valve.circuit, 1)  # Open valve
                tank.valve.is_open = True
                tank.valve.last_updated = timezone.now()
                tank.valve.save()
                Log.objects.create(
                    tank=tank,
                    event=f"Valve '{tank.valve.name}' opened.",
                    valve_state=True,
                )
                print(f"Valve '{tank.valve.name}' opened to cool tank '{tank.name}'.")

            elif current_temp <= tank.target_temperature and tank.valve.is_open:
                client.set_relay(tank.valve.circuit, 0)  # Close valve
                tank.valve.is_open = False
                tank.valve.last_updated = timezone.now()
                tank.valve.save()
                Log.objects.create(
                    tank=tank,
                    event=f"Valve '{tank.valve.name}' closed.",
                    valve_state=False,
                )
                print(f"Valve '{tank.valve.name}' closed as tank '{tank.name}' is at target temperature.")


def update_sensors():
    client = EvokClient()
    sensors = Sensor.objects.all()
    for sensor in sensors:
        temperature = client.get_temperature(sensor.circuit)
        if temperature is not None:
            sensor.current_temperature = temperature
            sensor.last_updated = timezone.now()
            sensor.save()
            print(f"Updated sensor '{sensor.name}' with temperature {temperature} °C")
        else:
            print(f"Failed to update sensor '{sensor.name}'")


def control_valve(valve_name, state):
    """
    Control a valve (open/close) using EVOK API.
    :param valve_name: Name of the valve to control.
    :param state: 1 to open, 0 to close.
    """
    client = EvokClient()
    try:
        valve = Valve.objects.get(name=valve_name)
        success = client.set_relay(valve.circuit, state)
        if success:
            valve.is_open = bool(state)
            valve.last_updated = timezone.now()
            valve.save()
            print(f"Valve '{valve.name}' set to {'Open' if state else 'Closed'}.")
        else:
            print(f"Failed to control valve '{valve.name}'.")
    except Valve.DoesNotExist:
        print(f"Error: Valve '{valve_name}' does not exist. Please add it to the database.")
