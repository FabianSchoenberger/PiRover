import threading

import camera
import mqtt

mqtt.connect()
mqtt.start()


# region subscribe to controls
# TODO
# endregion

# region publish video
def publishVideo():
    capture = camera.capture()
    while True:
        buffer = camera.read(capture)
        mqtt.publishImage(mqtt.CAMERA, buffer)


videoThread = threading.Thread(target=publishVideo)
videoThread.start()
# endregion

input()
