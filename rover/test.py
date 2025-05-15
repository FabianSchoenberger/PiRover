from hardware import *


def testServo(servo, low, high):
    for i in range(90, low, -1):
        setServo(servo, i)
        time.sleep(0.01)
    for i in range(low, high, 1):
        setServo(servo, i)
        time.sleep(0.01)
    for i in range(high, low, -1):
        setServo(servo, i)
        time.sleep(0.01)
    for i in range(low, 90, 1):
        setServo(servo, i)
        time.sleep(0.01)


def testMotor(motor):
    for i in range(500, 1000):
        setMotor(motor, i)
        time.sleep(0.001)
    setMotor(motor, 1000)
    time.sleep(1)
    setMotor(motor, 0)


testServo(STEER, 50, 130)
testServo(CAMERA_X, 70, 150)
testServo(CAMERA_Y, 40, 140)
testMotor(LEFT)
testMotor(RIGHT)
