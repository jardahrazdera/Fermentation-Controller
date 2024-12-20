from api.evok_client import EvokClient
from core.models import Sensor, Valve, Tank, Log, DigitalInput, Relay
from django.utils import timezone


def check_and_trigger_alarm():
    """
    Checks alarm conditions and activates the alarm relay if necessary.
    """
    client = EvokClient()

    # Alarm conditions
    alarm_triggered = False
    alarm_message = ""

    # Check sensors for errors or out-of-range temperatures
    sensors = Sensor.objects.all()
    for sensor in sensors:
        if sensor.is_faulty:
            alarm_triggered = True
            alarm_message += f"Sensor '{sensor.name}' is faulty. "
        elif sensor.current_temperature is not None:
            if sensor.current_temperature < sensor.min_temp or sensor.current_temperature > sensor.max_temp:
                alarm_triggered = True
                alarm_message += (f"Sensor '{sensor.name}' temperature {sensor.current_temperature}°C "
                                  f"is out of range ({sensor.min_temp}°C - {sensor.max_temp}°C). ")

    # Activate or deactivate the alarm relay
    alarm_relay = Relay.objects.get(name="Alarm_Relay")
    if alarm_triggered:
        client.set_relay(alarm_relay.circuit, 1)  # Turn on alarm relay
        alarm_relay.is_active = True
        Log.objects.create(message="Alarm triggered: " + alarm_message)
    else:
        client.set_relay(alarm_relay.circuit, 0)  # Turn off alarm relay
        alarm_relay.is_active = False
        Log.objects.create(message="Alarm manually deactivated.", tank=None)
        Log.objects.create(message="Alarm cleared.")

    alarm_relay.save()


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


def update_inputs_and_relays():
    """
    Updates the state of digital inputs and relays based on the current system status.
    """
    client = EvokClient()

    # Update digital inputs
    inputs = DigitalInput.objects.all()
    for di in inputs:
        state = client.get_digital_input_state(di.circuit)  # Read state from EVOK API
        if state is not None:
            di.state = state
            di.save()
            print(f"Digital Input '{di.name}' updated to {'Active' if state else 'Inactive'}.")

    # Process Total Stop first (highest priority)
    total_stop = DigitalInput.objects.get(name="Total_Stop_DI")
    if total_stop.state:
        print("Total Stop is active. Disabling all relays.")
        relays = Relay.objects.all()
        for relay in relays:
            client.set_relay(relay.circuit, 0)  # Turn off relay
            relay.is_active = False
            relay.save()
        return  # Skip other processing when total stop is active

    # Update relays based on inputs
    pump_di = DigitalInput.objects.get(name="Pump_DI")
    pump_relay = Relay.objects.get(name="Pump_Relay")
    if pump_di.state:
        client.set_relay(pump_relay.circuit, 1)  # Turn on relay
        pump_relay.is_active = True
    else:
        client.set_relay(pump_relay.circuit, 0)  # Turn off relay
        pump_relay.is_active = False
    pump_relay.save()

    chiller_di = DigitalInput.objects.get(name="Chiller_DI")
    chiller_relay = Relay.objects.get(name="Chiller_Relay")
    if chiller_di.state:
        client.set_relay(chiller_relay.circuit, 1)  # Turn on relay
        chiller_relay.is_active = True
    else:
        client.set_relay(chiller_relay.circuit, 0)  # Turn off relay
        chiller_relay.is_active = False
    chiller_relay.save()
