import time
from datetime import datetime, timezone

import smbus

import mqtt
from util import *

address = 0x18
bus = smbus.SMBus(1)
bus.open(1)

STEER = 0
CAMERA_Y = 1
CAMERA_X = 2
LEFT = [6, 4]
RIGHT = [7, 5]
LED_RED = 9
LED_GREEN = 10
LED_BLUE = 11
BUZZER = 8


def publish(hardware, value):
    topic = "none"
    if hardware == STEER:
        topic = "rover/servo/steer"
    elif hardware == CAMERA_X:
        topic = "rover/servo/camera_x"
    elif hardware == CAMERA_Y:
        topic = "rover/servo/camera_y"
    elif hardware == LEFT:
        topic = "rover/motor/left"
    elif hardware == RIGHT:
        topic = "rover/motor/right"
    elif hardware == LED_RED:
        topic = "rover/led/red"
    elif hardware == LED_GREEN:
        topic = "rover/led/green"
    elif hardware == LED_BLUE:
        topic = "rover/led/blue"
    elif hardware == BUZZER:
        topic = "rover/buzzer"
    timestamp = datetime.now(timezone.utc).isoformat()
    mqtt.publishJson(topic, {"timestamp": timestamp, "value": value})


def set(cmd, value):
    value = int(value)

    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)


def set_servo(servo, it):
    if servo == STEER or servo == CAMERA_Y: it = -it  # compensate for flipped servo
    value = scale(it, -90, 90, 500, 2500)

    set(servo, value)
    publish(servo, value)


def set_motor(motor, it):
    if it < 0:
        value = scale(it, -1, 0, -1000, -400)
    elif it > 0:
        value = scale(it, 0, 1, 400, 1000)
    else:
        value = 0

    [direction, speed] = motor
    if value < 0:
        set(direction, 0)
        set(speed, -value)
    else:
        set(direction, 1)
        set(speed, value)
    publish(motor, value)


def set_led(led, it):
    value = scale(it, 0, 1, 1, 0)
    set(led, value)
    publish(led, value)


def set_buzzer(buzzer, it):
    value = scale(it, 0, 1, 0, 65535)
    set(buzzer, value)
    publish(buzzer, value)


def reset():
    set_servo(STEER, 0)
    set_servo(CAMERA_Y, 0)
    set_servo(CAMERA_X, 0)
    set_motor(LEFT, 0)
    set_motor(RIGHT, 0)
    set_led(LED_RED, 0)
    set_led(LED_GREEN, 0)
    set_led(LED_BLUE, 0)
    set_buzzer(BUZZER, 0)


if __name__ == "main":
    reset()
