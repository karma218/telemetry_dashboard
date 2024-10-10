from django.db import models

class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TelemetryData(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    obstacle_detected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle.name} at {self.timestamp}"
