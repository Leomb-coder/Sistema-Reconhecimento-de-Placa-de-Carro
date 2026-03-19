import cv2
from config import CAMERA_INDEX

def get_camera_frames():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    while True:
        success, frame = cap.read()

        if not success:
            break

        # encode para enviar no Flask
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield frame, frame_bytes