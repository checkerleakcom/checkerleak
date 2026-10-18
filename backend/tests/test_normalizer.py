"""
Test suite for PhoneNormalizer - TDD Red Phase
Ensures strict E.164 compliance, country detection, line type classification, and boundary handling.
"""
import pytest
from app.core.normalizer import PhoneNormalizer, LineType, NormalizedPhone


def test_valid_moroccan_mobile_number():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("+212 661 123456")
    
    assert isinstance(result, NormalizedPhone)
    assert result.is_valid is True
    assert result.e164 == "+212661123456"
    assert result.country_code == 212
    assert result.country_iso == "MA"
    assert result.line_type == LineType.MOBILE


def test_valid_us_number_with_punctuation():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("(415) 555-2671", default_country="US")
    
    assert result.is_valid is True
    assert result.e164 == "+14155552671"
    assert result.country_code == 1
    assert result.country_iso == "US"


def test_international_prefix_with_zeros():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("0033612345678")
    
    assert result.is_valid is True
    assert result.e164 == "+33612345678"
    assert result.country_iso == "FR"
    assert result.line_type == LineType.MOBILE


def test_invalid_phone_number_handling():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("12345")
    
    assert result.is_valid is False
    assert result.e164 is None
    assert result.error == "INVALID_NUMBER_FORMAT"


def test_empty_or_whitespace_input():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("   ")
    
    assert result.is_valid is False
    assert result.error == "EMPTY_INPUT"


def test_immutability_of_result():
    normalizer = PhoneNormalizer()
    result = normalizer.normalize("+14155552671")
    
    with pytest.raises(Exception):
        result.e164 = "+999999999"  # Model should be frozen/immutable
