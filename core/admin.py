from django.contrib import admin
from .models import Tank, Sensor, Valve, Log

admin.site.register(Tank)
admin.site.register(Sensor)
admin.site.register(Valve)
admin.site.register(Log)