import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    database_path = current_app.config["DATABASE"]
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(database_path)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            browser_id TEXT NOT NULL DEFAULT '',
            customer_name TEXT NOT NULL,
            items_json TEXT NOT NULL,
            total_cents INTEGER NOT NULL,
            payment_method TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    existing_columns = {
        row[1] for row in db.execute("PRAGMA table_info(orders)").fetchall()
    }
    if "browser_id" not in existing_columns:
        db.execute("ALTER TABLE orders ADD COLUMN browser_id TEXT NOT NULL DEFAULT ''")
    if "payment_method" not in existing_columns:
        db.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT")
    db.execute("CREATE INDEX IF NOT EXISTS idx_orders_browser_created ON orders(browser_id, created_at)")
    db.commit()
    db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
