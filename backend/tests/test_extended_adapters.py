"""
Test suite for Extended Platform Adapters - TDD Red Phase
Validates Apple/iMessage, RCS, Social Footprint (Instagram/Facebook/LinkedIn), and Crypto (Binance).
"""
import pytest
from app.core.normalizer import PhoneNormalizer, LineType
from app.adapters.base import PlatformType, PlatformCheckResult
from app.adapters.apple import AppleAdapter
from app.adapters.rcs import RcsAdapter
from app.adapters.social import SocialFootprintAdapter
from app.adapters.crypto import CryptoAdapter


def test_apple_adapter_detects_imessage_for_valid_mobile():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+14155552671")
    
    adapter = AppleAdapter()
    result = adapter.check(phone)
    
    assert isinstance(result, PlatformCheckResult)
    assert result.platform == PlatformType.IMESSAGE
    assert result.is_registered is True
    assert result.confidence_score >= 85
    assert result.details.get("has_imessage") is True


def test_apple_adapter_skips_landlines():
    normalizer = PhoneNormalizer()
    # Fixed line check
    phone = normalizer.normalize("+12125551234")  # US number
    
    adapter = AppleAdapter()
    # Force landline test
    result = adapter.check(phone)
    assert isinstance(result, PlatformCheckResult)


def test_rcs_adapter_detects_android_capabilities():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+212 661 123456")
    
    adapter = RcsAdapter()
    result = adapter.check(phone)
    
    assert result.platform == PlatformType.RCS
    assert result.is_registered is True
    assert "rcs_version" in result.details


def test_social_footprint_adapter():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+212 661 123456")
    
    adapter = SocialFootprintAdapter()
    results = adapter.check_all(phone)
    
    assert "instagram" in results
    assert "facebook" in results
    assert "linkedin" in results
    assert results["instagram"].platform == PlatformType.INSTAGRAM


def test_crypto_adapter_binance_detection():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+212 661 123456")
    
    adapter = CryptoAdapter()
    result = adapter.check(phone)
    
    assert result.platform == PlatformType.BINANCE
    assert result.confidence_score >= 80
    assert "is_kyc_verified" in result.details
