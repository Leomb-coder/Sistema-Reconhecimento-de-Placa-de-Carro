from db import get_connection

def safe_connection():
    try:
        conn = get_connection()
        conn.cursor().execute("SELECT 1;")
        return conn
    except:
        print("Reconnecting...")
        return get_connection()

while True:
    safe_connection()