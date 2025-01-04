from django.db import models
from django.utils.timezone import now
from api.evok_client import EvokClient
from django.core.validators import RegexValidator


class Tank(models.Model):
    name = models.CharField(max_length=50, unique=True)
    target_temperature = models.FloatField(default=20.0, help_text="Desired temperature for the tank.")
    sensor = models.ForeignKey(
        'Sensor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The temperature sensor associated with this tank."
    )
    valve = models.ForeignKey(
        'Valve',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The valve associated with this tank."
    )

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^xG18_\d$', message="Circuit must match format 'xG18_<digit>'")],
        help_text="xG18 Modbus circuit ID (e.g., xG18_1, xG18_2)"
    )
    current_temperature = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    min_temp = models.FloatField(default=0.0, help_text="Minimum acceptable temperature")
    max_temp = models.FloatField(default=25.0, help_text="Maximum acceptable temperature")
    last_error_time = models.DateTimeField(null=True, blank=True, help_text="Time of the last detected error.")
    error_active = models.BooleanField(default=False, help_text="Indicates if the sensor is currently in error state.")

    @property
    def is_faulty(self):
        """Returns True if the sensor is in an error state."""
        return self.error_active

    @property
    def error_persistent(self):
        """Returns True if the error state has persisted for more than 60 seconds."""
        if self.last_error_time and self.error_active:
            return (now() - self.last_error_time).total_seconds() > 60
        return False

    def update_error_state(self, client=None):
        """Updates the error state based on the 'valid' parameter from the API."""
        client = client or EvokClient()
        valid = client.get_sensor_status(self.circuit)
        self.error_active = not valid
        self.last_error_time = now() if not valid and not self.last_error_time else None
        self.save()

    def __str__(self):
        status = "Error" if self.error_active else "OK"
        return f"{self.name} - {self.current_temperature} °C - {status}"


class Valve(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    is_open = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Open" if self.is_open else "Closed"
        return f"{self.name} - {status}"


class Log(models.Model):
    tank = models.ForeignKey(
        'Tank',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Related tank for this log, if applicable."
    )
    sensor = models.ForeignKey(
        'Sensor',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Related sensor for this log, if applicable."
    )
    event = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    valve_state = models.BooleanField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="No details provided")

    def __str__(self):
        if self.tank:
            return f"({self.tank.name}) at {self.timestamp}"
        if self.sensor:
            return f"({self.sensor.name}) at {self.timestamp}"
        if "Alarm" in self.message:
            return f"(Alarm) at {self.timestamp}"
        return f"(General) at {self.timestamp}"


class DigitalInput(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    state = models.BooleanField(default=False, help_text="Current state of the input")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Active" if self.state else "Inactive"
        return f"{self.name} - {status}"


class Relay(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    is_active = models.BooleanField(default=False, help_text="Current state of the relay")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} - {status}"
