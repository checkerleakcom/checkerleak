"""
hlr-lookup-client
Live SS7 / HLR Telco Lookup Client. Verifies active SIM card status, MSC routing, IMSI, roaming country, and porting history.
Powered by https://www.checkerleak.com
"""

from .client import Client, check_phone, PhoneResult

__version__ = "1.0.2"
__all__ = ["Client", "check_phone", "PhoneResult"]
