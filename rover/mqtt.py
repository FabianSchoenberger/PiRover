import base64
import json

import paho.mqtt.client as mqtt

# topics
CAMERA = "camera"

BROKER_HOST = "localhost"
BROKER_PORT = 1883
client = mqtt.Client()


def connect():
    client.connect(BROKER_HOST, BROKER_PORT)


def subscribe(topic, callback):
    client.subscribe(topic)
    client.message_callback_add(
        topic,
        lambda client, userdata, message: callback(message.payload.decode())
    )



def publish(topic, payload):
    client.publish(topic, payload)


def publishJson(topic, object):
    payload = json.dumps(object)
    publish(topic, payload)


def publishImage(topic, buffer):
    payload = base64.b64encode(buffer).decode('utf-8')
    publish(topic, payload)


def start():
    client.loop_start()


def stop():
    client.loop_stop()
