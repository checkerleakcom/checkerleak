"""
PhoneNormalizer: High-performance E.164 phone parser, region detector, and line-type classifier.
Enforces strict immutability and robust error classification.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberType


class LineType(str, Enum):
    MOBILE = "MOBILE"
    FIXED_LINE = "FIXED_LINE"
    VOIP = "VOIP"
    TOLL_FREE = "TOLL_FREE"
    PREMIUM_RATE = "PREMIUM_RATE"
    SHARED_COST = "SHARED_COST"
    UNKNOWN = "UNKNOWN"


_PHONE_TYPE_MAP = {
    PhoneNumberType.MOBILE: LineType.MOBILE,
    PhoneNumberType.FIXED_LINE: LineType.FIXED_LINE,
    PhoneNumberType.FIXED_LINE_OR_MOBILE: LineType.MOBILE,
    PhoneNumberType.VOIP: LineType.VOIP,
    PhoneNumberType.TOLL_FREE: LineType.TOLL_FREE,
    PhoneNumberType.PREMIUM_RATE: LineType.PREMIUM_RATE,
    PhoneNumberType.SHARED_COST: LineType.SHARED_COST,
}


class NormalizedPhone(BaseModel):
    """Immutable representation of normalized phone verification result."""
    model_config = ConfigDict(frozen=True)

    raw_input: str
    is_valid: bool
    e164: Optional[str] = None
    national_number: Optional[str] = None
    country_code: Optional[int] = None
    country_iso: Optional[str] = None
    line_type: LineType = LineType.UNKNOWN
    error: Optional[str] = None


class PhoneNormalizer:
    """Service to parse, validate, and normalize international phone numbers."""

    def normalize(self, raw_input: str, default_country: Optional[str] = None) -> NormalizedPhone:
        if not raw_input or not raw_input.strip():
            return NormalizedPhone(
                raw_input=raw_input or "",
                is_valid=False,
                error="EMPTY_INPUT",
            )

        cleaned_text = raw_input.strip()
        if cleaned_text.startswith("00") and len(cleaned_text) > 4 and cleaned_text[2].isdigit():
            cleaned_text = "+" + cleaned_text[2:]

        try:
            parsed = phonenumbers.parse(cleaned_text, default_country)
        except NumberParseException:
            return NormalizedPhone(
                raw_input=cleaned_text,
                is_valid=False,
                error="INVALID_NUMBER_FORMAT",
            )

        is_valid = phonenumbers.is_valid_number(parsed)
        if not is_valid:
            return NormalizedPhone(
                raw_input=cleaned_text,
                is_valid=False,
                error="INVALID_NUMBER_FORMAT",
            )

        e164_val = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        country_iso = phonenumbers.region_code_for_number(parsed)
        raw_type = phonenumbers.number_type(parsed)
        line_type = _PHONE_TYPE_MAP.get(raw_type, LineType.UNKNOWN)

        return NormalizedPhone(
            raw_input=cleaned_text,
            is_valid=True,
            e164=e164_val,
            national_number=str(parsed.national_number),
            country_code=parsed.country_code,
            country_iso=country_iso,
            line_type=line_type,
            error=None,
        )
