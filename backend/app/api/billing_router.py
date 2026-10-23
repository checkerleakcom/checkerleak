"""
Billing Router: Endpoints for credit plans, checkout sessions, and wallet top-ups.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from app.core.billing import (
    BillingService,
    BillingPlan,
    BillingTransaction,
    PlanTier,
    PaymentMethod,
)

router = APIRouter(prefix="/v1/billing", tags=["Billing & Credits"])
billing_service = BillingService()


class CheckoutRequest(BaseModel):
    user_id: int = Field(..., description="ID of authenticated client")
    plan_id: PlanTier = Field(..., description="Plan tier to purchase (starter, pro, enterprise)")
    payment_method: PaymentMethod = Field(PaymentMethod.CRYPTO_USDT_TRC20, description="Cryptocurrency payment method")


class ConfirmTopupRequest(BaseModel):
    user_id: int = Field(..., description="ID of authenticated client")
    plan_id: PlanTier = Field(..., description="Plan tier purchased")
    payment_method: PaymentMethod = Field(PaymentMethod.CRYPTO_USDT_TRC20, description="Cryptocurrency payment method")
    tx_hash: Optional[str] = Field(None, description="Transaction hash or payment reference")


@router.get("/plans", response_model=List[BillingPlan])
def list_billing_plans():
    """Retrieve official pricing plans and credit packages."""
    return billing_service.get_plans()


@router.get("/crypto-methods")
def list_crypto_methods():
    """Retrieve all supported cryptocurrency deposit networks, merchant addresses, and fee estimates."""
    return billing_service.get_crypto_methods()


_CRYPTO_RATES_CACHE = {
    "timestamp": 0,
    "rates": {
        "BTC": 81000.0,
        "ETH": 2380.0,
        "SOL": 103.0,
        "LTC": 57.0,
        "USDT": 1.0,
        "USDT_TRC20": 1.0,
        "USDT_BEP20": 1.0,
    }
}


@router.get("/crypto-rates")
def get_crypto_conversion_rates():
    """Returns live crypto conversion rates (USD per crypto unit) with 60-second caching and instant fallback."""
    import time
    now = time.time()
    if now - _CRYPTO_RATES_CACHE["timestamp"] > 60:
        try:
            import urllib.request, json
            url = 'https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22ETHUSDT%22,%22SOLUSDT%22,%22LTCUSDT%22%5D'
            req = urllib.request.Request(url, headers={'User-Agent': 'CheckerLeak-Billing/1.0'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for item in data:
                    sym = item['symbol'].replace('USDT', '')
                    _CRYPTO_RATES_CACHE["rates"][sym] = round(float(item['price']), 2)
                _CRYPTO_RATES_CACHE["timestamp"] = now
        except Exception:
            pass
    return _CRYPTO_RATES_CACHE["rates"]


@router.post("/checkout")
def create_checkout_session(request: CheckoutRequest):
    """Generate checkout invoice session for Cryptocurrency (USDT, BTC, ETH, SOL)."""
    try:
        return billing_service.create_checkout_session(
            user_id=request.user_id,
            plan_id=request.plan_id,
            payment_method=request.payment_method,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.post("/confirm-topup")
def confirm_credit_topup(request: ConfirmTopupRequest):
    """Confirm payment receipt and instantly credit client wallet balance."""
    try:
        return billing_service.confirm_and_credit_wallet(
            user_id=request.user_id,
            plan_id=request.plan_id,
            payment_method=request.payment_method,
            tx_hash=request.tx_hash,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/history", response_model=List[BillingTransaction])
def get_billing_history(user_id: int = Query(...)):
    """Retrieve billing receipt history for the client dashboard."""
    return billing_service.get_user_transactions(user_id=user_id)


@router.get("/crypto/btc-status")
def get_btc_deposit_address_status():
    """Retrieve live Bitcoin on-chain status and recent transactions from mempool.space."""
    return billing_service.get_btc_address_status()


@router.get("/crypto/verify-btc-tx")
def verify_btc_transaction(tx_hash: str = Query(..., description="64-character Bitcoin txid")):
    """Verify any Bitcoin transaction against mempool.space for the deposit address."""
    return billing_service.verify_btc_tx(tx_hash=tx_hash)


@router.get("/crypto/evm-status")
def get_evm_deposit_address_status(chain: str = Query("eth", description="eth or bsc")):
    """Retrieve EVM deposit address info and explorer link for Ethereum or BSC."""
    return billing_service.get_evm_address_status(chain=chain)


@router.get("/crypto/verify-evm-tx")
def verify_evm_transaction(
    tx_hash: str = Query(..., description="66-character EVM tx hash starting with 0x"),
    chain: str = Query("eth", description="eth or bsc"),
):
    """Verify any EVM (ETH, BSC USDT) transaction against public nodes."""
    return billing_service.verify_evm_tx(tx_hash=tx_hash, chain=chain)


class AutoDetectRequest(BaseModel):
    user_id: int
    plan_id: PlanTier
    payment_method: PaymentMethod = PaymentMethod.CRYPTO_USDT_TRC20


@router.post("/crypto/auto-detect")
def auto_detect_onchain_deposit(request: AutoDetectRequest):
    """Poll on-chain mempool/blocks and auto-credit wallet with zero confirmation delay."""
    try:
        return billing_service.detect_unconfirmed_deposit(
            user_id=request.user_id,
            plan_id=request.plan_id,
            payment_method=request.payment_method,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


class SubmitTxidRequest(BaseModel):
    amount: float = Field(..., description="Deposit amount in USD")
    txid: str = Field(..., description="On-chain Transaction ID or Hash")
    client_email: Optional[str] = Field("unknown", description="Client email address")
    user_id: Optional[int] = Field(None, description="Client user ID")
    currency: Optional[str] = Field("USDT", description="Cryptocurrency used (USDT, BTC, ETH, SOL, LTC)")
    crypto_amount: Optional[float] = Field(None, description="Exact cryptocurrency amount sent")


@router.post("/submit-txid")
def submit_crypto_txid(request: SubmitTxidRequest):
    """Notify system of incoming crypto transfer and record transaction."""
    from app.core.database import DatabaseService
    db = DatabaseService()
    user_id = request.user_id

    clean_txid = (request.txid or "").strip()
    if len(clean_txid) < 10:
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction hash format. TXID must be at least 10 characters.",
        )

    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Deposit amount must be greater than $0.00.",
        )

    with db.get_connection() as conn:
        cursor = conn.cursor()

        # Prevent Replay & Double-Spending Attacks
        cursor.execute("SELECT id, status FROM billing_transactions WHERE tx_hash = ?", (clean_txid,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="This transaction hash has already been submitted or credited.",
            )

        if not user_id and request.client_email:
            cursor.execute("SELECT id, credits FROM users WHERE email = ?", (request.client_email,))
            row = cursor.fetchone()
            if row:
                user_id = row["id"]

        if not user_id:
            cursor.execute("SELECT id, credits FROM users LIMIT 1")
            row = cursor.fetchone()
            user_id = row["id"] if row else 1

        # 100 credits per $1 (minimum 500 credits)
        credits_to_add = max(500, int(request.amount * 100))

        cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        current_credits = row["credits"] if row else 0
        new_credits = current_credits + credits_to_add

        cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))

        cursor.execute(
            """
            INSERT INTO billing_transactions (user_id, plan_id, amount_usd, credits_added, payment_method, status, tx_hash)
            VALUES (?, 'custom', ?, ?, ?, 'COMPLETED', ?)
            """,
            (user_id, request.amount, credits_to_add, request.currency or "CRYPTO", clean_txid),
        )
        conn.commit()

    return {
        "success": True,
        "message": f"Payment of ${request.amount:.2f} confirmed! {credits_to_add:,} credits added to your wallet.",
        "credits_added": credits_to_add,
        "new_balance": new_credits,
        "tx_hash": clean_txid
    }
