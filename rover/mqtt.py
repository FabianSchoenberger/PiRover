import json

import paho.mqtt.client as mqtt

# topics
EXAMPLE = "example"

BROKER_HOST = "localhost"
BROKER_PORT = 1883
mqtt = mqtt.Client()


def connect():
    mqtt.connect(BROKER_HOST, BROKER_PORT)


def subscribe(topic, callback):
    mqtt.subscribe(topic)
    mqtt.message_callback_add(
        topic,
        lambda client, userdata, message: callback(message.payload.decode())
    )


def publish(topic, payload):
    mqtt.publish(topic, payload)


def publishJson(topic, payload):
    publish(topic, json.dumps(payload))


def start():
    mqtt.loop_start()
