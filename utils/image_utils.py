import cv2

def draw_box(frame, x1, y1, x2, y2, text=""):
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

    if text:
        cv2.putText(frame, text, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0,255,0), 2)

    return frame