"""
VerificationPipeline: Next-generation smart cascading verification orchestrator.
Optimizes costs by short-circuiting dead leads and calculating unified reachability scores.
Supports WhatsApp, Telegram, Apple/iMessage, RCS, Social, and Crypto footprint channels.
"""
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict
from app.core.normalizer import PhoneNormalizer, NormalizedPhone, LineType
from app.core.carrier import CarrierService, CarrierInfo
from app.adapters.base import PlatformCheckResult
from app.adapters.whatsapp import WhatsAppAdapter
from app.adapters.telegram import TelegramAdapter
from app.adapters.apple import AppleAdapter
from app.adapters.rcs import RcsAdapter
from app.adapters.social import SocialFootprintAdapter
from app.adapters.crypto import CryptoAdapter


class LeadQuality(str, Enum):
    EXCELLENT = "EXCELLENT"      # Real mobile + active on messaging + 0 VoIP risk
    HIGH = "HIGH"                # Real mobile + active carrier
    MEDIUM = "MEDIUM"            # Fixed line or partial confidence
    LOW = "LOW"                  # VoIP or high risk score
    DEAD = "DEAD"                # Invalid phone format or unreachable


class VerificationReport(BaseModel):
    """Complete, immutable intelligence report for a phone number."""
    model_config = ConfigDict(frozen=True)

    raw_input: str
    is_valid: bool
    phone: NormalizedPhone
    carrier: Optional[CarrierInfo] = None
    whatsapp: Optional[PlatformCheckResult] = None
    telegram: Optional[PlatformCheckResult] = None
    imessage: Optional[PlatformCheckResult] = None
    rcs: Optional[PlatformCheckResult] = None
    social: Optional[Dict[str, PlatformCheckResult]] = None
    crypto: Optional[PlatformCheckResult] = None
    reachability_score: int       # 0 (dead) to 100 (maximum outreach probability)
    lead_quality: LeadQuality
    cost_savings_pct: int         # Estimated client savings from smart routing (0% to 100%)


class VerificationPipeline:
    """Cascading pipeline orchestrating normalization, carrier lookup, and platform probes."""

    def __init__(
        self,
        normalizer: Optional[PhoneNormalizer] = None,
        carrier_service: Optional[CarrierService] = None,
        whatsapp_adapter: Optional[WhatsAppAdapter] = None,
        telegram_adapter: Optional[TelegramAdapter] = None,
        apple_adapter: Optional[AppleAdapter] = None,
        rcs_adapter: Optional[RcsAdapter] = None,
        social_adapter: Optional[SocialFootprintAdapter] = None,
        crypto_adapter: Optional[CryptoAdapter] = None,
    ):
        self.normalizer = normalizer or PhoneNormalizer()
        self.carrier_service = carrier_service or CarrierService()
        self.whatsapp_adapter = whatsapp_adapter or WhatsAppAdapter()
        self.telegram_adapter = telegram_adapter or TelegramAdapter()
        self.apple_adapter = apple_adapter or AppleAdapter()
        self.rcs_adapter = rcs_adapter or RcsAdapter()
        self.social_adapter = social_adapter or SocialFootprintAdapter()
        self.crypto_adapter = crypto_adapter or CryptoAdapter()

    def verify_single(
        self,
        raw_number: str,
        default_country: Optional[str] = None,
        check_whatsapp: bool = True,
        check_telegram: bool = False,
        check_imessage: bool = False,
        check_rcs: bool = False,
        check_social: bool = False,
        check_crypto: bool = False,
    ) -> VerificationReport:
        # Step 1: Normalization (Free / Syntax check)
        phone = self.normalizer.normalize(raw_number, default_country)
        if not phone.is_valid:
            return VerificationReport(
                raw_input=raw_number,
                is_valid=False,
                phone=phone,
                reachability_score=0,
                lead_quality=LeadQuality.DEAD,
                cost_savings_pct=100,
            )

        # Step 2: Telephony & Carrier Risk
        carrier_info = self.carrier_service.lookup(phone)

        # Step 3: Smart Routing (Skip expensive checks if VoIP or dead fixed-line)
        whatsapp_res: Optional[PlatformCheckResult] = None
        telegram_res: Optional[PlatformCheckResult] = None
        imessage_res: Optional[PlatformCheckResult] = None
        rcs_res: Optional[PlatformCheckResult] = None
        social_res: Optional[Dict[str, PlatformCheckResult]] = None
        crypto_res: Optional[PlatformCheckResult] = None

        saved_steps = 0
        total_steps = (
            (1 if check_whatsapp else 0)
            + (1 if check_telegram else 0)
            + (1 if check_imessage else 0)
            + (1 if check_rcs else 0)
            + (1 if check_social else 0)
            + (1 if check_crypto else 0)
        )

        is_fixed = phone.line_type == LineType.FIXED_LINE

        if check_whatsapp:
            if is_fixed:
                saved_steps += 1
            else:
                whatsapp_res = self.whatsapp_adapter.check(phone)

        if check_telegram:
            telegram_res = self.telegram_adapter.check(phone)

        if check_imessage:
            if is_fixed:
                saved_steps += 1
            else:
                imessage_res = self.apple_adapter.check(phone)

        if check_rcs:
            if is_fixed:
                saved_steps += 1
            else:
                rcs_res = self.rcs_adapter.check(phone)

        if check_social:
            social_res = self.social_adapter.check_all(phone)

        if check_crypto:
            crypto_res = self.crypto_adapter.check(phone)

        cost_savings = int((saved_steps / total_steps) * 100) if total_steps > 0 else 0

        # Step 4: Compute Reachability Score & Lead Quality
        reachability = self._calculate_reachability(phone, carrier_info, whatsapp_res, imessage_res, crypto_res)
        lead_quality = self._classify_quality(reachability, carrier_info.is_voip)

        return VerificationReport(
            raw_input=raw_number,
            is_valid=True,
            phone=phone,
            carrier=carrier_info,
            whatsapp=whatsapp_res,
            telegram=telegram_res,
            imessage=imessage_res,
            rcs=rcs_res,
            social=social_res,
            crypto=crypto_res,
            reachability_score=reachability,
            lead_quality=lead_quality,
            cost_savings_pct=cost_savings,
        )

    def verify_batch(
        self,
        numbers: List[str],
        default_country: Optional[str] = None,
        check_whatsapp: bool = True,
        check_telegram: bool = False,
        check_imessage: bool = False,
        check_rcs: bool = False,
        check_social: bool = False,
        check_crypto: bool = False,
    ) -> List[VerificationReport]:
        return [
            self.verify_single(
                num,
                default_country=default_country,
                check_whatsapp=check_whatsapp,
                check_telegram=check_telegram,
                check_imessage=check_imessage,
                check_rcs=check_rcs,
                check_social=check_social,
                check_crypto=check_crypto,
            )
            for num in numbers
        ]

    def _calculate_reachability(
        self,
        phone: NormalizedPhone,
        carrier: CarrierInfo,
        whatsapp: Optional[PlatformCheckResult],
        imessage: Optional[PlatformCheckResult],
        crypto: Optional[PlatformCheckResult],
    ) -> int:
        score = 50  # Base for valid number
        if carrier.carrier_name:
            score += 15
        if carrier.is_voip:
            score -= 30
        if whatsapp and whatsapp.is_registered:
            score += 25
        if imessage and imessage.is_registered:
            score += 10
        if crypto and crypto.is_registered:
            score += 10

        return max(0, min(100, score))

    def _classify_quality(self, score: int, is_voip: bool) -> LeadQuality:
        if is_voip:
            return LeadQuality.LOW
        if score >= 85:
            return LeadQuality.EXCELLENT
        if score >= 65:
            return LeadQuality.HIGH
        if score >= 40:
            return LeadQuality.MEDIUM
        return LeadQuality.DEAD
