"""
DatabaseService: SQLite persistence layer for users, credits, and verification logs.
Thread-safe, lightweight, and zero external database dependencies.
"""
import sqlite3
import os
from typing import Optional


class DatabaseService:
    """Manages SQLite tables and connection lifecycle."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), "pulsecheck.db")
        self._init_tables()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_tables(self):
        with self.get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    credits INTEGER NOT NULL DEFAULT 0,
                    api_key TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS task_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    phone TEXT NOT NULL,
                    carrier TEXT,
                    reachability_score INTEGER NOT NULL,
                    lead_quality TEXT NOT NULL,
                    credits_used INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS billing_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plan_id TEXT NOT NULL,
                    amount_usd REAL NOT NULL,
                    credits_added INTEGER NOT NULL,
                    payment_method TEXT NOT NULL,
                    status TEXT NOT NULL,
                    tx_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
                CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON task_history(user_id);
                CREATE INDEX IF NOT EXISTS idx_billing_user_id ON billing_transactions(user_id);
            """)
