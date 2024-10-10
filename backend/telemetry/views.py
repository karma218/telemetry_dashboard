from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Vehicle, TelemetryData
from .serializers import VehicleSerializer, TelemetryDataSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class TelemetryDataViewSet(viewsets.ModelViewSet):
    queryset = TelemetryData.objects.all()
    serializer_class = TelemetryDataSerializer
