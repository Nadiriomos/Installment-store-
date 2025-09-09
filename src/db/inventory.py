import sqlite3
from pathlib import Path

from . import get_conn

def _create_suppliers():
    with get_conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone1 INTEGER,
            phone2 INTEGER,
            social TEXT,
            address TEXT
        );
        """)

def add_supplier(name, email, phone1, phone2, social, address):
    with get_conn() as c:
        c.execute("""
            INSERT INTO suppliers (name, email, phone1, phone2, social, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone1, phone2, social, address))

def list_suppliers():
    with get_conn() as c:
        cur = c.execute("""
            SELECT id, name, email, phone1, phone2, social, address
            FROM suppliers ORDER BY id DESC
        """)
        return cur.fetchall()