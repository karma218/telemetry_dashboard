from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/telemetry/<str:vehicle_id>/', consumers.TelemetryConsumer.as_asgi()),
]
