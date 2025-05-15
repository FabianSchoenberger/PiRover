import cv2

camera = 0
fps = 30


def capture():
    capture = cv2.VideoCapture(camera)
    if not capture.isOpened():
        raise Exception()
    capture.set(cv2.CAP_PROP_FPS, fps)
    return capture


def release(capture):
    capture.release()


def read(capture):
    ret, frame = capture.read()
    if not ret:
        raise Exception()
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer
