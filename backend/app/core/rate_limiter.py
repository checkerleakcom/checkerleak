"""
GuestRateLimiter: In-memory sliding window rate limiter for Guest / Non-authenticated checks.
Enforces a strict 3-check free trial quota per IP address per 24 hours to prevent scraping abuse.
Complies with ECC Security & Immutability standards.
"""
import time
import threading
from typing import Tuple, Dict, Any, Optional


class GuestRateLimiter:
    """Thread-safe rate limiter tracking guest trial verification quotas."""

    def __init__(self, max_free_checks: int = 3, window_seconds: int = 86400):
        self.max_free_checks = max_free_checks
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        # Mapping of ip -> {"count": int, "reset_at": float}
        self._storage: Dict[str, Dict[str, Any]] = {}

    def _cleanup_expired(self, current_time: float) -> None:
        """Periodically purge expired IP tracking records."""
        expired = [ip for ip, data in self._storage.items() if current_time >= data["reset_at"]]
        for ip in expired:
            del self._storage[ip]

    def check_guest_limit(self, ip: str) -> Tuple[bool, int, int]:
        """
        Check if a guest IP is allowed to perform a free verification.
        Returns: (is_allowed: bool, remaining_checks: int, max_free_checks: int)
        """
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()

        with self._lock:
            self._cleanup_expired(now)
            data = self._storage.get(clean_ip)
            if not data or now >= data["reset_at"]:
                # New session window
                remaining = self.max_free_checks
                return True, remaining, self.max_free_checks

            used = data["count"]
            if used >= self.max_free_checks:
                return False, 0, self.max_free_checks

            remaining = self.max_free_checks - used
            return True, remaining, self.max_free_checks

    def record_guest_check(self, ip: str) -> int:
        """
        Record a successful free check for the given guest IP.
        Returns the number of remaining free checks.
        """
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()

        with self._lock:
            data = self._storage.get(clean_ip)
            if not data or now >= data["reset_at"]:
                # First check in new window
                self._storage[clean_ip] = {
                    "count": 1,
                    "reset_at": now + self.window_seconds,
                }
                return self.max_free_checks - 1

            data["count"] += 1
            remaining = max(0, self.max_free_checks - data["count"])
            return remaining

    def get_remaining(self, ip: str) -> int:
        """Get remaining free checks for the given IP without incrementing."""
        _, remaining, _ = self.check_guest_limit(ip)
        return remaining

    def reset_ip(self, ip: str) -> None:
        """Reset quota for an IP (for testing purposes)."""
        clean_ip = ip.strip() or "127.0.0.1"
        with self._lock:
            if clean_ip in self._storage:
                del self._storage[clean_ip]


class AuthRateLimiter:
    """
    Enterprise rate limiter for Authentication endpoints.
    Protects /v1/auth/login against credential brute-forcing,
    and /v1/auth/register against bot account spamming.
    """

    def __init__(
        self,
        max_login_failures: int = 5,
        failure_window_sec: int = 60,
        lockout_duration_sec: int = 900,
        max_registrations_per_hour: int = 10,
    ):
        self.max_login_failures = max_login_failures
        self.failure_window_sec = failure_window_sec
        self.lockout_duration_sec = lockout_duration_sec
        self.max_registrations = max_registrations_per_hour
        self._lock = threading.Lock()
        # ip -> {"failures": int, "window_start": float, "lockout_until": float}
        self._login_attempts: Dict[str, Dict[str, Any]] = {}
        # ip -> [timestamp1, timestamp2, ...]
        self._registrations: Dict[str, list] = {}

    def check_login_allowed(self, ip: str) -> Tuple[bool, int]:
        """
        Check if IP is allowed to attempt login.
        Returns: (is_allowed: bool, retry_after_sec: int)
        """
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()

        with self._lock:
            entry = self._login_attempts.get(clean_ip)
            if not entry:
                return True, 0

            lockout_until = entry.get("lockout_until", 0)
            if now < lockout_until:
                return False, int(lockout_until - now)

            # If lockout expired, reset
            if lockout_until > 0 and now >= lockout_until:
                del self._login_attempts[clean_ip]
                return True, 0

            # If window expired without lockout, reset count
            if now - entry["window_start"] > self.failure_window_sec:
                del self._login_attempts[clean_ip]
                return True, 0

            return True, 0

    def record_login_failure(self, ip: str) -> Tuple[bool, int]:
        """
        Record a failed login attempt for the given IP.
        Returns: (is_now_locked: bool, retry_after_sec: int)
        """
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()

        with self._lock:
            entry = self._login_attempts.get(clean_ip)
            if not entry or (now - entry["window_start"] > self.failure_window_sec):
                entry = {
                    "failures": 1,
                    "window_start": now,
                    "lockout_until": 0,
                }
                self._login_attempts[clean_ip] = entry
                return False, 0

            entry["failures"] += 1
            if entry["failures"] >= self.max_login_failures:
                entry["lockout_until"] = now + self.lockout_duration_sec
                return True, self.lockout_duration_sec

            return False, 0

    def record_login_success(self, ip: str) -> None:
        """Clear login failures on successful authentication."""
        clean_ip = ip.strip() or "127.0.0.1"
        with self._lock:
            if clean_ip in self._login_attempts:
                del self._login_attempts[clean_ip]

    def check_register_allowed(self, ip: str) -> Tuple[bool, int]:
        """
        Check if IP is allowed to register another account.
        Returns: (is_allowed: bool, remaining_hourly: int)
        """
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()
        one_hour_ago = now - 3600

        with self._lock:
            timestamps = self._registrations.get(clean_ip, [])
            valid_timestamps = [t for t in timestamps if t > one_hour_ago]
            self._registrations[clean_ip] = valid_timestamps

            if len(valid_timestamps) >= self.max_registrations:
                return False, 0

            return True, self.max_registrations - len(valid_timestamps)

    def record_register(self, ip: str) -> None:
        """Record an account registration timestamp."""
        clean_ip = ip.strip() or "127.0.0.1"
        now = time.time()
        with self._lock:
            if clean_ip not in self._registrations:
                self._registrations[clean_ip] = []
            self._registrations[clean_ip].append(now)

