from django.db import models
from django.utils.timezone import now


class Tank(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    sensor = models.ForeignKey('Sensor', on_delete=models.SET_NULL, null=True, related_name='tanks')
    valve = models.ForeignKey('Valve', on_delete=models.SET_NULL, null=True, related_name='tanks')
    target_temperature = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="1-Wire address or EVOK API circuit ID")
    current_temperature = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    min_temp = models.FloatField(default=0.0, help_text="Minimum acceptable temperature")
    max_temp = models.FloatField(default=25.0, help_text="Maximum acceptable temperature")
    last_error_time = models.DateTimeField(null=True, blank=True, help_text="Time of the last detected error.")
    error_active = models.BooleanField(default=False, help_text="Indicates if the sensor is currently in error state.")

    @property
    def is_faulty(self):
        """
        Determines if the sensor is faulty using the 'lost' parameter from the API.
        """
        return self.error_active

    @property
    def error_persistent(self):
        """
        Checks if the error state has persisted for more than 60 seconds.
        """
        if self.last_error_time and self.error_active:
            elapsed_time = (now() - self.last_error_time).total_seconds()
            return elapsed_time > 60
        return False

    def update_error_state(self, lost):
        """
        Updates the error state of the sensor based on the 'lost' parameter.
        """
        if lost:
            if not self.error_active:
                self.last_error_time = now()
            self.error_active = True
        else:
            self.error_active = False
            self.last_error_time = None
        self.save()

    def __str__(self):
        return f"{self.name} - {self.current_temperature} °C - {'Error' if self.error_active else 'OK'}"


class Valve(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    is_open = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {'Open' if self.is_open else 'Closed'}"


class Log(models.Model):
    tank = models.ForeignKey(
        'Tank',
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Makes the field optional
        help_text="Related tank for this log, if applicable."
    )
    event = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    valve_state = models.BooleanField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        if self.tank:
            return f"({self.tank.name}) at {self.timestamp}"
        if "Alarm" in self.message:
            return f"(Alarm) at {self.timestamp}"
        return f"(General) at {self.timestamp}"


class DigitalInput(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    state = models.BooleanField(default=False, help_text="Current state of the input")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {'Active' if self.state else 'Inactive'}"


class Relay(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    is_active = models.BooleanField(default=False, help_text="Current state of the relay")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"
