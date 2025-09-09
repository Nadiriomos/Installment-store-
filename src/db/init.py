import sqlite3
from pathlib import Path

_DB = Path("app.db")

def get_conn():
    conn = sqlite3.connect(_DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    from .inventory import _create_suppliers
    _create_suppliers()