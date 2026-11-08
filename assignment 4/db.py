import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="hospital_db",
        user="postgres",
        password="7777"
    )