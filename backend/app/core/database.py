"""
DatabaseService: Unified persistence layer supporting both SQLite (local development)
and PostgreSQL (Render production). Automatically selects backend via DATABASE_URL or db_url.
Thread-safe, robust connection pooling, and auto-initializes all tables.
"""
import os
import sqlite3
from typing import Optional, Any
from contextlib import contextmanager

try:
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


class DictRowCursor:
    """Wrapper around sqlite3 or psycopg2 cursor providing standardized dict-like access."""
    def __init__(self, raw_cursor, is_pg: bool = False):
        self._cursor = raw_cursor
        self._is_pg = is_pg

    def execute(self, query: str, params: tuple = ()):
        if self._is_pg:
            # Convert SQLite '?' placeholders to PostgreSQL '%s'
            pg_query = query.replace("?", "%s")
            return self._cursor.execute(pg_query, params)
        else:
            return self._cursor.execute(query, params)

    def executemask(self, script: str):
        return self._cursor.executescript(script)

    def fetchone(self):
        row = self._cursor.fetchone()
        if not row:
            return None
        return dict(row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [dict(r) for r in rows]

    @property
    def lastrowid(self):
        if self._is_pg:
            try:
                return self._cursor.fetchone()[0]
            except Exception:
                return None
        return self._cursor.lastrowid


class DatabaseService:
    """Manages database connection lifecycle and schema migration."""

    def __init__(self, db_url: Optional[str] = None, db_path: Optional[str] = None):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        self.is_pg = bool(self.db_url and self.db_url.startswith(("postgres://", "postgresql://")))
        self.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), "pulsecheck.db")
        self._pg_pool = None

        if self.is_pg and PSYCOPG2_AVAILABLE:
            # Fix Render postgres:// to postgresql:// for SQLAlchemy/psycopg2 standard
            cleaned_url = self.db_url
            if cleaned_url.startswith("postgres://"):
                cleaned_url = cleaned_url.replace("postgres://", "postgresql://", 1)
            try:
                self._pg_pool = pool.SimpleConnectionPool(1, 10, cleaned_url)
            except Exception as e:
                print(f"[DatabaseService] Warning: Failed to connect to PostgreSQL ({e}). Falling back to SQLite.")
                self.is_pg = False

        self._init_tables()

    @contextmanager
    def get_connection(self):
        """Context manager returning a database connection compatible across SQLite & PostgreSQL."""
        if self.is_pg and self._pg_pool:
            conn = self._pg_pool.getconn()
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                self._pg_pool.putconn(conn)
        else:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=5000;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

    def get_cursor(self, conn) -> DictRowCursor:
        if self.is_pg:
            return DictRowCursor(conn.cursor(cursor_factory=RealDictCursor), is_pg=True)
        return DictRowCursor(conn.cursor(), is_pg=False)

    def _init_tables(self):
        with self.get_connection() as conn:
            if self.is_pg:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        salt VARCHAR(64) NOT NULL,
                        full_name VARCHAR(255) NOT NULL,
                        credits INTEGER NOT NULL DEFAULT 0,
                        api_key VARCHAR(128) UNIQUE NOT NULL,
                        status VARCHAR(32) NOT NULL DEFAULT 'active',
                        email_verified INTEGER NOT NULL DEFAULT 0,
                        verification_token VARCHAR(128),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS task_history (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id),
                        phone VARCHAR(64) NOT NULL,
                        carrier VARCHAR(128),
                        reachability_score INTEGER NOT NULL,
                        lead_quality VARCHAR(64) NOT NULL,
                        credits_used INTEGER NOT NULL DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS billing_transactions (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES users(id),
                        plan_id VARCHAR(64) NOT NULL,
                        amount_usd NUMERIC(10, 2) NOT NULL,
                        credits_added INTEGER NOT NULL,
                        payment_method VARCHAR(64) NOT NULL,
                        status VARCHAR(64) NOT NULL,
                        tx_hash VARCHAR(128),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS admin_audit_logs (
                        id SERIAL PRIMARY KEY,
                        admin_action VARCHAR(64) NOT NULL,
                        target_user_id INTEGER,
                        details TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS visitor_traffic (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(64),
                        ip_hash VARCHAR(64),
                        country VARCHAR(8) DEFAULT 'XX',
                        source_channel VARCHAR(32) NOT NULL,
                        source_engine VARCHAR(64) NOT NULL,
                        referrer_url TEXT,
                        landing_path VARCHAR(255) NOT NULL,
                        product_slug VARCHAR(128),
                        search_query VARCHAR(255),
                        utm_source VARCHAR(64),
                        utm_medium VARCHAR(64),
                        utm_campaign VARCHAR(64),
                        device_type VARCHAR(32) DEFAULT 'Desktop',
                        user_agent TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                    CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
                    CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON task_history(user_id);
                    CREATE INDEX IF NOT EXISTS idx_billing_user_id ON billing_transactions(user_id);
                    CREATE INDEX IF NOT EXISTS idx_audit_created ON admin_audit_logs(created_at DESC);
                    CREATE INDEX IF NOT EXISTS idx_traffic_created ON visitor_traffic(created_at DESC);
                    CREATE INDEX IF NOT EXISTS idx_traffic_channel ON visitor_traffic(source_channel);
                    CREATE INDEX IF NOT EXISTS idx_traffic_engine ON visitor_traffic(source_engine);
                    CREATE INDEX IF NOT EXISTS idx_traffic_product ON visitor_traffic(product_slug);
                """)
                # Safe migration: ensure status column exists if table was created previously
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(32) DEFAULT 'active';")
                    cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified INTEGER DEFAULT 0;")
                    cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR(128);")
                except Exception:
                    pass
            else:
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        credits INTEGER NOT NULL DEFAULT 0,
                        api_key TEXT UNIQUE NOT NULL,
                        status TEXT NOT NULL DEFAULT 'active',
                        email_verified INTEGER NOT NULL DEFAULT 0,
                        verification_token TEXT,
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

                    CREATE TABLE IF NOT EXISTS admin_audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_action TEXT NOT NULL,
                        target_user_id INTEGER,
                        details TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS visitor_traffic (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(64),
                        ip_hash VARCHAR(64),
                        country VARCHAR(8) DEFAULT 'XX',
                        source_channel VARCHAR(32) NOT NULL,
                        source_engine VARCHAR(64) NOT NULL,
                        referrer_url TEXT,
                        landing_path VARCHAR(255) NOT NULL,
                        product_slug VARCHAR(128),
                        search_query VARCHAR(255),
                        utm_source VARCHAR(64),
                        utm_medium VARCHAR(64),
                        utm_campaign VARCHAR(64),
                        device_type VARCHAR(32) DEFAULT 'Desktop',
                        user_agent TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                    CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
                    CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON task_history(user_id);
                    CREATE INDEX IF NOT EXISTS idx_billing_user_id ON billing_transactions(user_id);
                    CREATE INDEX IF NOT EXISTS idx_audit_created ON admin_audit_logs(created_at DESC);
                    CREATE INDEX IF NOT EXISTS idx_traffic_created ON visitor_traffic(created_at DESC);
                    CREATE INDEX IF NOT EXISTS idx_traffic_channel ON visitor_traffic(source_channel);
                    CREATE INDEX IF NOT EXISTS idx_traffic_engine ON visitor_traffic(source_engine);
                    CREATE INDEX IF NOT EXISTS idx_traffic_product ON visitor_traffic(product_slug);
                """)
                # Safe migration for sqlite if status column was absent
                try:
                    conn.execute("ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';")
                except Exception:
                    pass
                try:
                    conn.execute("ALTER TABLE users ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 0;")
                except Exception:
                    pass
                try:
                    conn.execute("ALTER TABLE users ADD COLUMN verification_token TEXT;")
                except Exception:
                    pass
