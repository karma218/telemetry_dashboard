import asyncio
import websockets
import json
import random

async def simulate(vehicle_id):
    ws_scheme = 'ws'
    uri = f'{ws_scheme}://localhost:8000/ws/telemetry/{vehicle_id}/'
    async with websockets.connect(uri) as websocket:
        while True:
            data = {
                'vehicle_id': vehicle_id,
                'latitude': random.uniform(-90, 90),
                'longitude': random.uniform(-180, 180),
                'speed': random.uniform(0, 120),
                'temperature': random.uniform(-10, 50),
                'obstacle_detected': random.choice([True, False]),
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(1)

if __name__ == '__main__':
    vehicle_id = 'vehicle_1'
    asyncio.run(simulate(vehicle_id))
