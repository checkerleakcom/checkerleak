"""
Test suite for Platform Adapters (WhatsApp, Telegram, Social Footprint) - TDD
"""
import pytest
from app.core.normalizer import PhoneNormalizer
from app.adapters.base import PlatformCheckResult, PlatformType
from app.adapters.whatsapp import WhatsAppAdapter
from app.adapters.telegram import TelegramAdapter


def test_whatsapp_adapter_detects_registered():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+212 661 123456")
    
    adapter = WhatsAppAdapter()
    result = adapter.check(phone)
    
    assert isinstance(result, PlatformCheckResult)
    assert result.platform == PlatformType.WHATSAPP
    assert result.is_registered is True
    assert result.confidence_score >= 80


def test_telegram_adapter_detects_account():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("+212 661 123456")
    
    adapter = TelegramAdapter()
    result = adapter.check(phone)
    
    assert isinstance(result, PlatformCheckResult)
    assert result.platform == PlatformType.TELEGRAM
    assert result.is_registered is True


def test_adapter_fails_fast_on_invalid_phone():
    normalizer = PhoneNormalizer()
    phone = normalizer.normalize("invalid")
    
    adapter = WhatsAppAdapter()
    result = adapter.check(phone)
    
    assert result.is_registered is False
    assert result.confidence_score == 0
    assert result.error == "INVALID_PHONE"
