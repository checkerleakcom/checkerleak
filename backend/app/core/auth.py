"""
AuthService: User registration, secure PBKDF2 authentication, and credit accounting.
Complies with ECC Security & Immutability standards.
"""
import hashlib
import secrets
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.database import DatabaseService


class User(BaseModel):
    """Immutable representation of an authenticated user."""
    model_config = ConfigDict(frozen=True)

    id: int
    email: str
    full_name: str
    credits: int
    api_key: str
    created_at: Optional[str] = None


class TaskRecord(BaseModel):
    """Immutable representation of a logged verification task."""
    model_config = ConfigDict(frozen=True)

    id: int
    user_id: int
    phone: str
    carrier: Optional[str] = None
    reachability_score: int
    lead_quality: str
    credits_used: int
    created_at: str


class AuthService:
    """Handles user identity, password hashing, and credit balances."""

    def __init__(self, db: Optional[DatabaseService] = None):
        self.db = db or DatabaseService()

    def _hash_password(self, password: str, salt: str) -> str:
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        )
        return key.hex()

    def register(self, email: str, password: str, full_name: str) -> User:
        clean_email = email.strip().lower()
        if not clean_email or "@" not in clean_email:
            raise ValueError("INVALID_EMAIL")
        if not password or len(password) < 6:
            raise ValueError("PASSWORD_TOO_SHORT")

        salt = secrets.token_hex(16)
        pwd_hash = self._hash_password(password, salt)
        api_key = f"pk_live_{secrets.token_urlsafe(24)}"
        initial_credits = 0  # Strict pay-as-you-go: users must top up to verify lists (prevents 1,000 credit free scraping abuse)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, salt, full_name, credits, api_key)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (clean_email, pwd_hash, salt, full_name.strip(), initial_credits, api_key),
                )
                user_id = cursor.lastrowid
                conn.commit()
            except Exception as e:
                if "UNIQUE constraint failed: users.email" in str(e):
                    raise ValueError("EMAIL_ALREADY_EXISTS")
                raise e

        return User(
            id=user_id,
            email=clean_email,
            full_name=full_name.strip(),
            credits=initial_credits,
            api_key=api_key,
        )

    def authenticate(self, email: str, password: str) -> User:
        clean_email = email.strip().lower()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, password_hash, salt, full_name, credits, api_key, created_at FROM users WHERE email = ?",
                (clean_email,),
            )
            row = cursor.fetchone()

        if not row:
            raise ValueError("INVALID_CREDENTIALS")

        expected_hash = self._hash_password(password, row["salt"])
        if not secrets.compare_digest(expected_hash, row["password_hash"]):
            raise ValueError("INVALID_CREDENTIALS")

        return User(
            id=row["id"],
            email=row["email"],
            full_name=row["full_name"],
            credits=row["credits"],
            api_key=row["api_key"],
            created_at=str(row["created_at"]),
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, full_name, credits, api_key, created_at FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        return User(
            id=row["id"],
            email=row["email"],
            full_name=row["full_name"],
            credits=row["credits"],
            api_key=row["api_key"],
            created_at=str(row["created_at"]),
        )

    def deduct_credits(self, user_id: int, amount: int = 1) -> User:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            current_credits = row["credits"]
            if current_credits < amount:
                raise ValueError("INSUFFICIENT_CREDITS")

            new_credits = current_credits - amount
            cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))
            conn.commit()

        return self.get_by_id(user_id)

    def add_credits(self, user_id: int, amount: int) -> User:
        if amount <= 0:
            raise ValueError("AMOUNT_MUST_BE_POSITIVE")
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            current_credits = row["credits"]
            new_credits = current_credits + amount
            cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))
            conn.commit()

        return self.get_by_id(user_id)

    def record_task(
        self,
        user_id: int,
        phone: str,
        reachability_score: int,
        lead_quality: str,
        carrier: Optional[str] = None,
        credits_used: int = 1,
    ) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO task_history (user_id, phone, carrier, reachability_score, lead_quality, credits_used)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, phone, carrier, reachability_score, lead_quality, credits_used),
            )
            conn.commit()
            return cursor.lastrowid

    def get_user_history(self, user_id: int, limit: int = 50) -> list[TaskRecord]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, phone, carrier, reachability_score, lead_quality, credits_used, created_at
                FROM task_history
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            )
            rows = cursor.fetchall()

        return [
            TaskRecord(
                id=row["id"],
                user_id=row["user_id"],
                phone=row["phone"],
                carrier=row["carrier"],
                reachability_score=row["reachability_score"],
                lead_quality=row["lead_quality"],
                credits_used=row["credits_used"],
                created_at=str(row["created_at"]),
            )
            for row in rows
        ]
