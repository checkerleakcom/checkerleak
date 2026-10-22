"""
AuthService: User registration, secure PBKDF2 authentication, and credit accounting.
Complies with ECC Security & Immutability standards.
Supports both SQLite and PostgreSQL backends via DatabaseService.
"""
import hashlib
import secrets
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.database import DatabaseService
from app.core.email_service import EmailService


class User(BaseModel):
    """Immutable representation of an authenticated user."""
    model_config = ConfigDict(frozen=True)

    id: int
    email: str
    full_name: str
    credits: int
    api_key: str
    email_verified: bool = False
    status: str = "active"
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

    def __init__(self, db: Optional[DatabaseService] = None, email_service: Optional[EmailService] = None):
        self.db = db or DatabaseService()
        self.email_service = email_service or EmailService()

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
        verification_token = secrets.token_urlsafe(32)
        initial_credits = 0

        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            try:
                if self.db.is_pg:
                    cursor.execute(
                        """
                        INSERT INTO users (email, password_hash, salt, full_name, credits, api_key, status, email_verified, verification_token)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        RETURNING id
                        """,
                        (clean_email, pwd_hash, salt, full_name.strip(), initial_credits, api_key, "active", 0, verification_token),
                    )
                    user_id = cursor.fetchone()["id"]
                else:
                    cursor.execute(
                        """
                        INSERT INTO users (email, password_hash, salt, full_name, credits, api_key, status, email_verified, verification_token)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (clean_email, pwd_hash, salt, full_name.strip(), initial_credits, api_key, "active", 0, verification_token),
                    )
                    user_id = cursor.lastrowid
            except Exception as e:
                err_str = str(e).lower()
                if "unique" in err_str or "duplicate" in err_str:
                    raise ValueError("EMAIL_ALREADY_EXISTS")
                raise e

        # Trigger transactional verification email (falls back to console link if SMTP is unset)
        try:
            self.email_service.send_verification_email(clean_email, verification_token, full_name.strip())
        except Exception as mail_err:
            print(f"[AuthService] Warning: Failed to send verification email ({mail_err})")

        return User(
            id=user_id,
            email=clean_email,
            full_name=full_name.strip(),
            credits=initial_credits,
            api_key=api_key,
            email_verified=False,
            status="active",
        )

    def authenticate(self, email: str, password: str) -> User:
        clean_email = email.strip().lower()
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "SELECT id, email, password_hash, salt, full_name, credits, api_key, status, email_verified, created_at FROM users WHERE email = ?",
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
            status=row.get("status") or "active",
            email_verified=bool(row.get("email_verified", 0)),
            created_at=str(row["created_at"]),
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "SELECT id, email, full_name, credits, api_key, status, email_verified, created_at FROM users WHERE id = ?",
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
            status=row.get("status") or "active",
            email_verified=bool(row.get("email_verified", 0)),
            created_at=str(row["created_at"]),
        )

    def get_by_api_key(self, api_key: str) -> Optional[User]:
        if not api_key:
            return None
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "SELECT id, email, full_name, credits, api_key, status, email_verified, created_at FROM users WHERE api_key = ?",
                (api_key.strip(),),
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
            status=row.get("status") or "active",
            email_verified=bool(row.get("email_verified", 0)),
            created_at=str(row["created_at"]),
        )

    def verify_email(self, token: str) -> User:
        """Atomically marks user's email as verified using token and clears token."""
        if not token or not token.strip():
            raise ValueError("INVALID_TOKEN")
        clean_token = token.strip()
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "SELECT id, email, full_name, credits, api_key, email_verified FROM users WHERE verification_token = ?",
                (clean_token,),
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("INVALID_OR_EXPIRED_TOKEN")

            user_id = row["id"]
            cursor.execute(
                "UPDATE users SET email_verified = 1, verification_token = NULL WHERE id = ?",
                (user_id,),
            )

        updated_user = self.get_by_id(user_id)
        if not updated_user:
            raise ValueError("USER_NOT_FOUND")
        return updated_user

    def resend_verification(self, email: str) -> bool:
        """Issues a fresh verification token and dispatches email."""
        clean_email = email.strip().lower()
        if not clean_email or "@" not in clean_email:
            raise ValueError("INVALID_EMAIL")

        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "SELECT id, full_name, email_verified FROM users WHERE email = ?",
                (clean_email,),
            )
            row = cursor.fetchone()
            if not row:
                # Return True or error to prevent account discovery
                raise ValueError("USER_NOT_FOUND")

            if row.get("email_verified"):
                raise ValueError("ALREADY_VERIFIED")

            new_token = secrets.token_urlsafe(32)
            cursor.execute(
                "UPDATE users SET verification_token = ? WHERE id = ?",
                (new_token, row["id"]),
            )

        self.email_service.send_verification_email(clean_email, new_token, row.get("full_name"))
        return True

    def admin_set_email_verified(self, user_id: int, verified: bool = True) -> User:
        """Admin override to mark email as verified directly."""
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute(
                "UPDATE users SET email_verified = ?, verification_token = NULL WHERE id = ?",
                (1 if verified else 0, user_id),
            )
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("USER_NOT_FOUND")
        return user

    def deduct_credits(self, user_id: int, amount: int = 1) -> User:
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            current_credits = row["credits"]
            if current_credits < amount:
                raise ValueError("INSUFFICIENT_CREDITS")

            new_credits = current_credits - amount
            cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))

        return self.get_by_id(user_id)

    def add_credits(self, user_id: int, amount: int) -> User:
        if amount <= 0:
            raise ValueError("AMOUNT_MUST_BE_POSITIVE")
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            current_credits = row["credits"]
            new_credits = current_credits + amount
            cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))

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
            cursor = self.db.get_cursor(conn)
            if self.db.is_pg:
                cursor.execute(
                    """
                    INSERT INTO task_history (user_id, phone, carrier, reachability_score, lead_quality, credits_used)
                    VALUES (?, ?, ?, ?, ?, ?)
                    RETURNING id
                    """,
                    (user_id, phone, carrier, reachability_score, lead_quality, credits_used),
                )
                return cursor.fetchone()["id"]
            else:
                cursor.execute(
                    """
                    INSERT INTO task_history (user_id, phone, carrier, reachability_score, lead_quality, credits_used)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, phone, carrier, reachability_score, lead_quality, credits_used),
                )
                return cursor.lastrowid

    def get_user_history(self, user_id: int, limit: int = 50) -> list[TaskRecord]:
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
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

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Securely updates a user password after verifying current credentials."""
        if not new_password or len(new_password) < 6:
            raise ValueError("PASSWORD_TOO_SHORT")

        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute("SELECT id, password_hash, salt FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            expected_hash = self._hash_password(current_password, row["salt"])
            if not secrets.compare_digest(expected_hash, row["password_hash"]):
                raise ValueError("INVALID_CURRENT_PASSWORD")

            new_salt = secrets.token_hex(16)
            new_hash = self._hash_password(new_password, new_salt)
            cursor.execute(
                "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
                (new_hash, new_salt, user_id),
            )
        return True

    def regenerate_api_key(self, user_id: int) -> User:
        """Issues a fresh secret API key for the user and invalidates previous credentials."""
        new_api_key = f"pk_live_{secrets.token_urlsafe(24)}"
        with self.db.get_connection() as conn:
            cursor = self.db.get_cursor(conn)
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")

            cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (new_api_key, user_id))

        updated = self.get_by_id(user_id)
        if not updated:
            raise ValueError("USER_NOT_FOUND")
        return updated

