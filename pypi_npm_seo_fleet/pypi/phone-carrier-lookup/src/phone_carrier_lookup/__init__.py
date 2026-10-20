"""
phone-carrier-lookup
Ultra-fast Phone Carrier & Line Type Detector. Identifies Verizon, AT&T, T-Mobile, Vodafone, Orange, VoIP, and Prepaid SIMs.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.2"
__all__ = ["Client", "check_phone", "PhoneResult"]
