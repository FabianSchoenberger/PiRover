import numpy as np

from hardware import *


def testServo(servo, low, high):
    for i in range(0, low, -1):
        set_servo(servo, i)
        time.sleep(0.01)
    for i in range(low, high, 1):
        set_servo(servo, i)
        time.sleep(0.01)
    for i in range(high, low, -1):
        set_servo(servo, i)
        time.sleep(0.01)
    for i in range(low, 0, 1):
        set_servo(servo, i)
        time.sleep(0.01)


def testMotor(motor):
    for i in np.arange(0, 1, 0.01):
        set_motor(motor, i)
        time.sleep(0.001)
    for i in np.arange(1, 0, -0.01):
        set_motor(motor, i)
        time.sleep(0.001)
    set_motor(motor, 0)
    for i in np.arange(0, -1, -0.01):
        set_motor(motor, i)
        time.sleep(0.001)
    for i in np.arange(-1, 0, 0.01):
        set_motor(motor, i)
        time.sleep(0.001)
    set_motor(motor, 0)


def testLed():
    set_led(LED_RED, 1)
    time.sleep(1)
    set_led(LED_RED, 0)

    set_led(LED_GREEN, 1)
    time.sleep(1)
    set_led(LED_GREEN, 0)

    set_led(LED_BLUE, 1)
    time.sleep(1)
    set_led(LED_BLUE, 0)

    set_led(LED_RED, 1)
    set_led(LED_GREEN, 1)
    set_led(LED_BLUE, 1)
    time.sleep(1)
    set_led(LED_RED, 0)
    set_led(LED_GREEN, 0)
    set_led(LED_BLUE, 0)


def testBuzzer():
    set_buzzer(BUZZER, 1)
    time.sleep(1)
    set_buzzer(BUZZER, 0)


testServo(STEER, -40, 40)
testServo(CAMERA_X, -20, 60)
testServo(CAMERA_Y, -50, 50)
testMotor(LEFT)
testMotor(RIGHT)
testLed()
testBuzzer()
