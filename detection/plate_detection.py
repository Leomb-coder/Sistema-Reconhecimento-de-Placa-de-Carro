from ultralytics import YOLO
from config import YOLO_MODEL_PATH
import cv2

model = YOLO(YOLO_MODEL_PATH)

def detect_plate(frame):
    results = model(frame)[0]

    plate_crop = None

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        pad = 10
        h, w, _ = frame.shape

        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w, x2 + pad)
        y2 = min(h, y2 + pad)

        # desenha caixa verde
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        plate_crop = frame[y1:y2, x1:x2]
        break

    return frame, plate_crop