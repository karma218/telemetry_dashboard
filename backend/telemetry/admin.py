from django.contrib import admin
from .models import Vehicle, TelemetryData

admin.site.register(Vehicle)
admin.site.register(TelemetryData)
