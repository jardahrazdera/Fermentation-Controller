from django.db import models


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


from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="1-Wire address or EVOK API circuit ID")
    current_temperature = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    min_temp = models.FloatField(default=0.0, help_text="Minimum acceptable temperature")
    max_temp = models.FloatField(default=25.0, help_text="Maximum acceptable temperature")

    @property
    def is_faulty(self):
        """
        Determines if the sensor is faulty.
        """
        return self.current_temperature is None

    def __str__(self):
        return f"{self.name} - {self.current_temperature} °C"


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
