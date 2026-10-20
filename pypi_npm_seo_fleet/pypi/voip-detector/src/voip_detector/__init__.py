"""
voip-detector
Detect virtual VoIP numbers, burner phones, Google Voice, TextNow, Skype, and temporary SMS services to prevent account fraud.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.2"
__all__ = ["Client", "check_phone", "PhoneResult"]
