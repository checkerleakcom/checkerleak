"""
CarrierService: Network carrier identification, HLR lookup simulation, and VoIP risk engine.
Returns frozen immutable models complying with ECC quality standards.
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict
import phonenumbers
from phonenumbers import carrier
from app.core.normalizer import NormalizedPhone, LineType


class CarrierInfo(BaseModel):
    """Immutable carrier and telephony network metadata."""
    model_config = ConfigDict(frozen=True)

    carrier_name: Optional[str] = None
    country_iso: Optional[str] = None
    is_known: bool = False
    is_voip: bool = False
    is_portable: bool = False
    mcc_mnc: Optional[str] = None
    risk_score: int = 0  # 0 (safe/real mobile) to 100 (high risk/invalid/spammer VoIP)


# Standard ITU / GSMA Mobile Country Codes (MCC)
MCC_TABLE = {
    "MA": "604",
    "US": "310",
    "FR": "208",
    "GB": "234",
    "DE": "262",
    "ES": "214",
    "IT": "222",
    "AE": "424",
    "SA": "420",
    "EG": "602",
    "DZ": "603",
    "TN": "605",
    "TR": "286",
    "RU": "250",
    "UA": "255",
    "BR": "724",
    "IN": "404",
    "CA": "302",
}

# Mobile Network Codes (MNC)
MNC_TABLE = {
    "Maroc Telecom": "01",
    "Orange": "00",
    "inwi": "02",
    "Inwi": "02",
    "AT&T": "410",
    "Verizon": "012",
    "T-Mobile": "260",
    "Sprint": "120",
    "Vodafone": "15",
    "EE": "30",
    "O2": "10",
    "SFR": "10",
    "Bouygues": "20",
    "Free": "15",
}


class CarrierService:
    """Service to look up telephony operator and assess line integrity."""

    def lookup(self, phone: NormalizedPhone, force_voip: bool = False) -> CarrierInfo:
        if not phone.is_valid or not phone.e164:
            return CarrierInfo(
                carrier_name=None,
                country_iso=None,
                is_known=False,
                is_voip=False,
                mcc_mnc=None,
                risk_score=100,
            )

        try:
            parsed = phonenumbers.parse(phone.e164, None)
            raw_carrier = carrier.name_for_number(parsed, "en")
        except Exception:
            raw_carrier = ""

        is_voip = force_voip or (phone.line_type == LineType.VOIP)
        carrier_name = raw_carrier if raw_carrier else ("VoIP Provider" if is_voip else None)

        # Risk scoring logic:
        # Real mobile number -> 0 risk
        # Fixed line -> 20 risk (cannot receive WhatsApp or SMS easily)
        # VoIP -> 75 risk (high disposable/bot spam rate)
        if is_voip:
            risk = 75
        elif phone.line_type == LineType.MOBILE:
            risk = 0
        elif phone.line_type == LineType.FIXED_LINE:
            risk = 30
        else:
            risk = 50

        # Compute realistic MCC/MNC
        country = phone.country_iso or "MA"
        mcc = MCC_TABLE.get(country, "999")
        mnc = MNC_TABLE.get(carrier_name, "01") if carrier_name else "00"
        mcc_mnc = f"{mcc}-{mnc}"

        return CarrierInfo(
            carrier_name=carrier_name,
            country_iso=phone.country_iso,
            is_known=bool(carrier_name),
            is_voip=is_voip,
            is_portable=True,
            mcc_mnc=mcc_mnc,
            risk_score=risk,
        )

