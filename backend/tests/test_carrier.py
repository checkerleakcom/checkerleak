"""
Test suite for CarrierService - TDD
Validates carrier identification, ported number flags, and VoIP risk profiling.
"""
from app.core.normalizer import PhoneNormalizer
from app.core.carrier import CarrierService, CarrierInfo


def test_carrier_identification_for_moroccan_number():
    normalizer = PhoneNormalizer()
    service = CarrierService()
    
    phone = normalizer.normalize("+212 661 123456")
    info = service.lookup(phone)
    
    assert isinstance(info, CarrierInfo)
    assert info.carrier_name is not None
    assert "Maroc Telecom" in info.carrier_name or "IAM" in info.carrier_name
    assert info.is_voip is False
    assert info.risk_score == 0


def test_carrier_lookup_for_invalid_phone():
    normalizer = PhoneNormalizer()
    service = CarrierService()
    
    phone = normalizer.normalize("invalid")
    info = service.lookup(phone)
    
    assert info.is_known is False
    assert info.carrier_name is None
    assert info.risk_score == 100


def test_voip_risk_calculation():
    normalizer = PhoneNormalizer()
    service = CarrierService()
    
    # Simulate a VOIP line classification
    phone = normalizer.normalize("+14155552671")
    info = service.lookup(phone, force_voip=True)
    
    assert info.is_voip is True
    assert info.risk_score >= 70
