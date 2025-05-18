import time

import smbus

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



def set(cmd, value):
    value = int(value)

    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)


def set_servo(servo, it):
    if servo == STEER or servo == CAMERA_Y: it = -it # compensate for flipped servo
    value = scale(it, -90, 90, 500, 2500)

    set(servo, value)


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

def set_led(led, it):
    if it == 1:
        set(led, 0)
    else:
        set(led, 1)

def set_buzzer(buzzer, it):
    set(buzzer, it)


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
