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


def set(cmd, value):
    value = int(value)

    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)
    bus.write_i2c_block_data(address, cmd, [value >> 8, value & 0xff])
    time.sleep(0.001)


def set_servo(servo, it):
    value = scale(it, 0, 180, 500, 2500)

    set(servo, value)


def set_motor(motor, it):
    if it < 0:
        value = scale(it, -1, 0, -1000, -400)
    else:
        value = scale(it, 0, 1, 400, 1000)

    [direction, speed] = motor
    if value > 0:
        set(direction, 1)
        set(speed, value)
    else:
        set(direction, 0)
        set(speed, -value)
