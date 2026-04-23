from flask import Flask, render_template, Response, jsonify
from camera.camera_stream import get_camera_frames
from detection.plate_detection import detect_plate
from ocr.plate_reader import read_plate
import psycopg2
import datetime
from config import DB_CONFIG
import time
import cv2

# ----------------------------
# CONTROLE DE DUPLICAÇÃO
# ----------------------------
last_plate = None
last_time = 0

def should_save(plate):
    global last_plate, last_time

    now = time.time()

    if plate == last_plate and now - last_time < 5:
        return False

    last_plate = plate
    last_time = now
    return True

# ----------------------------
app = Flask(__name__)

# ----------------------------
# BANCO
# ----------------------------
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def save_plate(plate):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO placas_reconhecidas (placa, data, permitido)
            VALUES (%s, %s, %s)
        """, (plate, datetime.datetime.now(), True))

        conn.commit()
        cur.close()
        conn.close()

        print("Placa salva:", plate)

    except Exception as e:
        print("Erro:", e)

# ----------------------------
# ROTAS
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    for frame, _ in get_camera_frames():

        # detecta e desenha caixa
        frame, plate_img = detect_plate(frame)

        if plate_img is not None:
            text = read_plate(plate_img)

            if text and should_save(text):
                save_plate(text)

                # mostra texto na tela
                cv2.putText(frame, text, (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,255,0), 2)

        # envia frame atualizado
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/placas')
def placas():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM placas_permitidas")
    dados = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(dados)

# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)