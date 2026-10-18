"""
Comprehensive Unit & Integration Tests for Crypto Exchange Accuracy & Zero-Hallucination Policy.
Verifies Binance, OKX, KuCoin, HTX, CoinW, and Crypto.com email and phone checkers:
- False positives eliminated: Non-existent emails (SMTP 550) return False (MAKINSH).
- Disposable burner emails return False (MAKINSH).
- Unlinked emails return False (MAKINSH) with honest non-registration status.
- Real corporate / verified Web3 / directory traders return True (KAIN).
- VoIP and landlines are rejected for exchange KYC mobile binding.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.core.universal_engine import UniversalCheckerEngine
from app.core.crypto_exchange_probe import CryptoExchangeProbeService, CryptoExchangeResult
from app.core.native_email_probe import NativeEmailProbeResult


@pytest.fixture
def engine():
    return UniversalCheckerEngine()


@pytest.fixture
def probe():
    return CryptoExchangeProbeService()


# ==============================================================================
# 1. EMAIL VERIFICATION ACCURACY (True Negative vs True Positive)
# ==============================================================================

def test_crypto_nonexistent_email_returns_false_makinsh(engine):
    """
    Emails that fail SMTP recipient handshake (550 NoSuchUser) CANNOT have an active
    crypto exchange account. Engine must return is_registered=False (MAKINSH).
    """
    target = "totallyfakenonexistenttrader998877@gmail.com"
    
    # Mock SMTP to simulate 550 mailbox rejection
    mock_email_result = NativeEmailProbeResult(
        email=target,
        domain="gmail.com",
        is_valid_format=True,
        is_registered=False,
        confidence_score=99,
        risk_level="CRITICAL",
        detection_method="LIVE_SMTP_HANDSHAKE",
        status_summary="Recipient address rejected: 550-5.1.1 The email account that you tried to reach does not exist.",
        details={"smtp_code": 550},
    )

    with patch.object(engine.email_probe, "verify", return_value=mock_email_result):
        res = engine.execute_check("binance_email_checker", target)
        assert res.is_registered is False, "Non-existent mailbox must NEVER be reported as registered!"
        assert res.confidence_score >= 95
        assert res.details.get("detection_method") == "SMTP_DELIVERABILITY_EXCLUSION"
        assert "Cannot be registered" in res.status_summary or "does not exist" in res.status_summary


def test_crypto_disposable_burner_email_rejected_makinsh(engine):
    """
    Burner / disposable email inboxes (e.g. mailinator, tempmail) are strictly prohibited
    by Binance/OKX AML & KYC regulations. Must return is_registered=False (MAKINSH).
    """
    target = "scammer_burner_lead@mailinator.com"
    res = engine.execute_check("binance_email_checker", target)
    assert res.is_registered is False
    assert res.confidence_score >= 95
    assert res.risk_level == "CRITICAL"
    assert res.details.get("is_disposable") is True or res.details.get("detection_method") == "AML_DISPOSABLE_BLACKLIST"


def test_crypto_honest_unregistered_email_makinsh(engine):
    """
    Valid, active mailbox with no crypto presence must return is_registered=False (MAKINSH)
    instead of fabricating a fake VIP 2 or Tier-2 KYC status.
    """
    target = "regular.accountant.office@gmail.com"
    
    mock_email_result = NativeEmailProbeResult(
        email=target,
        domain="gmail.com",
        is_valid_format=True,
        is_registered=True,
        confidence_score=85,
        risk_level="LOW",
        detection_method="GLOBAL_IDENTITY_PROBE",
        status_summary="Mailbox active.",
        details={},
    )

    with patch.object(engine.email_probe, "verify", return_value=mock_email_result):
        with patch.object(engine.crypto_probe, "_check_web3_identity", return_value=False):
            res = engine.execute_check("binance_email_checker", target)
            assert res.is_registered is False, "Active email without crypto record must be False (MAKINSH)!"
            assert res.confidence_score == 88
            assert res.details.get("detection_method") == "EXCHANGE_ENUMERATION_INSPECTION"
            assert "NO registered trading account" in res.status_summary


def test_crypto_corporate_exchange_domain_kain(engine):
    """Official exchange domain emails (@binance.com) are confirmed internal traders when mailbox exists."""
    target = "vip.trader@binance.com"
    
    mock_email_result = NativeEmailProbeResult(
        email=target,
        domain="binance.com",
        is_valid_format=True,
        is_registered=True,
        confidence_score=95,
        risk_level="LOW",
        detection_method="LIVE_SMTP_HANDSHAKE",
        status_summary="Mailbox active on binance.com.",
        details={"mailbox_exists": True},
    )

    with patch.object(engine.email_probe, "verify", return_value=mock_email_result):
        res = engine.execute_check("binance_email_checker", target)
        assert res.is_registered is True, "Official exchange domain must be confirmed KAIN!"
        assert res.confidence_score >= 95
        assert res.details.get("detection_method") == "EXCHANGE_CORPORATE_IDENTITY"


def test_crypto_verified_trader_fixture_kain(engine):
    """Directory / verified trader fixtures must return is_registered=True (KAIN)."""
    target = "trader@pulsecheck.com"
    res = engine.execute_check("binance_email_checker", target)
    assert res.is_registered is True
    assert res.confidence_score >= 95
    assert res.details.get("detection_method") == "VERIFIED_TRADER_DIRECTORY"


def test_crypto_web3_identity_kain(engine):
    """When Web3 / Gravatar cryptographic identity is detected, returns is_registered=True."""
    target = "crypto_whale_alpha@gmail.com"
    
    mock_email_result = NativeEmailProbeResult(
        email=target,
        domain="gmail.com",
        is_valid_format=True,
        is_registered=True,
        confidence_score=90,
        risk_level="LOW",
        detection_method="LIVE_SMTP_HANDSHAKE",
        status_summary="Mailbox active.",
        details={},
    )

    with patch.object(engine.email_probe, "verify", return_value=mock_email_result):
        with patch.object(engine.crypto_probe, "_check_web3_identity", return_value=True):
            res = engine.execute_check("binance_email_checker", target)
            assert res.is_registered is True
            assert res.confidence_score >= 95
            assert res.details.get("detection_method") == "WEB3_CRYPTOGRAPHIC_IDENTITY_PROBE"


# ==============================================================================
# 2. PHONE VERIFICATION ACCURACY (Carrier & AML Enforcement)
# ==============================================================================

def test_crypto_phone_voip_burner_rejected_makinsh(engine):
    """VoIP virtual numbers (+14155550199) must be rejected by exchange AML policy."""
    res = engine.execute_check("binance_checker", "+14155550199", default_country="US")
    assert res.is_registered is False
    assert res.confidence_score >= 95
    assert res.risk_level == "HIGH"
    assert res.details.get("detection_method") == "CARRIER_AML_POLICY"
    assert res.details.get("kyc_eligible") is False


def test_crypto_phone_landline_rejected_makinsh(engine):
    """Fixed landlines cannot receive SMS 2FA and cannot be registered for exchange mobile KYC."""
    res = engine.execute_check("binance_checker", "+212522001122", default_country="MA")
    assert res.is_registered is False
    assert res.confidence_score >= 95
    assert res.details.get("detection_method") == "TELECOM_LINE_RESTRICTION"
    assert res.details.get("kyc_eligible") is False


def test_crypto_phone_verified_trader_kain(engine):
    """Known verified trader test phone (+212661234567) must return is_registered=True (KAIN)."""
    res = engine.execute_check("binance_checker", "+212661234567", default_country="MA")
    assert res.is_registered is True
    assert res.confidence_score >= 95
    assert res.details.get("kyc_eligible") is True
    assert res.details.get("detection_method") == "VERIFIED_TRADER_DIRECTORY"


# ==============================================================================
# 3. MULTI-EXCHANGE COVERAGE (Binance, OKX, KuCoin, HTX, CoinW, Crypto.com)
# ==============================================================================

@pytest.mark.parametrize("service_id,exchange_name", [
    ("binance_email_checker", "Binance"),
    ("okx_email_checker", "OKX"),
    ("kucoin_email_checker", "KuCoin"),
    ("htx_email_checker", "HTX (Huobi)"),
    ("coinw_email_checker", "CoinW"),
    ("crypto_com_email_checker", "Crypto.com"),
])
def test_all_crypto_exchanges_honor_zero_hallucination(engine, service_id, exchange_name):
    """All crypto exchange email checkers must strictly honor the zero-hallucination policy."""
    target = "clean_unregistered_student@gmail.com"
    
    mock_email_result = NativeEmailProbeResult(
        email=target,
        domain="gmail.com",
        is_valid_format=True,
        is_registered=True,
        confidence_score=85,
        risk_level="LOW",
        detection_method="GLOBAL_IDENTITY_PROBE",
        status_summary="Mailbox active.",
        details={},
    )

    with patch.object(engine.email_probe, "verify", return_value=mock_email_result):
        with patch.object(engine.crypto_probe, "_check_web3_identity", return_value=False):
            res = engine.execute_check(service_id, target)
            assert res.is_registered is False, f"Expected {service_id} to return False (MAKINSH)"
            assert res.details.get("exchange_platform") == exchange_name
