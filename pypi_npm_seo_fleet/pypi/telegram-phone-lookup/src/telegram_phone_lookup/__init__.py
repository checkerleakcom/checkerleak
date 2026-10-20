"""
telegram-phone-lookup
Telegram Phone Number OSINT Tool. Verifies active Telegram account registration, user ID footprints, and profile status.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.2"
__all__ = ["Client", "check_phone", "PhoneResult"]
