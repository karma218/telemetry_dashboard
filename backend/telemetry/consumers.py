import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Vehicle, TelemetryData

logger = logging.getLogger(__name__)

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.vehicle_id = self.scope['url_route']['kwargs']['vehicle_id']
            self.group_name = f'vehicle_{self.vehicle_id}'

            logger.info(f"Attempting to add {self.channel_name} to group {self.group_name}")
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connection accepted for vehicle ID: {self.vehicle_id}")
        except Exception as e:
            logger.error(f"Error during connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            logger.info(f"Disconnecting WebSocket for vehicle ID: {self.vehicle_id} with close code: {close_code}")
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    async def receive(self, text_data):
        try:
            logger.info(f"Received data: {text_data}")
            data = json.loads(text_data)
            
            # Only process telemetry data (that contains vehicle_id and coordinates)
            if 'vehicle_id' in data and 'latitude' in data and 'longitude' in data:
                await self.save_telemetry_data(data)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'telemetry_data',
                        'data': data
                    }
                )
            else:
                logger.info("Received non-telemetry data, skipping save.")
        except Exception as e:
            logger.error(f"Error during receive: {e}")


    async def telemetry_data(self, event):
        try:
            data = event['data']
            logger.info(f"Broadcasting telemetry data to WebSocket: {data}")
            await self.send(text_data=json.dumps(data))
        except Exception as e:
            logger.error(f"Error during telemetry_data: {e}")
            await self.close()

    @database_sync_to_async
    def save_telemetry_data(self, data):
        try:
            vehicle, _ = Vehicle.objects.get_or_create(
                vehicle_id=data['vehicle_id'],
                defaults={'name': data['vehicle_id']}
            )
            TelemetryData.objects.create(
                vehicle=vehicle,
                latitude=data['latitude'],
                longitude=data['longitude'],
                speed=data.get('speed'),
                temperature=data.get('temperature'),
                obstacle_detected=data.get('obstacle_detected', False),
            )
            logger.info(f"Saved telemetry data for vehicle ID: {data['vehicle_id']}")
        except Exception as e:
            logger.error(f"Error saving telemetry data: {e}")
