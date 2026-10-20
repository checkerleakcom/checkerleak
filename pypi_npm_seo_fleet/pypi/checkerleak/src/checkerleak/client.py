import os
import requests
from typing import Optional, Dict, Any

DEFAULT_BASE_URL = os.getenv("CHECKERLEAK_BASE_URL", "https://www.checkerleak.com")


class PhoneResult:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.phone = raw.get("phone", "")
        self.carrier = raw.get("carrier", "Unknown")
        self.line_type = raw.get("lead_quality", raw.get("line_type", "Mobile"))
        self.reachability_score = raw.get("reachability_score", 90)
        self.is_valid = bool(raw.get("is_valid", True))
        self.whatsapp = raw.get("whatsapp", {})
        self.telegram = raw.get("telegram", {})

    def to_dict(self) -> Dict[str, Any]:
        return self.raw

    def __repr__(self) -> str:
        return f"<PhoneResult phone={self.phone} carrier={self.carrier} line_type={self.line_type} score={self.reachability_score}>"


class Client:
    """
    CheckerLeak Python SDK Client.
    Get your API key at https://www.checkerleak.com/dashboard
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key or os.getenv("CHECKERLEAK_API_KEY")
        self.base_url = base_url.rstrip("/")

    def verify(self, phone: str) -> PhoneResult:
        url = f"{self.base_url}/v1/verify"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        payload = {"phone": phone}
        res = requests.post(url, json=payload, headers=headers, timeout=12.0)
        res.raise_for_status()
        return PhoneResult(res.json())


def check_phone(phone: str, api_key: Optional[str] = None) -> PhoneResult:
    """Quick helper to check any international phone number."""
    return Client(api_key=api_key).verify(phone)
