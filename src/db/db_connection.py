import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 5432),
        database=os.getenv('DB_NAME', 'financials'),
        user=os.getenv('DB_USER', 'your_username'),
        password=os.getenv('DB_PASSWORD', 'your_password')
    )
    return conn
