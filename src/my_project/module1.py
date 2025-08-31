import sqlite3
from socket import create_connection

class Database:
    def create_connection():
        conn = sqlite3.connect("installment_store.db")
        return conn

    def create_table():

        conn = create_connection()
        cursor = conn.cursor()


        conn.commit()
        conn.close()
