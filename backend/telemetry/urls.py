from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, TelemetryDataViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'telemetry', TelemetryDataViewSet)

urlpatterns = [
    path('', include(router.urls)),  # The router URLs include `/vehicles/` and `/telemetry/`
]
