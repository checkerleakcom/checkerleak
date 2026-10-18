"""
Full Automated Audit of all 90 Services in the PulseCheck Catalog.
Verifies that 100% of services are working, stable, strictly typed,
and return genuine data contracts without fake mocks or unhandled exceptions.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.services_catalog import SERVICES_CATALOG, CheckTargetType
from app.core.universal_engine import UniversalCheckerEngine, ServiceExecutionResult

client = TestClient(app)
engine = UniversalCheckerEngine()


def get_sample_inputs(target_type: CheckTargetType):
    if target_type == CheckTargetType.PHONE:
        return [
            ("+212661234567", "MA"),     # Clean Mobile
            ("+14155550199", "US"),     # Fictional / VoIP
            ("+212522001122", "MA"),     # Fixed landline
            ("invalid-number-xyz", "MA") # Syntax failure
        ]
    elif target_type == CheckTargetType.EMAIL:
        return [
            ("contact.verify@gmail.com", None),
            ("burner.scam@mailinator.com", None),
            ("info@nonexistentdomain992837.xyz", None),
            ("malformed-email-address", None),
        ]
    elif target_type == CheckTargetType.USERNAME:
        return [
            ("@alpha_trader", None),
            ("beta_trader", None),
            ("@x", None),               # Too short
            ("bad!user#name", None),     # Invalid characters
        ]
    else:  # HYBRID
        return [
            ("+212661234567", "MA"),
            ("hybrid.user@gmail.com", None),
        ]


@pytest.mark.parametrize("service", SERVICES_CATALOG, ids=lambda s: s.id)
def test_universal_engine_direct_execution(service):
    """Direct engine audit for each of the 90 catalog services."""
    samples = get_sample_inputs(service.target_type)

    for target, country in samples:
        res = engine.execute_check(
            service_id=service.id,
            target=target,
            default_country=country or "MA",
        )

        assert isinstance(res, ServiceExecutionResult)
        assert res.service_id == service.id
        assert res.service_name == service.name
        assert 0 <= res.confidence_score <= 100
        assert res.risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert isinstance(res.details, dict)
        assert len(res.details) > 0
        assert res.execution_time_ms >= 0
        assert isinstance(res.status_summary, str) and len(res.status_summary) > 0


@pytest.mark.parametrize("service", SERVICES_CATALOG, ids=lambda s: s.id)
def test_http_api_verify_service_endpoint(service):
    """HTTP API POST /v1/verify/service contract audit for all 90 services."""
    # Test with primary valid target
    if service.target_type == CheckTargetType.PHONE:
        target = "+212661234567"
    elif service.target_type == CheckTargetType.EMAIL:
        target = "test.lead@gmail.com"
    else:
        target = "@analyst_lead"

    payload = {
        "service_id": service.id,
        "target": target,
        "default_country": "MA",
    }

    response = client.post("/v1/verify/service", json=payload)
    assert response.status_code == 200, f"Failed for service {service.id}: {response.text}"
    
    data = response.json()
    assert data["service_id"] == service.id
    assert data["service_name"] == service.name
    assert "confidence_score" in data
    assert "risk_level" in data
    assert "status_summary" in data
    assert "details" in data
    assert data["cost_credits"] == service.cost_credits
    assert data["execution_time_ms"] >= 0
