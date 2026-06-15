import sqlite3
import datetime

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        type TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT,
        assigned_to INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        admin_id INTEGER,
        action TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_order(order_id, user_id, amount, type_, status, created_at):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO orders (order_id, user_id, amount, type, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, user_id, amount, type_, status, created_at))

    conn.commit()
    conn.close()


def update_status(order_id, status, admin_id=None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    now = str(datetime.datetime.now())

    if admin_id:
        cur.execute("""
        UPDATE orders
        SET status=?, updated_at=?, assigned_to=?
        WHERE order_id=?
        """, (status, now, admin_id, order_id))
    else:
        cur.execute("""
        UPDATE orders
        SET status=?, updated_at=?
        WHERE order_id=?
        """, (status, now, order_id))

    conn.commit()
    conn.close()


def add_log(order_id, admin_id, action):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO logs (order_id, admin_id, action, created_at)
    VALUES (?, ?, ?, ?)
    """, (order_id, admin_id, action, str(datetime.datetime.now())))

    conn.commit()
    conn.close()