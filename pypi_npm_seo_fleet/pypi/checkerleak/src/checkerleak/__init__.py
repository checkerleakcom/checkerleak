"""
checkerleak
Official Python SDK & CLI for CheckerLeak.com - Real-Time Carrier Lookup, HLR Pings, WhatsApp, Telegram, and 102 OSINT Engines.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.4"
__all__ = ["Client", "check_phone", "PhoneResult"]
