import easyocr
import cv2
import re

reader = easyocr.Reader(['en'])

def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh

def clean_plate(text):
    text = re.sub(r'[^A-Z0-9]', '', text)

    if len(text) < 6 or len(text) > 8:
        return None

    return text

def read_plate(image):
    # aumenta resolução
    image = cv2.resize(image, None, fx=2, fy=2)

    processed = preprocess(image)

    # DEBUG (opcional)
    cv2.imwrite("debug_plate.jpg", processed)

    results = reader.readtext(processed)

    for (_, text, prob) in results:
        if prob > 0.6:
            plate = clean_plate(text.upper())

            if plate:
                return plate

    return None