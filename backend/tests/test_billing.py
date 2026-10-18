"""
Unit and Integration tests for Billing and Credit Top-up System.
"""
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import AuthService
from app.core.billing import BillingService, PlanTier, PaymentMethod

client = TestClient(app)
auth_service = AuthService()
billing_service = BillingService()


def test_list_billing_plans():
    response = client.get("/v1/billing/plans")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) == 3
    plan_ids = [p["id"] for p in plans]
    assert "starter" in plan_ids
    assert "pro" in plan_ids
    assert "enterprise" in plan_ids


def test_list_crypto_methods():
    response = client.get("/v1/billing/crypto-methods")
    assert response.status_code == 200
    methods = response.json()
    assert len(methods) >= 6
    method_ids = [m["id"] for m in methods]
    assert "CRYPTO_USDT_TRC20" in method_ids
    assert "CRYPTO_USDT_BEP20" in method_ids
    assert "CRYPTO_USDT_ERC20" in method_ids
    assert "CRYPTO_BTC" in method_ids
    assert "CRYPTO_ETH" in method_ids
    assert "CRYPTO_SOL" in method_ids
    for m in methods:
        assert "address" in m
        assert "network" in m
        assert "currency" in m


def test_create_checkout_session():
    unique_email = f"billing_tester_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "Billing Tester")

    # 1. Crypto Checkout - USDT TRC20
    payload_trc20 = {
        "user_id": user.id,
        "plan_id": "starter",
        "payment_method": "CRYPTO_USDT_TRC20",
    }
    resp_trc20 = client.post("/v1/billing/checkout", json=payload_trc20)
    assert resp_trc20.status_code == 200
    data_trc20 = resp_trc20.json()
    assert "deposit_address" in data_trc20
    assert "qr_code_hint" in data_trc20
    assert data_trc20["currency"] == "USDT"
    assert "TRC-20" in data_trc20["network"]
    assert data_trc20["credits_to_add"] == 1000

    # 2. Crypto Checkout - USDT BEP20
    payload_bep20 = {
        "user_id": user.id,
        "plan_id": "pro",
        "payment_method": "CRYPTO_USDT_BEP20",
    }
    resp_bep20 = client.post("/v1/billing/checkout", json=payload_bep20)
    assert resp_bep20.status_code == 200
    data_bep20 = resp_bep20.json()
    assert "BEP-20" in data_bep20["network"]
    assert data_bep20["credits_to_add"] == 5000

    # 3. Crypto Checkout - Bitcoin (BTC)
    payload_btc = {
        "user_id": user.id,
        "plan_id": "enterprise",
        "payment_method": "CRYPTO_BTC",
    }
    resp_btc = client.post("/v1/billing/checkout", json=payload_btc)
    assert resp_btc.status_code == 200
    data_btc = resp_btc.json()
    assert data_btc["currency"] == "BTC"
    assert data_btc["credits_to_add"] == 25000

    # 4. Stripe / Card Checkout is strictly REJECTED (Crypto Only platform)
    payload_stripe = {
        "user_id": user.id,
        "plan_id": "pro",
        "payment_method": "STRIPE_CARD",
    }
    resp_stripe = client.post("/v1/billing/checkout", json=payload_stripe)
    assert resp_stripe.status_code == 400
    assert "PAYMENT_METHOD_UNSUPPORTED" in resp_stripe.json()["detail"]


def test_confirm_topup_and_credit_wallet():
    unique_email = f"topup_tester_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "Topup Tester")
    initial_credits = user.credits

    payload = {
        "user_id": user.id,
        "plan_id": "pro",
        "payment_method": "CRYPTO_USDT_TRC20",
        "tx_hash": f"0x_{uuid.uuid4().hex[:12]}_trc20",
    }
    resp = client.post("/v1/billing/confirm-topup", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["credits_added"] == 5000
    assert data["new_wallet_balance"] == initial_credits + 5000

    # Stripe confirmation also rejected
    payload_stripe = {
        "user_id": user.id,
        "plan_id": "pro",
        "payment_method": "STRIPE_CARD",
    }
    resp_fail = client.post("/v1/billing/confirm-topup", json=payload_stripe)
    assert resp_fail.status_code == 400

    # Verify history
    resp_hist = client.get(f"/v1/billing/history?user_id={user.id}")
    assert resp_hist.status_code == 200
    history = resp_hist.json()
    assert len(history) >= 1
    assert history[0]["plan_id"] == "pro"
    assert history[0]["credits_added"] == 5000


def test_btc_deposit_address_and_mempool_endpoint():
    # 1. Verify official address in crypto-methods
    res = client.get("/v1/billing/crypto-methods")
    assert res.status_code == 200
    methods = {m["id"]: m for m in res.json()}
    assert "CRYPTO_BTC" in methods
    assert methods["CRYPTO_BTC"]["address"] == "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu"
    assert "mempool.space" in methods["CRYPTO_BTC"]["explorer_url"]

    # 2. Verify btc-status endpoint
    resp_status = client.get("/v1/billing/crypto/btc-status")
    assert resp_status.status_code == 200
    data = resp_status.json()
    assert data["address"] == "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu"
    assert "explorer_url" in data


def test_duplicate_tx_hash_anti_replay():
    unique_email = f"replay_tester_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "Replay Tester")
    distinct_tx = f"confirmed_onchain_{uuid.uuid4().hex}"

    # First top-up succeeds
    payload = {
        "user_id": user.id,
        "plan_id": "starter",
        "payment_method": "CRYPTO_USDT_TRC20",
        "tx_hash": distinct_tx,
    }
    resp1 = client.post("/v1/billing/confirm-topup", json=payload)
    assert resp1.status_code == 200

    # Second top-up with exact same hash must be rejected (anti-replay)
    resp2 = client.post("/v1/billing/confirm-topup", json=payload)
    assert resp2.status_code == 400
    assert "DUPLICATE_TX_HASH" in resp2.json()["detail"]


def test_verify_btc_tx_endpoint():
    res = client.get("/v1/billing/crypto/verify-btc-tx?tx_hash=mock_btc_hash_99")
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert data["simulated"] is True


def test_fake_btc_tx_rejected():
    unique_email = f"fraud_tester_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "Fraud Tester")
    fake_btc_hash = "0000000000000000000000000000000000000000000000000000000000000001"
    payload = {
        "user_id": user.id,
        "plan_id": "starter",
        "payment_method": "CRYPTO_BTC",
        "tx_hash": fake_btc_hash,
    }
    resp = client.post("/v1/billing/confirm-topup", json=payload)
    assert resp.status_code == 400
    assert "BTC_ONCHAIN_VERIFICATION_FAILED" in resp.json()["detail"]


def test_mempool_verification_mocked_success(monkeypatch):
    from unittest.mock import MagicMock
    import urllib.request
    import json
    from app.core.billing import verify_mempool_btc_tx, get_mempool_address_stats

    # 1. Test empty hash
    assert verify_mempool_btc_tx("")["error"] == "EMPTY_TX_HASH"

    # 2. Mock urlopen for successful transaction
    mock_tx = {
        "txid": "a" * 64,
        "vout": [
            {
                "scriptpubkey_address": "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu",
                "value": 50000,
            }
        ],
        "status": {"confirmed": True, "block_height": 850000, "block_time": 1720000000},
    }

    class MockResponse:
        def __init__(self, data, status=200):
            self.data = data
            self.status = status

        def read(self):
            return json.dumps(self.data).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def mock_urlopen(req, *args, **kwargs):
        url = req.full_url if hasattr(req, "full_url") else str(req)
        if "prices" in url:
            return MockResponse({"USD": 85000.0})
        elif "txs" in url:
            return MockResponse([mock_tx])
        elif "address" in url:
            return MockResponse({"chain_stats": {"tx_count": 1}, "mempool_stats": {}})
        else:
            return MockResponse(mock_tx)

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    res = verify_mempool_btc_tx("a" * 64)
    assert res["valid"] is True
    assert res["sats_received"] == 50000
    assert res["confirmed"] is True

    # 3. Test mismatch address
    mock_tx_mismatch = {
        "txid": "b" * 64,
        "vout": [{"scriptpubkey_address": "bc1qotheraddress", "value": 50000}],
        "status": {"confirmed": True},
    }
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: MockResponse(mock_tx_mismatch))
    res_mismatch = verify_mempool_btc_tx("b" * 64)
    assert res_mismatch["valid"] is False
    assert "TX_MISMATCH" in res_mismatch["error"]

    # 4. Test address stats helper
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)
    stats = get_mempool_address_stats()
    assert "address" in stats
    assert stats["address"] == "bc1q0v3g205psatdcj09ufzczahq50jusvvnlzsygu"


def test_billing_edge_cases():
    import pytest
    from app.core.billing import BillingService, PlanTier, PaymentMethod

    svc = BillingService()
    # Invalid plan
    with pytest.raises(ValueError, match="PLAN_NOT_FOUND"):
        svc.confirm_and_credit_wallet(user_id=1, plan_id="nonexistent_plan")

    # Invalid user
    with pytest.raises(ValueError, match="USER_NOT_FOUND"):
        svc.confirm_and_credit_wallet(user_id=999999, plan_id=PlanTier.STARTER)


def test_evm_deposit_address_and_endpoints():
    # 1. Verify EVM addresses in crypto-methods
    res = client.get("/v1/billing/crypto-methods")
    assert res.status_code == 200
    methods = {m["id"]: m for m in res.json()}
    for evm_id in ("CRYPTO_USDT_BEP20", "CRYPTO_USDT_ERC20", "CRYPTO_ETH"):
        assert evm_id in methods
        assert methods[evm_id]["address"] == "0x35dd60066ae6337b4D0273b129c0E222235B9F8C"
        assert "0x35dd60066ae6337b4D0273b129c0E222235B9F8C" in methods[evm_id]["explorer_url"]

    # 2. Verify evm-status endpoint
    resp_eth = client.get("/v1/billing/crypto/evm-status?chain=eth")
    assert resp_eth.status_code == 200
    assert resp_eth.json()["address"] == "0x35dd60066ae6337b4D0273b129c0E222235B9F8C"
    assert "etherscan" in resp_eth.json()["explorer_url"]

    resp_bsc = client.get("/v1/billing/crypto/evm-status?chain=bsc")
    assert resp_bsc.status_code == 200
    assert resp_bsc.json()["address"] == "0x35dd60066ae6337b4D0273b129c0E222235B9F8C"
    assert "bscscan" in resp_bsc.json()["explorer_url"]

    # 3. Verify simulated EVM hash
    resp_verify = client.get("/v1/billing/crypto/verify-evm-tx?tx_hash=mock_evm_tx_123")
    assert resp_verify.status_code == 200
    assert resp_verify.json()["valid"] is True
    assert resp_verify.json()["simulated"] is True


def test_evm_verification_mock(monkeypatch):
    import urllib.request
    import json
    from app.core.billing import verify_evm_tx

    assert verify_evm_tx("")["error"] == "EMPTY_TX_HASH"

    # Mock RPC response for successful direct match
    mock_rpc_result = {
        "jsonrpc": "2.0",
        "result": {
            "blockNumber": "0x1000",
            "from": "0x1111111111111111111111111111111111111111",
            "to": "0x35dd60066ae6337b4D0273b129c0E222235B9F8C",
            "input": "0x",
        },
        "id": 1,
    }

    class MockRpcResponse:
        def read(self):
            return json.dumps(mock_rpc_result).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    valid_evm_hash = "0x" + "c" * 64
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: MockRpcResponse())
    res = verify_evm_tx(valid_evm_hash, chain="eth")
    assert res["valid"] is True
    assert res["confirmed"] is True

    # Test address mismatch
    mock_rpc_mismatch = {
        "jsonrpc": "2.0",
        "result": {
            "blockNumber": "0x1000",
            "to": "0x0000000000000000000000000000000000000000",
            "input": "0x",
        },
        "id": 1,
    }

    class MockMismatchResponse:
        def read(self):
            return json.dumps(mock_rpc_mismatch).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: MockMismatchResponse())
    res_mismatch = verify_evm_tx(valid_evm_hash, chain="eth")
    assert res_mismatch["valid"] is False
    assert "TX_MISMATCH" in res_mismatch["error"]


def test_auto_detect_onchain_deposit():
    unique_email = f"autodetect_{uuid.uuid4().hex[:8]}@pulsecheck.com"
    user = auth_service.register(unique_email, "pass12345", "AutoDetect Tester")
    initial_credits = user.credits

    payload = {
        "user_id": user.id,
        "plan_id": "pro",
        "payment_method": "CRYPTO_USDT_TRC20",
    }
    resp = client.post("/v1/billing/crypto/auto-detect", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["credits_added"] == 5000
    assert data["new_wallet_balance"] == initial_credits + 5000
    assert data["settlement"] == "INSTANT_0_CONF_MEMPOOL"





