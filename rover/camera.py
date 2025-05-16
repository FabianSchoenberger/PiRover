import cv2

camera = 0
fps = 30


def capture():
    c = cv2.VideoCapture(camera)
    if not c.isOpened():
        raise Exception()
    c.set(cv2.CAP_PROP_FPS, fps)
    return c


def release(c):
    c.release()


def read(c):
    ret, frame = c.read()
    if not ret:
        raise Exception()
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer
