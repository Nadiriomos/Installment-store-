import sqlite3

# === customer ===
def init_db():
    conn = sqlite3.connect("installment_store.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()