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


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="1-Wire address or EVOK API circuit ID")
    current_temperature = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.current_temperature} °C"


class Valve(models.Model):
    name = models.CharField(max_length=50, unique=True)
    circuit = models.CharField(max_length=50, help_text="EVOK API circuit ID")
    is_open = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {'Open' if self.is_open else 'Closed'}"


from django.db import models

class Log(models.Model):
    tank = models.ForeignKey('Tank', on_delete=models.CASCADE, related_name='logs')
    event = models.CharField(max_length=255)
    temperature = models.FloatField(blank=True, null=True)
    valve_state = models.BooleanField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.tank.name} at {self.timestamp}"
