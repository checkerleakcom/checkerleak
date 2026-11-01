"""
Test Suite: Admin Unified Access (Client Portal & Admin Cockpit)
Verifies that the admin can seamlessly log into the client portal with the admin credentials,
has 999,999 credits, and can transition between admin cockpit and client portal.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.admin_router import ADMIN_SECRET_KEY

client = TestClient(app)


def test_admin_login_as_client_with_full_email():
    """Verify admin can authenticate on /v1/auth/login using admin@checkerleak.com and ADMIN_SECRET_KEY."""
    res = client.post("/v1/auth/login", json={
        "email": "admin@checkerleak.com",
        "password": ADMIN_SECRET_KEY
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["user"]["email"] == "admin@checkerleak.com"
    assert data["user"]["credits"] >= 999999
    assert data["user"]["email_verified"] is True
    assert data["token"].startswith("clk_live_master_admin_")


def test_admin_login_as_client_with_short_username():
    """Verify admin can authenticate on /v1/auth/login simply using 'admin' as username."""
    res = client.post("/v1/auth/login", json={
        "email": "admin",
        "password": ADMIN_SECRET_KEY
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["user"]["email"] == "admin@checkerleak.com"
    assert data["user"]["credits"] >= 999999


def test_admin_login_with_wrong_password():
    """Verify that wrong password for admin returns 401."""
    res = client.post("/v1/auth/login", json={
        "email": "admin@checkerleak.com",
        "password": "WrongPassword123!"
    })
    assert res.status_code == 401


def test_admin_client_session_endpoint():
    """Verify /v1/admin/client-session generates client portal session."""
    res = client.get("/v1/admin/client-session", headers={
        "X-Admin-Key": ADMIN_SECRET_KEY
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["success"] is True
    assert data["user"]["email"] == "admin@checkerleak.com"
    assert data["token"].startswith("clk_live_master_admin_")


def test_prevent_public_registration_of_admin_email():
    """Verify external attackers cannot register the admin email."""
    res = client.post("/v1/auth/register", json={
        "email": "admin@checkerleak.com",
        "password": "AttackerPassword123!",
        "full_name": "Fake Admin"
    })
    assert res.status_code == 400
    assert "reserved for administration" in res.json()["detail"]
