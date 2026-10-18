"""
Tests for Upstream Crypto Bridge and Dual-Engine Architecture.
"""
from unittest.mock import patch, MagicMock
from app.core.universal_engine import UniversalCheckerEngine


def test_crypto_local_mode_when_no_api_key():
    """Verify local enterprise heuristic engine works when no upstream API key is configured."""
    engine = UniversalCheckerEngine(upstream_api_key="")
    res = engine.execute_check("binance_checker", "+212661234567")
    assert res.is_valid_format is True
    assert res.is_registered is True
    assert res.details.get("kyc_eligible") is True


def test_crypto_upstream_bridge_when_api_key_configured():
    """Verify upstream bridge delegates to CheckNumber.ai network when API key is provided."""
    engine = UniversalCheckerEngine(upstream_api_key="cn_test_key_live_998877")

    mock_resp_data = b'{"registered": true, "confidence": 99, "status": "verified_on_chain", "exchange": "binance"}'
    mock_resp = MagicMock()
    mock_resp.read.return_value = mock_resp_data
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = engine.execute_check("binance_checker", "+212661234567")
        assert res.is_registered is True
        assert res.confidence_score == 99
        assert res.details.get("engine_mode") == "LIVE_UPSTREAM"
        assert res.details.get("provider") == "CheckNumber.ai"
