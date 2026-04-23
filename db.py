from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_connection():
    if os.environ.get("DB_HOST") == "localhost":
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_DATABASE"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            sslmode="disable",
            channel_binding="disable"
        )
    else:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_DATABASE"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            sslmode=os.environ.get("DB_SSLMODE"),
            channel_binding=os.environ.get("DB_CHANNEL_BINDING")
        )
    return conn