"""
Tests for NativeEmailProbeService.
Tests real live existence probe, Gravatar detection, and invalid format handling.
"""
from app.core.native_email_probe import NativeEmailProbeService, NativeEmailProbeResult

service = NativeEmailProbeService(smtp_timeout=4.0)


def test_invalid_email_format():
    res = service.verify("invalid-email-address")
    assert isinstance(res, NativeEmailProbeResult)
    assert res.is_valid_format is False
    assert res.is_registered is False
    assert res.risk_level == "CRITICAL"


def test_nonexistent_email_live_google_smtp():
    """Verify that a fake random email is accurately reported as NOT existing by Google MX."""
    res = service.verify("fake_nonexistent_random_user_99881122@this-domain-does-not-exist-9912.com")
    assert isinstance(res, NativeEmailProbeResult)
    assert res.is_valid_format is True
    assert res.is_registered is False


def test_gravatar_identity_detection():
    """Verify Gravatar avatar detection for known address."""
    res = service.verify("matt@automattic.com")
    assert isinstance(res, NativeEmailProbeResult)
    assert res.is_valid_format is True
    assert res.is_registered is True
    assert res.confidence_score == 99
    assert res.detection_method == "GLOBAL_IDENTITY_PROBE"
