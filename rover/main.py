import asyncio
import base64
import json
import threading
import time
from datetime import datetime, timezone

import camera
import hardware
import mqtt
import websocket

fps = 30


def send_alive():
    while True:
        topic = "rover/is_online"
        timestamp = datetime.now(timezone.utc).isoformat()
        mqtt.publishJson(topic, {"timestamp": timestamp, "value": 1})
        time.sleep(10)


async def send_video(ws):
    capture = camera.capture()
    while True:
        buffer = camera.read(capture)
        payload = base64.b64encode(buffer).decode('utf-8')
        await ws.send(payload)
        await asyncio.sleep(1 / fps)


async def _handler(ws):
    asyncio.create_task(send_video(ws))

    async for message in ws:
        payload = json.loads(message)
        type = payload["type"]
        if type == "drive":
            hardware.set_motor(hardware.LEFT, payload["speed"])
            hardware.set_motor(hardware.RIGHT, payload["speed"])
        elif type == "steer":
            hardware.set_servo(hardware.STEER, payload["angle"])
        elif type == "camera":
            hardware.set_servo(hardware.CAMERA_X, payload["x"])
            hardware.set_servo(hardware.CAMERA_Y, payload["y"])
        elif type == "led":
            hardware.set_led(hardware.LED_RED, payload["red"])
            hardware.set_led(hardware.LED_GREEN, payload["green"])
            hardware.set_led(hardware.LED_BLUE, payload["blue"])
        elif type == "buzzer":
            hardware.set_buzzer(hardware.BUZZER, payload["buzzer"])


def run_websocket():
    websocket.start(_handler)


def run_mqtt():
    mqtt.connect()
    mqtt.start()


run_websocket()
run_mqtt()
hardware.reset()

alive_thread = threading.Thread(target=send_alive)
alive_thread.start()

input()
