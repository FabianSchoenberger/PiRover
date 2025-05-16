import asyncio
import base64
import json
import time

import camera
import mqtt
import websocket
import hardware


# region websocket
async def send_video(ws):
    capture = camera.capture()
    while True:
        buffer = camera.read(capture)
        payload = base64.b64encode(buffer).decode('utf-8')
        await ws.send(payload)
        time.sleep(1 / 10)  # 10 FPS


async def _handler(ws):
    asyncio.create_task(send_video(ws))

    async for message in ws:
        payload = json.load(message)
        if payload["type"] == "drive":
            hardware.set_motor(hardware.LEFT, payload["speed"])
            hardware.set_motor(hardware.RIGHT, payload["speed"])
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
