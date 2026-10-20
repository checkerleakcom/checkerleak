"""
whatsapp-phone-checker
High-speed WhatsApp Number Probe. Checks if a phone number is registered on WhatsApp, business status, and profile footprint.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.2"
__all__ = ["Client", "check_phone", "PhoneResult"]
