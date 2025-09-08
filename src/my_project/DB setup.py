import sqlite3

# === customer ===
def init_db():
    conn = sqlite3.connect("installment_store.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS suplier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone1 INTEGER NOT NULL,
            phone2 INTEGER NOT NULL,
            social_media TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()