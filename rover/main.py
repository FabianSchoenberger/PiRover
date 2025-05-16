import asyncio
import base64
import time

import camera
import mqtt
import websocket


# region websocket
async def send_video(ws):
    capture = camera.capture()
    while True:
        buffer = camera.read(capture)
        payload = base64.b64encode(buffer).decode('utf-8')
        await ws.send(payload)
        time.sleep(1 / 10) # 10 FPS


async def _handler(ws):
    asyncio.create_task(send_video(ws))

    async for message in ws:
        # TODO handle controls
        print(message)


def run_websocket():
    websocket.start(_handler)


# endregion

# region mqtt
def run_mqtt():
    mqtt.connect()
    mqtt.start()


# endregion

run_websocket()
run_mqtt()

input()
